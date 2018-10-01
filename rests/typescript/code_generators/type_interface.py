from typing import List

from rests.core.typescript.code_generator import CodeGenerator
from rests.typescript.code_generators.type_declaration import TypeDeclaration


# =================================
# Type Interface
# ---------------------------------

class TypeInterface(CodeGenerator):

    TEMPLATE = """interface {{ type_interface.name }}{
    {{ type_interface.type_declarations }}
    }
    
    """

    def __init__(self, name, type_declarations: List[TypeDeclaration]):
        self.name = name
        self._type_declarations = type_declarations

        CodeGenerator.__init__(self)

    @property
    def type_declarations(self):
        val = ";\n".join(str(td) for td in self._type_declarations)
        return val

    def _render(self):
        return self._render_template(type_interface=self)
