import json

from .types import CreatePipelineParams
from .types import UpdatePipelineParams

from .utils import ComplexEncoder

BASE_PATH = "/v1/pipelines"


class Pipelines:
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

    async def create(self, createPipelineParameters: CreatePipelineParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createPipelineParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    async def update(self, updatePipelineParameters: UpdatePipelineParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updatePipelineParameters.name),
            json=json.dumps(updatePipelineParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
