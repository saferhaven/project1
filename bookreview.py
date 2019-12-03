import requests
import csv
import os
import datetime

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/home")
def index():
    now = datetime.datetime.now()
    code_day = now.month == 9 and now.day == 23
    return render_template("index.html", code_day=code_day, now_month=now.month,now_day=now.day)


@app.route("/api/<string: isbn>", methods=["GET","POST"])
def book():
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "yNiykXNjv4cHILH6W9FnQ", "isbns": ":isbn"})
    r = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if res.status_code != 200:
        raise Exception("Error: API request unsuccesful")
    data = res.json()
    return render_template("book.html",data = data)
