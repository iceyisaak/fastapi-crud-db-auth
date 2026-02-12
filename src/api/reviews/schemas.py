from pydantic import BaseModel, Field, ConfigDict
import uuid
from typing import Optional
from datetime import datetime



class Review(BaseModel):
    uid:uuid.UUID
    rating:int=Field(lt=5)
    review_text:str
    user_uid:Optional[uuid.UUID]
    book_uid:Optional[uuid.UUID]
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    rating:int=Field(lt=5)
    review_text:str