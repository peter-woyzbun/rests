from rests.typescript.queryset.method import QuerysetMethod
from rests.typescript import code_generators as ts


# =================================
# Serialize Method
# ---------------------------------

class SerializeMethod(QuerysetMethod):

    def generator(self):

        return ts.public + ts.Function(
            name='serialize', return_type='object'
        )(f"""
        return {{
            filters: this.lookups,
            exclude: this.excludedLookups,
            or_: this._or.map((queryset) => queryset.serialize())
        }}
                """)