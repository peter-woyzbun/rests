from typing import TypeVar, Sequence


# =================================
# Typescript Type Literals
# ---------------------------------

STRING = 'string'
NUMBER = 'number'
OBJECT = 'object'
UNDEFINED = 'undefined'
ARRAY = 'Array'
ANY = 'any'
PROMISE = 'Promise'
BOOLEAN = 'boolean'
NULL = 'null'
DATE = 'Date'

# =================================
# Typescript Type Base
# ---------------------------------

TypeScriptType = TypeVar('TypeScriptType')


# =================================
# Typescript Types
# ---------------------------------

class Promise(Sequence[TypeScriptType]):
    pass


class Undefined(object):
    pass


