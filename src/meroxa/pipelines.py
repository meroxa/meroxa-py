import json

from aiohttp import ClientSession

from .types import EnvironmentIdentifier
from .utils import ComplexEncoder

PIPELINE_BASE_PATH = "/v1/pipelines"


class CreatePipelineParams:
    def __init__(
        self,
        name: str,
        metadata: dict[str, str] = None,
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
    def __init__(self, name: str, metadata: dict[str, str] = None) -> None:
        self._name = name
        self._metadata = metadata

    def repr_json(self):
        return dict(name=self._name, metadata=self._metadata)


class PipelineIdentifiers:
    def __init__(self, name=None, uuid=None):
        self._name = name
        self._uuid = uuid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._uuid:
            self._uuid = None
        self._name = value

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if self._name:
            self._name = None
        self._uuid = value

    def repr_json(self):
        return dict(name=self._name, uuid=self._uuid)


class Pipelines:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get(self, name_or_id: str):
        async with self._session.get(
            PIPELINE_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.json()

    async def list(self):
        async with self._session.get(PIPELINE_BASE_PATH) as resp:
            return await resp.json()

    async def delete(self, name_or_id: str):
        async with self._session.delete(
            PIPELINE_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.json()

    async def create(self, create_pipeline_parameters: CreatePipelineParams):
        async with self._session.post(
            PIPELINE_BASE_PATH,
            data=json.dumps(create_pipeline_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.json()

    async def update(
        self, pipeline_name_or_id: str, update_pipeline_parameters: UpdatePipelineParams
    ):
        async with self._session.post(
            PIPELINE_BASE_PATH + "/{}".format(pipeline_name_or_id),
            json=json.dumps(update_pipeline_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.json()
