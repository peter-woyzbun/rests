from unittest import TestCase

from rests.core.utils.signature import Signature


# =================================
# Test Signature
# ---------------------------------

class TestSignature(TestCase):

    def test_param_types(self):

        def some_func(a: int, b: str):
            return a, b

        signature = Signature(some_func)
        self.assertEqual(signature['a'].type, int)
        self.assertEqual(signature['b'].type, str)

    def test_param_defaults(self):

        def some_func(a: int, b: str = None):
            return a, b

        signature = Signature(some_func)
        self.assertTrue(signature['b'].has_default)
        self.assertFalse(signature['a'].has_default)