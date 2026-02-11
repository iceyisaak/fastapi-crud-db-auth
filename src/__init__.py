from fastapi import FastAPI
from .books import books_router
from .auth import auth_router
from .reviews import reviews_router
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting up...")
    await init_db()
    yield {}
    print(f"Server is shutting down...")

version="v1"

app=FastAPI(
    title="bookly",
    description="A simple book management API.",
    version=version,
    # lifespan=life_span(app) # Uncomment this line to use the lifespan context manager.
)

baseURL=f"/api/{version}"

app.include_router(books_router, prefix=f"{baseURL}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"{baseURL}/auth", tags=["Auth"])
app.include_router(reviews_router, prefix=f"{baseURL}/reviews", tags=["Reviews"])


# Rebuild schemas after all routers are imported to resolve forward references
from src.auth.schemas import UserBooks
from src.books.schemas import Book, BookDetail
from src.reviews.schemas import Review

UserBooks.model_rebuild()
Book.model_rebuild()
BookDetail.model_rebuild()
Review.model_rebuild()
