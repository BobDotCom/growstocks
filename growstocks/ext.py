import datetime

if __name__ != '__main__':
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
        email: :class:`str`, optional
            The user's email
        growid: :class:`str`, optional
            The user's growid
        balance: :class:`int`, optional
            The user's balance
        discord_id: :class:`int`, optional
            The user's discord id

        Attributes
        -----------
        id: :class:`int`
            The user's id
        name: :class:`str`, optional
            The user's name
        email: :class:`str`, optional
            The user's email
        growid: :class:`str`, optional
            The user's growid
        balance: :class:`int`, optional
            The user's balance
        discord_id: :class:`int`, optional
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

        def __str__(self):
            return self.name

        # def __repr__(self) -> repr:  #     return str(self)


    class PartialTransaction:
        """
        A placeholder transaction object, can be initialized partially without fetching all information

        Parameters
        -----------
        id: :class:`int`
            The transaction ID
        user: :class:`int`, optional
            The ID of the user
        party: :class:`int`, optional
            The developer account’s user ID
        amount: :class:`int`, optional
            The amount of World Locks the transaction holds
        status: :class:`int`, optional
            The payment status of the transaction (integer)
        date_time: :class:`str`, optional
            The date of creation of the transaction(yyyy-mm-dd HH:MM:SS)
        client: :class:`Client`, optional
            The client object

        Attributes
        -----------
        id: :class:`int`
            The transaction id
        user: :class:`int`, optional
            The ID of the user
        party: :class:`int`, optional
            The developer account’s user ID
        amount: :class:`int`, optional
            The amount of World Locks the transaction holds
        status: :class:`int`, optional
            The payment status of the transaction (integer)
        datetime: :class:`datetime.datetime`, optional
            The date of creation of the transaction
        client: :class:`Client`, optional
            The client object
        """

        def __init__(self, id, user=None, party=None, amount=None, status=None, date_time=None, client=None):
            self.id = id
            self.user = user
            self.party = party
            self.amount = amount
            self.status = status
            self.datetime = date_time
            self._client = client

        def make_payment_url(self, redirect_uri=None):
            """
            Shortcut of :meth:`Client.pay.make_payment_url`

            Parameters
            ----------
            redirect_uri: :class:`str`, optional
                Where to redirect user after payment

            Returns
            -------
            :class:`str`
                A payment url to send the user to
            """
            return self._client.pay.make_payment_url(self, redirect_uri=redirect_uri)

        def fetch_info(self):
            """
            Shortcut of :meth:`Client.pay.fetch_transaction`

            Returns
            -------
            :class:`Transaction`
                Transaction object with info about the fetched transaction.
            """
            return self._client.pay.fetch_transaction(self)

        @property
        def datetime(self):
            """
            :meta private:
            """
            return self._datetime

        @datetime.setter
        def datetime(self, value):
            self._datetime = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

        @property
        def user(self):
            """
            :meta private:
            """
            return self._user

        @user.setter
        def user(self, value):
            self._user = PartialUser(value)


    class Transaction(PartialTransaction):

        @classmethod
        def from_dict(cls, input_dict, client=None):
            """
            Extract a transaction object from a dict returned by api

            Parameters
            ----------
            input_dict: :class:`dict`
                Input dict of info fetched from api
            client: :class:`Client`, optional
                Client object

            Returns
            -------
            :class:`Transaction`
                Transaction object
            """
            id_ = input_dict['id']
            user = input_dict['user']
            party = input_dict['party']
            amount = input_dict['amount']
            status = input_dict['status']
            date_time = input_dict['date_time']
            return cls(id=id_, user=user, party=party, amount=amount, status=status, date_time=date_time, client=client)

        @property
        def paid(self):
            """
            If the order is paid

            Returns
            -------
            :class:`bool`
                Whether the order is paid or not
            """
            return bool(int(self.status))
