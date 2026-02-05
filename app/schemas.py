from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated




###################################

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class User(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes=True


##################################

class UserLogin(BaseModel):
    email:EmailStr
    password:str




class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[int]=None



##############################



class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:User


    class Config:
        from_attributes=True


class PostInfo(BaseModel):
    Post:Post
    votes:int

    class Config:
        from_attributes=True


###########################


class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(le=1, ge=-1)]