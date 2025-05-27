from flask import request, jsonify
from flask_restful import Resource
from app.schemas import BookSchema
from flasgger import swag_from

books = []
book_schema = BookSchema()

class BookListResource(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Список всіх книг',
                'examples': {
                    'application/json': [
                        {'id': 1, 'title': '1984', 'author': 'George Orwell'}
                    ]
                }
            }
        }
    })
    def get(self):
        return books, 200

    @swag_from({
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': BookSchema.schema()
            }
        ],
        'responses': {
            201: {
                'description': 'Книга додана'
            },
            400: {
                'description': 'Помилка валідації'
            }
        }
    })
    def post(self):
        json_data = request.get_json()
        errors = book_schema.validate(json_data)
        if errors:
            return {"message": "Validation failed", "errors": errors}, 400
        json_data['id'] = len(books) + 1
        books.append(json_data)
        return json_data, 201

class BookResource(Resource):
    @swag_from({
        'responses': {
            200: {'description': 'Книга знайдена'},
            404: {'description': 'Книгу не знайдено'}
        }
    })
    def get(self, book_id):
        for book in books:
            if book['id'] == book_id:
                return book, 200
        return {'message': 'Book not found'}, 404

    @swag_from({
        'responses': {
            200: {'description': 'Книга видалена'},
            404: {'description': 'Книгу не знайдено'}
        }
    })
    def delete(self, book_id):
        global books
        books = [book for book in books if book['id'] != book_id]
        return {'message': 'Book deleted (if existed)'}, 200
