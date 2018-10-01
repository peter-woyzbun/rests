from typing import Union, Type

from jinja2 import Template

from rests.core.typescript.code_generator import CodeGenerator
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.code_generators.call_signature import CallSignature


# =================================
# Function
# ---------------------------------

class Function(CodeGenerator):

    TEMPLATE = """{{ func.accessor }}{{ func.name }}({{func.call_signature}}){{ func.return_sig }}{
        {{ func.body }}
    }
    """

    def __init__(self, name: str, call_signature: CallSignature=None, return_type: Union[Type, str] = None):
        self.name = name
        self.call_signature = call_signature if call_signature is not None else ""
        self.return_type = return_type
        self.body = None
        self.accessor = ""
        self._async = ""
        CodeGenerator.__init__(self)

    @property
    def return_sig(self):
        if isinstance(self.return_type, str):
            return ": " + self.return_type
        if self.return_type:
            return ": " + TypeTranspiler.transpile(self.return_type)
        return ""

    def async(self):
        self.prefixes.append('async')
        return self

    def __call__(self, *args: Union[CodeGenerator, str]):
        self.body = "\n".join(args)
        return self

    def _render(self):
        return self._render_template(func=self)

