#import pathlib
#import sys
#pcwd = pathlib.Path(__file__).parent.resolve()
#sys.path.append(pcwd)
#import disnake
from disnake.ext import commands, tasks
from tokens import tokens
from my_queue.q import MyQueue


BOT_TOKEN = tokens['bot_token']
my_guild = 793945580048875591

bot = commands.InteractionBot(
    test_guilds=[793945580048875591]
)

@bot.event
async def on_ready():
    print("The bot is ready!")
    q = MyQueue(bot)




bot.run(BOT_TOKEN)
