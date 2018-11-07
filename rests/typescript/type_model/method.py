from rests import interface
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.utils.render_object import render_object


# =================================
# Type Model Method
# ---------------------------------

class Method(object):

    def __init__(self, type_method: interface.TypeMethod):
        self.type_method = type_method

    @property
    def name(self):
        return self.type_method.name

    @property
    def arg_map(self):
        return "{ " + ", ".join(self.type_method.func_signature.parameters.keys()) + " }"

    @property
    def arg_declarations(self):
        for param in self.type_method.func_signature.parameters.values():
            yield param.name + ": " + TypeTranspiler.transpile(param.type)

    @property
    def arg_signature(self):
        print("HELLO!")
        arg_decs = list(self.arg_declarations)
        print(arg_decs)
        if len(arg_decs) == 0:
            return ''
        return ", ".join(arg_decs) + ', '


