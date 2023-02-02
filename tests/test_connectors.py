import json
from unittest.mock import patch

import pytest

from meroxa import Connectors
from meroxa import CreateConnectorParams

CONNECTOR_JSON = {
    "id": 14426,
    "uuid": "80b59b23-2256-46f4-9d71-aa994972b4c2",
    "name": "connectorb228bee5-0580-4955-b3b1-cb09c0904b45-889371",
    "type": "debezium-mysql-source",
    "config": {},
    "state": "pending",
    "resource_id": 15184,
    "resource_uuid": "80b59b23-2256-46f4-9d71-aa994972b4c2",
    "pipeline_id": 8826,
    "pipeline_name": "pAfpKLolrz",
    "resource_name": "testin",
    "streams": {"dynamic": False, "output": ["resource-15184-589682.testin.something"]},
    "metadata": {"mx:connectorType": "source"},
    "created_at": "2022-04-20T22:20:38Z",
    "updated_at": "2022-04-20T22:20:38Z",
    "collection": "example_collection",
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find function"}


# All test coroutines will be treated as marked.
def assert_response_eq(response, comparison):
    assert sorted(response.items()) == sorted(comparison.items())


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connector_get_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text.return_value = (
        json.dumps(CONNECTOR_JSON)
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    connectors_response = await Connectors(mock_session).get("connector")

    assert mock_session.get.call_count == 1

    assert_response_eq(connectors_response, CONNECTOR_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connectors_list_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text.return_value = (
        json.dumps([CONNECTOR_JSON, CONNECTOR_JSON])
    )
    mock_session.get.return_value.__aenter__.return_value.status = 200

    resource_response = await Connectors(mock_session).list()

    assert mock_session.get.call_count == 1

    assert isinstance(resource_response, list)
    assert len(resource_response) == 2

    assert_response_eq(resource_response[0], CONNECTOR_JSON)
    assert_response_eq(resource_response[1], CONNECTOR_JSON)


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connectors_delete_success(mock_session):
    mock_session.delete.return_value.__aenter__.return_value.text.return_value = (
        json.dumps({})
    )
    mock_session.delete.return_value.__aenter__.return_value.status = 200

    await Connectors(mock_session).delete("function_i_want_gone")
    assert mock_session.delete.call_count == 1


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_connectors_create_success(mock_session):
    mock_session.post.return_value.__aenter__.return_value.text.return_value = (
        json.dumps(CONNECTOR_JSON)
    )
    mock_session.post.return_value.__aenter__.return_value.status = 202

    ccp = CreateConnectorParams(
        resource_name="testin",
        pipeline_name="pAfpKLolrz",
        config={"input": "something?"},
    )

    create_response = await Connectors(mock_session).create(ccp)

    assert mock_session.post.call_count == 1
    assert isinstance(create_response, dict)

    assert_response_eq(create_response, CONNECTOR_JSON)
