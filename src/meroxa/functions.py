import json

from aiohttp import ClientSession

from .pipelines import PipelineIdentifiers
from .utils import ComplexEncoder

FUNCTIONS_BASE_PATH = "/v1/functions"


class CreateFunctionParams:
    def __init__(
        self,
        name: str,
        input_stream: str,
        output_stream: str,
        pipeline: PipelineIdentifiers,
        image: str,
        command: list[str],
        args: list[str],
        env_vars: dict[str, str],
    ) -> None:
        self._name = name
        self._input_stream = input_stream
        self._output_stream = output_stream
        self._image = image
        self._command = command
        self._args = args
        self._env_vars = env_vars
        self._pipeline = pipeline

    def repr_json(self):
        return dict(
            name=self._name,
            input_stream=self._input_stream,
            output_stream=self._output_stream,
            image=self._image,
            command=self._command,
            args=self._args,
            pipeline=self._pipeline,
            env_vars=self._env_vars,
        )


class Functions:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get(self, name_or_id: str):
        async with self._session.get(
            FUNCTIONS_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.json()

    async def list(self):
        async with self._session.get(FUNCTIONS_BASE_PATH) as resp:
            return await resp.json()

    async def delete(self, name_or_id: str):
        async with self._session.delete(
            FUNCTIONS_BASE_PATH + "/{}".format(name_or_id)
        ) as resp:
            return await resp.json()

    async def create(self, create_function_parameters: CreateFunctionParams):
        async with self._session.post(
            FUNCTIONS_BASE_PATH,
            data=json.dumps(create_function_parameters.repr_json(), cls=ComplexEncoder),
        ) as resp:
            return await resp.json()
