from typing import Callable, Type, TYPE_CHECKING, Tuple, Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission

from rests.core.utils.urls import underscore_to_dash
from rests.core.exceptions import EndpointError
from rests.core.utils.signature import Signature

# This provides type hinting without circular import issues.
if TYPE_CHECKING:
    from rests.interface.object.object import Object


# =================================
# Interface Object Endpoint
# ---------------------------------

class Endpoint(object):

    """
    An `Endpoint` is a view for an `interface.Object`.

    """

    def __init__(self, func: Callable,
                 permission_classes: Optional[Tuple[Type[BasePermission]]]=None,
                 arg_serializer: Callable = None):
        self.obj_cls: Type['Object'] = None
        self.func = func
        self.func_signature = Signature(func)
        self.permission_classes = permission_classes
        self.arg_serializer = arg_serializer

        self._validate()

    def _validate(self):
        if self.arg_serializer is not None:
            serializer_sig = Signature(self.arg_serializer)
            if not set(serializer_sig.param_names) <= set(self.func_signature.param_names):
                raise EndpointError("The `arg_serializer` callable's signature parameter set should be a subset of "
                                    " the endpoint's function signature parameter set. ")

    @property
    def url_name(self) -> str:
        return underscore_to_dash(self.func.__name__)

    @property
    def view_name(self):
        return self.func.__name__

    def as_view(self):
        """
        Return the view function for this `Endpoint` instance. The view accepts
        POST requests only. The view does the following:

            1) Create an instance of this `Endpoint`'s `obj_cls` using
            provided `__init__` data, which will be passed to `func` as `self`,
            2) Call the `func` of this `Endpoint` instance, passing it
            args, where appropriate, and
            3) Returns the output of `func` in a `Response`.


        """
        def view_func(request: Request):
            obj = self.obj_cls(**request.data['__init__'])
            if 'args' in request.data:
                output = self.func(obj, **request.data['args'])
            else:
                output = self.func(obj)
            return Response(output, status=status.HTTP_200_OK)
        if self.permission_classes:
            view_func.permission_classes = self.permission_classes
        return api_view(['POST'])(view_func)
