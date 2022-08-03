import sqlite3 


def open_conn(dbname):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    return con, cur

class DBManager(object):
    def __init__(self, dbname):
        self.db = None
        self.dbname = dbname

    def __enter__(self):
        self.db = sqlite3.connect(self.dbname)
        return self.db.cursor()

    def __exit__(self, type, value, traceback):
        self.db.commit()
        self.db.close()
        #print('closed db connection')
