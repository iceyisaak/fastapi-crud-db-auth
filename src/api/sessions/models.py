from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
import uuid
from datetime import datetime


class Session(SQLModel, table=True):
    __tablename__ = "sessions"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    user_uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, index=True)
    )
    access_jti: str = Field(
        sa_column=Column(pg.VARCHAR(255), unique=True, nullable=False, index=True)
    )
    refresh_jti: str = Field(
        sa_column=Column(pg.VARCHAR(255), unique=True, nullable=False, index=True)
    )
    access_token: str = Field(
        sa_column=Column(pg.TEXT, nullable=False)
    )
    refresh_token: str = Field(
        sa_column=Column(pg.TEXT, nullable=False)
    )
    is_active: bool = Field(
        sa_column=Column(
            pg.BOOLEAN, 
            nullable=False, 
            server_default='true',
            index=True  # Index in Column, not Field
        )
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), 
            nullable=False,
            server_default=func.now()
        )
    )
    expires_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), 
            nullable=False,
            index=True  # Index in Column, not Field
        )
    )

    def __repr__(self):
        return f"<Session {self.access_jti}>"