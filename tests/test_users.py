import json
from unittest.mock import AsyncMock
from unittest.mock import patch

from meroxa import CreateResourceParams
from meroxa import ResourceCredentials
from meroxa import Resources
from meroxa.resources import ResourcesResponse
from meroxa.types import ResourceType

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


def assert_resource_equality(response, comparison):
    assert response.connector_count == comparison.get("connector_count")
    assert response.created_at == comparison.get("created_at")
    assert response.metadata == comparison.get("metadata")
    assert response.name == comparison.get("name")
    assert response.type == comparison.get("type")
    assert response.updated_at == comparison.get("updated_at")
    assert response.url == comparison.get("url")
    assert response.uuid == comparison.get("uuid")
    assert response.status.last_updated_at == comparison["status"]["last_updated_at"]
    assert response.status.state == comparison["status"]["state"]


@patch("aiohttp.ClientSession")
async def test_resources_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps(RESOURCE_JSON)]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, resource_response = await Resources(mock_session).get("resource_name")

    assert mock_session.get.call_count == 1
    assert error is None

    assert_resource_equality(resource_response, RESOURCE_JSON)


@patch("aiohttp.ClientSession")
async def test_resources_get_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 404

    error, resource_response = await Resources(mock_session).get("something")

    assert mock_session.get.call_count == 1
    assert resource_response is None

    # TODO: Better comparison logic
    assert ERROR_MESSAGE.items() <= error.__dict__.items()


@patch("aiohttp.ClientSession")
async def test_resources_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps([RESOURCE_JSON, RESOURCE_JSON])]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, resource_response = await Resources(mock_session).list()

    assert mock_session.get.call_count == 1
    assert error is None

    assert isinstance(resource_response, list)
    assert len(resource_response) == 2

    assert_resource_equality(resource_response[0], RESOURCE_JSON)
    assert_resource_equality(resource_response[1], RESOURCE_JSON)


@patch("aiohttp.ClientSession")
async def test_resources_list_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 404

    error, resource_response = await Resources(mock_session).list()

    assert mock_session.get.call_count == 1
    assert resource_response is None

    # TODO: Better comparison logic
    assert ERROR_MESSAGE.items() <= error.__dict__.items()


@patch("aiohttp.ClientSession")
async def test_resources_delete_success(mock_session):
    mock_session.delete.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=None
    )

    mock_session.delete.return_value.__aenter__.return_value.status = 200

    await Resources(mock_session).delete("delete")

    assert mock_session.delete.call_count == 1


@patch("aiohttp.ClientSession")
async def test_resources_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(RESOURCE_JSON)
    )
    mock_session.post.return_value.__aenter__.return_value.status = 202

    crp = CreateResourceParams(
        name="resource_name",
        type=ResourceType.POSTGRES.value,
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

    error, create_response = await Resources(mock_session).create(crp)

    assert mock_session.post.call_count == 1

    assert error is None

    assert isinstance(create_response, ResourcesResponse)

    assert_resource_equality(create_response, RESOURCE_JSON)


# @patch("aiohttp.ClientSession")
# async def test_resources_list_error(mock_session):
#     mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
#         return_value=json.dumps(ERROR_MESSAGE)
#     )
#
#     mock_session.get.return_value.__aenter__.return_value.status = 200
#
#     error, resource_response = await Resources(mock_session).list()
#
#     assert mock_session.get.call_count == 1
#     assert resource_response is None
#
#     # TODO: Better comparison logic
#     assert ERROR_MESSAGE.items() <= error.__dict__.items()
