from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional
import uuid

class Book(SQLModel, table=True):
    __tablename__= "books" # type: ignore[assignment]
    uid:uuid.UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title:str 
    author:str
    publisher:str 
    published_date:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    page_count:int 
    language:str 
    user_uid:Optional[uuid.UUID]=Field(default=None,foreign_key="users.uid")
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now))


    def __repr__(self):
        return f"<Book {self.title}>"