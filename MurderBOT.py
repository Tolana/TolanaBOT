import pathlib
import sys
#pcwd = pathlib.Path(__file__).parent.resolve()
#sys.path.append(pcwd)
import disnake
from disnake.ext import commands, tasks
from tokens import tokens
from my_queue.q import MyQueue
from my_db.db import open_conn, DBManager
import pprint
import sqlite3

pp = pprint.PrettyPrinter()
#pprint.pp(sys.path)


BOT_TOKEN = tokens['bot_token']
my_guild = 793945580048875591

bot = commands.InteractionBot(
    test_guilds=[793945580048875591]
)

@bot.event
async def on_ready():
    print("The bot is ready!")
    q = MyQueue(bot)

with DBManager('example.db') as cur:
    try:
        cur.execute("INSERT INTO book VALUES('Harry Potter','JK Rowling','Steven Fry','url-hp','220707','1 hour and 1 minute');")
    except sqlite3.IntegrityError as err:
        print(str(err))
        if str(err).startswith("UNIQUE constraint failed"):
            print('Duplicate!')



#bot.run(BOT_TOKEN)
