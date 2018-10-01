from unittest import TestCase
from typing import List, Union

from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript import types


# =================================
# Test Type Transpiler
# ---------------------------------

class TestTypeTranspiler(TestCase):

    def test_transpiler_atomic(self):
        type_a = int
        type_b = str
        type_c = bool
        type_d = types.Undefined
        self.assertEqual(TypeTranspiler.transpile(type_a), types.NUMBER)
        self.assertEqual(TypeTranspiler.transpile(type_b), types.STRING)
        self.assertEqual(TypeTranspiler.transpile(type_c), types.BOOLEAN)
        self.assertEqual(TypeTranspiler.transpile(type_d), types.UNDEFINED)

    def test_transpiler_container_types(self):
        type_a = List[int]
        type_b = List[str]
        type_c = types.Promise[int]
        self.assertEqual(TypeTranspiler.transpile(type_a), "Array<number>")
        self.assertEqual(TypeTranspiler.transpile(type_b), "Array<string>")
        self.assertEqual(TypeTranspiler.transpile(type_c), "Promise<number>")

    def test_transpiler_composite_types(self):
        type_a = Union[int, str]
        type_b = Union[List[str], bool]
        self.assertEqual(TypeTranspiler.transpile(type_a), "number | string")
        self.assertEqual(TypeTranspiler.transpile(type_b), "Array<string> | boolean")