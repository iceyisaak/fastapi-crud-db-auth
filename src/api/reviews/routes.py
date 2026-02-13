from fastapi import APIRouter,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import Any, TYPE_CHECKING
import uuid


# Only import for type checking
# if TYPE_CHECKING:
from . import schemas,services
from ..auth import dependencies as auth_dependencies


router = APIRouter()
review_service=services.Review()

@router.post("/book/{book_uid}")
async def add_review(
    book_uid:uuid.UUID,
    review_data:schemas.ReviewCreate,
    current_user:Any=Depends(auth_dependencies.get_current_user),
    session:AsyncSession=Depends(get_session)
):
    new_review=await review_service.add_review(
        user_email=current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session
    )
    return new_review
