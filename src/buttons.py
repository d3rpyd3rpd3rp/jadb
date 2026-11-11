import discord

class MenuView(discord.ui.View):
    def __init__(self, buttons, timeout=180):
        super().__init__(timeout=timeout)
        
        for button in buttons:
            self.add_item(button)

class MenuButton(discord.ui.Button):
    def __init__(self, label, embed, style=discord.ButtonStyle.primary):
        super().__init__(label=label, style=style)
        self.embed = embed
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=self.embed,
            view=self.view
        )