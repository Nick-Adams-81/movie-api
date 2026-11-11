from flask import Flask, send_file, jsonify, request, g
import sqlite3

DATABASE = "books.db"

app = Flask(__name__)

def get_db():
    if "db" not in g:
        print("Opening new db connection")
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        print("Closing db connection")
        db.close()

@app.get("/")
def hello():
    conn = get_db()
    return jsonify({ "message": "Books.api" })

@app.get("/books")
def list_books():
    db = get_db()
    cursor = db.execute("SELECT * from books")
    rows = cursor.fetchall()
    books = [dict(row) for row in rows]
    return jsonify(books)

@app.get("/books/<int:book_id>")
def get_book(book_id):
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id, )
    )
    row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "book not found"}), 404
    return jsonify(dict(row))

@app.get("/books/<int:book_id>/full")
def get_book_with_author(book_id):
    db = get_db()
    cursor = db.execute(
        """
        SELECT 
          books.id AS book_id, 
          books.title, 
          books.year,
          authors.id AS author_id,
          authors.name AS author_name
        FROM books
        INNER JOIN authors
          ON books.author_id = authors.id
        WHERE books.id = ?
        """,
        (book_id, ),
    )
    row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "book not found"}), 404

    data = {
        "id": row["book_id"],
        "title": row["title"],
        "year": row["year"],
        "author": {
            "id": row["author_id"],
            "name": row["author_name"]
        }
    }
    return jsonify(data)

@app.post("/books")
def create_book():
    db = get_db()
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    title = data.get("title")
    year = data.get("year")
    author_id = data.get("author_id")

    missing_fields = []
    if not title:
        missing_fields.append("title")
    if year is None:
        missing_fields.append("year")
    if author_id is None:
        missing_fields.append("author_id")

    if missing_fields:
        return(
            jsonify({"error": "Missing required fields", "fields": missing_fields}), 400
        )
    
    for field in ("title", "year", "author_id"):
        if field not in data:
            return {"error": f"{field} is required"}, 400
    
    try:
        year = int(data["year"])
        author_id = int(data["author_id"])
    except (TypeError, ValueError):
        return {"error": "year and author_id must be integers"}, 400
    
    try:
        cursor = db.execute(
        "INSERT INTO books(title, year, author_id) VALUES (?, ?, ?)",
        (title, year, author_id)
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Book already exists"}), 409

    new_id = cursor.lastrowid

    created_book = {
        "id": new_id,
        "title": title,
        "year": year,
        "author_id": author_id
    }

    return jsonify(created_book), 201

@app.patch("/books/<int:book_id>")
def update_book(book_id):
    db = get_db()
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "Request must be JSON"}), 400
    new_title = data["title"]
    if not new_title:
        return jsonify({"error": "Field title is required"}), 400

    cursor = db.execute(
        "UPDATE books SET title = ? WHERE id = ?",
        (new_title, book_id)
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"Error": "Book ot found"}), 404
    
    updated_book = {
        "id": book_id,
        "title": new_title
    }

    return jsonify(updated_book), 200


@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM books WHERE id = ?",
        (book_id,)
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Book not found"}), 404
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)