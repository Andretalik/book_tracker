from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/book_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Book_User_Link_Table(db.Model):
    """Store linking IDs for books and users."""

    __tablename__ = "book_user_link"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))

    books = db.relationship("Book")
    users = db.relationship("User")


class Book(db.Model):
    """Store the Book details."""
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    reading = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)


class User(db.Model):
    """Store User details."""
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    books = db.relationship("Book",
                            secondary="book_user_link", lazy="dynamic")
