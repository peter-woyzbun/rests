from typing import TYPE_CHECKING

# This prevents any circular import issues but still allows for type hinting.
if TYPE_CHECKING:
    from rests.typescript.model.model import Model


# =================================
# Typescript Model Method
# ---------------------------------

class ModelMethod(object):

    """
    Base class for defining Model class methods.

    """

    def __init__(self, model: 'Model'):
        self.model = model

    def generator(self):
        raise NotImplementedError