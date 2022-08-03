import pathlib
import sys
#pcwd = pathlib.Path(__file__).parent.resolve()
#sys.path.append('C:\Programming\TolanaBOT')
import sqlite3
import disnake
from disnake.ext import tasks
from my_db.db import DBManager, open_conn
from disnake.ext import commands
import my_tasks

import pprint

pp = pprint.PrettyPrinter()
pprint.pp(sys.path)


class MyQueue():
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #self.con = sqlite3.connect('example.db')
        dbcon, dbcur = open_conn('example.db')
        self.con = dbcon
        self.cur = dbcur
        self.queue = self.check_q.start()
        print("Queue initialized!")

    @tasks.loop(minutes=15)
    async def check_q(self):
            print('checking Q for tasks: ...')
            with DBManager('example.db') as cursor:
                cursor.execute("SELECT * FROM queue")
                r = cursor.fetchall()
                print(r)
                if len(r) > 0:
                    await self.bot.get_channel(793945580715638806).send(content="QUEUE")
                else: 
                    print('no tasks to complete')
            #self.cur.execute("SELECT * FROM queue")
            #r = self.cur.fetchall()
            #print(r)
            #if len(r) > 0:
            #    await self.bot.get_channel(793945580715638806).send(content="QUEUE")
            #else: 
            #    print('no tasks to complete')