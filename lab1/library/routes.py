
from flask import Blueprint, jsonify, request
from .schema import BookSchema

bp = Blueprint('library', __name__)

books = []

@bp.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    schema = BookSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    books.append(data)
    return jsonify(data), 201

@bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({'message': 'Book deleted'}), 200
    return jsonify({'error': 'Book not found'}), 404
