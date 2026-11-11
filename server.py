# mongodb+srv://thebigdeal916:Theking1#40@cluster0.jdpn8ie.mongodb.net/
from pymongo import MongoClient

uri = "mongodb+srv://thebigdeal916:Theking1%40@cluster0.jdpn8ie.mongodb.net/"
client = MongoClient(uri)

db = client["movies_db"]
movies = db["movies"]

# movie = {
#     "title": "Inception",
#     "year": 2010,
#     "rating": 4.8
# }

# INSERT MOVIE
# result = movies.insert_one(movie)
# print("Inserted _id:", result.inserted_id)

# FIND ONE MOVIE BY FIELD
cursor = movies.find({"title": "Inception"})

for doc in cursor:
    print(doc)

# UPDATE MOVIE BY FIELD
update_result = movies.update_one(
    {"title": "Inception"},
    {"$set": {"rating": 9.0}}
)

print(f"Mathed: {update_result.matched_count}")
print(f"Modified: {update_result.modified_count}")

cursor2 = movies.find({"title": "Inception"})

for doc in cursor2:
    print(doc)

# DELETE BY FIELD
delete_result = movies.delete_one({"title": "Inception"})
print(f"Deleted count: {delete_result.deleted_count}")

cursor3 = movies.find({"title": "Inception"})
for doc in cursor3:
    print("Still in db:", doc)

CREATE TABLE movies (
  id            INT PRIMARY KEY,
  title         VARCHAR(255) NOT NULL,
  genre         VARCHAR(100),
  release_year  INT,
  average_rating DECIMAL(3,2)  -- e.g. 8.75
);

CREATE TABLE actors (
  id    INT PRIMARY KEY,
  name  VARCHAR(255) NOT NULL
);

CREATE TABLE movie_cast (
  id        INT PRIMARY KEY,
  movie_id  INT NOT NULL,
  actor_id  INT NOT NULL,
  role      VARCHAR(255),

  FOREIGN KEY (movie_id) REFERENCES movies(id),
  FOREIGN KEY (actor_id) REFERENCES actors(id)
);

CREATE TABLE reviews (
  id             INT PRIMARY KEY,
  score          DECIMAL(3,1) NOT NULL,      -- e.g. 8.5
  short_comment  VARCHAR(500),
  reviewer_name  VARCHAR(255),
  submission_date DATE,
  movie_id       INT NOT NULL,
  FOREIGN KEY (movie_id) REFERENCES movies(id)
);

{
  "_id": 1,
  "title": "some movie",
  "genre": "fiction",
  "avg_rating": 8.6,
  "review_count": 12,
  "cast": [
    { "actor_name": "John Doe", "role": "Lead" },
    { "actor_name": "Jane Doe", "role": "supporting" }
  ]
}

{
  "_id": 100,
  "movie_id": 1,
  "score": 7.9,
  "short_comment": "Decent",
  "reviewer_name": "Nick",
  "submission_date": "2026-10-25"
}