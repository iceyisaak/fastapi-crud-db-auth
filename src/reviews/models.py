from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from ..auth import models
from typing import Optional
import uuid


class Review(SQLModel, table=True):
    __tablename__= "reviews" # type: ignore[assignment]
    uid:uuid.UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating:int=Field(lt=5)
    review_text:str
    user_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="users.uid")
    book_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="books.uid")
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now))
    user:Optional["models.User"]=Relationship(back_populates="books")


    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"