import json

from .types import CreateResourceParams
from .types import UpdateResourceParams

from .utils import ComplexEncoder, api_response

BASE_PATH = "/v1/resources"


class Status(object):
    def __init__(self, state: str, last_updated_at: str) -> None:
        self.state = state
        self.last_updated_at = last_updated_at


class ResourcesResponse(object):
    def __init__(
            self, id: int, uuid: str, name: str, type: str,
            url: str, metadata: dict, connector_count: int,
            status: Status, created_at: str, updated_at: str) -> None:
        self.id = id
        self.uuid = uuid
        self.name = name
        self.type = type
        self.url = url
        self.metadata = metadata
        self.connector_count = connector_count
        self.status = Status(**status)
        self.created_at = created_at
        self.updated_at = updated_at


class Resources:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(ResourcesResponse)
    async def get(self, nameOrId: str):
        async with self._session.get(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    async def list(self):
        async with self._session.get(BASE_PATH) as resp:
            res = await resp.text()
            return [ResourcesResponse(**rr) for rr in json.loads(res)]

    async def delete(self, nameOrId: str):
        async with self._session.delete(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    @api_response(ResourcesResponse)
    async def create(self, createResourceParameters: CreateResourceParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createResourceParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    @api_response(ResourcesResponse)
    async def update(self, updateResourceParameters: UpdateResourceParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updateResourceParameters.name),
            json=json.dumps(updateResourceParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            res = await resp.text()
            return ResourcesResponse(**json.loads(res))
