from typing import TYPE_CHECKING

# This prevents any circular import issues but still allows for type hinting.
if TYPE_CHECKING:
    from rests.typescript.queryset.queryset import Queryset


# =================================
# Typescript Queryset Method
# ---------------------------------

class QuerysetMethod(object):

    """
    Base class for defining Queryset class methods.

    """

    def __init__(self, queryset: 'Queryset'):
        self.queryset = queryset

    def generator(self):
        raise NotImplementedError