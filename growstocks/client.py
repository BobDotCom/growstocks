"""
MIT License

Copyright (c) 2021-present BobDotCom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Optional, Union

import requests
import aiohttp

from .scopes import Scopes
from .types.client import DefaultRedirects
from .wrapper import Auth, Pay

__all__ = "Client",


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
    auth: :class:`Auth`
        Base class for authorization endpoints.
    pay: :class:`Pay`
        Base class for pay endpoints.
    client: :class:`int`
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

    def __init__(
            self,
            client: int,
            secret: str,
            *,
            default_scopes: Scopes = Scopes(),
            default_redirects: Optional[DefaultRedirects] = None
    ):
        if default_redirects is None:
            default_redirects = DefaultRedirects(site='', auth=None, pay=None)
        self.client = client
        self.secret = secret
        self._session: Union[requests.Session, aiohttp.ClientSession] = requests.session()
        self.default_scopes = default_scopes
        self.default_redirects = default_redirects
        self.api_url = 'https://api.growstocks.xyz/v1'
        self.auth = Auth(self)
        self.pay = Pay(self)
        self.is_async = False

    @property
    def session(self) -> Union[requests.Session, aiohttp.ClientSession]:
        """
        Session object used when querying api. May be an instance of :class:`requests.Session` or
        :class:`aiohttp.ClientSession`.

        :meta private:
        """
        return self._session
