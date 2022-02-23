class Users:
    def __init__(self, session) -> None:
        self._session = session

    async def me(self):
        async with self._session.get("/v1/users/me") as resp:
            return await resp.text()
