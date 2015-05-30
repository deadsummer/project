import sqlite3
conn=sqlite3.connect("mydb.s3db")
cur=conn.cursor()
cur.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, author TEXT, title TEXT);")