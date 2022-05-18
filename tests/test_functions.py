import json
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from meroxa import CreateFunctionParams
from meroxa import FunctionResponse
from meroxa import Functions
from meroxa import PipelineIdentifiers

FUNCTION_JSON = {
    "uuid": "f52ee43e-4ce0-482f-979b-10b0f2bf407f",
    "name": "function-123lol",
    "input_stream": "resource-123-456-stuff",
    "output_stream": "resource-678-0123-stuff-function-123lol",
    "image": "imageName",
    "command": ["python"],
    "args": ["main.py", "anonymize"],
    "env_vars": {},
    "status": {"state": "pending", "details": ""},
    "pipeline": {"name": "default"},
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find function"}


def assert_function_equality(response, comparison):
    print(response.__dict__)
    assert response.input_stream == comparison.get("input_stream")
    assert response.command == comparison.get("command")
    assert response.args == comparison.get("args")
    assert response.image == comparison.get("image")
    assert response.env_vars == comparison.get("env_vars")
    assert response.pipeline == comparison.get("pipeline")


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_functions_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps(FUNCTION_JSON)]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, functions_response = await Functions(mock_session).get("function_identifier")

    assert mock_session.get.call_count == 1
    assert error is None

    assert_function_equality(functions_response, FUNCTION_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_functions_get_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 404

    error, functions_response = await Functions(mock_session).get("function_identifier")

    assert mock_session.get.call_count == 1
    assert functions_response is None

    # TODO: Better comparison logic
    assert ERROR_MESSAGE.items() <= error.__dict__.items()


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps([FUNCTION_JSON, FUNCTION_JSON])]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, resource_response = await Functions(mock_session).list()

    assert mock_session.get.call_count == 1
    assert error is None

    assert isinstance(resource_response, list)
    assert len(resource_response) == 2

    assert_function_equality(resource_response[0], FUNCTION_JSON)
    assert_function_equality(resource_response[1], FUNCTION_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_list_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 404

    error, resource_response = await Functions(mock_session).list()

    assert mock_session.get.call_count == 1
    assert resource_response is None

    # TODO: Better comparison logic
    assert ERROR_MESSAGE.items() <= error.__dict__.items()


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_delete_success(mock_session):
    mock_session.delete.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=None
    )

    mock_session.delete.return_value.__aenter__.return_value.status = 200

    await Functions(mock_session).delete("function_i_want_gone")
    assert mock_session.delete.call_count == 1


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(FUNCTION_JSON)
    )
    mock_session.post.return_value.__aenter__.return_value.status = 202

    cfp = CreateFunctionParams(
        name="function-123lol",
        input_stream="resource-123-456-stuff",
        output_stream="resource-678-0123-stuff-function-123lol",
        pipeline=PipelineIdentifiers(name="default"),
        image="imageName",
        command=["python"],
        args=["main.py", "anonymize"],
        env_vars={},
    )

    error, create_response = await Functions(mock_session).create(cfp)

    assert mock_session.post.call_count == 1
    assert error is None
    assert isinstance(create_response, FunctionResponse)
    assert_function_equality(create_response, FUNCTION_JSON)


# # @patch("aiohttp.ClientSession")
# # async def test_resources_list_error(mock_session):
# #     mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
# #         return_value=json.dumps(ERROR_MESSAGE)
# #     )
# #
# #     mock_session.get.return_value.__aenter__.return_value.status = 200
# #
# #     error, resource_response = await Resources(mock_session).list()
# #
# #     assert mock_session.get.call_count == 1
# #     assert resource_response is None
# #
# #     # TODO: Better comparison logic
# #     assert ERROR_MESSAGE.items() <= error.__dict__.items()
