from my_db.db import open_conn
"""author
authors
book
bookq
narrator
narrators
series
seriesauthors
seriescount"""
tables = ["seriescount","seriesauthors","series","narrators","narrator","bookq","book","authors","author"]
con, cur = open_conn()


for table in tables: 
    cur.execute(f'TRUNCATE `{table}`')

print("### TRUNCATED ###")
con.commit()
con.close()
