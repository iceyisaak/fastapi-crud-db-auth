from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class Session(SQLModel, table=True):
    __tablename__ = "sessions"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    user_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, index=True)
    )
    access_jti: str = Field(index=True, unique=True, nullable=False)
    refresh_jti: str = Field(index=True, unique=True, nullable=False)
    access_token: str = Field(nullable=False)
    refresh_token: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now)
    )
    expires_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False)
    )

    def __repr__(self):
        return f"<Session {self.access_jti}>"