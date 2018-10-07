from jinja2 import Template


# =================================
# Server Client Generator
# ---------------------------------

class ServerClient(object):

    TEMPLATE = """
// -------------------------
// Server Client
//
// -------------------------

export const serverClient = new ServerClient('{{ server_url }}');

    """

    def __init__(self, server_url):
        self.server_url = server_url

    def render(self):
        return Template(self.TEMPLATE).render(server_url=self.server_url)

    @classmethod
    def required_imports(cls):
        return "import {ServerClient, ResponseHandlers} from './server_client' "

