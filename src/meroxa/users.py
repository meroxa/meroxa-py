from aiohttp import ClientSession


class Users:
    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def me(self):
        try:
            async with self._session.get("/v1/users/me") as resp:
                return await resp.json()
        except Exception as e:
            raise e
