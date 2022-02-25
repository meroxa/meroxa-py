RESOURCE_PATH = "/v1/resources"


class Resources:
    def __init__(self, session) -> None:
        self._session = session

    async def get(self, nameOrId: str):
        async with self._session.get(RESOURCE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    async def list(self):
        async with self._session.get(RESOURCE_PATH) as resp:
            return await resp.text()

    async def delete(self, nameOrId: str):
        async with self._session.delete(RESOURCE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    # Options most likely would be passed in like a dictionary
    async def create(self, createParam: dict):
        async with self._session.post(
            RESOURCE_PATH,
            data=createParam
        ) as resp:
            return await resp.text()
