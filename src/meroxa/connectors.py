import json
from typing import Any

from aiohttp import ClientSession

from .utils import ComplexEncoder

CONNECTORS_BASE_PATH = "/v1/connectors"


class CreateConnectorParams:
    def __init__(
        self,
        resource_name: str,
        pipeline_name: str,
        name: str = None,
        config: dict[str, str] = None,
        metadata: dict[str, str] = None,
        connector_type: str = None,
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
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get(self, name_or_id: str):
        async with self._session.get(
            CONNECTORS_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.json()

    async def list(self):
        async with self._session.get(CONNECTORS_BASE_PATH) as resp:
            return await resp.json()

    async def delete(self, name_or_id: str):
        async with self._session.delete(
            CONNECTORS_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.json()

    async def create(self, create_connector_parameters: CreateConnectorParams):
        async with self._session.post(
            CONNECTORS_BASE_PATH,
            data=json.dumps(
                create_connector_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.json()

    async def update(
        self, name_or_id: str, update_connector_parameters: UpdateConnectorParams
    ):
        async with self._session.post(
            CONNECTORS_BASE_PATH + "/{}".format(name_or_id),
            json=json.dumps(
                update_connector_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.json()
