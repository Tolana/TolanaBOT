import sqlite3 
import mysql.connector

def open_conn(dbname=""):
    con = mysql.connector.connect(host="localhost",user="root",password="",database="audiblebooks")
    cur = con.cursor()
    return con, cur

class DBManager(object):
    def __init__(self, dbname=""):
        self.db = None
        self.dbname = dbname

    def __enter__(self):
        return cur

    def __exit__(self, type, value, traceback):
        print(con.commit())
        #print('closed db connection')
