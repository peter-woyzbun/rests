from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts
from rests.typescript.server_client.server_client import RESPONSE_HANDLERS_TYPE, response_handler_kwarg


# =================================
# Create Method
# ---------------------------------

class CreateMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            ts.TypeDeclaration(var_name='data', type_=self.queryset.model_name + "Data"),
            kwargs=response_handler_kwarg
        )
        return ts.public + ts.static + ts.async_ + ts.Function(name='create', call_signature=call_sig)(f"""
            let responseData = await serverClient.post({ self.queryset.create_url }, data, responseHandlers)
            if (responseData){{return new { self.queryset.model_name }(responseData)}}
            return undefined
                """)