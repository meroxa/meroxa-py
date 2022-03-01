import json

from .types import CreateConnectorParams
from .types import UpdateConnectorParams

from .utils import ComplexEncoder

RESOURCE_PATH = "/v1/connectors"


class Connectors:
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

    async def create(self, createConnectorParameters: CreateConnectorParams):
        async with self._session.post(
            RESOURCE_PATH,
            data=json.dumps(createConnectorParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updateConnectorParameters: UpdateConnectorParams):
        async with self._session.post(
            RESOURCE_PATH + "/{}".format(updateConnectorParameters.name),
            json=json.dumps(updateConnectorParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
