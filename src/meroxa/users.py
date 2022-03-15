import json

from .utils import meroxa_api_response


class UserResponse(object):
    def __init__(
            self, uuid: str, email: str, given_name: str,
            family_name: str, email_verified: bool,
            picture: str, last_login: str, features: list[str]) -> None:
        self.uuid = uuid
        self.email = email
        self.given_name = given_name
        self.family_name = family_name
        self.email_verified = email_verified
        self.picture = picture
        self.last_login = last_login
        self.features = features


class Users:
    def __init__(self, session) -> None:
        self._session = session

    @meroxa_api_response(return_type=UserResponse)
    async def me(self):
        async with self._session.get("/v1/users/me") as resp:
            res = await resp.text()
            return UserResponse(**json.loads(res))
