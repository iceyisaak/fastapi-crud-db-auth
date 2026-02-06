from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from src.config import Config
from sqlalchemy.orm import sessionmaker


async_engine=AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
))


async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables created successfully.")


# Session dependency for FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session