import json, yaml
from fastapi import Request
from models.kubectl import KubectlService
from pages.common import StandardPage

from nicegui import events, ui
from core.config import config
import logging

class WorkloadsPage(StandardPage):
    """WorkloadsPage
    """

    def init(self):
        self.columns = [
            {'name': 'ApiVersion', 'label': 'ApiVersion', 'field': 'apiVersion'},
            {'name': 'Kind', 'label': 'Kind', 'field': 'kind'},
            {'name': 'Name', 'label': 'Name', 'field': 'name'},
            {'name': 'Creation', 'label': 'Creation', 'field': 'creationTimestamp'},
            {'label': 'Json'},
            {'label': 'Yaml'},
            {'label': 'Wk.'},
        ]
        self.rows = []
        self.pod = None
        self.deployment = None
        self.daemonset = None
        self.statefulset = None
        self.job = None
        self.cronjob = None

    def template(self, namespace = None, type = None, ext = None) -> None:
        self.rows = []

        for namespace in KubectlService().getWithNamespace(type, namespace)["items"]:
            self.rows.append({
                "apiVersion": namespace['apiVersion'],
                "kind": namespace['kind'],
                "name": namespace['metadata']['name'],
                "creationTimestamp": namespace['metadata']['creationTimestamp'],
                })

        self.table = ui.table(columns=self.columns, rows=self.rows, row_key='name', pagination={'rowsPerPage': 50, 'sortBy': 'name'})
        self.table.classes('w-full')

        act = []
        for key in ext:
            act.append(key)
            self.table.on(key, ext[key])

        self.table.add_slot('body', r'''
            <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
                <q-td auto-width>
                    <q-btn color="info" round dense
                        @click="() => $parent.$emit('@0', props.row)"
                        :icon="'search'" />
                </q-td>
                <q-td auto-width>
                    <q-btn color="info" round dense
                        @click="() => $parent.$emit('@1', props.row)"
                        :icon="'search'" />
                </q-td>
                <q-td auto-width>
                    <q-btn color="info" round dense
                        @click="() => $parent.$emit('selectWorkload', props.row)"
                        :icon="'view_in_ar'" />
                </q-td>
            </q-tr>
        '''.replace("@0", act[0]).replace("@1", act[1]))

    @ui.refreshable
    def pods(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "pods", ext = {
            'selectPodAsJson': self.selectPodAsJson,
            'selectPodAsYaml': self.selectPodAsYaml,
        })

    @ui.refreshable
    def deployments(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "deployments", ext = {
            'selectDeploymentAsJson': self.selectDeploymentAsJson,
            'selectDeploymentAsYaml': self.selectDeploymentAsYaml,
        })

    @ui.refreshable
    def daemonsets(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "daemonsets", ext = {
            'selectDaemonsetAsJson': self.selectDaemonsetAsJson,
            'selectDaemonsetAsYaml': self.selectDaemonsetAsYaml,
        })

    @ui.refreshable
    def statefulsets(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "statefulsets", ext = {
            'selectStatefulsetAsJson': self.selectStatefulsetAsJson,
            'selectStatefulsetAsYaml': self.selectStatefulsetAsYaml,
        })

    @ui.refreshable
    def jobs(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "jobs", ext = {
            'selectJobAsJson': self.selectJobAsJson,
            'selectJobAsYaml': self.selectJobAsYaml,
        })

    @ui.refreshable
    def cronJobs(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "cronJobs", ext = {
            'selectCronjobAsJson': self.selectCronjobAsJson,
            'selectCronjobAsYaml': self.selectCronjobAsYaml,
        })

    def markdownFromYaml(self, type, name, namespace) -> None:
        if name:
            ui.markdown("```yaml\n{}\n```".format(yaml.dump(KubectlService().getWithNameInNamespace(type, name, namespace))))

    def markdownFromJson(self, type, name, namespace) -> None:
        if name:
            print(type, name, namespace)
            ui.markdown("```json\n{}\n```".format(json.dumps(KubectlService().getWithNameInNamespace(type, name, namespace), indent = 2)))

    # pods
        
    @ui.refreshable
    def podAsYaml(self) -> None:
        self.markdownFromYaml("pods", self.pod, self.namespace)

    @ui.refreshable
    def podAsJson(self) -> None:
        self.markdownFromJson("pods", self.pod, self.namespace)

    def selectPodAsJson(self, e: events.GenericEventArguments) -> None:
        self.pod = e.args['name']
        self.podAsJson.refresh()
        self.dialog_pod_json.open()

    def selectPodAsYaml(self, e: events.GenericEventArguments) -> None:
        self.pod = e.args['name']
        self.podAsYaml.refresh()
        self.dialog_pod_yaml.open()

    # deployments

    @ui.refreshable
    def deploymentAsYaml(self) -> None:
        self.markdownFromYaml("deployments", self.deployment, self.namespace)

    @ui.refreshable
    def deploymentAsJson(self) -> None:
        self.markdownFromJson("deployments", self.deployment, self.namespace)

    def selectDeploymentAsJson(self, e: events.GenericEventArguments) -> None:
        self.deployment = e.args['name']
        self.deploymentAsJson.refresh()
        self.dialog_deployment_json.open()

    def selectDeploymentAsYaml(self, e: events.GenericEventArguments) -> None:
        self.deployment = e.args['name']
        self.deploymentAsYaml.refresh()
        self.dialog_deployment_yaml.open()

    # daemonsets

    @ui.refreshable
    def daemonsetAsYaml(self) -> None:
        self.markdownFromYaml("daemonsets", self.daemonset, self.namespace)

    @ui.refreshable
    def daemonsetAsJson(self) -> None:
        self.markdownFromJson("daemonsets", self.daemonset, self.namespace)

    def selectDaemonsetAsJson(self, e: events.GenericEventArguments) -> None:
        self.daemonset = e.args['name']
        self.daemonsetAsJson.refresh()
        self.dialog_daemonset_json.open()

    def selectDaemonsetAsYaml(self, e: events.GenericEventArguments) -> None:
        self.daemonset = e.args['name']
        self.daemonsetAsYaml.refresh()
        self.dialog_daemonset_yaml.open()

    # statefulsets

    @ui.refreshable
    def statefulsetAsYaml(self) -> None:
        self.markdownFromYaml("statefulsets", self.statefulset, self.namespace)

    @ui.refreshable
    def statefulsetAsJson(self) -> None:
        self.markdownFromJson("statefulsets", self.statefulset, self.namespace)

    def selectStatefulsetAsJson(self, e: events.GenericEventArguments) -> None:
        self.statefulset = e.args['name']
        self.statefulsetAsJson.refresh()
        self.dialog_statefulset_json.open()

    def selectStatefulsetAsYaml(self, e: events.GenericEventArguments) -> None:
        self.statefulset = e.args['name']
        self.statefulsetAsYaml.refresh()
        self.dialog_statefulset_yaml.open()

    # jobs

    @ui.refreshable
    def jobAsYaml(self) -> None:
        self.markdownFromYaml("jobs", self.job, self.namespace)

    @ui.refreshable
    def jobAsJson(self) -> None:
        self.markdownFromJson("jobs", self.job, self.namespace)

    def selectJobAsJson(self, e: events.GenericEventArguments) -> None:
        self.job = e.args['name']
        self.jobAsJson.refresh()
        self.dialog_job_json.open()

    def selectJobAsYaml(self, e: events.GenericEventArguments) -> None:
        self.job = e.args['name']
        self.jobAsYaml.refresh()
        self.dialog_job_yaml.open()

    # cronjobs

    @ui.refreshable
    def cronjobAsYaml(self) -> None:
        self.markdownFromYaml("cronjobs", self.cronjob, self.namespace)

    @ui.refreshable
    def cronjobAsJson(self) -> None:
        self.markdownFromJson("cronjobs", self.cronjob, self.namespace)

    def selectCronjobAsJson(self, e: events.GenericEventArguments) -> None:
        self.cronjob = e.args['name']
        self.cronjobAsJson.refresh()
        self.dialog_cronjob_json.open()

    def selectCronjobAsYaml(self, e: events.GenericEventArguments) -> None:
        self.cronjob = e.args['name']
        self.cronjobAsYaml.refresh()
        self.dialog_cronjob_yaml.open()

    def build(self, request, namespace):
        self.namespace = namespace
        # Call inheritance to check roles
        if StandardPage.build(self, request = request, roles = ['ADMIN']):
            with self.body:
                self.chat(message = "Workload", detail = "scan all existing workloads")

                with ui.tabs().classes('w-full') as tabs:
                    pods = ui.tab('Pods')
                    deployments = ui.tab('Deployments')
                    daemonsets = ui.tab('DaemonSets')
                    statefulsets = ui.tab('StatefulSets')
                    jobs = ui.tab('Jobs')
                    cronJobs = ui.tab('CronJobs')

                with ui.tab_panels(tabs, value=pods).classes('w-full'):
                    with ui.tab_panel(pods):
                        self.pods(namespace = self.namespace)
                    with ui.tab_panel(deployments):
                        self.deployments(namespace = self.namespace)
                    with ui.tab_panel(daemonsets):
                        self.daemonsets(namespace = self.namespace)
                    with ui.tab_panel(statefulsets):
                        self.statefulsets(namespace = self.namespace)
                    with ui.tab_panel(jobs):
                        self.jobs(namespace = self.namespace)
                    with ui.tab_panel(cronJobs):
                        self.cronJobs(namespace = self.namespace)

                # pods
                self.dialog_pod_json = ui.dialog()
                with self.dialog_pod_json, ui.card():
                    self.podAsJson()

                self.dialog_pod_yaml = ui.dialog()
                with self.dialog_pod_yaml, ui.card():
                    self.podAsYaml()

                # deployments
                self.dialog_deployment_json = ui.dialog()
                with self.dialog_deployment_json, ui.card():
                    self.deploymentAsJson()

                self.dialog_deployment_yaml = ui.dialog()
                with self.dialog_deployment_yaml, ui.card():
                    self.deploymentAsYaml()

                # daemonsets
                self.dialog_daemonset_json = ui.dialog()
                with self.dialog_daemonset_json, ui.card():
                    self.daemonsetAsJson()

                self.dialog_daemonset_yaml = ui.dialog()
                with self.dialog_daemonset_yaml, ui.card():
                    self.daemonsetAsYaml()

                # statefulsets
                self.dialog_statefulset_json = ui.dialog()
                with self.dialog_statefulset_json, ui.card():
                    self.statefulsetAsJson()

                self.dialog_statefulset_yaml = ui.dialog()
                with self.dialog_statefulset_yaml, ui.card():
                    self.statefulsetAsYaml()

                # jobs
                self.dialog_job_json = ui.dialog()
                with self.dialog_job_json, ui.card():
                    self.jobAsJson()

                self.dialog_job_yaml = ui.dialog()
                with self.dialog_job_yaml, ui.card():
                    self.jobAsYaml()

                # cronJobs
                self.dialog_cronjob_json = ui.dialog()
                with self.dialog_cronjob_json, ui.card():
                    self.cronjobAsJson()

                self.dialog_cronjob_yaml = ui.dialog()
                with self.dialog_cronjob_yaml, ui.card():
                    self.cronjobAsYaml()

@ui.page('/namespaces/{namespace}/workload', dark=True)
def workloadsPage(request: Request = None, namespace: str = None):
    WorkloadsPage().build(request = request, namespace = namespace)
