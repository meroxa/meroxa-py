import aiohttp
import asyncio


class ClientOptions:
    auth = None
    timeout = None,
    url = None


class Client:
    def __init__(self, clientSession) -> None:
        self._clientSession = clientSession
        self.users = Users(self._clientSession)
        self.resources = Resources(self._clientSession)


async def main():
    async with aiohttp.ClientSession(
        base_url='https://api.staging.meroxa.io',
        headers={
            "Authorization": "Bearer {}".format("")
        }
    ) as session:
        client = Client(session)
        resp = await client.resources.list()
        print(resp)


asyncio.run(main())
