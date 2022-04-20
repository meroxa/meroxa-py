import json
from enum import Enum
from typing import Any

from .types import MeroxaApiResponse, ConnectorType, EntityIdentifier
from .utils import ComplexEncoder, api_response

BASE_PATH = "/v1/connectors"


class ConnectorState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    CRASHED = "crashed"
    FAILED = "failed"
    DOA = "doa"


class ConnectorsResponse(MeroxaApiResponse):
    def __init__(
        self,
        config: dict[str, str],
        created_at: str,
        metadata: dict[str, str],
        name: str,
        resource_name: str,
        pipeline_name: str,
        streams: dict[str, str],
        state: ConnectorState,
        type: ConnectorType,
        updated_at: str,
        uuid: str,
        trace: str = None,
        environment: EntityIdentifier = None,
    ) -> None:
        self._config = config
        self._created_at = created_at
        self._metadata = metadata
        self._name = name
        self._resource_name = resource_name
        self._pipeline_name = pipeline_name
        self._streams = streams
        self._state = state
        self._type = type
        self._updated_at = updated_at
        self._uuid = uuid
        self._trace = trace
        self._environment = environment
        super().__init__()


class CreateConnectorParams:
    def __init__(
        self,
        resource_name: str,
        pipeline_name: str,
        name: str = None,
        config: dict[str, Any] = None,
        metadata: dict[str, Any] = None,
        connector_type: ConnectorType = None,
        input: str = None,
    ) -> None:
        self._resource_name = resource_name
        self._pipeline_name = pipeline_name
        self._name = name
        self._config = config
        self._metadata = metadata
        self._connector_type = connector_type
        self._input = input

    def repr_json(self):
        return dict(
            resource_name=self._resource_name,
            pipeline_name=self._pipeline_name,
            name=self._name,
            config=self._config,
            metadata=self._metadata,
            connector_type=self._connector_type,
            input=self._input,
        )


class UpdateConnectorParams:
    def __init__(
        self,
        name: str = None,
        config: dict[str, Any] = None,
    ) -> None:
        self._name = name
        self._config = config

    def repr_json(self):
        return dict(
            config=self._config,
            name=self._name,
        )


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
    async def create(self, create_connector_parameters: CreateConnectorParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(
                create_connector_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.text()

    @api_response(ConnectorsResponse)
    async def update(
        self, name_or_id: str, update_connector_parameters: UpdateConnectorParams
    ):
        async with self._session.post(
            BASE_PATH + "/{}".format(name_or_id),
            json=json.dumps(
                update_connector_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.text()
