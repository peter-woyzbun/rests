from rests.typescript.model.method import ModelMethod
from rests.typescript.server_client.server_client import response_handler_kwarg
from rests.typescript import code_generators as ts


# =================================
# Delete Method
# ---------------------------------

class DeleteMethod(ModelMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            kwargs=response_handler_kwarg
        )
        return ts.public + ts.async_ + ts.Function(
            name='delete', call_signature=call_sig
        )(f"""
        let response = await serverClient.delete(`/{ self.model.type_url }/${{ this.pk() }}/delete/`, responseHandlers)
        """)