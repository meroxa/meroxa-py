import json

from .types import CreateFunctionParams
from .types import UpdateFunctionParams

from .utils import ComplexEncoder

RESOURCE_PATH = "/v1/functions"


class Functions:
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

    async def create(self, createFunctionParameters: CreateFunctionParams):
        print(createFunctionParameters.reprJSON())
        async with self._session.post(
            RESOURCE_PATH,
            data=json.dumps(createFunctionParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updateFunctionParameters: UpdateFunctionParams):
        async with self._session.post(
            RESOURCE_PATH + "/{}".format(updateFunctionParameters.name),
            json=json.dumps(updateFunctionParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
