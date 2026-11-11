import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='jadb.log', encoding='utf-8', mode='w')

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
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.events")
        
        await self.tree.sync()

bot = JADB()
    
bot.run(token, log_handler=handler, log_level=logging.DEBUG)