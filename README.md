# meroxa-py

meroxa-py is an async-first library created to interact with the Meroxa platform-api

## Installation 

`pip install /path/to/your/cloned/repo` 

(note: this will change once this package gets properly published)

## Usage
```python
import meroxa
import asyncio

from pprint import pprint

opts = meroxa.ClientOptions(
    auth="auth token", 
    url="https://api.staging.meroxa.io"
)

async def main():
    async with meroxa.createSession(opts) as session:
        client = meroxa.Client(session)
        resp = await client.users.me()
        pprint.pprint(resp)


asyncio.run(main())
```