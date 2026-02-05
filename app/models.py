from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default='true',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password: Mapped[str]=mapped_column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))