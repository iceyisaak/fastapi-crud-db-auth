from fastapi import FastAPI
from .books import books_router
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
    lifespan=life_span
)

baseURL=f"/api/{version}"

app.include_router(books_router, prefix=f"{baseURL}/books", tags=["Books"])
