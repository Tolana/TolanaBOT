import sqlite3 
import mysql.connector

def open_conn(dbname):
    con = mysql.connector.connect(host="localhost",user="admin",password="")
    cur = con.cursor()
    return con, cur

class DBManager(object):
    def __init__(self, dbname):
        self.db = None
        self.dbname = dbname

    def __enter__(self):
        self.db = mysql.connector.connect(host="localhost",user="root",password="",database="audiblebooks")
        return self.db.cursor()

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()
        #print('closed db connection')
