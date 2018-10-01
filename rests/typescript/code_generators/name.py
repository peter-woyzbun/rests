from rests.core.typescript.code_generator import CodeGenerator
from rests.core.utils.snake_to_camel import snake_to_camel_case


# =================================
# Name Code Generator
# ---------------------------------

class Name(CodeGenerator):

    def __init__(self, name: str = None, convert_to_camelcase=True):
        self.py_name = name
        self.convert_to_camelcase = convert_to_camelcase
        CodeGenerator.__init__(self)

    def _render(self) -> str:
        if not self.convert_to_camelcase:
            return self.py_name
        return snake_to_camel_case(self.py_name)

