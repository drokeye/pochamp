import asyncio
import typing as t

import aiohttp
import orjson
import websockets

from .user import User
from .channel import Channel
from .message import Message

class InvalidToken(Exception):
    ...

class Bot:
    WS_URL: t.ClassVar[str] = "wss://ws.revolt.chat"
    REST_URL: t.ClassVar[str] = "https://api.revolt.chat"
    
    def __init__(self, token: str, /, loop: asyncio.AbstractEventLoop = None) -> None:
        self.token = token
        self.loop = loop or asyncio.get_event_loop()

    async def on_ready(self) -> None:
        """Event which is triggered when the bot is connected to websocket"""
        ...

    async def on_message(self, message: Message) -> None:
        ...

    async def keep_alive(self, ws) -> None:
        while True:
            packet = await ws.recv()
            packet = orjson.loads(packet)
            if packet["type"] == "Error":
                raise Exception(packet["error"])
            if packet["type"] == "Ready":
                await self.on_ready()
            elif packet["type"] == "Message":
                message = Message(packet, state=self)
                await self.on_message(message)

    async def connect(self) -> None:
        async with websockets.connect(self.WS_URL) as ws:
            payload = {
                "type": "Authenticate",
                "token": self.token
            }
            payload = orjson.dumps(payload)
            await ws.send(payload.decode())
            self.loop.create_task(await self.keep_alive(ws))

    async def fetch_user(self, user_id: str, /) -> t.Union[User, None]:
        headers = {
            "x-bot-token": self.token
        }
        route = self.REST_URL + f"/users/{user_id}"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=route) as req:
                if req.status == 200:
                    return User(await req.json())
                if req.status == 404:
                    return None

    async def fetch_channel(self, channel_id: str, /) -> Channel:
        headers = {
            "x-bot-token": self.token
        }
        route = self.REST_URL + f"/channels/{channel_id}"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=route) as req:
                if req.status == 200:
                    return Channel(await req.json(), state=self)
                if req.status == 404:
                    return None