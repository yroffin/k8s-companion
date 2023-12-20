import json, yaml
from fastapi import Request
from models.kubectl import KubectlService
from pages.common import StandardPage

from nicegui import events, ui
from core.config import config
import logging

class ApiResourcesPage(StandardPage):
    """ApiResourcesPage
    """

    def init(self):
        self.columns = [
            {'name': 'Name', 'label': 'Name', 'field': 'name'},
            {'name': 'ShortNames', 'label': 'ShortNames', 'field': 'shortnames'},
            {'name': 'ApiVersion', 'label': 'ApiVersion', 'field': 'apiversion'},
            {'name': 'Namespaced', 'label': 'Namespaced', 'field': 'namespaced'},
            {'name': 'Kind', 'label': 'Kind', 'field': 'kind'},
        ]
        self.rows = []

    @ui.refreshable
    def template(self) -> None:
        self.rows = []

        for namespace in KubectlService().getApiResources():
            self.rows.append({
                "name": namespace['name'],
                "shortnames": namespace['shortnames'],
                "apiversion": namespace['apiversion'],
                "namespaced": namespace['namespaced'],
                "kind": namespace['kind'],
                })

        self.table = ui.table(columns=self.columns, rows=self.rows, row_key='name', pagination={'rowsPerPage': 100, 'sortBy': 'name'})
        self.table.classes('w-full')

        self.table.add_slot('body', r'''
            <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
            </q-tr>
        ''')

    def build(self, request):
        # Call inheritance to check roles
        if StandardPage.build(self, request = request, roles = ['ADMIN']):
            with self.body:
                self.chat(message = "ApiResources", detail = "scan all api resources")

                self.template()

@ui.page('/apiresources', dark=True)
def apiResourcesPage(request: Request = None):
    ApiResourcesPage().build(request = request)
