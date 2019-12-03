import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#engine = create_engine("postgres://nxvgwaqdvfzzyv:c4874689c45894b3823233f5340cd67225042c165ff628c5b22b80e9214ced3c@ec2-174-129-227-205.compute-1.amazonaws.com:5432/d7nuinbqb0dp2j")
engine = create_engine("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))

def main():
    p = open("books.csv")
    reader = csv.reader(p)
    for isbn, title, author, year in reader:
        if db.execute("SELECT * FROM books WHERE isbn = :isbn",
        {"isbn": isbn}).rowcount == 0:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added book: {title}")
        else:
            print(f"Book {title} already exists.")

    db.commit()

if __name__ == "__main__":
    main()
