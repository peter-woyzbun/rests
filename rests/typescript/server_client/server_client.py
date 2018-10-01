import os

from jinja2 import Template

from rests.typescript.code_generators.type_declaration import TypeDeclaration


# =================================
# Types
# ---------------------------------

RESPONSE_HANDLERS_TYPE = 'ResponseHandlers'

response_handler_type_dec = TypeDeclaration(var_name='responseHandlers', type_=RESPONSE_HANDLERS_TYPE)

response_handler_kwarg = {TypeDeclaration(var_name='responseHandlers', type_=RESPONSE_HANDLERS_TYPE): '{}'}


# =================================
# Server Client Template
# ---------------------------------

server_client_template = Template("""

// -------------------------
// Server Client
//
// -------------------------

const serverClient = new ServerClient('{{ server_url }}');
""")


# =================================
# Server Client Generator
# ---------------------------------

class ServerClient(object):

    SOURCE_DIR = os.path.join(os.path.dirname(__file__), 'src')
    SOURCE_PATH = os.path.join(SOURCE_DIR, 'server_client.ts')

    def __init__(self, server_url):
        self.server_url = server_url

    def render(self):
        return server_client_template.render(server_url=self.server_url)

    @classmethod
    def required_imports(cls):
        return "import {ServerClient, ResponseHandlers} from './server_client' "

