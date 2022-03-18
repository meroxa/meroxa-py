import json

from .types import CreateConnectorParams
from .types import MeroxaApiResponse
from .types import UpdateConnectorParams

from .utils import ComplexEncoder, api_response

BASE_PATH = "/v1/connectors"


class Streams(object):
    def __init__(self, dynamic: bool, input=None, output=None) -> None:
        self.dynamic = dynamic
        self.input = input
        self.output = output


class ConnectorsResponse(MeroxaApiResponse):
    def __init__(
            self, id: int, uuid: str, name: str, type: str,
            config: dict, state: str, resource_id: int,
            pipeline_id: int, pipeline_name: str, streams: Streams,
            metadata: dict, created_at: str, updated_at: str) -> None:
        self.id = id
        self.uuid = uuid
        self.name = name
        self.type = type
        self.config = config
        self.state = state
        self.resource_id = resource_id
        self.pipeline_id = pipeline_id
        self.pipeline_name = pipeline_name
        self.streams = Streams(**streams)
        self.metadata = metadata
        self.created_at = created_at
        self.updated_at = updated_at


class Connectors:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(ConnectorsResponse)
    async def get(self, nameOrId: str):
        async with self._session.get(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def list(self):
        async with self._session.get(BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, nameOrId: str):
        async with self._session.delete(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def create(self, createConnectorParameters: CreateConnectorParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createConnectorParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def update(self, updateConnectorParameters: UpdateConnectorParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updateConnectorParameters.name),
            json=json.dumps(updateConnectorParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            return await resp.text()
