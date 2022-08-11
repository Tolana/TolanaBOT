import disnake
from disnake.ext import commands
from my_tasks.adbl_tasks import upcomming_books
from my_db.audible_db import get_upcomming_books

class AudibleCommands(commands.Cog):

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
    
    @commands.slash_command()
    async def audible(self, inter: disnake.ApplicationCommandInteraction):
        pass

    
    @audible.sub_command()
    async def upcomming(self, inter: disnake.ApplicationCommandInteraction):
        """Get the bot's current websocket latency."""
        upc_books = get_upcomming_books()
        if upc_books is not None:
            upc = upcomming_books(get_upcomming_books())
            await inter.response.send_message(embed=upc)
        else:
            await inter.response.send_message("no upcomming books!")


def setup(bot: commands.InteractionBot):
    bot.add_cog(AudibleCommands(bot))