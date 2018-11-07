from typing import Callable, Type, TYPE_CHECKING, Tuple, Optional

from django.db import models
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
# Interface Type Method
# ---------------------------------

class Method(object):

    """
    An `Endpoint` is a view for an `interface.Object`.

    """

    def __init__(self, func: Callable,
                 permission_classes: Optional[Tuple[Type[BasePermission]]]=None,
                 arg_serializer: Callable = None,
                 literal_return_type: str = None,
                 is_static=False):
        self.obj_cls: Type['Object'] = None
        self.func = func
        self.func_signature = Signature(func)
        self.permission_classes = permission_classes
        self.arg_serializer = arg_serializer
        self.literal_return_type = literal_return_type
        self.is_static = is_static
        self.model_cls: Type[models.Model] = None

        self._validate()

    def _validate(self):
        if self.arg_serializer is not None:
            serializer_sig = Signature(self.arg_serializer)
            if not set(serializer_sig.param_names) <= set(self.func_signature.param_names):
                raise EndpointError("The `arg_serializer` callable's signature parameter set should be a subset of "
                                    " the endpoint's function signature parameter set. ")

    @property
    def name(self):
        return self.func.__name__

    @property
    def url_name(self) -> str:
        return underscore_to_dash(self.func.__name__)

    @property
    def view_name(self):
        return self.func.__name__

    def as_view(self, model_cls):
        """
        Return the view function for this `Endpoint` instance. The view accepts
        POST requests only. The view does the following:

            1) Call the `func` of this `Endpoint` instance, passing it
            args, where appropriate, and
            2) Returns the output of `func` in a `Response`.


        """

        def view_func(request: Request, pk):
            obj = model_cls.objects.get(pk=pk)
            if not self.is_static:
                output = self.func(obj, **request.data)
            else:
                output = self.func(**request.data)
            return Response(output, status=status.HTTP_200_OK)
        if self.permission_classes:
            view_func.permission_classes = self.permission_classes
        return api_view(['POST'])(view_func)
