from rests.typescript.model.method import ModelMethod
from rests.typescript import code_generators as ts
from rests.typescript import types


# =================================
# To Data Method
# ---------------------------------

class PrivateToData(ModelMethod):

    def generator(self):
        return ts.private + ts.Function(
            name='_toData', call_signature=None, return_type=types.OBJECT
        )(f"""
        let data = {{}};
        { self.model.name }.FIELDS.map((fieldName) => {{
            if (fieldName !== '{ self.model.pk_field_name }'){{
                data[fieldName] = this[fieldName];
            }}
        }})
        return data;
                        """)