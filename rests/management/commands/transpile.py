from typing import Type
import subprocess
import importlib

from django.core.management.base import BaseCommand

from rests.core.exceptions import TranspileError
from rests.interface.interface import Interface
from rests.transpile import Transpiler
from rests import config


# =================================
# Transpile Command
# ---------------------------------

class Command(BaseCommand):

    help = 'Transpile `rests` Interface into TypeScript code.'

    def handle(self, *args, **options):
        path = config.INTERFACE_SRC
        dest = config.TRANSPILE_DEST
        server_url = config.BASE_URL
        self.stdout.write(f"Attempting to transpile `{path}` to destination `{dest}`."
                          f" Using server URL: `{server_url}` ")
        module = importlib.import_module(path)
        if not hasattr(module, 'Interface'):
            raise TranspileError("Could not find `Interface` class in module `{path}`".format(path=path))
        InterfaceCls: Type[Interface] = getattr(module, 'Interface')
        transpiler = Transpiler(interface=InterfaceCls, server_url=server_url, root_dest_dir=dest)
        transpiler.transpile()
        if config.POST_TRANSPILE_COMMAND:
            subprocess.check_call(config.POST_TRANSPILE_COMMAND.split(' '), cwd=dest)
        self.stdout.write("Transpile successful.")
