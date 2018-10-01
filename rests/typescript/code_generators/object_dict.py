from typing import Tuple, Dict, Any

from rests.core.typescript.code_generator import CodeGenerator
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.code_generators.type_declaration import TypeDeclaration


# =================================
# Object Dict
# ---------------------------------

class ObjectDict(CodeGenerator):

    TEMPLATE = "{{{ object_dict.body }}}"

    def __init__(self, object_dict: dict):
        self.object_dict = object_dict
        CodeGenerator.__init__(self)
