from sqlmodel import SQLModel
import uuid
from datetime import datetime


class BookBase(SQLModel):
    """Shared properties across schemas"""
    title: str 
    author: str
    publisher: str 
    published_date: datetime
    page_count: int 
    language: str


class BookCreate(BookBase):
    """Properties to receive on creation"""
    pass


class BookUpdate(SQLModel):
    """Properties to receive on update (all optional)"""
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    published_date: str | None = None
    page_count: int | None = None
    language: str | None = None


class Book(BookBase):
    """Properties to return to client (includes DB fields)"""
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime