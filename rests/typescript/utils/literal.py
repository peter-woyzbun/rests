

class Literal(object):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return "null"
