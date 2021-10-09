from flask import Flask, render_template, request, redirect, url_for

from json_engine import add_book, get_books, get_book_with_id, delete_book

app = Flask(__name__)


@app.route('/')
@app.route('/booksApi', methods=['GET', 'POST'])
def book_function():
    if request.method == 'GET':
        return get_books()
    elif request.method == 'POST':
        title = request.args.get('title', '')
        author = request.args.get('author', '')
        genre = request.args.get('genre', '')
        return add_book(title, author, genre)


@app.route('/bookApi/<int:book_id>', methods=['GET', 'DELETE'])
def book_function_id(book_id):
    if request.method == "GET":
        return get_book_with_id(book_id)
    elif request.method == "DELETE":
        return delete_book(book_id)


if __name__ == '__main__':
    app.debug = True
    app.run()
