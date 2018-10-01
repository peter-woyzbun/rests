from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts
from rests.typescript.server_client.server_client import response_handler_kwarg


# =================================
# Get Method
# ---------------------------------

class GetMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            ts.TypeDeclaration(var_name='id', type_=self.queryset.pk_field_type),
            kwargs=response_handler_kwarg,
        )
        return ts.public + ts.static + ts.async_ + ts.Function(name='get', call_signature=call_sig)(f"""
                let responseData = await serverClient.get({self.queryset.get_url}, responseHandlers)
                if (responseData){{return new { self.queryset.model_name }(responseData)}}
                return undefined
                """)