from rests.typescript.model.method import ModelMethod
from rests.typescript.server_client.server_client import response_handler_kwarg
from rests.typescript import code_generators as ts


# =================================
# Update Method
# ---------------------------------

class UpdateMethod(ModelMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            ts.TypeDeclaration(var_name='data', type_=f"Partial<{self.model.fields_type_interface_name}>"),
            kwargs=response_handler_kwarg,
        )
        return ts.public + ts.async_ + ts.Function(
            name='update', call_signature=call_sig
        )(f"""
        Object.keys(data).map((fieldName) => {{
            this[fieldName] = data[fieldName];
        }})
        await this.save();
        """)