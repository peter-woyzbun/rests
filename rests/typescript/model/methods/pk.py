from rests.typescript.model.method import ModelMethod
from rests.typescript import code_generators as ts


# =================================
# Get Primary Key Method
# ---------------------------------

class PkMethod(ModelMethod):

    def generator(self):
        return ts.public + ts.Function(
            name='pk', call_signature=None, return_type=self.model.pk_field_type
        )(f"""
        return this.{self.model.pk_field_name}
                        """)