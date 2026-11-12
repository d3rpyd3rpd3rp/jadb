import discord
from discord import app_commands
from discord.ext import commands
from os import getenv

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="member", description="Change your role from guest to member!")
    async def member(self, interaction: discord.Interaction):
        user = interaction.user
        guest_role = interaction.guild.get_role(int(getenv('GUEST_ROLE_ID')))
        member_role = interaction.guild.get_role(int(getenv('MEMBER_ROLE_ID')))
        
        if guest_role is None or member_role is None:
            staff_chat = await self.bot.fetch_channel(getenv('OFFICER_CHAT_ID'))
            await staff_chat.send(
                content="<@426160449302560780>",
                embed=discord.Embed(
                    title="Role Error",
                    description=f"Guest Role Status: {"Active" if guest_role else "Inactive"}\nMember Role Status: {"Active" if member_role else "Inactive"}",
                    color=discord.Color.red()
                )
            )
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="One or more roles are incorrect\nStaff have been contacted",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return
        
        if member_role in user.roles:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Nice try",
                    description="You already have the member role :)",
                    color=discord.Color.red(),
                ),
                ephemeral=True
            )
            return
        
        await user.remove_roles(guest_role) if guest_role in user.roles else None
        await user.add_roles(member_role)
        
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Success!",
                description=f"Welcome to the club {user.mention}!",
                color=discord.Color.green()
            ),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))