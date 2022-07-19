import disnake
from disnake.ext import commands
from tokens import tokens

BOT_TOKEN = tokens['bot_token']
my_guild = 793945580048875591

bot = commands.Bot(
    
    test_guilds=[793945580048875591]
)


@bot.event
async def on_ready():
    print("The bot is ready!")


bot.load_extension("cogs.ping")  # Note: We did not append the .py extension.
#git test comment a
#bot.run(BOT_TOKEN)