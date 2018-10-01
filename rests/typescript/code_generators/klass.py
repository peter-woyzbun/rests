from typing import List, Union

from jinja2 import Template

from rests.core.typescript.code_generator import CodeGenerator
from rests.typescript.code_generators.call_signature import CallSignature
from rests.typescript.code_generators.type_declaration import TypeDeclaration
from rests.typescript.code_generators.destructuring import Destructuring
from rests.typescript.code_generators.function import Function


# =================================
# Class Code Generator
# ---------------------------------

class Klass(CodeGenerator):

    TEMPLATE = """class {{ cls.name }} {

    {{ cls.type_declarations }}

    {{ cls.constructor }}

    {{ cls.body }}    

    }

    """

    def __init__(self, name: str, constructor_signature: CallSignature, type_declarations: List[TypeDeclaration]):
        self.name = name
        self.constructor_signature = constructor_signature
        self._type_declarations = type_declarations
        self.body = ''
        CodeGenerator.__init__(self)

    @property
    def type_declarations(self):
        return "\n".join(str(td) for td in self._type_declarations)

    @property
    def _constructor_var_names(self):
        var_names = list()
        for type_dec in self.constructor_signature.type_declarations():
            if isinstance(type_dec.var_name, Destructuring):
                var_names += type_dec.var_name.var_names
            else:
                var_names.append(type_dec.var_name)
        return var_names

    @property
    def constructor(self):
        return Function(name='constructor', call_signature=self.constructor_signature)(
            *[
                "this.{0} = {0}".format(var_name) for var_name in self._constructor_var_names
            ]
        )

    def __call__(self, *args: Union[str, CodeGenerator]):
        self.body = "\n".join(str(a) for a in args)
        return self

    def _render(self):
        return self._render_template(cls=self)

    def new(self, *args):
        return "new {instance_name}({args})".format(instance_name=self.name.lower(), args=", ".join(args))




