from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/book_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


book_to_user_relationship_table = db.Table(
    book_id=db.Column(db.Integer, db.ForeignKey("books.id")),
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"))
)


class Book(db.Model):
    """Store the Book details."""

    table_name = "books"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean)


class User(db.Model):
    """Store User details."""

    table_name = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)

    books = db.relationship("Book",
                            secondary="book_to_user_relationship_table")
