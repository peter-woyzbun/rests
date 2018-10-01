import os
from shutil import copy2
from typing import Type

from rests.interface.interface import Interface
from rests import typescript


# =================================
# Transpiler
# ---------------------------------

class Transpiler(object):

    def __init__(self, interface: Type[Interface], server_url: str):
        self.interface = interface
        self.server_url = server_url

    def transpile(self, dest, models_filename):
        self._write_server_client_source(dest=dest)
        self._write_models_source(dest=dest, models_filename=models_filename)

    @property
    def model_pool(self):
        return self.interface.models()

    def model_source(self, model, type_url) -> str:
        """
        Generate and return TypeScript source code for given model.

        """
        typescript_model = typescript.Model(model=model, model_pool=self.model_pool, type_url=type_url)
        typescript_queryset = typescript.Queryset(model=model, model_pool=self.model_pool, type_url=type_url)
        return typescript_queryset.render() + '\n' + typescript_model.render()

    def server_client_source(self):
        return typescript.ServerClient(server_url=self.server_url).render()

    def _write_models_source(self, dest, models_filename):
        models_file = open(os.path.join(dest, models_filename), "w+")
        code = list()
        code.append(typescript.ServerClient.required_imports())
        code.append(self.server_client_source())
        for interface_type in self.interface.types().values():
            code.append(self.model_source(model=interface_type.model_cls, type_url=interface_type.base_url))
        models_file.write("\n".join(code))
        models_file.close()

    @staticmethod
    def _write_server_client_source(dest):
        copy2(typescript.ServerClient.SOURCE_PATH, dest)