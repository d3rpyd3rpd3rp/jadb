import discord
from discord.ext import commands
from discord import app_commands

import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from os import getenv

import json
from pathlib import Path

load_dotenv()
handler = RotatingFileHandler(
    filename=getenv('LOG_FILE'),
    encoding="utf-8",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    mode="a"
)

STATE_FILE = Path(__file__).parent / "bot_state.json"

def load_maintenance_mode():
    if not STATE_FILE.exists():
        return False
    
    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        
        return data.get("maintenance_mode", False)
    except (json.JSONDecodeError, OSError):
        print(f"WARNING: Could not read {"bot_state.json"}!")
        return True

class JADBCommandTree(app_commands.CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.client.maintenance_mode and interaction.user.id not in self.client.developer_ids:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Under Maintenance",
                    description="Apologies, but JADB is currently undergoing maintenance.\nPlease check back later! :)",
                    color=discord.Color.brand_red()
                ),
                ephemeral=True
            )
            return False
        return True

class JADB(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            tree_cls=JADBCommandTree
        )
        
        self.maintenance_mode = load_maintenance_mode()
        self.developer_ids = {
            int(user_id.strip()) for user_id in getenv('DEVELOPER_IDS', '').split(',') if user_id.strip()
        }
    
    def save_state(self):
        data = {
            "maintenance_mode": self.maintenance_mode
        }
        
        with STATE_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
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