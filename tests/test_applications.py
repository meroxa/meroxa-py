import json
from unittest.mock import patch

import pytest

from meroxa import Applications
from meroxa import CreateApplicationParams
from meroxa import PipelineIdentifiers

APP_JSON = {
    "uuid": "5485b8b5-7b96-49aa-a9ec-f98cafdc6941",
    "name": "test-test",
    "language": "python",
    "git_sha": "123sha",
    "status": {"details": "App is running", "state": "running"},
    "pipeline": {
        "name": "test-pipeline",
        "uuid": "aa05937e-28b0-4dca-872b-4f36fcda9f2f",
    },
    "created_at": "2022-07-01T20:34:42Z",
    "updated_at": "2022-07-01T20:34:42Z",
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find application"}


# All test coroutines will be treated as marked.
def assert_response_eq(response, comparison):
    assert sorted(response.items()) == sorted(comparison.items())


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_application_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text.return_value = (
        json.dumps(APP_JSON)
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    apps_response = await Applications(mock_session).get("app_identifier")

    assert mock_session.get.call_count == 1

    assert_response_eq(apps_response, APP_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_applications_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text.return_value = (
        json.dumps([APP_JSON, APP_JSON])
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    resource_response = await Applications(mock_session).list()

    assert mock_session.get.call_count == 1

    assert isinstance(resource_response, list)
    assert len(resource_response) == 2

    assert_response_eq(resource_response[0], APP_JSON)
    assert_response_eq(resource_response[1], APP_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_applications_delete_success(mock_session):
    mock_session.delete.return_value.__aenter__.return_value.text.return_value = (
        json.dumps({})
    )
    mock_session.delete.return_value.__aenter__.return_value.status = 200

    await Applications(mock_session).delete("app_to_be_booped")
    assert mock_session.delete.call_count == 1


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_applications_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.text.return_value = (
        json.dumps(APP_JSON)
    )
    mock_session.post.return_value.__aenter__.return_value.status = 202

    cap = CreateApplicationParams(
        name="test-test",
        language="python",
        git_sha="123sha",
        pipeline=PipelineIdentifiers(name="test-pipeline"),
    )

    create_response = await Applications(mock_session).create(cap)

    assert mock_session.post.call_count == 1
    assert isinstance(create_response, dict)
    assert_response_eq(create_response, APP_JSON)
