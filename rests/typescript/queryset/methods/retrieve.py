from rests.typescript.server_client.server_client import RESPONSE_HANDLERS_TYPE, response_handler_kwarg
from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts
from rests.typescript import types


# =================================
# Retrieve Method
# ---------------------------------

class RetrieveMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            kwargs=response_handler_kwarg
        )
        return ts.public + ts.async_ + ts.Function(name='retrieve',
                                                   call_signature=call_sig,
                                                   return_type=f"Promise<{ self.queryset.model_name }[] | undefined>")(
        f"""
        const urlQuery = "query=" + JSON.stringify(this.serialize())
        let responseData = await serverClient.get({ self.queryset.list_url }, responseHandlers, urlQuery)
        return responseData.map((data) => new { self.queryset.model_name }(data) )
        """
        )