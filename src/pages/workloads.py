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

    @ui.refreshable
    def pods(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "pods", ext = {
            'selectPod_AsJson': self.selectPod_AsJson,
            'selectPod_AsYaml': self.selectPod_AsYaml,
        })

    @ui.refreshable
    def deployments(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "deployments", ext = {
            'selectDeployment_AsJson': self.selectDeployment_AsJson,
            'selectDeployment_AsYaml': self.selectDeployment_AsYaml,
        })

    @ui.refreshable
    def daemonsets(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "daemonsets", ext = {
            'selectDaemonset_AsJson': self.selectDaemonset_AsJson,
            'selectDaemonset_AsYaml': self.selectDaemonset_AsYaml,
        })

    @ui.refreshable
    def statefulsets(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "statefulsets", ext = {
            'selectStatefulset_AsJson': self.selectStatefulset_AsJson,
            'selectStatefulset_AsYaml': self.selectStatefulset_AsYaml,
        })

    @ui.refreshable
    def jobs(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "jobs", ext = {
            'selectJob_AsJson': self.selectJob_AsJson,
            'selectJob_AsYaml': self.selectJob_AsYaml,
        })

    @ui.refreshable
    def cronJobs(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "cronJobs", ext = {
            'selectCronjob_AsJson': self.selectCronjob_AsJson,
            'selectCronjob_AsYaml': self.selectCronjob_AsYaml,
        })

    # pods
        
    @ui.refreshable
    def pod_AsYaml(self) -> None:
        self.markdownFromYaml("pods", self.pod, self.namespace)

    @ui.refreshable
    def pod_AsJson(self) -> None:
        self.markdownFromJson("pods", self.pod, self.namespace)

    def selectPod_AsJson(self, e: events.GenericEventArguments) -> None:
        self.pod = e.args['name']
        self.pod_AsJson.refresh()
        self.pod_DlgAsJson.open()

    def selectPod_AsYaml(self, e: events.GenericEventArguments) -> None:
        self.pod = e.args['name']
        self.pod_AsYaml.refresh()
        self.pod_DlgAsYaml.open()

    # deployments

    @ui.refreshable
    def deployment_AsYaml(self) -> None:
        self.markdownFromYaml("deployments", self.deployment, self.namespace)

    @ui.refreshable
    def deployment_AsJson(self) -> None:
        self.markdownFromJson("deployments", self.deployment, self.namespace)

    def selectDeployment_AsJson(self, e: events.GenericEventArguments) -> None:
        self.deployment = e.args['name']
        self.deployment_AsJson.refresh()
        self.deployment_DlgAsJson.open()

    def selectDeployment_AsYaml(self, e: events.GenericEventArguments) -> None:
        self.deployment = e.args['name']
        self.deployment_AsYaml.refresh()
        self.deployment_DlgAsYaml.open()

    # daemonsets

    @ui.refreshable
    def daemonset_AsYaml(self) -> None:
        self.markdownFromYaml("daemonsets", self.daemonset, self.namespace)

    @ui.refreshable
    def daemonset_AsJson(self) -> None:
        self.markdownFromJson("daemonsets", self.daemonset, self.namespace)

    def selectDaemonset_AsJson(self, e: events.GenericEventArguments) -> None:
        self.daemonset = e.args['name']
        self.daemonset_AsJson.refresh()
        self.daemonset_DlgAsJson.open()

    def selectDaemonset_AsYaml(self, e: events.GenericEventArguments) -> None:
        self.daemonset = e.args['name']
        self.daemonset_AsYaml.refresh()
        self.daemonset_DlgAsYaml.open()

    # statefulsets

    @ui.refreshable
    def statefulset_AsYaml(self) -> None:
        self.markdownFromYaml("statefulsets", self.statefulset, self.namespace)

    @ui.refreshable
    def statefulset_AsJson(self) -> None:
        self.markdownFromJson("statefulsets", self.statefulset, self.namespace)

    def selectStatefulset_AsJson(self, e: events.GenericEventArguments) -> None:
        self.statefulset = e.args['name']
        self.statefulset_AsJson.refresh()
        self.statefulset_DlgAsJson.open()

    def selectStatefulset_AsYaml(self, e: events.GenericEventArguments) -> None:
        self.statefulset = e.args['name']
        self.statefulset_AsYaml.refresh()
        self.statefulset_DlgAsYaml.open()

    # jobs

    @ui.refreshable
    def job_AsYaml(self) -> None:
        self.markdownFromYaml("jobs", self.job, self.namespace)

    @ui.refreshable
    def job_AsJson(self) -> None:
        self.markdownFromJson("jobs", self.job, self.namespace)

    def selectJob_AsJson(self, e: events.GenericEventArguments) -> None:
        self.job = e.args['name']
        self.job_AsJson.refresh()
        self.job_DlgAsJson.open()

    def selectJob_AsYaml(self, e: events.GenericEventArguments) -> None:
        self.job = e.args['name']
        self.job_AsYaml.refresh()
        self.job_DlgAsYaml.open()

    # cronjobs

    @ui.refreshable
    def cronjob_AsYaml(self) -> None:
        self.markdownFromYaml("cronjobs", self.cronjob, self.namespace)

    @ui.refreshable
    def cronjob_AsJson(self) -> None:
        self.markdownFromJson("cronjobs", self.cronjob, self.namespace)

    def selectCronjob_AsJson(self, e: events.GenericEventArguments) -> None:
        self.cronjob = e.args['name']
        self.cronjob_AsJson.refresh()
        self.cronjob_DlgAsJson.open()

    def selectCronjob_AsYaml(self, e: events.GenericEventArguments) -> None:
        self.cronjob = e.args['name']
        self.cronjob_AsYaml.refresh()
        self.cronjob_DlgAsYaml.open()

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
                self.pod_DlgAsJson = ui.dialog()
                with self.pod_DlgAsJson, ui.card():
                    self.pod_AsJson()

                self.pod_DlgAsYaml = ui.dialog()
                with self.pod_DlgAsYaml, ui.card():
                    self.pod_AsYaml()

                # deployments
                self.deployment_DlgAsJson = ui.dialog()
                with self.deployment_DlgAsJson, ui.card():
                    self.deployment_AsJson()

                self.deployment_DlgAsYaml = ui.dialog()
                with self.deployment_DlgAsYaml, ui.card():
                    self.deployment_AsYaml()

                # daemonsets
                self.daemonset_DlgAsJson = ui.dialog()
                with self.daemonset_DlgAsJson, ui.card():
                    self.daemonset_AsJson()

                self.daemonset_DlgAsYaml = ui.dialog()
                with self.daemonset_DlgAsYaml, ui.card():
                    self.daemonset_AsYaml()

                # statefulsets
                self.statefulset_DlgAsJson = ui.dialog()
                with self.statefulset_DlgAsJson, ui.card():
                    self.statefulset_AsJson()

                self.statefulset_DlgAsYaml = ui.dialog()
                with self.statefulset_DlgAsYaml, ui.card():
                    self.statefulset_AsYaml()

                # jobs
                self.job_DlgAsJson = ui.dialog()
                with self.job_DlgAsJson, ui.card():
                    self.job_AsJson()

                self.job_DlgAsYaml = ui.dialog()
                with self.job_DlgAsYaml, ui.card():
                    self.job_AsYaml()

                # cronJobs
                self.cronjob_DlgAsJson = ui.dialog()
                with self.cronjob_DlgAsJson, ui.card():
                    self.cronjob_AsJson()

                self.cronjob_DlgAsYaml = ui.dialog()
                with self.cronjob_DlgAsYaml, ui.card():
                    self.cronjob_AsYaml()

@ui.page('/namespaces/{namespace}/workload', dark=True)
def workloadsPage(request: Request = None, namespace: str = None):
    WorkloadsPage().build(request = request, namespace = namespace)
