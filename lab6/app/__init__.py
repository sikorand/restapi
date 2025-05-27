from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from app.routes import BookListResource, BookResource

books = []

def create_app():
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app)

    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')

    return app
