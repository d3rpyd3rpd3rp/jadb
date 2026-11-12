import discord
from discord import app_commands
from discord.ext import commands
from buttons import MenuView, MenuButton

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Displays the help menu.")
    async def help(self, interaction: discord.Interaction):
        main_embed = discord.Embed(
            title="Help Menu",
            description="""
This menu gives some additional information about how I work!

Click the buttons below for other screens :)
""",
            color=discord.Color.ash_embed()
        )
        general_embed = discord.Embed(
            title="General Commands",
            description=(
                "/help - Displays the help menu.\n"
                "/hello - jadb gives you a greeting!\n"
                "/serverinfo - Gives information about the server."
            ),
            color=discord.Color.blue()
        )
        moderation_embed = discord.Embed(
            title="Moderation Commands",
            description=(
                "/member - Change your role from guest to member!"
            ),
            color=discord.Color.red()
        )
        fun_embed = discord.Embed(
            title="Fun Commands",
            description=(
                "No commands yet :("
            ),
            color=discord.Color.green()
        )
        
        view = MenuView([
            MenuButton("General", general_embed),
            MenuButton("Moderation", moderation_embed, discord.ButtonStyle.danger),
            MenuButton("Fun", fun_embed, discord.ButtonStyle.success)
        ])
        
        await interaction.response.send_message(
            embed=main_embed,
            view=view,
            ephemeral=True
        )
    
    @app_commands.command(name="hello", description="jadb gives you a greeting!")
    async def hello(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Hello there!",
            description="My name is Just Another Discord Bot,\nbut you can call me JADB :)",
            color=discord.Color.fuchsia()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
    
    @app_commands.command(name="serverinfo", description="Gives information about the server.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        embed = discord.Embed(
            title="Server Information",
            color=discord.Color.dark_red()
        )
        embed.add_field(
            name="Server Name",
            value=guild.name,
            inline=False
        )
        embed.add_field(
            name="Member Count",
            value=str(guild.member_count),
            inline=True
        )
        embed.add_field(
            name="Owner",
            value=str(guild.owner.mention),
            inline=True
        )
        embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(General(bot))