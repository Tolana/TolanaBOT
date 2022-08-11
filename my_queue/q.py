import pathlib
import sys
#pcwd = pathlib.Path(__file__).parent.resolve()
#sys.path.append('C:\Programming\TolanaBOT')
import sqlite3
from webbrowser import get
import disnake
from disnake.ext import tasks
from my_db.db import DBManager, open_conn
from disnake.ext import commands
from my_tasks.adbl_tasks import new_books
from my_db.audible_db import delete_new_books, get_new_books

class MyQueue():
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def start(self):
        self.check_q.start()
        print("Queue task running...")

    @tasks.loop(minutes=15)
    async def check_q(self):
        print('checking Q for tasks: ...')
        books = get_new_books() 
        if books is not None:
            embed_books = new_books(books)
            await self.bot.get_channel(793945580715638806).send(embed=embed_books)
            delete_new_books()