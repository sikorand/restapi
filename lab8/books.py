from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from tokens import decode_token
from models import Book
from limiter import rate_limiter

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

books_db = [
    Book(id=1, title="Book 1", author="Author A"),
    Book(id=2, title="Book 2", author="Author B"),
]

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("sub")

@router.get("/books", dependencies=[Depends(rate_limiter("10"))])
def get_books(user: str = Depends(get_current_user)):
    return books_db

@router.get("/public-books", dependencies=[Depends(rate_limiter("2"))])
def get_public_books():
    return books_db
