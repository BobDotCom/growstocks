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
from typing import Tuple, Union, Optional

from .types.user import User as UserData

__all__ = "User",


class User:
    """
    A user object, fetched from the api.

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

    def __init__(
            self,
            id: int,
            name: Optional[str] = None,
            email: Optional[str] = None,
            growid: Optional[str] = None,
            balance: Optional[int] = None,
            discord_id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.growid = growid
        self.balance = balance
        self.discord_id = discord_id

    @classmethod
    def from_dict(cls, input_dict: UserData) -> 'User':
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
        discord_id = input_dict.get('discordID')

        return cls(
            id=input_dict["id"],
            name=input_dict.get('name'),
            email=input_dict.get('email'),
            growid=input_dict.get('growid'),
            balance=input_dict.get('balance'),
            discord_id=int(discord_id) if discord_id is not None else None,
        )

    def as_dict(self) -> UserData:
        """
        Get a dict of the current user. This may also be used as ``dict(User)``

        Returns
        --------
        :class:`dict`
            dict of user
        """
        dict_val = dict(self)
        return UserData(
            id=self.id,
            name=self.name,
            email=self.email,
            growid=self.growid,
            balance=self.balance,
            discordID=str(self.discord_id),
        )

    def __iter__(self) -> 'User':
        self._n = 0
        return self

    def __next__(self) -> Tuple[str, Optional[Union[str, int]]]:  # TODO: Type this better
        self_info = [('id', self.id), ('name', self.name), ('email', self.email), ('growid', self.growid),
                     ('balance', self.balance), ('discordID', str(self.discord_id))]
        if self._n <= len(self_info):
            ret = self_info[self._n - 1]
            self._n += 1
            return ret
        else:
            raise StopIteration

    def __str__(self) -> str:
        return self.name or ""

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id={self.id}>'
