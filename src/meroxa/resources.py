import json

from .types import CreateResourceParams
from .types import UpdateResourceParams

from .utils import ComplexEncoder

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

    async def create(self, createResourceParameters: CreateResourceParams):
        async with self._session.post(
            RESOURCE_PATH,
            data=json.dumps(createResourceParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updateResourceParameters: UpdateResourceParams):
        async with self._session.post(
            RESOURCE_PATH + "/{}".format(updateResourceParameters.name),
            data=json.dumps(updateResourceParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
