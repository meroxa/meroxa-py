import json
from typing import Any

from .types import MeroxaApiResponse, EnvironmentIdentifier
from .utils import ComplexEncoder, api_response


PIPELINE_BASE_PATH = "/v1/pipelines"


class PipelineResponse(MeroxaApiResponse):
    def __init__(
        self,
        uuid: str,
        account_id: int,
        project_id: int,
        name: str,
        state: str,
        created_at: str,
        updated_at: str,
        environment: EnvironmentIdentifier = None,
        metadata: dict[str, Any] = None,
        **kwargs
    ) -> None:
        self._created_at = created_at
        self._uuid = uuid
        self._account_id = account_id
        self._project_id = project_id
        self._name = name
        self._state = state
        self._updated_at = updated_at
        self._environment = environment
        self._metadata = metadata
        super().__init__()


class CreatePipelineParams:
    def __init__(
        self,
        name: str,
        metadata: dict[str, Any] = None,
        environment: EnvironmentIdentifier = None,
    ) -> None:
        self._name = name
        self._metadata = metadata
        self._environment = environment

    def repr_json(self):
        return dict(
            name=self._name, metadata=self._metadata, environment=self._environment
        )


class UpdatePipelineParams:
    def __init__(self, name: str, metadata: dict[str, Any] = None) -> None:
        self._name = name
        self._metadata = metadata

    def repr_json(self):
        return dict(name=self._name, metadata=self._metadata)


class Pipelines:
    def __init__(self, session) -> None:
        self._session = session

    @api_response(PipelineResponse)
    async def get(self, name_or_id: str):
        async with self._session.get(
            PIPELINE_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.text()

    @api_response(PipelineResponse)
    async def list(self):
        async with self._session.get(PIPELINE_BASE_PATH) as resp:
            return await resp.text()

    async def delete(self, name_or_id: str):
        async with self._session.delete(
            PIPELINE_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.text()

    @api_response(PipelineResponse)
    async def create(self, create_pipeline_parameters: CreatePipelineParams):
        async with self._session.post(
            PIPELINE_BASE_PATH,
            data=json.dumps(create_pipeline_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.text()

    @api_response(PipelineResponse)
    async def update(
        self, pipline_name_or_id: str, update_pipeline_parameters: UpdatePipelineParams
    ):
        async with self._session.post(
            PIPELINE_BASE_PATH + "/{}".format(pipline_name_or_id),
            json=json.dumps(update_pipeline_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.text()
