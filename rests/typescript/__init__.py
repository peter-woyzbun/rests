import pathlib

from rests.typescript.model.model import Model
from rests.typescript.queryset.queryset import Queryset
from rests.typescript.server_client import ServerClient


SOURCE_DIR = str(pathlib.Path(__file__).parent / 'src' / 'core')