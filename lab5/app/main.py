from fastapi import FastAPI, HTTPException
from app.models import BookModel
from app import crud

app = FastAPI()

@app.post("/books/")
async def add_book(book: BookModel):
    book_dict = book.dict(by_alias=True)
    book_dict.pop("_id", None)
    new_id = await crud.create_book(book_dict)
    return {"id": new_id}

@app.get("/books/")
async def list_books():
    books = await crud.get_all_books()
    return books

@app.get("/books/{book_id}")
async def get_book(book_id: str):
    book = await crud.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}")
async def remove_book(book_id: str):
    deleted = await crud.delete_book(book_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "deleted"}
