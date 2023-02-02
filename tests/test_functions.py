import json
from unittest.mock import patch

import pytest
from tests import assert_response_eq

from meroxa import CreateFunctionParams
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
    "created_at": "2022-03-02T20:18:14Z",
    "updated_at": "2022-03-02T20:18:14Z",
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find function"}


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_functions_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.json.return_value = (
        json.dumps(FUNCTION_JSON)
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    functions_response = await Functions(mock_session).get("function_identifier")

    assert mock_session.get.call_count == 1

    assert_response_eq(json.loads(functions_response), FUNCTION_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_functions_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.json.return_value = (
        json.dumps([FUNCTION_JSON, FUNCTION_JSON])
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    response = await Functions(mock_session).list()
    json_resp = json.loads(response)

    assert mock_session.get.call_count == 1

    assert isinstance(json_resp, list)
    assert len(json_resp) == 2

    assert_response_eq(json_resp[0], FUNCTION_JSON)
    assert_response_eq(json_resp[1], FUNCTION_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_functions_delete_success(mock_session):
    mock_session.delete.return_value.__aenter__.return_value.json.return_value = (
        json.dumps({})
    )
    mock_session.delete.return_value.__aenter__.return_value.status = 200

    await Functions(mock_session).delete("function_i_want_gone")
    assert mock_session.delete.call_count == 1


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_functions_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.json.return_value = (
        json.dumps(FUNCTION_JSON)
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

    create_response = await Functions(mock_session).create(cfp)
    json_resp = json.loads(create_response)

    assert mock_session.post.call_count == 1
    assert isinstance(json_resp, dict)
    assert_response_eq(json_resp, FUNCTION_JSON)
