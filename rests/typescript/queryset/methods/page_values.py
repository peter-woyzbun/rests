from rests.typescript.server_client.server_client import RESPONSE_HANDLERS_TYPE, response_handler_kwarg
from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts
from rests.typescript import types


# =================================
# Page Values Method
# ---------------------------------

class PageValuesMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            ts.TypeDeclaration(var_name='...fields', type_=self.queryset.model_name + 'FieldName[]', rest_parameter=True),
            kwargs={
                ts.TypeDeclaration(var_name='pageNum', type_=types.NUMBER): '1',
                ts.TypeDeclaration(var_name='pageSize', type_=types.NUMBER): '25',
                **response_handler_kwarg
            }
        )
        return ts.public + ts.async_ + ts.Function(name='pageValues',
                                                   call_signature=call_sig,
                                                   return_type='Promise<{num_results: number, num_pages: number, data: object[]}>')(
        f"""
        const urlQuery = "query=" + JSON.stringify(this.serialize()) + "&fields=" + JSON.stringify(fields) + "&page=" + pageNum + "&pagesize=" + pageSize;
        let responseData = await serverClient.get({ self.queryset.list_url }, responseHandlers, urlQuery)
        return responseData;
        """
        )