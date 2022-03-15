import json

from .types import CreatePipelineParams
from .types import UpdatePipelineParams

from .utils import ComplexEncoder

BASE_PATH = "/v1/pipelines"


class PipelineResponse(object):
    def __init__(
            self,  id: int, uuid: str, account_id: int, project_id: int, 
            name: str, state: str, created_at: str,updated_at: str,  
            environment=None, metadata=None) -> None:
        self.created_at = created_at
        self.id = id
        self.uuid = uuid
        self.account_id = account_id
        self.project_id = project_id
        self.name = name
        self.state = state
        self.updated_at = updated_at
        self.environment = environment
        self.metadata = metadata


class Pipelines:
    def __init__(self, session) -> None:
        self._session = session

    async def get(self, nameOrId: str):
        async with self._session.get(BASE_PATH + "/{}".format(nameOrId)) as resp:
            res = await resp.text()
            return PipelineResponse(**json.loads(res))

    async def list(self):
        async with self._session.get(BASE_PATH) as resp:
            res = await resp.text()
            return [PipelineResponse(**pr) for pr in json.loads(res)]

    async def delete(self, nameOrId: str):
        async with self._session.delete(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    async def create(self, createPipelineParameters: CreatePipelineParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createPipelineParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            res = await resp.text()
            return PipelineResponse(**json.loads(res))

    async def update(self, updatePipelineParameters: UpdatePipelineParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updatePipelineParameters.name),
            json=json.dumps(updatePipelineParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            res = await resp.text()
            return PipelineResponse(**json.loads(res))
