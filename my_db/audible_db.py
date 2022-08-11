from my_db.db import DBManager


def get_new_books():
    with DBManager('example.db') as cur:
        cur.execute("SELECT series.title as 'series', bookQ.book_id, book.title, book.`series-url`, book.releaseDate FROM book,bookQ,series WHERE book.`series-url` = series.`series-url` AND bookQ.book_id = book.id")
        books = cur.fetchall()
        if len(books) > 0:
            return books
        else:
            return None
"SELECT series.title as 'series',book.title, book.`series-url`, book.releaseDate FROM book,series WHERE book.`series-url` = series.`series-url` AND '220811' < book.releaseDate"

def get_upcomming_books():
    with DBManager('example.db') as cur:
        cur.execute("SELECT series.title as 'series',book.title, book.`series-url`, book.releaseDate FROM book,series WHERE book.`series-url` = series.`series-url` AND '220811' < book.releaseDate")
        books = cur.fetchall()
        if len(books) > 0:
            return books
        else:
            return None