from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts


# =================================
# Exclude Method
# ---------------------------------

class ExcludeMethod(QuerysetMethod):

    def generator(self):
        call_sig = ts.CallSignature(
            self.queryset.lookups_type_dec,
        )
        return ts.public + ts.Function(
            name='exclude', call_signature=call_sig, return_type=self.queryset.class_name
        )(f"""
                let updatedLookups = this.excludedLookups;
                Object.keys(lookups).map((lookupKey) => {{
                    const lookupValue = lookups[lookupKey];
                    if (lookupValue !== undefined){{ updatedLookups[lookupKey] = lookupValue }}
                }})
                this.excludedLookups = updatedLookups;
                return this;
                """)