import aiohttp

from .resources import Resources
from .users import Users
from .pipelines import Pipelines
from .functions import Functions
from .connectors import Connectors
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
    def __init__(self, session) -> None:
        self._session = session

        self.connectors = Connectors(self._session)
        self.functions = Functions(self._session)
        self.pipelines = Pipelines(self._session)
        self.resources = Resources(self._session)
        self.users = Users(self._session)
