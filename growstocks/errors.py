"""
All custom errors that can be raised from this module.
"""


class GrowstocksException(Exception):
    """
    Base Exception for all errors raised from this module.
    """
    pass


class RequestFailure(GrowstocksException):
    """
    Raised when a query to the API failed.
    """
    pass


class RedirectUriNone(GrowstocksException):
    """
    Raised when a redirect uri is :class:`None`.
    """
    pass
