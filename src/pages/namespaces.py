import json
from fastapi import Request
from models.kubectl import KubectlService
from pages.common import StandardPage

from nicegui import Tailwind, app, events, ui
from core.config import config
import logging

class NamespacesPage(StandardPage):
    """NamespacesPage
    """

    def init(self):
        self.columns = [
            {'name': 'ApiVersion', 'label': 'ApiVersion', 'field': 'apiVersion'},
            {'name': 'Kind', 'label': 'Kind', 'field': 'kind'},
            {'name': 'Name', 'label': 'Name', 'field': 'name'},
            {'name': 'Creation', 'label': 'Creation', 'field': 'creationTimestamp'},
            {'label': 'Json'},
            {'label': 'Wrk'},
            {'label': 'Svc'},
        ]
        self.rows = []
        self.namespace = None

    @ui.refreshable
    def namespacesArea(self) -> None:
        self.rows = []

        for namespace in KubectlService().get("namespaces")["items"]:
            self.rows.append({
                "apiVersion": namespace['apiVersion'],
                "kind": namespace['kind'],
                "name": namespace['metadata']['name'],
                "creationTimestamp": namespace['metadata']['creationTimestamp'],
                })

        logging.info(self.rows)
        self.table = ui.table(columns=self.columns, rows=self.rows, row_key='name', pagination={'rowsPerPage': 50, 'sortBy': 'name'})
        self.table.classes('w-full')

        self.table.add_slot('body', r'''
            <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
                <q-td auto-width>
                    <q-btn color="info" round dense
                        @click="() => $parent.$emit('selectNamespace', props.row)"
                        :icon="'search'" />
                </q-td>
                <q-td auto-width>
                    <q-btn color="info" round dense
                        @click="() => $parent.$emit('selectWorkload', props.row)"
                        :icon="'view_in_ar'" />
                </q-td>
                <q-td auto-width>
                    <q-btn color="info" round dense
                        @click="() => $parent.$emit('selectService', props.row)"
                        :icon="'view_in_ar'" />
                </q-td>
            </q-tr>
        ''')

        self.table.on('selectNamespace', self.selectNamespace)
        self.table.on('selectWorkload', self.selectWorkload)
        self.table.on('selectService', self.selectService)

    @ui.refreshable
    def namespaceAsJson(self) -> None:
        if self.namespace:
            value = KubectlService().getWithName("namespaces", self.namespace)
            ui.markdown("```json\n{}\n```".format(json.dumps(value, indent = 2)))

    def selectNamespace(self, e: events.GenericEventArguments) -> None:
        self.namespace = e.args['name']
        self.namespaceAsJson.refresh()
        self.dialog_namespace.open()

    def selectWorkload(self, e: events.GenericEventArguments) -> None:
        ui.open("/namespaces/{}/workload".format(e.args['name']))

    def selectService(self, e: events.GenericEventArguments) -> None:
        ui.open("/namespaces/{}/service".format(e.args['name']))

    def build(self, request):
        # Call inheritance to check roles
        if StandardPage.build(self, request = request, roles = ['ADMIN']):
            with self.body:
                self.chat(message = "Namespace", detail = "scan all existing namespaces")

                # namespaces
                self.namespacesArea()

                # namespace dialod
                self.dialog_namespace = ui.dialog()
                with self.dialog_namespace, ui.card():
                    self.namespaceAsJson()

@ui.page('/namespaces', dark=True)
def namespacesPage(request: Request = None):
    NamespacesPage().build(request = request)
