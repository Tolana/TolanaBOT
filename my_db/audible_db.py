from my_db.db import open_conn

con, cur = open_conn()

def get_new_books():
    #with DBManager('example.db') as cur:
    cur.execute("SELECT `series`.`title` as 'series', `bookQ`.`book_id`, `book`.`title`, `book`.`series_url`, `book`.`releaseDate` FROM `book`,`bookQ`,`series` WHERE `book`.`series_url` = `series`.`series_url` AND `bookQ`.`book_id` = `book`.`id`")
    books = cur.fetchall()
    if len(books) > 0:
        return books
    else:
        return None

def delete_new_books():
    #with DBManager('example.db') as cur:
    cur.execute('DELETE FROM bookQ;')
    return
def get_upcomming_books():
    #with DBManager('example.db') as cur:
    cur.execute("SELECT `series.title` as `series`,`book.title`, `book`.`series_url`, `book`.`releaseDate` FROM `book`,`series` WHERE `book`.`series_url` = `series`.`series_url` AND '220811' < `book`.`releaseDate`")
    books = cur.fetchall()
    if len(books) > 0:
        return books
    else:
        return None