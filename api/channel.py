import asyncio
from typing import Any, Dict

import aiohttp
import ulid

class Channel:

    def __init__(self, data: Dict[str, Any], state):
        self.data = data
        self.state = state
        self.id: str = data.get("_id")
        self.type: str = data.get("channel_type")
        self.name: str = data.get("pog")
        self.nonce: str = data.get("nonce")

    async def send(self, content: str) -> None:
        headers = {
            "x-bot-token": self.state.token
        }
        data = {
            "content": content,
            "nonce": str(ulid.new())
        }
        route = self.state.REST_URL + f"/channels/{self.id}/messages"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url=route, json=data) as req:
                if req.status == 200:
                    return
                if req.status == 429:
                    retry_after = int(req.headers.get("Retry-After"))
                    await asyncio.sleep(retry_after)
                    return

                raise Exception(f"API Returned: {req.status} code")