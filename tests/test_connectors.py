import json
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from meroxa import Connectors
from meroxa import ConnectorsResponse
from meroxa import CreateConnectorParams

CONNECTOR_JSON = {
    "id": 14426,
    "uuid": "80b59b23-2256-46f4-9d71-aa994972b4c2",
    "name": "connectorb228bee5-0580-4955-b3b1-cb09c0904b45-889371",
    "type": "debezium-mysql-source",
    "config": {},
    "state": "pending",
    "resource_id": 15184,
    "pipeline_id": 8826,
    "pipeline_name": "pAfpKLolrz",
    "resource_name": "testin",
    "streams": {"dynamic": False, "output": ["resource-15184-589682.testin.something"]},
    "metadata": {"mx:connectorType": "source"},
    "created_at": "2022-04-20T22:20:38Z",
    "updated_at": "2022-04-20T22:20:38Z",
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find function"}


def assert_connector_equality(response, comparison):
    print(response.__dict__)
    assert response.resource_name == comparison.get("resource_name")
    assert response.pipeline_name == comparison.get("pipeline_name")
    assert response.config == comparison.get("config")


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connector_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps(CONNECTOR_JSON)]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, connectors_response = await Connectors(mock_session).get("connector")

    assert mock_session.get.call_count == 1
    assert error is None

    assert_connector_equality(connectors_response, CONNECTOR_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connectors_get_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 404

    error, connectors_response = await Connectors(mock_session).get("connector")

    assert mock_session.get.call_count == 1
    assert connectors_response is None

    assert ERROR_MESSAGE.items() <= error.__dict__.items()


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connectors_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps([CONNECTOR_JSON, CONNECTOR_JSON])]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, resource_response = await Connectors(mock_session).list()

    assert mock_session.get.call_count == 1
    assert error is None

    assert isinstance(resource_response, list)
    assert len(resource_response) == 2

    assert_connector_equality(resource_response[0], CONNECTOR_JSON)
    assert_connector_equality(resource_response[1], CONNECTOR_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connection_list_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 404

    error, resource_response = await Connectors(mock_session).list()

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

    await Connectors(mock_session).delete("function_i_want_gone")
    assert mock_session.delete.call_count == 1


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_resources_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(CONNECTOR_JSON)
    )
    mock_session.post.return_value.__aenter__.return_value.status = 202

    ccp = CreateConnectorParams(
        resource_name="testin",
        pipeline_name="pAfpKLolrz",
        config={"input": "something?"},
    )

    error, create_response = await Connectors(mock_session).create(ccp)

    assert mock_session.post.call_count == 1
    assert error is None
    assert isinstance(create_response, ConnectorsResponse)
    assert_connector_equality(create_response, CONNECTOR_JSON)
