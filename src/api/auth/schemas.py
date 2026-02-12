from pydantic import BaseModel,Field
from ..books import schemas
import uuid
from typing import List, TYPE_CHECKING
from datetime import datetime
from pydantic import ConfigDict

if TYPE_CHECKING:
    from ..books.schemas import Book
    from ..reviews.schemas import Review

class UserCreate(BaseModel):
    first_name:str=Field(max_length=50)
    last_name:str=Field(max_length=50)
    username:str=Field(max_length=8)
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)


class User(BaseModel):
    uid:uuid.UUID
    username: str
    email: str
    first_name: str 
    last_name: str
    role:str
    is_verified: bool 
    password_hash:str=Field(exclude=True)
    created_at:datetime
    updated_at:datetime


class UserBooks(User): 
    books:List["Book"]
    reviews:List["Review"]

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email:str=Field(max_length=40)
    password:str=Field(min_length=6)


