import json
from nicegui import app, ui
import yaml
from models.kubectl import KubectlService
from utils.security import SecurityService
from core.config import config
from utils.message import MessageService
from datetime import datetime
import logging

class StandardPage():
    """StandardPage
    All page must inherit this page for security issue
    """

    def __init__(self):
        self.header = ui.row().style('background-color: #ebf1fa').props('bordered')
        self.body = ui.row()
        self.footer = ui.row()

        self.init()

    def init(self):
        logging.getLogger().setLevel(logging.DEBUG)
        None

    def logout(self):
        app.storage.user['identity'] = None
        ui.open(config['gui']['login_uri'])

    @ui.refreshable
    def chatArea(target = None) -> None:
        for msg in MessageService().get():
            ui.chat_message(msg['detail'],
                name=msg['message'],
                stamp = msg['stamp'],
                avatar='https://robohash.org/{}'.format(msg['avatar']))

    def build(self, request, roles = None):
        if roles == None:
            # no roles is set so denied
            return False

        session_roles = []
        with ui.header(elevated=True).style('background-color: #e8dfdf').classes('items-center justify-between'):

            logging.debug('Read from session {}'.format(app.storage.user))
    
            if 'identity' in app.storage.user and app.storage.user['identity']:
                logging.debug('Read from session {}'.format(app.storage.user['identity']))
                if 'roles' in app.storage.user['identity']:
                    session_roles = app.storage.user['identity']['roles']
                ui.label('Hi, {} {}'.format(app.storage.user['identity']['username'],session_roles)).style('color: #000000')
                ui.button('LOGOUT', on_click=lambda: self.logout())
            else:
                ui.label('No user identified !!!').style('color: #000000')
                auth_uri = SecurityService().initiateCodeFlow(request = request, scopes = config['security']['scopes'])
                ui.button('LOGIN', on_click=lambda: ui.open(auth_uri))

        allRoleMatch = True

        for role in roles:
            if role not in session_roles:
                allRoleMatch = False

        with self.body:
            if not allRoleMatch:
                ui.label('/!\ permission denied')
            else:
                None

        self.left_side = ui.left_drawer(top_corner=True, bottom_corner=True)
        with self.left_side.style('background-color: #bdb7b7'):
            ui.link('namespaces','/namespaces')
            ui.link('apiresources','/apiresources')
    
        self.session_dialog = ui.dialog()
        with self.session_dialog, ui.card():
            ui.json_editor({'content': {'json': app.storage.user}},
                    on_select=lambda e: ui.notify(f'Select: {e}'),
                    on_change=lambda e: ui.notify(f'Change: {e}'))

        self.chat_dialog = ui.dialog()
        with self.chat_dialog, ui.card():
            self.chatArea()

        with ui.footer().style('background-color: #e8dfdf'):
            if not allRoleMatch:
                ui.label('/!\ permission denied')
            else:
                ui.button('Chat', on_click=self.chat_dialog.open)
                ui.button('Session', on_click=self.session_dialog.open)
                self.switch = ui.switch('left side', value = True)
                self.switch.on(type = 'update:model-value', handler = lambda: self.on_switch())

        return allRoleMatch

    # Switch left side pane
    def on_switch(self):
        if self.switch.value:
            self.left_side.show()
        else:
            self.left_side.hide()

    # Chat a new message
    def chat(self, message = None, detail = None, avatar = 'info'):
        MessageService().push({
            "message": message,
            "detail": detail,
            'stamp': "{}".format(datetime.now()),
            'avatar': avatar
        })
        self.chatArea.refresh()

    # Template
    def template(self, namespace = None, type = None, ext = None) -> None:
        self.rows = []

        for item in KubectlService().getWithNamespace(type, namespace)["items"]:
            self.rows.append({
                "apiVersion": item['apiVersion'],
                "kind": item['kind'],
                "name": item['metadata']['name'],
                "creationTimestamp": item['metadata']['creationTimestamp'],
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

    def markdownFromYaml(self, type, name, namespace) -> None:
        if name:
            ui.markdown("```yaml\n{}\n```".format(yaml.dump(KubectlService().getWithNameInNamespace(type, name, namespace))))

    def markdownFromJson(self, type, name, namespace) -> None:
        if name:
            ui.markdown("```json\n{}\n```".format(json.dumps(KubectlService().getWithNameInNamespace(type, name, namespace), indent = 2)))
