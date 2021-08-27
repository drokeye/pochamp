from typing import Dict

from .user import User
from .channel import Channel

class Message:
    def __init__(self, data: Dict[str, str], state):
        self.data = data
        self.state = state
        self.id: str = data.get("_id")
        self.nonce: str = data.get("nonce")

    @property
    def content(self) -> str:
        return self.data.get("content")

    async def fetch_channel(self) -> Channel:
        self.channel = await self.state.fetch_channel(self.data.get("channel"))
        return self.channel

    async def fetch_author(self) -> User:
        self.author = await self.state.fetch_user(self.data.get("author"))
        return self.author
        