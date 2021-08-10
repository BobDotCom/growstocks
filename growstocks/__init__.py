"""
===================
growstocks
===================

A wrapper for the GrowStocks API, made for both synchronous and asynchronous applications.

PyPI: https://pypi.org/project/growstocks/

Docs: https://growstocks.readthedocs.io/en/latest/

Installation
############

You can install released versions of growstocks from the Python Package Index via pip or a similar tool:

**Stable Release:** ``pip install growstocks``

**Working Version:** ``pip install git+https://github.com/BobDotCom/growstocks.git``

Usage
#####

.. code-block:: python
    >>> import growstocks
    >>> client = growstocks.Client(913117854995652992,"T%GRD4iEiFmgyYE!O5&ZCx3Rn%uqwPV3")
    >>> client.default_scopes = growstocks.Scopes(profile=True, balance=True, discord=True)
    >>> user = client.auth.fetch_user('31G4k57rG3asdyyi5Lqk')
    >>> dict(user)
    {'discord_id': '690420846774321221',
     'id': 1916,
     'name': 'BobDotCom',
     'email': None,
     'growid': 'Bob430',
     'balance': 3}

Using Async
###########
To use in an async context, just use ``import growstocks.aio as growstocks`` as your import and make sure to await the
functions marked as coroutines.

.. code-block:: python

    import growstocks.aio as growstocks
"""
import asyncio

import requests

from . import errors
from .ext import *
from .wrapper import *

# PACKAGE INFO
__title__ = "growstocks"
__author__ = 'BobDotCom'
__version__ = '1.0.1'

__license__ = "MIT License"
__copyright__ = "Copyright 2021 {}".format(__author__)


class Client:
    """
    Base client object. Contains classes for both authorization and pay endpoints.

    Parameters
    -----------
    client: :class:`int`
        Client ID
    secret: :class:`str`
        Client secret, it is recommended to store this in an environment variable or other secure method
    default_scopes: :class:`Scopes`, optional
        Default scopes to use for endpoints requiring scopes. May be defined after initialization
    default_redirects: :class:`dict`, optional
        A dict of the default redirects. Accepted keys are "site", "auth", and "pay". The site value
        is used for shorthand and will be substituted in for "{0}" in the other values.

    Attributes
    -----------
    auth: :class:`auth`
        Base class for authorization endpoints.
    pay: :class:`pay`
        Base class for pay endpoints.
    client: :class:`client`
        Client ID
    secret: :class:`str`
        Client secret
    default_scopes: :class:`Scopes`
        Default scopes to use for endpoints requiring scopes.
    default_redirects: :class:`dict`
        A dict of the default redirects
    api_url: :class:`str`
        The url to use when querying the api
    """

    def __init__(self, client, secret, default_scopes=Scopes(), default_redirects=None):
        if default_redirects is None:
            default_redirects = {
                'site': '', 'auth': None
                }
        self.client = client
        self.secret = secret
        self._session = requests.session()
        self.default_scopes = default_scopes
        self.default_redirects = default_redirects
        self.api_url = 'https://api.growstocks.xyz/v1'
        self.auth = auth(self)
        self.pay = pay(self)

    @property
    def session(self):
        """
        Session object used when querying api. May be an instance of :class:`requests.Session` or
        :class:`aiohttp.ClientSession`.

        :meta private:
        """
        return self._session
