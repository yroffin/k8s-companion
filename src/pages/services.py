import json, yaml
from fastapi import Request
from models.kubectl import KubectlService
from pages.common import StandardPage

from nicegui import events, ui
from core.config import config
import logging

class ServicesPage(StandardPage):
    """ServicesPage
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
            "service": {
                "AsJson": self.service_AsJson,
                "AsYaml": self.service_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "ingress": {
                "AsJson": self.ingress_AsJson,
                "AsYaml": self.ingress_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
            "endpoint": {
                "AsJson": self.endpoint_AsJson,
                "AsYaml": self.endpoint_AsYaml,
                "DlgAsJson": None,
                "DlgAsYaml": None,
            },
        }

    @ui.refreshable
    def pods_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "services", ext = {
            'selectService_AsJson': self.selectService_AsJson,
            'selectService_AsYaml': self.selectService_AsYaml,
        })

    @ui.refreshable
    def ingresses_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "ingress", ext = {
            'selectIngress_AsJson': self.selectIngress_AsJson,
            'selectIngress_AsYaml': self.selectIngress_AsYaml,
        })

    @ui.refreshable
    def endpoints_tab(self, namespace = None) -> None:
        self.template(namespace = namespace, type = "endpoints", ext = {
            'selectEndpoint_AsJson': self.selectEndpoint_AsJson,
            'selectEndpoint_AsYaml': self.selectEndpoint_AsYaml,
        })

    # services
        
    @ui.refreshable
    def service_AsYaml(self) -> None:
        self.markdownFromYaml("services", self.context['name'], self.namespace)

    @ui.refreshable
    def service_AsJson(self) -> None:
        self.markdownFromJson("services", self.context['name'], self.namespace)

    def selectService_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['service']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectService_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['service']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # ingresses

    @ui.refreshable
    def ingress_AsYaml(self) -> None:
        self.markdownFromYaml("ingress", self.context['name'], self.namespace)

    @ui.refreshable
    def ingress_AsJson(self) -> None:
        self.markdownFromJson("ingress", self.context['name'], self.namespace)

    def selectIngress_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['ingress']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectIngress_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['ingress']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    # endpoints

    @ui.refreshable
    def endpoint_AsYaml(self) -> None:
        self.markdownFromYaml("endpoints", self.context['name'], self.namespace)

    @ui.refreshable
    def endpoint_AsJson(self) -> None:
        print("endpoints", self.context['name'], self.namespace)
        self.markdownFromJson("endpoints", self.context['name'], self.namespace)

    def selectEndpoint_AsJson(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['endpoint']
        self.context['name'] = e.args['name']
        ctx['AsJson'].refresh()
        ctx['DlgAsJson'].open()

    def selectEndpoint_AsYaml(self, e: events.GenericEventArguments) -> None:
        ctx = self.context['endpoint']
        self.context['name'] = e.args['name']
        ctx['AsYaml'].refresh()
        ctx['DlgAsYaml'].open()

    def build(self, request, namespace):
        self.namespace = namespace
        # Call inheritance to check roles
        if StandardPage.build(self, request = request, roles = ['ADMIN']):
            with self.body:
                self.chat(message = "Service", detail = "scan all existing services")

                tabs = {
                        "Service": {
                            "tab": None,
                            "component": self.pods_tab,
                        },
                        "Ingress": {
                            "tab": None,
                            "component": self.ingresses_tab,
                        },
                        "Endpoint": {
                            "tab": None,
                            "component": self.endpoints_tab,
                        },
                }

                with ui.tabs().classes('w-full') as tabui:
                    for tab in tabs:
                        tabs[tab]["tab"] = ui.tab(tab)

                with ui.tab_panels(tabui, value=tabs["Service"]['tab']).classes('w-full'):
                    for tab in tabs:
                        with ui.tab_panel(tabs[tab]["tab"]):
                            tabs[tab]["component"](namespace = self.namespace)

                # create dialog box
                for item in ['service','ingress','endpoint']:
                    ctx = self.context[item]
                    ctx["DlgAsJson"] = ui.dialog()
                    with ctx["DlgAsJson"] as dialog:
                        with dialog, ui.card():
                            ctx["AsJson"]()

                    ctx["DlgAsYaml"] = ui.dialog()
                    with ctx["DlgAsYaml"] as dialog:
                        with dialog, ui.card():
                            ctx["AsYaml"]()

@ui.page('/namespaces/{namespace}/service', dark=True)
def servicesPage(request: Request = None, namespace: str = None):
    ServicesPage().build(request = request, namespace = namespace)
