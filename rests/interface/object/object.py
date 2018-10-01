from typing import List
import re

from django.urls import path, include

from rests.interface.object.endpoint import Endpoint
from rests.core.utils.signature import Signature


# =================================
# Interface Object
# ---------------------------------

class Object(object):

    """
    An interface `Object` represents an arbitrary TypeScript class whose
    methods will be calls to the `Endpoint`s of this `Object`.


    """

    @classmethod
    def urlpatterns(cls):
        return [path(endpoint.url_name + "/", endpoint.as_view(), name=endpoint.view_name) for endpoint in cls.endpoints()]

    @classmethod
    def endpoints(cls) -> List[Endpoint]:
        endpoints = list()
        for k, v in cls.__dict__.items():
            if isinstance(v, Endpoint):
                v.obj_cls = cls
                endpoints.append(v)
        return endpoints

    @classmethod
    def init_signature(cls) -> Signature:
        return Signature(cls.__init__)

    @classmethod
    def endpoint(cls, permission_classes=None):
        """
        Register decorated class method as an `Endpoint`.

        """
        def decorator(func):
            endpoint = Endpoint(func=func, permission_classes=permission_classes)
            return endpoint
        return decorator

    @classmethod
    def base_url(cls):
        """
        Return the 'base url' for this interface `Object`. For an `Object` class `CamelCase`,
        this will return `camel-case`.

        """
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', cls.__name__)
        return "-".join([m.group(0).lower() for m in matches])

