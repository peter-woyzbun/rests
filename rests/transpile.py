import os
from shutil import copy2
from distutils.dir_util import copy_tree
import subprocess
from subprocess import check_output
from typing import Type

from rests.interface.interface import Interface
from rests import typescript


# =================================
# Transpiler
# ---------------------------------

class Transpiler(object):

    """
    The Transpile class generates the source code for `rests` interfaces.

    """

    ROOT_DIR_NAME = 'server'
    MODELS_FILENAME = 'models.ts'

    SERVER_CLIENT_CORE_IMPORT = "import {ResponseHandlers} from './core/server_client'"
    SERVER_CLIENT_IMPORT = "import {serverClient} from './client'"
    MODEL_IMPORT = "import {Model} from './core/model'"
    QUERYSET_IMPORT = "import {Queryset} from './core/queryset'"
    FOREIGN_KEY_IMPORT = "import {foreignKeyField} from './core/fields'"

    def __init__(self, interface: Type[Interface], server_url: str, root_dest_dir, confirm_overwrite=False):
        self.interface = interface
        self.server_url = server_url
        self.root_dest_dir = root_dest_dir
        self.confirm_overwrite = confirm_overwrite

    @property
    def dest_dir(self):
        return os.path.join(self.root_dest_dir, self.ROOT_DIR_NAME)

    def transpile(self):
        if not self._pre_transpile_checks_passed():
            return
        self._initialize_dest_dir()
        self._write_core_src()
        self._write_server_client()
        self._write_models_and_querysets()

    def _pre_transpile_checks_passed(self):
        if os.path.exists(self.dest_dir) and self.confirm_overwrite:
            response = input(f"The directory `{self.dest_dir}` already exists, do you want to overwrite? y / N")
            return response == 'y'
        return True

    def _initialize_dest_dir(self):
        """
        Create `index.ts` in destination directory.

        """
        if not os.path.exists(self.dest_dir):
            os.mkdir(self.dest_dir)
        index_ts = open(os.path.join(self.dest_dir, 'index.ts'), "w+")
        index_ts.close()

    def _write_core_src(self):
        """
        Write the "core" source files to destination directory.

        """
        copy_tree(str(typescript.SOURCE_DIR), os.path.join(self.dest_dir, 'core'))

    def _write_server_client(self):
        """
        Write source for the `ServerClient` instance used by all models and
        querysets. This is where we set the 'base' server URL.

        """
        client_ts = open(os.path.join(self.dest_dir, 'client.ts'), "w+")
        code = list()
        code.append(self.SERVER_CLIENT_CORE_IMPORT)
        code.append(typescript.ServerClient(server_url=self.server_url).render())
        client_ts.write("\n".join(code))
        client_ts.close()

    def _write_models_and_querysets(self):
        models_file = open(os.path.join(self.dest_dir, self.MODELS_FILENAME), "w+")
        index_ts = open(os.path.join(self.dest_dir, 'index.ts'), "w+")
        index_ts.close()
        code = list()
        # Imports
        code.append(self.MODEL_IMPORT)
        code.append(self.QUERYSET_IMPORT)
        code.append(self.FOREIGN_KEY_IMPORT)
        code.append(self.SERVER_CLIENT_CORE_IMPORT)
        code.append(self.SERVER_CLIENT_IMPORT)
        for interface_type in self.interface.types().values():
            code.append(self.model_source(model=interface_type.model_cls, type_url=interface_type.base_url))
        models_file.write("\n".join(code))
        models_file.close()
        try:
            subprocess.check_call(['tsfmt', '-r', self.MODELS_FILENAME], cwd=self.dest_dir)
        except Exception as e:
            print("Could not format `models.ts`. Install `typescript-formatter` "
                  "(`npm install -g typescript-formatter`) to enable code formatting.")


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
