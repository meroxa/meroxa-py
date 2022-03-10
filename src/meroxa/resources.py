import json

from .types import CreateResourceParams
from .types import UpdateResourceParams

from .utils import ComplexEncoder

BASE_PATH = "/v1/resources"


class Resources:
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

    async def create(self, createResourceParameters: CreateResourceParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createResourceParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updateResourceParameters: UpdateResourceParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updateResourceParameters.name),
            json=json.dumps(updateResourceParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
