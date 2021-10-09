from flask import jsonify, json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Book, Base


# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_book(title, author, genre):
    new_book = Book(title=title, author=author, genre=genre)
    session.add(new_book)
    session.commit()
    return jsonify(Book=new_book.serialize)


def get_books():
    books = session.query(Book).all()
    return jsonify(books=[b.serialize for b in books])


def get_book_with_id(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book.serialize)


def delete_book(book_id):
    delete_book_id = session.query(Book).filter_by(id=book_id).one()
    session.delete(delete_book_id)
    session.commit()
    return 'Removed Book with id %s\n' % book_id
