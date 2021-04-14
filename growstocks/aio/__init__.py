import aiohttp

from growstocks import *


class Client(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._session = aiohttp.ClientSession()
