from unittest import TestCase
from typing import List

from rests.typescript.code_generators.type_declaration import TypeDeclaration
from rests.typescript.code_generators.call_signature import CallSignature
from rests.typescript.code_generators.name import Name
from rests.typescript.code_generators.function import Function
from rests.typescript.code_generators.klass import Klass
from rests.test.utils import clean_str


# =================================
# Test Type Declaration
# ---------------------------------

class TestTypeDeclaration(TestCase):

    def test_optional_declaration(self):
        declaration = TypeDeclaration(var_name='some_var', type_=List[str], optional=True)
        self.assertEqual(str(declaration), 'some_var?: Array<string>')

    def test_declaration(self):
        declaration = TypeDeclaration(var_name='some_var', type_=List[str], optional=False)
        self.assertEqual(str(declaration), 'some_var: Array<string>')

    def test_private(self):
        declaration = TypeDeclaration(var_name='some_var', type_=List[str], optional=False).private()
        self.assertEqual(str(declaration), 'private some_var: Array<string>')


# =================================
# Test Call Signature
# ---------------------------------

class TestCallSignature(TestCase):

    def test_w_kwargs(self):
        sig = CallSignature(TypeDeclaration(var_name='x', type_=str, optional=False),
                            TypeDeclaration(var_name='y', type_=float, optional=False),
                            kwargs={TypeDeclaration(var_name='z', type_=float, optional=False): '10'})
        self.assertEqual(str(sig), 'x: string, y: number, z: number = 10')


# =================================
# Test Call Signature
# ---------------------------------

class TestName(TestCase):

    def test_snake_to_camel(self):
        name = Name('python_name')
        self.assertEqual(str(name), 'pythonName')


# =================================
# Test Function
# ---------------------------------

class TestFunction(TestCase):

    def test_function(self):
        sig = CallSignature(TypeDeclaration(var_name='x', type_=str, optional=False),
                            TypeDeclaration(var_name='y', type_=float, optional=False),
                            kwargs={TypeDeclaration(var_name='z', type_=float, optional=False): '10'})
        test_func = Function(name='constructor', call_signature=sig)("return {x, y, z}")
        expected = """
        constructor(x: string, y: number, z: number = 10){
            return {x, y, z}
        }
        """
        self.assertEqual(clean_str(str(test_func)),
                         clean_str(expected))

    def test_public_function(self):
        sig = CallSignature(TypeDeclaration(var_name='x', type_=str, optional=False),
                            TypeDeclaration(var_name='y', type_=float, optional=False),
                            kwargs={TypeDeclaration(var_name='z', type_=float, optional=False): '10'})
        test_func = Function(name='myFunc', call_signature=sig)("return {x, y, z}").public()
        expected = """
                public myFunc(x: string, y: number, z: number = 10){
                    return {x, y, z}
                }
                """
        self.assertEqual(clean_str(str(test_func)),
                         clean_str(expected))


# =================================
# Test Klass
# ---------------------------------

class TestKlass(TestCase):

    def test_klass_no_body(self):
        type_decs = [
            TypeDeclaration(var_name='x', type_=str, optional=False),
            TypeDeclaration(var_name='y', type_=float, optional=False),
            TypeDeclaration(var_name='z', type_=float, optional=False)
        ]
        sig = CallSignature(TypeDeclaration(var_name='x', type_=str, optional=False),
                            TypeDeclaration(var_name='y', type_=float, optional=False),
                            kwargs={TypeDeclaration(var_name='z', type_=float, optional=False): '10'})
        klass = Klass(name='TestClass', constructor_signature=sig, type_declarations=type_decs)
        expected = """
        class TestClass {
        
            x: string
            y: number
            z: number
        
            constructor(x: string, y: number, z: number = 10){
                this.x = x
                this.y = y
                this.z = z
            }
            
        }
        
        """

        self.assertEqual(clean_str(str(klass)),
                         clean_str(expected))