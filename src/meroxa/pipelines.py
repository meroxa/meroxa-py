import json

from .types import CreatePipelineParams
from .types import UpdatePipelineParams

from .utils import ComplexEncoder

RESOURCE_PATH = "/v1/pipelines"


class Pipelines:
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

    async def create(self, createPipelineParameters: CreatePipelineParams):
        async with self._session.post(
            RESOURCE_PATH,
            data=json.dumps(createPipelineParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updatePipelineParameters: UpdatePipelineParams):
        async with self._session.post(
            RESOURCE_PATH + "/{}".format(updatePipelineParameters.name),
            json=json.dumps(updatePipelineParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
