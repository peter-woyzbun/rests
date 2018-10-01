import typing
import inspect

from django.urls import path, include
from django.db import models

from rests.interface.type import Type as InterfaceType
from rests.interface.object import Object
from rests.core.utils.urls import camel_case_to_underscore
from rests.core.exceptions import InterfaceError


# =================================
# Interface
# ---------------------------------

class Interface(object):

    """
    Class for defining a rests 'interface'.

    """

    def __init_subclass__(cls, **kwargs):
        """
        Do a check for duplicate models, which would result in a bad 'transpile'.

        """
        model_names = [m.__name__ for m in cls.models()]
        if len(model_names) > len(set(model_names)):
            raise InterfaceError("Interface has one or more duplicate models. Every `interface.Type` for an interface "
                                 "must have a unique model. ")

    @classmethod
    def types(cls) -> typing.Dict[str, InterfaceType]:
        """
        Return a dictionary mapping the name of every `interface.Type`
        associated with this Interface to its instance.

        """
        types = {}
        for k, v in cls.__dict__.items():
            if isinstance(v, InterfaceType):
                    types[k] = v
        return types

    @classmethod
    def objects(cls) -> typing.Dict[str, typing.Type[Object]]:
        """
        Return a dictionary mapping the name of every `interface.Object`
        associated with this Interface to its class.

        """
        objects = {}
        for k, v in cls.__dict__.items():
            if inspect.isclass(v):
                if issubclass(v, Object) or (Object in v.__mro__):
                    objects[k] = v
        return objects

    @classmethod
    def models(cls) -> typing.List[typing.Type[models.Model]]:
        """
        Return list of Model classes for this Interface. Each `interface.Type`
        has a model.

        """
        models_ = list()
        for interface_type in cls.types().values():
            models_.append(interface_type.model_cls)
        return models_

    @classmethod
    def urlpatterns(cls):
        """
        Return the Django URL patterns for this interface.

        """
        urlpatterns = []
        for interface_type in cls.types().values():
            urlpatterns.append(
                path('{}/'.format(interface_type.base_url),
                     include((interface_type.urlpatterns(), camel_case_to_underscore(interface_type.model_name)))),
            )
        for object_cls in cls.objects().values():
            urlpatterns.append(
                path('{}/'.format(object_cls.base_url()),
                     include((object_cls.urlpatterns(), camel_case_to_underscore(object_cls.__name__)))),
            )
        return urlpatterns

    @classmethod
    def base_url(cls):
        return '/'