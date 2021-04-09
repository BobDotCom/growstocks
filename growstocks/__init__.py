"""
===================
growstocks
===================

A wrapper for the GrowStocks API, made for both synchronous and asynchronous applications.

NOTE: asynchronous support has not been implemented yet, but is planned for the near future.

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
    >>> user = client.oauth.fetch_user('31G4k57rG3asdyyi5Lqk')
    >>> dict(user)
    {'discord_id': '690420846774321221',
     'id': 1916,
     'name': 'BobDotCom',
     'email': None,
     'growid': 'Bob430',
     'balance': 3}
"""
import base64
import typing

import requests
import urllib3

# PACKAGE INFO
__title__ = "growstocks"
__author__ = 'BobDotCom'
__version__ = '0.0.1'

__license__ = "MIT License"
__copyright__ = "Copyright 2021 {}".format(__author__)


api_url: str = 'https://api.growstocks.xyz/v1/auth'


class Scopes:

    def __init__(self, profile: bool = True, email: bool = False, balance: bool = False, discord: bool = False) -> None:
        if balance or discord:
            profile = True
        if email:
            profile = False

        self.profile: bool = profile
        self.email: bool = email
        self.balance: bool = balance
        self.discord: bool = discord

    @property
    def as_list(self):
        return [k for k, v in self.as_dict.items() if v]

    @property
    def as_dict(self):
        return {
            'profile': self.profile, 'email': self.email, 'balance': self.balance, 'discord': self.discord
            }

    def __str__(self):
        return ','.join(self.as_list)

    def __repr__(self):
        return str(self)


class PartialUser:

    def __init__(self, id: int, name: str, email: str = None, growid: str = None, balance: int = None,
                 discord_id: int = None):
        self.id: int = id
        self.name: typing.Optional[str] = name
        self.email: typing.Optional[str] = email
        self.growid: typing.Optional[str] = growid
        self.balance: typing.Optional[int] = balance
        self.discord_id: typing.Optional[int] = discord_id


class User(PartialUser):

    @classmethod
    def from_dict(cls, input_dict: dict) -> 'User':
        id_ = input_dict.get('id')
        name = input_dict.get('name')
        email = input_dict.get('email')
        growid = input_dict.get('growid')
        balance = input_dict.get('balance')
        discord_id = input_dict.get('discordID')

        return cls(id=id_, name=name, email=email, growid=growid, balance=balance, discord_id=discord_id)

    def as_dict(self) -> dict:
        return dict(self)

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        self_info = [('id', self.id), ('name', self.name), ('email', self.email), ('growid', self.growid),
                     ('balance', self.balance), ('discord_id', self.discord_id)]
        if self._n <= len(self_info):
            ret = self_info[self._n - 1]
            self._n += 1
            return ret
        else:
            raise StopIteration

    def __str__(self) -> str:
        return self.name

    # def __repr__(self) -> repr:  #     return str(self)


class Client:

    def __init__(self, client: int, secret: str, default_scopes: Scopes = Scopes(), default_redirects=None) -> None:
        """
        Base client object. Contains classes for both authorization and pay endpoints.

        :param client: Client ID
        :type client: int
        :param secret: Client secret, it is recommended to store this in an environment variable or other secure method
        :type secret: str
        :param default_scopes: Default scopes to use for endpoints requiring scopes. May be defined after initialization
        :type default_scopes: Scopes
        :param default_redirects: A dict of the default redirects. Accepted keys are "site" and "auth". The site value
        is used for shorthand and will be substituted in for "{site}" in the other values.
        :type default_redirects: dict
        """
        if default_redirects is None:
            default_redirects = {
                'site': '', 'auth': None
                }
        self.client: int = client
        self.secret: str = secret
        self.default_scopes: Scopes = default_scopes
        self.default_redirects: dict = default_redirects
        self.auth: auth = auth(self)
        self.pay: pay = pay(self)


class auth:

    def __init__(self, client: Client) -> None:
        """
        Base class for authorization endpoints. Not meant to be initialized outside a client object.

        :param client: Client object
        :type client: Client
        """
        self.client: Client = client
        self._ratelimits = NotImplemented

    def make_url(self, redirect_uri: str = None, scopes: Scopes = None) -> str:
        """
        Generate an authorization url with set parameters

        :param redirect_uri: Url to redirect to after authorization, defaults to Client.default_redirects['auth']
        :type redirect_uri: str
        :param scopes: Scopes for the authorization, defaults to Client.default_scopes
        :type scopes: Scopes
        :return: Authorization url
        :rtype: str
        """
        if redirect_uri is None:
            redirect_uri = self.client.default_redirects['auth']
            if redirect_uri is None:
                raise ValueError('redirect_uri must not be None')
        scopes = self.client.default_scopes if scopes is None else scopes
        _redirect_uri = base64.b64encode(redirect_uri.encode('ascii')).decode('ascii')
        url = 'https://auth.growstocks.xyz/user/authorize'
        params = urllib3.request.urlencode({
            'secret': self.client.secret, 'scopes': str(scopes), 'redirect_uri': _redirect_uri
            })
        return f'{url}?{params}'

    def fetch_user(self, token: str, scopes: Scopes = None) -> User:
        scopes = self.client.default_scopes if scopes is None else scopes
        payload = {
            'secret': self.client.secret, 'token': token, 'scopes': scopes
            }
        if scopes is None:
            del payload['scopes']

        with requests.post(api_url + '/user', data=payload) as resp:
            rtrn_json = resp.json()

        return User.from_dict(rtrn_json['user'])


class pay:

    def __init__(self, client):
        self.client = client
