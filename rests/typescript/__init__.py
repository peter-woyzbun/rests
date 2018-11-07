import pathlib

from rests.typescript.type_model.type_model import TypeModel
from rests.typescript.queryset.queryset import Queryset
from rests.typescript.server_client import ServerClient


SOURCE_DIR = str(pathlib.Path(__file__).parent / 'src' / 'core')