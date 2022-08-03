from datetime import datetime
import pathlib
import sys
from types import NoneType
pcwd = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(pcwd))
import requests
from bs4 import BeautifulSoup
from my_db.db import DBManager
from time import sleep
import sqlite3

_DELAY = 10


def scrape(url,page=None):
    url = url + "?pageSize=50"
    if page is not None:
        url = url + f'&page={page}'
        r = requests.get(url)
        return r.content
    r = requests.get(url)
    return r.content

# PARSER FUNCTIONS 
def saveBooks(soup,books=None):
    if books is None:
        saved_books = []
    else:
        saved_books = books
    books = soup.select('.productListItem')
    for book in books:
        saved_book = {}
        if book.select_one('h3 > a') is not None:
            saved_book['title'] = book.select_one('h3 > a').get_text().strip()
        else: 
            saved_book = None
            saved_books.append(saved_book)
            continue
        if book.select('.authorLabel > span > a') is not None:
            saved_book['authors'] = [(author.get_text().strip(),author.get('href').strip()) for author in book.select('.authorLabel > span > a')]
        else:
            saved_book = None
            saved_books.append(saved_book)
            continue
        saved_book['narrators'] = [(narrator.get_text().strip(),narrator.get('href').strip()) for narrator in book.select('.narratorLabel > span > a')]
        length = book.select_one('.runtimeLabel > span').get_text().strip()
        length = [int(s) for s in length.split() if s.isdigit()]
        if len(length) == 1:
            saved_book['length'] = (length[0]*60)
        else:
            saved_book['length'] = (length[0]*60 + length[1])
        release_date = book.select_one('.releaseDateLabel > span').get_text().strip()
        release_date = "".join(release_date.split())
        release_date = release_date[12:]
        reverse_date = datetime.strptime(release_date,'%m-%d-%y')
        saved_book['release_date'] = datetime.strftime(reverse_date,'%y%m%d')
        saved_books.append(saved_book)
    return saved_books

def getSeriesTitle(soup):
    series = soup.select_one('h1').get_text().strip()
    return series

def getSeriesPages(soup):
    pages = soup.select('.pageNumberElement')
    pages = [int(page.get_text().strip()) for page in pages]
    return pages
# PARSER FUNCTIONS END


# DB FUNCTIONS 

def checkForNewBook(url,count):
    with DBManager('example.db') as cur:
        cur.execute(f'SELECT books FROM seriesCount WHERE "series-url" = "{url}"')
        book_count = cur.fetchone()
        if book_count is None:
            print('was none!')
            cur.execute(f'REPLACE INTO seriesCount VALUES("{url}","{count}")')
            return 0
        else: 
            cur.execute(f'SELECT books FROM seriesCount WHERE "series-url" = "{url}"')
            old_count = cur.fetchone()[0]
            print(old_count)
            cur.execute(f'REPLACE INTO seriesCount VALUES("{url}","{count}")')
            return old_count
            

def getUrls(): 
    with DBManager('example.db') as cur:
        cur.execute('SELECT url FROM url') 
        urls = [row[0] for row in cur]
        return urls

def insertSeries(url,title,authors):
    rowid = ""
    for author in authors:
        insertAuthor(author[0],author[1])
    with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO series ("title","series-url") VALUES("{title}","{url}");')
            rowid = cur.lastrowid
        except sqlite3.IntegrityError:
            '''cur.execute(f'SELECT id FROM series WHERE "series.series-url" = "{url}"')
            for row in cur:
                rowid = row[0]'''
            return
    for author in authors:
        insertSeriesAuthor(author[1],rowid)
    return

def insertSeriesAuthor(url,id):
    with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO seriesAuthors VALUES("{url}","{id}")')
        except sqlite3.IntegrityError:
            pass
    return

def insertAuthor(name,url):
    with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO author VALUES("{name}","{url}")')
        except sqlite3.IntegrityError:
            pass
    return

def insertNarrator(name,url):
    with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO narrator VALUES("{name}","{url}")')
        except sqlite3.IntegrityError:
            pass
    return

def insertBook(book,url):
    rowid = ''
    title = book['title']
    length = book['length']
    releaseDate = book['release_date']
    with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO book ("title","series-url","length","releaseDate") VALUES("{title}","{url}","{length}","{releaseDate}")')
            rowid = cur.lastrowid
            cur.execute(f'INSERT INTO bookQ VALUES({rowid});')
        except sqlite3.IntegrityError:
            return
    return rowid

def insertBookAuthors(authors,id):
    for author in authors:
        url = author[1]
        with DBManager('example.db') as cur:
            try:
                cur.execute(f'INSERT INTO authors VALUES("{url}","{id}")')
            except sqlite3.IntegrityError:
                pass
    return

def insertBookNarrators(narrators,id):
    for narrator in narrators:
        url = narrator[1]
        with DBManager('example.db') as cur:
            try:
                cur.execute(f'INSERT INTO narrators VALUES("{url}","{id}")')
            except sqlite3.IntegrityError:
                pass
    return

def insertBooks(books,url):
    for book in books:
        if book is not None:
            for author in book['authors']:
                insertAuthor(author[0],author[1])
            for narrator in book['narrators']:
                insertNarrator(narrator[0],narrator[1])
            id = insertBook(book,url)
            if isinstance(id,int):
                insertBookAuthors(book['authors'],id)
                insertBookNarrators(book['narrators'],id)
            else:
                pass
    return

# END OF DB FUNCTIONS


def run():
    urls = getUrls()
    start_time = datetime.now()
    for url in urls:
        print('waiting on delay...')
        sleep(_DELAY)
        html = scrape(url)
        soup = BeautifulSoup(html, 'html.parser')
        pages = getSeriesPages(soup)
        if len(pages) != 0:
            pages = pages[1:]
            books = saveBooks(soup)
            for page in pages:
                print('waiting on delay...')
                sleep(_DELAY)
                html = scrape(url,page)
                soup = BeautifulSoup(html, 'html.parser')
                books = saveBooks(soup,books)
        else: 
            books = saveBooks(soup)
        count = len(books)
        if count > checkForNewBook(url,count):
            insertSeries(url,getSeriesTitle(soup),books[0]['authors'])
            insertBooks(books,url)
        else:
            print('nothing new...')
    end_time = datetime.now() - start_time
    print(f'Completed in: {end_time}')
    return
#run()
