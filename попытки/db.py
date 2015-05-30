import sqlite3
conn=sqlite3.connect("mydb.s3db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, author TEXT, title TEXT);")
cur.execute("INSERT INTO books(author,title) VALUES(?,?)",['someauthor','sometitle'])
print(cur.execute("SELECT * FROM books").fetchall())
#ИЛИ 
print(cur.execute("SELECT * FROM books").fetchoneg())