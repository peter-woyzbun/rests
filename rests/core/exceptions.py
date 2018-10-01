

class RestsException(Exception):
    pass


class TranspileError(RestsException):
    pass


class InterfaceError(RestsException):
    pass


class EndpointError(InterfaceError):
    pass
