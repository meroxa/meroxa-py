import json

from .types import CreateFunctionParams
from .types import UpdateFunctionParams

from .utils import ComplexEncoder

BASE_PATH = "/v1/functions"


class FunctionResponse(object):
    def __init__(
            self, uuid: str, name: str, input_stream: str,
            output_stream: str, image: str, command: list[str],
            args: list[str], env_vars: dict, status: dict,
            pipeline: dict) -> None:
        self.uuid = uuid
        self.name = name
        self.input_stream = input_stream
        self.ouput_stream = output_stream
        self.image = image
        self.command = command
        self.args = args
        self.env_vars = env_vars
        self.status = status
        self.pipline = pipeline

class ListFunctionResponse(object):
    def __init__(self, functions: list[FunctionResponse]):
        self.functions = functions

class Functions:
    def __init__(self, session) -> None:
        self._session = session

    async def get(self, nameOrId: str):
        async with self._session.get(BASE_PATH + "/{}".format(nameOrId)) as resp:
            res = await resp.text()
            return FunctionResponse(**json.loads(res))

    async def list(self):
        async with self._session.get(BASE_PATH) as resp:
            res = await resp.text()
            return [FunctionResponse(**fr) for fr in json.loads(res)]

    async def delete(self, nameOrId: str):
        async with self._session.delete(BASE_PATH + "/{}".format(nameOrId)) as resp:
            return await None

    async def create(self, createFunctionParameters: CreateFunctionParams):
        async with self._session.post(
            BASE_PATH,
            data=json.dumps(createFunctionParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            res = await resp.text()
            return FunctionResponse(**json.loads(res))

    async def update(self, updateFunctionParameters: UpdateFunctionParams):
        async with self._session.post(
            BASE_PATH + "/{}".format(updateFunctionParameters.name),
            json=json.dumps(updateFunctionParameters.reprJSON(),
                            cls=ComplexEncoder)
        ) as resp:
            res = await resp.text()
            return FunctionResponse(**json.loads(res))
