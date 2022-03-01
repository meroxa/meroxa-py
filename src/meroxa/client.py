import aiohttp

from .resources import Resources
from .users import Users
from .pipelines import Pipelines
from .functions import Functions
from .connectors import Connectors

from meroxa.constants import MEROXA_API_ROUTE, MEROXA_TIMEOUT

class Meroxa:
    """Asynchronous Meroxa API handler
    """

    # Default Meroxa API route
    meroxa_api = MEROXA_API_ROUTE

    def __init__(
            self,
            auth,
            api_route=MEROXA_API_ROUTE,
            timeout=MEROXA_TIMEOUT,
            session=None):
        """Create a session if one is not provided.
        """

        if session is None:
            session = aiohttp.ClientSession(
                base_url=api_route,
                headers={
                    "Authorization": "Bearer {}".format(auth)
                },
                timeout=aiohttp.ClientTimeout(timeout)
            )

        self._session = session

        # Meroxa API Handlers
        self.connectors = Connectors(self._session)
        self.functions = Functions(self._session)
        self.pipelines = Pipelines(self._session)
        self.resources = Resources(self._session)
        self.users = Users(self._session)

    """
    Enable async context management.

    e.g.:

    mySession = aiohttp.ClientSession()
    async with meroxa.Meroxa(session) as m:
        m.doTheThing()
    """
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def close(self):
        await self._session.close()