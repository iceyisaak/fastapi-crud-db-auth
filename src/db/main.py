from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from src.config import Config


async_engine=AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
))


async def init_db():
    async with async_engine.begin() as conn:
        from src.api.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables created successfully.")


# Session dependency for FastAPI
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session