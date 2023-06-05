from datetime import datetime
import pathlib
import sys
from types import NoneType
pcwd = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(pcwd))
import requests
from bs4 import BeautifulSoup
from my_db.db import DBManager
from my_db.db import open_conn
from time import sleep
import sqlite3
import mysql.connector
_DELAY = 10
headers = {
    'User-Agent': "TolanaBOT for new book notifications, contact: tolanatolana@gmail.com"
}

"""def file_get_contents(filename):
    with open(filename,'rb') as f:
        return f.read()"""

con, cur = open_conn()

def scrape(url,page=None):
    url = url + "?pageSize=50"
    #return file_get_contents('cradle')
    if page is not None:
        url = url + f'&page={page}'
        r = requests.get(url,headers=headers)
        return r.content
    r = requests.get(url,headers=headers)
    print("scraped..")
    return r.content

# PARSER FUNCTIONS 
def saveBooks(soup,books=None):
    print('save books')
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
    print("end of save book")
    return saved_books

def getSeriesTitle(soup):
    series = soup.select_one('h1').get_text().strip()
    return series

def getSeriesPages(soup):
    pages = soup.select('.pageNumberElement')
    pages = [int(page.get_text().strip()) for page in pages]
    return pages
# PARSER FUNCTIONS END


# DB FUNCTIONS :)
#with DBManager() as cur:
def checkForNewBook(url,count):
    #with DBManager('example.db') as cur:
    cur.execute(f'SELECT `books` FROM `seriesCount` WHERE `series_url` = "{url}"')
    #print(f'SELECT `books` FROM `seriesCount` WHERE `series_url` = "{url}"')
    book_count = cur.fetchone()
    if book_count is not None:
        book_count = book_count[0]
    print("BOOK_COUNT: ",book_count)
    if book_count is None:
        print('was none!')
        cur.execute(f'REPLACE INTO `seriesCount` VALUES("{url}","{count}")')
        con.commit()
        return 0
    else: 
        cur.execute(f'SELECT `books` FROM `seriesCount` WHERE `series_url` = "{url}"')
        old_count = cur.fetchone()[0]
        print(old_count)
        cur.execute(f'REPLACE INTO `seriesCount` VALUES("{url}","{count}")')
        con.commit()
        return old_count
            

def getUrls(): 
    #with DBManager('example.db') as cur:
    cur.execute('SELECT url FROM url') 
    urls = [row[0] for row in cur]
    return urls

def insertSeries(url,title,authors):
    print("Insert Series")
    rowid = ""
    for author in authors:
        insertAuthor(author[0],author[1])
    #with DBManager('example.db') as cur:
    try:
        #print('InsertSeries: '+ f'INSERT INTO series ("title","series_url") VALUES("{title}","{url}");')
        cur.execute(f'INSERT INTO `series` (`title`,`series_url`) VALUES("{title}","{url}");')
        rowid = cur.lastrowid
    except sqlite3.IntegrityError:
        '''cur.execute(f'SELECT id FROM `series` WHERE `series.series_url` = "{url}"')
        for row in cur:
            rowid = row[0]'''
        return
    else:
        print("Commit!")
        con.commit()
    for author in authors:
        insertSeriesAuthor(author[1],rowid)
    print("end of insert series")
    return

def insertSeriesAuthor(url,id):
    #with DBManager('example.db') as cur:
    try:
        cur.execute(f'INSERT INTO `seriesAuthors` VALUES("{url}","{id}")')
    except mysql.connector.IntegrityError:
        pass
    else:
        print("Commit!")
        con.commit()
    return

def insertAuthor(name,url):
    #with DBManager('example.db') as cur:
    try:
        cur.execute(f'INSERT INTO `author` VALUES("{name}","{url}")')
    except mysql.connector.IntegrityError:
        pass
    else:
        print("Commit!")
        con.commit()
    return

def insertNarrator(name,url):
    #with DBManager('example.db') as cur:
    try:
        cur.execute(f'INSERT INTO `narrator` VALUES("{name}","{url}")')
    except mysql.connector.IntegrityError:
        pass
    else:
        print("Commit!")
        con.commit()
    return

def insertBook(book,url):
    rowid = ''
    title = book['title']
    length = book['length']
    releaseDate = book['release_date']
    #with DBManager('example.db') as cur:
    try:
        cur.execute(f'INSERT INTO book (`title`,`series_url`,`length`,`releaseDate`) VALUES("{title}","{url}","{length}","{releaseDate}")')
        rowid = cur.lastrowid
        cur.execute(f'INSERT INTO bookQ VALUES({rowid});')
    except mysql.connector.IntegrityError:
        return
    else:
        print("Commit!")
        con.commit()
    return rowid

def insertBookAuthors(authors,id):
    for author in authors:
        url = author[1]
        #with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO `authors` VALUES("{url}","{id}")')
        except mysql.connector.IntegrityError:
            pass
        else:
            print("Commit!")
            con.commit()
    return

def insertBookNarrators(narrators,id):
    for narrator in narrators:
        url = narrator[1]
        #with DBManager('example.db') as cur:
        try:
            cur.execute(f'INSERT INTO `narrators` VALUES("{url}","{id}")')
        except mysql.connector.IntegrityError:
            pass
        else:
            print("commit!")
            con.commit()
    return

def insertBooks(books,url):
    print("Insert books ")
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
    print("end of insert books")
    return

# END OF DB FUNCTIONS


def run():
    urls = getUrls()
    start_time = datetime.now()
    for url in urls:
        print('waiting on delay...')
        sleep(_DELAY)
        print('end of delay')
        html = scrape(url)
        soup = BeautifulSoup(html, 'html.parser')
        print("Got soup")
        pages = getSeriesPages(soup)
        print('got pages')
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
run()


cur.execute('SELECT * FROM bookQ') 
count = len(cur.fetchall())
if count > 100:
    cur.execute('DELETE FROM bookQ;')
else: 
    pass

con.commit()
con.close()