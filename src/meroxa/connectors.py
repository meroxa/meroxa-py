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
        self,
        uuid: str,
        name: str,
        type: str,
        config: dict,
        state: str,
        resource_name: str,
        pipeline_name: str,
        streams: Streams,
        metadata: dict,
        created_at: str,
        updated_at: str,
        **kwargs
    ) -> None:
        self.uuid = uuid
        self.name = name
        self.type = type
        self.config = config
        self.state = state
        self.resource_name = resource_name
        self.pipeline_name = pipeline_name
        self.streams = Streams(**streams)
        self.metadata = metadata
        self.created_at = created_at
        self.updated_at = updated_at


class Connectors:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(ConnectorsResponse)
    async def get(self, name_or_id: str):
        async with self._session.get(BASE_PATH + "/{}".format(name_or_id)) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def list(self):
        async with self._session.get(BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, name_or_id: str):
        async with self._session.delete(BASE_PATH + "/{}".format(name_or_id)) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def create(self, createConnectorParameters: CreateConnectorParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createConnectorParameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def update(self, updateConnectorParameters: UpdateConnectorParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updateConnectorParameters.name),
            json=json.dumps(updateConnectorParameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.text()
