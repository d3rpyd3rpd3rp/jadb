import discord
from discord.ext import commands
from os import getenv

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot logged in\nName: {self.bot.user.name}\nID: {self.bot.user.id}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.bot.fetch_channel(int(getenv('WELCOME_CHANNEL_ID')))
        
        embed = discord.Embed(
            title=f"Welcome {member.display_name if member.display_name else member.name}!",
            description="We're so happy you could make it :)",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(getenv('WELCOME_CHANNEL_ID')))
        
        embed = discord.Embed(
            title=f"Goodbye {member.display_name if member.display_name else member.name}!",
            description="We're sad to see them go :(",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        if channel is not None:
            await channel.send(embed=embed)
    
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