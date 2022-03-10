# meroxa-py

meroxa-py is an async-first library created to interact with the Meroxa platform-api

## Installation 

`pip install /path/to/your/cloned/repo` 

## Usage
```python
import asyncio

from meroxa import Meroxa
from pprint import pprint


auth="auth.token", 
url="https://api.staging.meroxa.io"

async def main():
    async with Meroxa(auth=auth, api_route=url) as m:
        resp = await m.users.me()
        pprint.pprint(resp)

asyncio.run(main())
```