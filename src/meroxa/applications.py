import json

from aiohttp import ClientSession

from .pipelines import PipelineIdentifiers
from .utils import ComplexEncoder


APPLICATIONS_BASE_PATH = "/v1/applications"


class CreateApplicationParams:
    def __init__(
        self,
        name: str,
        language: str,
        git_sha: str,
        pipeline: PipelineIdentifiers,
    ) -> None:
        self._name = name
        self._language = language
        self._git_sha = git_sha
        self._pipeline = pipeline

    def repr_json(self):
        return dict(
            name=self._name,
            language=self._language,
            git_sha=self._git_sha,
            pipeline=self._pipeline,
        )


class Applications:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get(self, name_or_uuid: str):
        async with self._session.get(
            APPLICATIONS_BASE_PATH + "/{}".format(name_or_uuid)
        ) as resp:
            return await resp.json()

    async def list(self):
        async with self._session.get(APPLICATIONS_BASE_PATH) as resp:
            return await resp.json()

    async def delete(self, name_or_uuid: str):
        async with self._session.delete(
            APPLICATIONS_BASE_PATH + "/{}".format(name_or_uuid)
        ) as resp:
            return await resp.json()

    async def create(self, create_application_parameters: CreateApplicationParams):
        async with self._session.post(
            APPLICATIONS_BASE_PATH,
            data=json.dumps(
                create_application_parameters.repr_json(), cls=ComplexEncoder
            ),
        ) as resp:
            return await resp.json()
