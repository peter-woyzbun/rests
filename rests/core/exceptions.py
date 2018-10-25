from django.core.exceptions import ImproperlyConfigured


class RestsException(Exception):
    pass


class TranspileError(RestsException):
    pass


class InterfaceError(RestsException, ImproperlyConfigured):
    pass


class EndpointError(InterfaceError):
    pass
