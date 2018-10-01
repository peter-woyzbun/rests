from rests.typescript.model.method import ModelMethod
from rests.typescript.server_client.server_client import response_handler_kwarg
from rests.typescript import code_generators as ts


# =================================
# Save Method
# ---------------------------------

class SaveMethod(ModelMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            kwargs=response_handler_kwarg
        )
        return ts.public + ts.async_ + ts.Function(
            name='save', call_signature=call_sig
        )(f"""
        let response = await serverClient.post(`/{ self.model.type_url }/${{ this.pk() }}/update/`, this._toData(), responseHandlers)
        """)