from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
# from ..books import models
# from ..reviews import models as reviews_models
from typing import List, TYPE_CHECKING
import uuid
from datetime import datetime


if TYPE_CHECKING:
    from ..reviews.models import Review
    from ..books.models import Book


class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore
    uid:uuid.UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    first_name: str 
    last_name: str
    role: str=Field(sa_column=Column(pg.VARCHAR,nullable=False,server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash:str=Field(exclude=True)
    created_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now))
    updated_at:datetime=Field(sa_column=Column(pg.TIMESTAMP(timezone=True),default=datetime.now))
    books:List["Book"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})
    reviews:List["Review"]=Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})



def __repr__(self):
    return f"<User {self.username}>"