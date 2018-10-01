import inspect
from typing import Callable, Type, Dict


# =================================
# Parameter
# ---------------------------------

class Parameter(object):

    def __init__(self, name, type_: Type, optional: bool):
        self.name = name
        self.type = type_
        self.has_default = optional


# =================================
# Signature
# ---------------------------------

class Signature(object):

    def __init__(self, callable_: Callable):
        self.callable = callable_
        self.parameters: Dict[str, Parameter] = dict()

        self._make_parameters()

    @property
    def param_names(self):
        return [p.name for p in self.parameters.values()]

    def _make_parameters(self):
        signature = inspect.signature(self.callable)
        for param in signature.parameters.values():
            if param.name != 'self':
                self.parameters[param.name] = Parameter(name=param.name,
                                                        type_=signature.parameters[param.name].annotation,
                                                        optional=param.default != inspect.Parameter.empty)

    def __getitem__(self, item) -> Parameter:
        return self.parameters[item]