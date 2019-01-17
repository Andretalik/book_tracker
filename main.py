import jwt
import os
import datetime
from flask import request
from models import app, User, Book, Book_User_Link_Table, db
from helpers import (response_builder, identity, decode_auth_token,
                     token_required)

@app.route("/")
def hello():
    """Home Page."""
    return "Welcome to the Book Tracker"


@app.route("/register", methods=["POST"])
def register():
    """Register a new User in the application."""
    payload = request.get_json(silent=True)

    if not payload:
        return response_builder({
            "message": "Full credentials have not been provided.",
            "status": "fail"
            }, 400)

    if payload.get('username') and payload.get('password'):
        identity_details = identity(payload)

        if not identity_details[1]:
            return response_builder({
                "message": "User already exists. Please login.",
                "status": "fail"
                }, 403)
        else:
            new_user = User(
                name=identity_details[0],
                password=identity_details[1]
            )
            db.session.add(new_user)
            db.session.commit()
            return response_builder({
                "message": "User registration successful.",
                "user_id": str(new_user.id),
                "status": "success"
                })
    else:
        return response_builder({
            "message": "Full credentials have not been provided.",
            "status": "fail"
            }, 400)


@app.route("/login", methods=["POST"])
def login():
    """Login existing users."""
    payload = request.get_json(silent=True)

    identity_details = identity(payload)

    if identity_details:
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': identity_details
            }
            token = jwt.encode(payload, os.environ['SECRET'],
                               algorithm='HS256')
            return response_builder({
                "message": "Login successful.",
                "status": "success",
                "token": str(token)
                }, 200)
        except Exception as e:
            return response_builder({
                "message": "Username and password are incorrect.",
                "status": "fail",
                "error": str(e)
                }, 400)
    else:
        return response_builder({
            "message": "Username and password are incorrect.",
            "status": "fail"
            }, 400)


@app.route("/book/add", methods=["POST"])
@token_required
def add_book():
    """Add book to system."""
    payload = request.get_json(silent=True)

    if not payload:
        return response_builder({
            "message": "Full details have not been provided.",
            "status": "fail"
            }, 400)

    if payload.get('name') and payload.get('description'):
        book = Book.query.filter_by(name=payload.get("name")).first()

        if book:
            return response_builder({
                "message": "Book already exists.",
                "status": "fail"
                }, 403)
        else:
            new_book = Book(
                name=payload.get('name'),
                description=payload.get('description')
            )
            db.session.add(new_book)
            db.session.commit()
            return response_builder({
                "message": "Book registration successful.",
                "status": "success"
                })
    else:
        return response_builder({
            "message": "Full details have not been provided.",
            "status": "fail"
            }, 400)


@token_required
@app.route("/user/link/book", methods=["POST"])
def link_book_user():
    """Link book to user reading it."""
    payload = request.get_json(silent=True)

    if not payload:
        return response_builder({
            "message": "Full details have not been provided.",
            "status": "fail"
            }, 400)

    if payload.get('name'):
        book = Book.query.filter_by(name=payload.get("name")).first()

        if not book:
            return response_builder({
                "message": "Book doesn't exist. Please register it.",
                "status": "fail"
                }, 403)

        user_id = decode_auth_token(request.headers.get('Authorisation'))
        user = User.query.filter_by(id=user_id).first()

        linked_books = Book_User_Link_Table.query.filter_by(book_id=book.id).all()
        for book in linked_books:
            if book.user_id == user.id:
                return response_builder({
                    "message": "Book has already been linked to user.",
                    "status": "fail"
                    }, 403)

        book_user_link = Book_User_Link_Table(
            book_id=book.id,
            user_id=user.id
        )
        user.books.append(book)
        db.session.add(book_user_link)
        db.session.commit()
        return response_builder({
            "message": "Link of {} to User {} successful.".format(book.name,
                                                                  user.name),
            "status": "success"
            })


    else:
        return response_builder({
            "message": "Book name must be provided.",
            "status": "fail"
            }, 403)

@token_required
@app.route("/user/books", methods=["GET"])
def view_linked_books():
    """View books linked to user."""
    payload = request.get_json(silent=True)

    if not payload:
        return response_builder({
            "message": "Full details have not been provided.",
            "status": "fail"
            }, 400)

    user_id = decode_auth_token(request.headers.get('Authorisation'))
    user = User.query.filter_by(id=user_id).first()

    if len([q for q in user.books]) == 0:
        return response_builder({
            "message": "User has no books linked",
            "status": "success"
            }, 200)

    list_books = []
    read_books = []
    for book in user.books:
        list_books.append({
            "book_name": book.name,
            "book_description": book.description
        })
        if book.completed:
            read_books.append({
                "book_name": book.name,
                "book_description": book.description
            })

    return response_builder({
        "books": list_books,
        "read_books": read_books,
        "status": "success"
        }, 200)

@token_required
@app.route("/user/books/update", methods=["POST"])
def update_completed_books():
    """Update books linked to user if completed or not."""
    payload = request.get_json(silent=True)

    if not payload:
        return response_builder({
            "message": "Full details have not been provided.",
            "status": "fail"
            }, 400)

    if payload.get("book_name") and payload.get("completed"):
        book = Book.query.filter_by(name=payload.get("book_name")).first()

        if not book:
            return response_builder({
                "message": "Book doesn't exist. Please register it.",
                "status": "fail"
                }, 403)

        user_id = decode_auth_token(request.headers.get('Authorisation'))
        user = User.query.filter_by(id=user_id).first()

        linked_books = Book_User_Link_Table.query.filter_by(book_id=book.id).all()
        for update_book in linked_books:
            if update_book.user_id == user.id:
                update_book.completed = True
                continue

        return response_builder({
            "message": "Book {} has been marked as completed.".format(book.name),
            "status": "success"
            }, 200)


    else:
        return response_builder({
            "message": "Name of completed book must be provided.",
            "status": "fail"
            }, 403)

@app.route("/books", methods=["GET"])
def view_books():
    books = Book.query.all()
    list_books = []

    if not books:
        return response_builder({
            "books": list_books,
            "message": "No books in the system currently.",
            "status": "success"
            }, 200)

    for book in books:
        list_books.append({
            "book_name": book.name,
            "book_description": book.description
        })
    return response_builder({
        "books": list_books,
        "status": "success"
        }, 200)
