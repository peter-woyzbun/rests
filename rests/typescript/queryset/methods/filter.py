from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts


# =================================
# Filter Method
# ---------------------------------

class FilterMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            self.queryset.lookups_type_dec,
        )
        return ts.public + ts.Function(
            name='filter', call_signature=call_sig, return_type=self.queryset.class_name
        )(f"""
           let updatedLookups = this.lookups;
        Object.keys(lookups).map((lookupKey) => {{
            const lookupValue = lookups[lookupKey];
            if (lookupValue !== undefined){{ updatedLookups[lookupKey] = lookupValue }}
        }})
        this.lookups = updatedLookups;
        return this;
                """)