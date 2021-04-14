import base64

import urllib3

from .ext import PartialTransaction, Transaction, User

if __name__ != '__main__':
    class auth:
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

        def __init__(self, client):
            self.client = client
            self.api_url = '{0}/auth'.format(self.client.api_url)

        def make_url(self, redirect_uri=None, scopes=None):
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
            ValueError
                redirect_uri is :class:`None`

            Returns
            --------
            :class:`str`
                Authorization url
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
                'client': self.client.client, 'scopes': str(scopes), 'redirect_uri': _redirect_uri
                })
            return '{0}?{1}'.format(url, params)

        def fetch_user(self, token, scopes=None):
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
            RuntimeError
                API call failed.

            Returns
            --------
            :class:`User`
                The user fetched from the api.
            """
            scopes = self.client.default_scopes if scopes is None else scopes
            payload = {
                'secret': self.client.secret, 'token': token, 'scopes': str(scopes)
                }
            if scopes is None:
                del payload['scopes']

            resp = self.client.maybe_await(self.client.session.post('{0}/user'.format(self.api_url), data=payload))
            rtrn_json = self.client.maybe_await(resp.json())
            if not rtrn_json['success']:
                raise RuntimeError('Request to api was unsuccessful: {0}'.format(rtrn_json))

            return User.from_dict(rtrn_json['user'])


    class pay:
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

        def __init__(self, client):
            self.client = client
            self.api_url = '{0}/pay'.format(self.client.api_url)

        def create_transaction(self, user, amount, notes=None):
            """
            Create a transaction.

            Parameters
            ----------
            user: :class:`PartialUser`
                The user to create the transaction for. Usually a :class:`User` but a :class:`PartialUser` will do fine.
            amount: :class:`int`
                The amount of world locks to request
            notes: :class:`str`, optional
                Transaction notes to send. Maximum of 50 chars.

            Raises
            ------
            RuntimeError
                API call failed

            Returns
            -------
            :class:`PartialTransaction`
                The transaction object
            """
            payload = {
                'secret': self.client.secret, 'user': int(user.id), 'amount': int(amount), 'notes': str(notes)
                }
            if notes is None:
                del payload['notes']

            resp = self.client.maybe_await(
                self.client.session.post('{0}/transaction/create'.format(self.api_url), data=payload))
            rtrn_json = self.client.maybe_await(resp.json())
            if not rtrn_json['success']:
                raise RuntimeError('Request to api was unsuccessful: {0}'.format(rtrn_json))

            rtrn_transaction = PartialTransaction(rtrn_json['transaction'], client=self.client)

            return rtrn_transaction

        def make_payment_url(self, transaction, redirect_uri=None):
            """
            Make a payment url for a transaction

            Parameters
            -----------
            transaction: :class:`PartialTransaction`
                The transaction to make a payment url for. Normally :class:`PartialTransaction` but :class:`Transaction`
                will work fine
            redirect_uri: :class:`str`, optional
                URL to redirect the user to

            Raises
            -------
            ValueError
                redirect_uri is None

            Returns
            --------
            :class:`str`
                Payment URL
            """
            if redirect_uri is None:
                redirect_uri = self.client.default_redirects['pay']
                if redirect_uri is None:
                    raise ValueError('redirect_uri must not be None')
                else:
                    redirect_uri = redirect_uri.format(self.client.default_redirects['site'])
            _redirect_uri = base64.b64encode(redirect_uri.encode('ascii')).decode('ascii')
            url = 'https://pay.growstocks.xyz/pay'
            params = urllib3.request.urlencode({
                'client': self.client.client, 'redirect_uri': _redirect_uri, 'transaction': str(transaction.id)
                })
            return '{0}?{1}'.format(url, params)

        def fetch_transaction(self, transaction):
            """
            Fetch info about a transaction.

            Parameters
            ----------
            transaction: :class:`PartialTransaction`
                Transaction object to fetch info about.

            Raises
            ------
            RuntimeError
                API call failed.

            Returns
            -------
            :class:`Transaction`
                Transaction object with info about the fetched transaction.
            """
            payload = {
                'secret': self.client.secret, 'transaction': transaction.id
                }

            resp = self.client.maybe_await(
                self.client.session.post('{0}/transaction/create'.format(self.api_url), data=payload))
            rtrn_json = self.client.maybe_await(resp.json())
            if not rtrn_json['success']:
                raise RuntimeError('Request to api was unsuccessful: {0}'.format(rtrn_json))

            rtrn_transaction = Transaction.from_dict(rtrn_json['transaction'], client=self.client)

            return rtrn_transaction

        def send(self, user, amount, notes=None):
            """
            Send world locks to a user.

            Parameters
            ----------
            user: :class:`PartialUser`
                User to send to
            amount: :class:`int`
                Amount to send
            notes: :class:`str`, optional
                Information about the transaction

            Raises
            ------
            RuntimeError
                Request to api failed

            Returns
            -------
            :class:`dict`
                Response from the API
            """
            payload = {
                'secret': self.client.secret, 'party': user.id, 'amount': amount, 'notes': notes
                }
            resp = self.client.maybe_await(self.client.session.post('{0}/send'.format(self.api_url), data=payload))
            rtrn_json = self.client.maybe_await(resp.json())
            if not rtrn_json['success']:
                raise RuntimeError('Request to api was unsuccessful: {0}'.format(rtrn_json))
            return rtrn_json

        def get_balance(self):
            """
            Get the current balance of your account

            Raises
            ------
            RuntimeError
                Request to api failed

            Returns
            -------
            :class:`int`
                Your balance
            """
            payload = {
                'secret': self.client.secret
                }
            resp = self.client.maybe_await(self.client.session.post('{0}/balance'.format(self.api_url), data=payload))
            rtrn_json = self.client.maybe_await(resp.json())
            if not rtrn_json['success']:
                raise RuntimeError('Request to api was unsuccessful: {0}'.format(rtrn_json))
            return int(rtrn_json['balance'])
