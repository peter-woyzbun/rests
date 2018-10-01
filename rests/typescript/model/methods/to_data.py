from rests.typescript.model.method import ModelMethod
from rests.typescript import code_generators as ts
from rests.typescript import types


# =================================
# To Data Method
# ---------------------------------

class ToData(ModelMethod):

    def generator(self):
        return ts.public + ts.Function(
            name='toData', call_signature=None, return_type=types.OBJECT
        )(f"""
        let data = {{}};
        { self.model.name }.FIELDS.map((fieldName) => {{
            data[fieldName] = this[fieldName];
        }})
        return data;
                        """)