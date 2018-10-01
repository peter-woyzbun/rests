from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts


# =================================
# Or Method
# ---------------------------------

class OrMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            ts.TypeDeclaration(var_name='queryset', type_=self.queryset.class_name),
        )
        return ts.public + ts.Function(
            name='or', call_signature=call_sig, return_type=self.queryset.class_name
        )(f"""
        this._or.push(queryset)
        return this
                """)