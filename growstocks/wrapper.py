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
import base64
import inspect
from typing import Union, Awaitable, TYPE_CHECKING, TypeVar, Optional, Any, Dict

import aiohttp.web_response
import requests
import urllib3.request

from .errors import RequestFailure, RedirectUriNone
from .transaction import Transaction
from .user import User

if TYPE_CHECKING:
    from .client import Client
    from .scopes import Scopes
else:
    Client = TypeVar("Client")
    Scopes = TypeVar("Scopes")

__all__ = "Auth", "Pay"

AiohttpResponse = TypeVar("AiohttpResponse", bound=aiohttp.client._RequestContextManager)
Response = Union[requests.Response, AiohttpResponse]


class Auth:
    """
    Base class for authorization endpoints. Not meant to be initialized outside a client object.

    Parameters
    -----------
    client: :class:`Client`
        Client object

    Attributes
    -----------
    client: :class:`Client`
        The client object passed in initialization
    api_url: :class:`str`
        The base url to use for authorization endpoints. Uses :obj:`Client.api_url` to generate.

    """

    def __init__(self, client: Client):
        self.client = client
        self.api_url = '{0}/auth'.format(self.client.api_url)

    def make_url(self, redirect_uri: Optional[str] = None, scopes: Optional[Scopes] = None) -> str:
        """
        Generate an authorization url with set parameters

        Parameters
        -----------
        redirect_uri: :class:`str`, optional
            Url to redirect to after authorization, defaults to Client.default_redirects['auth']
        scopes: :class:`Scopes`, optional
            Scopes for the authorization, defaults to Client.default_scopes

        Raises
        -------
        RedirectUriNone
            redirect_uri is :class:`None`

        Returns
        --------
        :class:`str`
            Authorization url
        """
        if redirect_uri is None:
            redirect_uri = self.client.default_redirects['auth']
            if redirect_uri is None:
                raise RedirectUriNone('redirect_uri must not be None')
            else:
                redirect_uri = redirect_uri.format(self.client.default_redirects['site'])
        scopes = self.client.default_scopes if scopes is None else scopes
        _redirect_uri = base64.b64encode(redirect_uri.encode('ascii')).decode('ascii')
        url = 'https://auth.growstocks.xyz/user/authorize'
        # TODO: Do something better here
        params = urllib3.request.urlencode({  # type: ignore[attr-defined]
            'client': self.client.client, 'scopes': str(scopes), 'redirect_uri': _redirect_uri
        })
        return '{0}?{1}'.format(url, params)

    def fetch_user(self, token: str, scopes: Optional[Scopes] = None) -> Union[User, Awaitable[User]]:
        """
        Fetch a user from the api by their token.

        Parameters
        -----------
        token: :class:`str`
            The user's authorization token, granted from :meth:`make_url`.
        scopes: :class:`Scopes`, optional
            The scopes to use for authenticating the user, defaults to client default scopes.

        Raises
        ------
        RequestFailure
            API call failed.

        Returns
        --------
        :class:`User`
            The user fetched from the api.

        Notes
        -----
        When used in async, this is a coroutine.
        """
        scopes = self.client.default_scopes if scopes is None else scopes
        payload = {
            'secret': self.client.secret, 'token': token, 'scopes': str(scopes)
        }
        if scopes is None:
            del payload['scopes']

        resp = self.client.session.post('{0}/user'.format(self.api_url), data=payload)
        if inspect.isawaitable(resp):
            async def ret_coro(resp_: AiohttpResponse) -> User:
                resp_val = await resp_
                try:
                    rtrn_json_ = await resp_val.json()
                except:
                    raise RequestFailure('Request to api was unsuccessful: {0}'.format(await resp_val.text()))
                if not rtrn_json_['success']:
                    raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json_))

                return User.from_dict(rtrn_json_['user'])

            return ret_coro(resp)  # type: ignore[type-var]
        else:
            try:
                rtrn_json = resp.json()  # type: ignore[union-attr]
            except:
                raise RequestFailure(
                    'Request to api was unsuccessful: {0}'.format(resp.text)  # type: ignore[union-attr]
                )
            if not rtrn_json['success']:
                raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json))

            return User.from_dict(rtrn_json['user'])


class Pay:
    """
    Base class for pay endpoints. Not meant to be initialized outside a client object.

    Parameters
    -----------
    client: :class:`Client`
        Client object

    Attributes
    -----------
    client: :class:`Client`
        The client object passed in initialization
    api_url: :class:`str`
        Api url used for endpoints
    """

    def __init__(self, client: Client):
        self.client = client
        self.api_url = '{0}/pay'.format(self.client.api_url)

    def create_transaction(
            self,
            user: User,
            amount: int,
            notes: Optional[str] = None
    ) -> Union[Transaction, Awaitable[Transaction]]:
        """
        Create a transaction.

        Parameters
        ----------
        user: :class:`User`
            The user to create the transaction for.
        amount: :class:`int`
            The amount of world locks to request
        notes: :class:`str`, optional
            Transaction notes to send. Maximum of 50 chars.

        Raises
        ------
        RequestFailure
            API call failed

        Returns
        -------
        :class:`Transaction`
            The transaction object

        Notes
        -----
        When used in async, this is a coroutine.
        """
        payload = {
            'secret': self.client.secret, 'user': int(user.id), 'amount': int(amount), 'notes': str(notes)
        }
        if notes is None:
            del payload['notes']

        resp = self.client.session.post('{0}/transaction/create'.format(self.api_url), data=payload)
        if inspect.isawaitable(resp):
            async def ret_coro(resp_: AiohttpResponse) -> Transaction:
                resp_val = await resp_
                rtrn_json_ = await resp_val.json()
                if not rtrn_json_['success']:
                    raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json_))

                rtrn_transaction_ = Transaction(rtrn_json_['transaction'], client=self.client)

                return rtrn_transaction_

            return ret_coro(resp)  # type: ignore[type-var]
        else:
            rtrn_json = resp.json()  # type: ignore[union-attr]
            if not rtrn_json['success']:
                raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json))

            rtrn_transaction = Transaction(rtrn_json['transaction'], client=self.client)

            return rtrn_transaction

    def make_payment_url(
            self,
            transaction: Transaction,
            redirect_uri: Optional[str] = None
    ) -> str:
        """
        Make a payment url for a transaction

        Parameters
        -----------
        transaction: :class:`Transaction`
            The transaction to make a payment url for.
        redirect_uri: :class:`str`, optional
            URL to redirect the user to

        Raises
        -------
        RedirectUriNone
            redirect_uri is None

        Returns
        --------
        :class:`str`
            Payment URL
        """
        if redirect_uri is None:
            redirect_uri = self.client.default_redirects['pay']
            if redirect_uri is None:
                raise RedirectUriNone('redirect_uri must not be None')
            else:
                redirect_uri = redirect_uri.format(self.client.default_redirects['site'])
        _redirect_uri = base64.b64encode(redirect_uri.encode('ascii')).decode('ascii')
        url = 'https://pay.growstocks.xyz/pay'
        params = urllib3.request.urlencode({  # type: ignore[attr-defined]
            'client': self.client.client, 'redirect_uri': _redirect_uri, 'transaction': str(transaction.id)
        })
        return '{0}?{1}'.format(url, params)

    def fetch_transaction(self, transaction: Transaction) -> Union[Transaction, Awaitable[Transaction]]:
        """
        Fetch info about a transaction.

        Parameters
        ----------
        transaction: :class:`Transaction`
            Transaction object to fetch info about.

        Raises
        ------
        RequestFailure
            API call failed.

        Returns
        -------
        :class:`Transaction`
            Transaction object with info about the fetched transaction.

        Notes
        -----
        When used in async, this is a coroutine.
        """
        payload = {
            'secret': self.client.secret, 'transaction': transaction.id
        }

        resp = self.client.session.post('{0}/transaction/create'.format(self.api_url), data=payload)
        if inspect.isawaitable(resp):
            async def ret_coro(resp_: AiohttpResponse) -> Transaction:
                resp_val = await resp_
                rtrn_json_ = await resp_val.json()
                if not rtrn_json_['success']:
                    raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json_))

                rtrn_transaction_ = Transaction.from_dict(rtrn_json_['transaction'], client=self.client)

                return rtrn_transaction_

            return ret_coro(resp)  # type: ignore[type-var]
        else:
            rtrn_json = resp.json()  # type: ignore[union-attr]
            if not rtrn_json['success']:
                raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json))

            rtrn_transaction = Transaction.from_dict(rtrn_json['transaction'], client=self.client)

            return rtrn_transaction

    def send(
            self,
            user: User,
            amount: int,
            notes: Optional[str] = None
    ) -> Union[Dict[str, Any], Awaitable[Dict[str, Any]]]:
        """
        Send world locks to a user.

        Parameters
        ----------
        user: :class:`User`
            User to send to
        amount: :class:`int`
            Amount to send
        notes: :class:`str`, optional
            Information about the transaction

        Raises
        ------
        RequestFailure
            Request to api failed

        Returns
        -------
        :class:`dict`
            Response from the API

        Notes
        -----
        When used in async, this is a coroutine.
        """
        payload = {
            'secret': self.client.secret, 'party': user.id, 'amount': amount, 'notes': notes
        }
        resp = self.client.session.post('{0}/send'.format(self.api_url), data=payload)
        if inspect.isawaitable(resp):
            async def ret_coro(resp_: AiohttpResponse) -> dict[str, Any]:
                resp_val = await resp_
                rtrn_json_ = await resp_val.json()
                if not rtrn_json_['success']:
                    raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json_))
                return rtrn_json_  # type: ignore[no-any-return]

            return ret_coro(resp)  # type: ignore[type-var]
        else:
            rtrn_json = resp.json()  # type: ignore[union-attr]
            if not rtrn_json['success']:
                raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json))
            return rtrn_json  # type: ignore[no-any-return]

    def get_balance(self) -> Union[int, Awaitable[int]]:
        """
        Get the current balance of your account

        Raises
        ------
        RequestFailure
            Request to api failed

        Returns
        -------
        :class:`int`
            Your balance

        Notes
        -----
        When used in async, this is a coroutine.
        """
        payload = {
            'secret': self.client.secret
        }
        resp = self.client.session.post('{0}/balance'.format(self.api_url), data=payload)
        if inspect.isawaitable(resp):
            async def ret_coro(resp_: AiohttpResponse) -> int:
                resp_val = await resp_
                rtrn_json_ = await resp_val.json()
                if not rtrn_json_['success']:
                    raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json_))
                return int(rtrn_json_['balance'])

            return ret_coro(resp)  # type: ignore[type-var]
        else:
            rtrn_json = resp.json()  # type: ignore[union-attr]
            if not rtrn_json['success']:
                raise RequestFailure('Request to api was unsuccessful: {0}'.format(rtrn_json))
            return int(rtrn_json['balance'])
