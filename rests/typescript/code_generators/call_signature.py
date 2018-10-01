from typing import List, Dict, Any

from rests.core.typescript.code_generator import CodeGenerator
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.code_generators.type_declaration import TypeDeclaration


# =================================
# Call Signature
# ---------------------------------

class CallSignature(CodeGenerator):

    def __init__(self, *args: TypeDeclaration, kwargs: Dict[TypeDeclaration, Any]=None):
        self.args = list(args)
        self.kwargs = kwargs if kwargs else {}
        CodeGenerator.__init__(self)

    def type_declarations(self) -> List[TypeDeclaration]:
        return self.args + list(self.kwargs.keys())

    @property
    def var_names(self):
        return set([td.var_name for td in self.args] + [td.var_name for td in self.kwargs.keys()])

    def _render(self):
        args = list()
        rest_parameters = list()
        for type_dec in self.args:
            if not type_dec.rest_parameter:
                args.append(str(type_dec))
            else:
                rest_parameters.append(str(type_dec))
        for type_dec, val in self.kwargs.items():
            args.append(str(type_dec) + " = " + val)

        return ", ".join(
            args +
            rest_parameters
        )
