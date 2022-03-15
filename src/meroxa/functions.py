import json

from .types import CreateFunctionParams
from .types import UpdateFunctionParams

from .utils import ComplexEncoder

BASE_PATH = "/v1/functions"


class Functions:
    def __init__(self, session) -> None:
        self._session = session

    async def get(self, nameOrId: str):
        async with self._session.get(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    async def list(self):
        async with self._session.get(BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, nameOrId: str):
        async with self._session.delete(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    async def create(self, createFunctionParameters: CreateFunctionParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createFunctionParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updateFunctionParameters: UpdateFunctionParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updateFunctionParameters.name),
            json=json.dumps(updateFunctionParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
