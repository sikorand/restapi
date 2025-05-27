from fastapi import FastAPI
from auth import router as auth_router
from books import router as books_router
from limiter import init_redis

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_redis()

app.include_router(auth_router)
app.include_router(books_router)
