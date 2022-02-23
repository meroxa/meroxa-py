class Resources:
    def __init__(self, session) -> None:
        self._session = session

    async def list(self):
        async with self._session.get("/v1/resources") as resp:
            return await resp.text()
