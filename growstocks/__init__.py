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
    >>> user = client.auth.fetch_user('31G4k57rG3asdyyi5Lqk')
    >>> dict(user)
    {'discord_id': '690420846774321221',
     'id': 1916,
     'name': 'BobDotCom',
     'email': None,
     'growid': 'Bob430',
     'balance': 3}

"""
import base64

import requests
import urllib3

# PACKAGE INFO
__title__ = "growstocks"
__author__ = 'BobDotCom'
__version__ = '0.2.3'

__license__ = "MIT License"
__copyright__ = "Copyright 2021 {}".format(__author__)


class Scopes:
    """
    Scopes to use in authorization endpoints

    Parameters
    -----------
    profile: :class:`bool`
        Whether to fetch the user's profile. Defaults to ``True``.
    email: :class:`bool`
        Whether to fetch the user's email. If this is selected then profile will automatically be selected by the
        API. Defaults to ``False``.
    balance: :class:`bool`
        Whether to fetch the user's balance. If this is selected then either email or profile must be
        selected. If both are not selected, it will automatically select profile. Defaults to ``False``.
    discord: :class:`bool`
        Whether to fetch the user's profile. If this is selected then either email or profile must be
        selected. If both are not selected, it will automatically select profile. Defaults to ``False``.

    Attributes
    -----------
    profile: :class:`bool`
        Whether to fetch the user's profile.
    email: :class:`bool`
        Whether to fetch the user's email.
    balance: :class:`bool`
        Whether to fetch the user's balance.
    discord: :class:`bool`
        Whether to fetch the user's profile.
    """

    def __init__(self, profile=True, email=False, balance=False, discord=False):
        if balance or discord:
            profile = True
        if email:
            profile = False

        self.profile = profile
        self.email = email
        self.balance = balance
        self.discord = discord

    @property
    def as_list(self):
        """
        The scopes set in this object in the form of a :class:`list`

        Returns
        --------
        :class:`list`
            List of scopes
        """
        return [k for k, v in self.as_dict.items() if v]

    @property
    def as_dict(self):
        """
        The scopes set in this object in the form of a :class:`dict`

        Returns
        --------
        :class:`dict`
            Dict of scopes
        """
        return {
            'profile': self.profile, 'email': self.email, 'balance': self.balance, 'discord': self.discord
            }

    def __str__(self):
        return ','.join(self.as_list)

    def __repr__(self):
        return str(self)


class PartialUser:
    """
    A placeholder user object, can be initialized partially without fetching all information

    Parameters
    -----------
    id: :class:`int`
        The user's id
    name: :class:`str`, optional
        The user's name
    email: Optional[:class:`str`]
        The user's email
    growid: Optional[:class:`str`]
        The user's growid
    balance: Optional[:class:`int`]
        The user's balance
    discord_id: Optional[:class:`int`]
        The user's discord id

    Attributes
    -----------
    id: :class:`int`
        The user's id
    name: Optional[:class:`str`]
        The user's name
    email: Optional[:class:`str`]
        The user's email
    growid: Optional[:class:`str`]
        The user's growid
    balance: Optional[:class:`int`]
        The user's balance
    discord_id: Optional[:class:`int`]
        The user's discord id
    """

    def __init__(self, id, name=None, email=None, growid=None, balance=None, discord_id=None):
        self.id = id
        self.name = name
        self.email = email
        self.growid = growid
        self.balance = balance
        self.discord_id = discord_id


class User(PartialUser):
    """
    A user object, fetched from the api. Subclass of :class:`PartialUser`
    """

    @classmethod
    def from_dict(cls, input_dict):
        """
        Return a user object extracted from a :class:`dict`

        Parameters
        -----------
        input_dict: :class:`dict`
            Dict to extract information from

        Returns
        --------
        :class:`User`
            User object
        """
        id_ = input_dict.get('id')
        name = input_dict.get('name')
        email = input_dict.get('email')
        growid = input_dict.get('growid')
        balance = input_dict.get('balance')
        discord_id = input_dict.get('discordID')

        return cls(id=id_, name=name, email=email, growid=growid, balance=balance, discord_id=discord_id)

    def as_dict(self):
        """
        Get a dict of the current user. This may also be used as ``dict(User)``

        Returns
        --------
        :class:`dict`
            dict of user
        """
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

    def next(self):
        """
        Python 2 compatibility

        :meta private:
        """
        return self.__next__()

    def __str__(self):
        return self.name

    # def __repr__(self) -> repr:  #     return str(self)


class Client:
    """
    Base client object. Contains classes for both authorization and pay endpoints.

    Parameters
    -----------
    client: :class:`int`
        Client ID
    secret: :class:`str`
        Client secret, it is recommended to store this in an environment variable or other secure method
    default_scopes: Optional[:class:`Scopes`]
        Default scopes to use for endpoints requiring scopes. May be defined after initialization
    default_redirects: Optional[:class:`dict`]
        A dict of the default redirects. Accepted keys are "site" and "auth". The site value
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
        self.api_url = 'https://api.growstocks.xyz/v1/'
        self.auth = auth(self)
        self.pay = pay(self)

    @property
    def session(self):
        """
        :meta private:
        """
        return self._session

    @staticmethod
    def maybe_await(maybe_coro):
        """
        Await if it is a coro, return if not.

        :meta private:
        """
        return maybe_coro  # will add support later for async, going to build a python 2 compatible version first


class auth:
    """
    Base class for authorization endpoints. Not meant to be initialized outside a client object.

    Parameters
    -----------
    client: :class:`Client`
        Client object

    Attributes
    -----------
    api_url: :class:`str`
        The base url to use for authorization endpoints. Uses :obj:`Client.api_url` to generate.

    """

    def __init__(self, client):
        self.client = client
        self.api_url = '{0}/auth'.format(self.client.api_url)

    def make_url(self, redirect_uri=None, scopes=None):
        """
        Generate an authorization url with set parameters

        Parameters
        -----------
        redirect_uri: :class:`str`
            Url to redirect to after authorization, defaults to Client.default_redirects['auth']
        scopes: :class:`Scopes`
            Scopes for the authorization, defaults to Client.default_scopes

        Returns
        --------
        :class:`str`
            Authorization url

        Raises
        -------
        ValueError
            redirect_uri is :class:`None`
        """
        if redirect_uri is None:
            redirect_uri = self.client.default_redirects['auth']
            if redirect_uri is None:
                raise ValueError('redirect_uri must not be None')
            else:
                redirect_uri = redirect_uri.format(self.client.default_redirects['site'])
        scopes = self.client.default_scopes if scopes is None else scopes
        _redirect_uri = base64.b64encode(redirect_uri.encode('ascii')).decode('ascii')
        url = 'https://auth.growstocks.xyz/user/authorize'
        params = urllib3.request.urlencode({
            'secret': self.client.secret, 'scopes': str(scopes), 'redirect_uri': _redirect_uri
            })
        return '{0}?{1}'.format(url, params)

    def fetch_user(self, token, scopes=None):
        """
        Fetch a user from the api by their token.

        Parameters
        -----------
        token: :class:`str`
            The user's authorization token, granted from :meth:`make_url`
        scopes: :class:`Scopes`
            The scopes to use for authenticating the user

        Returns
        --------
        :class:`User`
            The user fetched from the api
        """
        scopes = self.client.default_scopes if scopes is None else scopes
        payload = {
            'secret': self.client.secret, 'token': token, 'scopes': str(scopes)
            }
        if scopes is None:
            del payload['scopes']

        resp = self.client.maybe_await(self.client.session.post('{0}/user'.format(self.api_url), data=payload))
        rtrn_json = resp.json()

        return User.from_dict(rtrn_json['user'])


class pay:
    """
    Coming in future minor versions


    Base class for pay endpoints. Not meant to be initialized outside a client object.

        Parameters
        -----------
        client: :class:`Client`
            Client object
    """

    def __init__(self, client):
        self.client = client
