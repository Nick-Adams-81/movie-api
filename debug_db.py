import sqlite3
import os

print("CWD:", os.getcwd())
print("Exists books.db:", os.path.exists("books.db"))

conn = sqlite3.connect("books.db")
print("Opened:", conn)

cur = conn.cursor()

print("Tables:")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print("  ", row)

print("\nTrying SELECT from books:")
try:
    cur.execute("SELECT COUNT(*) FROM books;")
    print("Books count:", cur.fetchone()[0])
except Exception as e:
    print("ERROR:", repr(e))

conn.close()