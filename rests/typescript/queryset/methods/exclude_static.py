from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts


# =================================
# Exclude Static Method
# ---------------------------------

class ExcludeStaticMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            self.queryset.lookups_type_dec,
        )
        return ts.public + ts.static + ts.Function(
            name='exclude', call_signature=call_sig, return_type=self.queryset.class_name
        )(f"""
            return new { self.queryset.class_name }({{}}, lookups)
            """)