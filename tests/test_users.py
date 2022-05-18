import json
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from meroxa.users import Users

USER_RESPONSE_JSON = {
    "uuid": "e882051d-56cc-4962-88ed-d1d730567220",
    "email": "jimbob@company.com",
    "given_name": "Jim",
    "family_name": "Bob",
    "email_verified": True,
    "picture": "www.url.com",
    "last_login": "2022-04-21T16:42:03.162Z",
    "username": None,
    "features": ["functions", "turbine"],
}

ERROR_MESSAGE = {"code": "not_found", "message": "could not find user"}


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_user_me_success(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        side_effect=[json.dumps(USER_RESPONSE_JSON)]
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    _, user_response = await Users(mock_session).me()

    assert mock_session.get.call_count == 1
    assert user_response.__dict__ == USER_RESPONSE_JSON


@pytest.mark.asyncio
@patch("aiohttp.ClientSession")
async def test_user_me_error(mock_session):
    mock_session.get.return_value.__aenter__.return_value.text = AsyncMock(
        return_value=json.dumps(ERROR_MESSAGE)
    )

    mock_session.get.return_value.__aenter__.return_value.status = 200

    error, user_response = await Users(mock_session).me()

    assert mock_session.get.call_count == 1
    assert user_response is None

    # TODO: Better comparison logic
    assert ERROR_MESSAGE.items() <= error.__dict__.items()
