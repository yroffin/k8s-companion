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
        ]
        self.rows = []
        self.context = {
            "name": None,
            "pod": {
                "AsJson": self.pod_AsJson,
                "AsYaml": self.pod_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "deployment": {
                "AsJson": self.deployment_AsJson,
                "AsYaml": self.deployment_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "daemonset": {
                "AsJson": self.daemonset_AsJson,
                "AsYaml": self.daemonset_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "statefulset": {
                "AsJson": self.statefulset_AsJson,
                "AsYaml": self.statefulset_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "job": {
                "AsJson": self.job_AsJson,
                "AsYaml": self.job_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "cronjob": {
                "AsJson": self.cronjob_AsJson,
                "AsYaml": self.cronjob_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
        }

    @ui.refreshable
    def pods_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "pods", ext = {
            'selectPod_AsJson': self.selectPod_AsJson,
            'selectPod_AsYaml': self.selectPod_AsYaml,
        })

    @ui.refreshable
    def deployments_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "deployments", ext = {
            'selectDeployment_AsJson': self.selectDeployment_AsJson,
            'selectDeployment_AsYaml': self.selectDeployment_AsYaml,
        })

    @ui.refreshable
    def daemonsets_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "daemonsets", ext = {
            'selectDaemonset_AsJson': self.selectDaemonset_AsJson,
            'selectDaemonset_AsYaml': self.selectDaemonset_AsYaml,
        })

    @ui.refreshable
    def statefulsets_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "statefulsets", ext = {
            'selectStatefulset_AsJson': self.selectStatefulset_AsJson,
            'selectStatefulset_AsYaml': self.selectStatefulset_AsYaml,
        })

    @ui.refreshable
    def jobs_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "jobs", ext = {
            'selectJob_AsJson': self.selectJob_AsJson,
            'selectJob_AsYaml': self.selectJob_AsYaml,
        })

    @ui.refreshable
    def cronJobs_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "cronJobs", ext = {
            'selectCronjob_AsJson': self.selectCronjob_AsJson,
            'selectCronjob_AsYaml': self.selectCronjob_AsYaml,
        })

    # pods
        
    @ui.refreshable
    def pod_AsYaml(self) -> None:
        self.markdownFromYaml("pods", self.context['name'], self.namespace)

    @ui.refreshable
    def pod_AsJson(self) -> None:
        self.markdownFromJson("pods", self.context['name'], self.namespace)

    def selectPod_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['pod']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectPod_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['pod']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # deployment

    @ui.refreshable
    def deployment_AsYaml(self) -> None:
        self.markdownFromYaml("deployments", self.context['name'], self.namespace)

    @ui.refreshable
    def deployment_AsJson(self) -> None:
        self.markdownFromJson("deployments", self.context['name'], self.namespace)

    def selectDeployment_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['deployment']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectDeployment_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['deployment']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # daemonset

    @ui.refreshable
    def daemonset_AsYaml(self) -> None:
        self.markdownFromYaml("daemonsets", self.context['name'], self.namespace)

    @ui.refreshable
    def daemonset_AsJson(self) -> None:
        self.markdownFromJson("daemonsets", self.context['name'], self.namespace)

    def selectDaemonset_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['daemonset']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectDaemonset_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['daemonset']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # statefulset

    @ui.refreshable
    def statefulset_AsYaml(self) -> None:
        self.markdownFromYaml("statefulsets", self.context['name'], self.namespace)

    @ui.refreshable
    def statefulset_AsJson(self) -> None:
        self.markdownFromJson("statefulsets", self.context['name'], self.namespace)

    def selectStatefulset_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['statefulset']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectStatefulset_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['statefulset']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # job

    @ui.refreshable
    def job_AsYaml(self) -> None:
        self.markdownFromYaml("jobs", self.context['name'], self.namespace)

    @ui.refreshable
    def job_AsJson(self) -> None:
        self.markdownFromJson("jobs", self.context['name'], self.namespace)

    def selectJob_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['job']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectJob_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['job']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # cronjob

    @ui.refreshable
    def cronjob_AsYaml(self) -> None:
        self.markdownFromYaml("cronjobs", self.context['name'], self.namespace)

    @ui.refreshable
    def cronjob_AsJson(self) -> None:
        self.markdownFromJson("cronjobs", self.context['name'], self.namespace)

    def selectCronjob_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['cronjob']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectCronjob_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['cronjob']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    def build(self, request, namespace):
        self.namespace = namespace
        # Call inheritance to check roles
        if StandardPage.build(self, request = request, roles = ['ADMIN']):
            with self.body:
                self.chat(message = "Workload", detail = "scan all existing workloads")

                tabs = {
                        "Pods": {
                            "tab": None,
                            "component": self.pods_tab,
                        },
                        "Deployments": {
                            "tab": None,
                            "component": self.deployments_tab,
                        },
                        "DaemonSets": {
                            "tab": None,
                            "component": self.daemonsets_tab,
                        },
                        "StatefulSets": {
                            "tab": None,
                            "component": self.statefulsets_tab,
                        },
                        "Jobs": {
                            "tab": None,
                            "component": self.jobs_tab,
                        },
                        "CronJobs": {
                            "tab": None,
                            "component": self.cronJobs_tab,
                        },
                }

                with ui.tabs().classes('w-full') as tabui:
                    for tab in tabs:
                        tabs[tab]["tab"] = ui.tab(tab)

                with ui.tab_panels(tabui, value=tabs["Pods"]['tab']).classes('w-full'):
                    for tab in tabs:
                        with ui.tab_panel(tabs[tab]["tab"]):
                            tabs[tab]["component"](namespace = self.namespace)

                # create dialog box
                for item in ['pod','deployment','daemonset','statefulset','job','cronjob']:
                    ctx = self.context[item]
                    ctx["DlgAsJson"] = ui.dialog()
                    with ctx["DlgAsJson"], ui.card():
                        ctx["AsJson"]()

                    ctx["DlgAsYaml"] = ui.dialog()
                    with ctx["DlgAsYaml"], ui.card():
                        ctx["AsYaml"]()

@ui.page('/namespaces/{namespace}/workload', dark=True)
def workloadsPage(request: Request = None, namespace: str = None):
    WorkloadsPage().build(request = request, namespace = namespace)
