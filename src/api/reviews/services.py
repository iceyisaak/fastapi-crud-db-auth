from . import models,services, schemas
# from ..books import services as books_services
# from ..auth import services as auth_services
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
import uuid
import logging




class Review:

    @staticmethod
    async def add_review(user_email:str,book_uid:uuid.UUID,review_data:schemas.ReviewCreate,session:AsyncSession):
        from ..books import services as books_services
        from ..auth import services as auth_services
        books_service = books_services.Book()
        auth_service=auth_services.User()


        try:
            book=await books_service.get_single_book(
                uid=book_uid,
                session=session
            )
            user=await auth_service.get_user_by_email(
                email=user_email,
                session=session
            )
            new_review_data= review_data.model_dump()
            new_review=models.Review(
                **new_review_data
            )

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )


            new_review.user=user    # type: ignore
            new_review.book=book    # type: ignore
            session.add(new_review)
            await session.commit()

            return new_review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong"
            )