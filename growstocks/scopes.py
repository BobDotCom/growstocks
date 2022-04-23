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
from typing import List, Dict

__all__ = "Scopes",


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

    def __init__(
            self,
            profile: bool = True,
            email: bool = False,
            balance: bool = False,
            discord: bool = False
    ) -> None:
        if balance or discord:
            profile = True
        if email:
            profile = False

        self.profile = profile
        self.email = email
        self.balance = balance
        self.discord = discord

    @property
    def as_list(self) -> List[str]:
        """
        The scopes set in this object in the form of a :class:`list`

        Returns
        --------
        :class:`list`
            List of scopes
        """
        return [k for k, v in self.as_dict.items() if v]

    @property
    def as_dict(self) -> Dict[str, bool]:
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

    def __str__(self) -> str:
        return ','.join(self.as_list)

    def __repr__(self) -> str:
        return str(self)
