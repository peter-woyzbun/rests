from typing import Type, Union
import copy

from rests.core.typescript.code_generator import CodeGenerator
from rests.typescript.code_generators.destructuring import Destructuring
from rests.typescript.type_transpiler import TypeTranspiler


# =================================
# Type Declaration
# ---------------------------------

class TypeDeclaration(CodeGenerator):

    def __init__(self, var_name: Union[str, Destructuring],
                 type_: Union[str, Type], optional: bool = False, rest_parameter: bool = False):
        self.var_name = var_name
        self._type = type_
        self.optional = optional
        self.rest_parameter = rest_parameter
        self.accessor = ""

        CodeGenerator.__init__(self)

    def __lt__(self, other: 'TypeDeclaration'):
        """
        This allows for `TypeDeclarations` to be sorted based on TypeScript's
        grammar - i.e "rest parameters" first, then arguments with default values.

        See: https://www.typescriptlang.org/docs/handbook/functions.html

        """
        if self.rest_parameter:
            return False
        if not self.rest_parameter and other.rest_parameter:
            return True

        if not self.optional and (other.optional or other.rest_parameter):
            return True

    def public(self):
        clone = copy.copy(self)
        clone.accessor = "public "
        return clone

    def private(self):
        clone = copy.copy(self)
        clone.accessor = "private "
        return clone

    def protected(self):
        clone = copy.copy(self)
        clone.accessor = "protected "
        return clone

    @property
    def type(self):
        if isinstance(self._type, str):
            return self._type
        return TypeTranspiler.transpile(type_=self._type)

    def _render(self):
        return self.accessor + str(self.var_name) + '?' * self.optional + ": " + self.type