from concurrent.futures.process import BrokenProcessPool
import disnake




def new_books(books):
    new_books = disnake.Embed(
    title="New Books:",
    type="rich"
    )
    for book in books:
        new_books.add_field(book[0],f'{book[2]} | Release: {book[4]}',inline=False)
    return new_books

def upcomming_books(books):
    upc_books = disnake.Embed(
    title="Upcomming Books:",
    type="rich"
    )
    for book in books:
        upc_books.add_field(book[0],f'{book[1]} | Release: {book[3]}',inline=False)
    return upc_books




#new_books.add_field("test-field","New Book Title Here?\n test",inline=True)
#new_books.add_field("test-field","New Book Title Here?",inline=False)