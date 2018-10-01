from rests.typescript.server_client.server_client import RESPONSE_HANDLERS_TYPE, response_handler_kwarg
from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts


# =================================
# Values Method
# ---------------------------------

class ValuesMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            ts.TypeDeclaration(var_name='...fields', type_=self.queryset.model_name + 'FieldName[]', rest_parameter=True),
            kwargs=response_handler_kwarg
        )
        return ts.public + ts.async_ + ts.Function(name='values',
                                                   call_signature=call_sig,
                                                   return_type='Promise<object[]>')(
        f"""
        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields)
        let responseData = await serverClient.get({ self.queryset.list_url }, responseHandlers, urlQuery)
        return responseData;
        """
        )