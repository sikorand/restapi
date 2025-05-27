
from fastapi import FastAPI, HTTPException
from models import Book

app = FastAPI()

books = []

@app.get("/books")
async def get_books():
    return books

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books")
async def add_book(book: Book):
    books.append(book.dict())
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
