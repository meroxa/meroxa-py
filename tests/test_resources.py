import json
from unittest.mock import patch

import pytest
from tests import assert_response_eq

from meroxa import CreateResourceParams
from meroxa import ResourceCredentials
from meroxa import Resources

RESOURCE_JSON = {
    "id": 9652,
    "uuid": "7cff65a0-ba9f-4b02-9fb8-1f7b3d1d5bc4",
    "name": "resource_name",
    "type": "postgres",
    "url": "postgres:/connection_url:5432/my_user",
    "metadata": {"logical_replication": False},
    "connector_count": 1,
    "status": {"state": "ready", "last_updated_at": "2022-03-02T20:18:14Z"},
    "created_at": "2022-03-02T20:18:14Z",
    "updated_at": "2022-03-02T20:18:14Z",
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find resource"}


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.json.return_value = (
        json.dumps(RESOURCE_JSON)
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    response = await Resources(mock_session).get("resource_name")

    assert mock_session.get.call_count == 1
    assert_response_eq(json.loads(response), RESOURCE_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.json.return_value = (
        json.dumps([RESOURCE_JSON, RESOURCE_JSON])
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    response = await Resources(mock_session).list()
    json_resp = json.loads(response)

    assert mock_session.get.call_count == 1

    assert isinstance(json_resp, list)
    assert len(json_resp) == 2

    assert_response_eq(json_resp[0], RESOURCE_JSON)
    assert_response_eq(json_resp[1], RESOURCE_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_delete_success(mock_session):
    mock_session.delete.return_value.__aenter__.return_value.json.return_value = (
        json.dumps({})
    )
    mock_session.delete.return_value.__aenter__.return_value.status = 200

    await Resources(mock_session).delete("delete")
    assert mock_session.delete.call_count == 1


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.json.return_value = (
        json.dumps(RESOURCE_JSON)
    )
    mock_session.post.return_value.__aenter__.return_value.status = 202

    crp = CreateResourceParams(
        name="resource_name",
        type="postgres",
        url="postgres:/connection_url:5432/my_user",
        metadata={"logical_replication": "false"},
        credentials=ResourceCredentials(
            username="testuser",
            password="123password",
            ca_cert="ca_cert",
            client_cert="client_cert",
            client_cert_key="key",
            ssl=True,
        ),
    )

    create_response = await Resources(mock_session).create(crp)
    json_resp = json.loads(create_response)

    assert mock_session.post.call_count == 1
    assert isinstance(json_resp, dict)

    assert_response_eq(json_resp, RESOURCE_JSON)
