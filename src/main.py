import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from os import getenv

load_dotenv()
handler = RotatingFileHandler(
    filename=getenv('LOG_FILE'),
    encoding="utf-8",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    mode="a"
)

class JADB(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents
        )
    
    async def setup_hook(self):
        await self.load_extension("cogs.events")
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.fun")
        
        synced = await self.tree.sync()
        
        print("Commands synchronized:")
        for command in synced:
            print(f"- {command.name}")
        print("--------------------------------")

bot = JADB()
    
bot.run(getenv('DISCORD_TOKEN'), log_handler=handler, log_level=logging.DEBUG)