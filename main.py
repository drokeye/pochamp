import asyncio

from api import gateway
from api.message import Message

class Bot(gateway.Bot):
    def __init__(self):
        super().__init__(token="poggers")
    
    async def on_ready(self) -> None:
        print("pogchamp logged in")

    async def on_message(self, message: Message) -> None:
        author = await message.fetch_author()
        channel = await message.fetch_channel()
        print(message.content)
        if author.is_bot:
            return
        if channel.type == "TextChannel":
            if "keycap" in message.content:
                return await channel.send("https://thumbs.gfycat.com/CriminalDapperGoldenmantledgroundsquirrel-mobile.mp4")
            if message.content == "<@01FE05FHHMQ9Z5W5P5H21WXR9C>":
                return await channel.send(f"<@{author.id}> wassup my little pogchamp?")

async def main():
    bot = Bot()
    user = await bot.fetch_channel("pog_channel")
    await user.send("poggers **dude**")
    await bot.connect()

asyncio.run(main())