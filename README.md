# Book Tracker API
This is the book tracker API for the assessment.

This API can be consumed using Postman.

Allowing a user to register, login, add books and mark them as completed.
It's super easy to setup.

## Setting up the API
  - Start by setting up your environment:
    - Clone this repo.
    - Create your virtualenv.
    - Pip install the requirements.

## Running the API
To run the API, you need a few environment variables to the set, and don't forget to activate your virtualenv.
Here is an example of the environment variables:
  ```
  export FLASK_ENV=development
  export FLASK_APP=main.py

  SECRET=Lookatthissuperlingsecretkey
  ```

You can set the FLASK_ENV to what is in the example, or to production if you want to.
The SECRET is what shall be used for authentication so be sure to change that.

Once all the above is done simply running `flask run` will run the API.


## Using the API
The API has a few endpoint up and ready for use.
All parameter are to be provided in JSON format.

| Method | Endpoint | Description | Parameters | Output |
| ----- | ------ | ------ | ------ | ------ |
| GET | "/" | Home | N/A | The home page |
| POST | "/register" | Register a User | username and password | Confirmation of registration |
| POST | "/login" | Login a User | username and password | Confirmation of login and token |
| POST | "/book/add" | Add Book | Book name and description | Confirmation of registration of book |
| POST | "/user/link/book" | Add book to Users' list of books | Book name | Confirmation of link |
| GET | "/user/books" | View all books linked to User | N/A | List of all books, read or unread |
| POST | "/user/books/update" | Update on status of book if completed | Book name and status | Confirmation if success |
| GET | "/books" | View all Books in system | N/A | List of all books in system  |
