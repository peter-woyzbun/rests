import json


# =================================
# Literal Value Helper
# ---------------------------------

def literal(value: str):
    return "'" + value + "'"


# =================================
# Ava Test
# ---------------------------------

class Test(object):

    def __init__(self, name: str):
        self.name = name
        self.imports = None
        self._async = False
        self._body = ''
        self._assertion = None

    def import_model(self, model_cls):
        self.imports = "import {} from './models'".format("{" + model_cls.__name__ + "}")
        return self

    def import_object(self, object_cls):
        self.imports = "import {} from './objects'".format("{" + object_cls.__name__ + "}")
        return self

    def async(self):
        self._async = True
        return self

    def body(self, src):
        self._body = src
        return self

    def deep_equal(self, a: str, b):
        if isinstance(b, (dict, list)):
            b = json.dumps(b)
        self._assertion = "t.deepEqual({a}, {b});".format(a=a, b=b)
        return self

    def source(self):
        source = "import test from 'ava'; \n"
        if self.imports:
            source += self.imports + "\n"
        source += "test('get-object-property', " + self._async * 'async ' + 't => {'
        source += self._body
        source += self._assertion
        source += '});'
        return source




