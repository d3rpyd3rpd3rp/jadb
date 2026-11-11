import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as\nName: {self.bot.user.name}\nID: {self.bot.user.id}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member.name} joined the server!")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member.name} left the server!")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if self.bot.user.mention in message.content:
            await message.delete()
            await message.channel.send(f"Please refrain from pinging me {message.author.mention}, I am very busy.")
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Events(bot))