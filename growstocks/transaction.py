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
import datetime
from typing import Optional, TYPE_CHECKING, TypeVar, Awaitable, Union

from .types.transaction import Transaction as TransactionData
from .user import User

if TYPE_CHECKING:
    from .client import Client
else:
    Client = TypeVar("Client")

__all__ = "Transaction",


class Transaction:
    """
    A transaction object.

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
    user: :class:`User`, optional
        The user object belonging to the transaction
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

    def __init__(
            self,
            id: int,
            client: Client,
            user: Optional[User] = None,
            party: Optional[int] = None,
            amount: Optional[int] = None,
            status: Optional[int] = None,
            date_time: Optional[str] = None,
    ):
        self.id = id
        self.user = user
        self.party = party
        self.amount = amount
        self.status = status
        self.datetime: Optional[datetime.datetime] = None
        if date_time is not None:
            self.set_datetime(date_time)
        self._client = client

    def make_payment_url(self, redirect_uri: Optional[str] = None) -> str:
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

    def fetch_info(self) -> Union['Transaction', Awaitable['Transaction']]:
        """
        Shortcut of :meth:`Client.pay.fetch_transaction`

        Returns
        -------
        :class:`Transaction`
            Transaction object with info about the fetched transaction.
        """
        return self._client.pay.fetch_transaction(self)

    def set_datetime(self, value: str) -> None:
        self.datetime = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    @property
    def user(self) -> Optional[User]:
        """
        :meta private:
        """
        return self._user

    @user.setter
    def user(self, value: int) -> None:
        self._user = User(id=value)

    @classmethod
    def from_dict(cls, input_dict: TransactionData, client: Client) -> 'Transaction':
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
        return cls(
            id=id_,
            user=User(id=user),
            party=party,
            amount=amount,
            status=int(status),
            date_time=date_time,
            client=client
        )

    @property
    def paid(self) -> Optional[bool]:
        """
        If the order is paid

        Returns
        -------
        :class:`bool`
            Whether the order is paid or not
        """
        return bool(int(self.status)) if self.status is not None else None
