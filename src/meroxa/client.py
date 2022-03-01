import aiohttp

from .resources import Resources
from .users import Users
from .types import ClientOptions

def createSession(options: ClientOptions):
    return aiohttp.ClientSession(
        base_url=options.url or "https://api.staging.meroxa.io",
        headers={
            "Authorization": "Bearer {}".format(options.auth)
        },
        timeout=aiohttp.ClientTimeout(
            total=options.timeout if options.timeout > 0.0 else 10.0
        )
    )


class Client:
    def __init__(self, clientSession) -> None:
        self._clientSession = clientSession

        self.users = Users(self._clientSession)
        self.resources = Resources(self._clientSession)
