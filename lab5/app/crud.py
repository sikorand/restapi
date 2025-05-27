from pydantic_mongo import PydanticObjectId
from app.database import books_collection
from app.models import BookModel

async def create_book(book_data: dict):
    result = await books_collection.insert_one(book_data)
    return str(result.inserted_id)

async def get_all_books():
    books = await books_collection.find().to_list(length=100)
    return books

async def get_book_by_id(book_id: str):
    return await books_collection.find_one({"_id": PydanticObjectId(book_id)})

async def delete_book(book_id: str):
    result = await books_collection.delete_one({"_id": PydanticObjectId(book_id)})
    return result.deleted_count
