import sqlite3

def main():
    conn = sqlite3.connect("books.db")
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            books.id,
            books.title,
            books.year,
            authors.name AS author
        FROM books
        INNER JOIN authors
            ON books.author_id = authors.id
        ORDER BY books.id
        """
        )

        print("Access by column name:")
        for row in cursor:
            book = dict(row)
            print(book)

    finally:
        conn.close()

if __name__ == "__main__":
    main()