
from flask import request, jsonify
from . import db
from .models import Book
from flask import current_app as app

@app.route('/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=10, type=int)
    cursor = request.args.get('cursor', default=0, type=int)

    query = Book.query.filter(Book.id > cursor).order_by(Book.id).limit(limit)
    books = query.all()
    next_cursor = books[-1].id if books else None

    return jsonify({
        'books': [{'id': b.id, 'title': b.title, 'author': b.author} for b in books],
        'next_cursor': next_cursor
    })

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'author')):
        return jsonify({'error': 'Invalid data'}), 400
    book = Book(title=data['title'], author=data['author'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author}), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})
