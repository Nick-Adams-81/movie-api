import sqlite3

def execute_cursor(sql, data):
    result = cursor.execute(sql, data)
    return result

# input boook title to find
title = input("Book title: ")

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# SQL query to get data based on user inputted title(parameterized query)
sql = "SELECT id, title, year FROM books WHERE title = ?"
print("Running sql")
print(sql)

execute_cursor(sql, (title,))
rows = cursor.fetchall()

for row in rows:
    print(row)

# post new data
insert_sql = "INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)"
# execute_cursor(insert_sql, ("Test Book", 2026, 1))

# update existing data
update_sql = "UPDATE books SET year = ? WHERE title = ?"
execute_cursor(update_sql, (2030, "Test Book"))


conn.commit()
conn.close()