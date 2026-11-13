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
    
    @app_commands.command(name="maintenance", description="Enable or disable maintenance mode for JADB.")
    @app_commands.default_permissions(administrator=True)
    async def maintenance(self, interaction: discord.Interaction, enabled: bool):
        if interaction.user.id not in self.bot.developer_ids:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You do not have permission to use this command",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
        
        self.bot.maintenance_mode = enabled
        self.bot.save_state()
        
        if enabled:
            await self.bot.change_presence(
                status=discord.Status.invisible
            )
        else:
            await self.bot.change_presence(
                status=discord.Status.online
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Maintenance Mode",
                description=f"Has been set {enabled}",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))