from fastapi import APIRouter, status, HTTPException,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from . import schemas,service
from src.db.main import get_session
import uuid


# app=FastAPI()
router=APIRouter()
# book_service = service.Book()



@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.Book])
async def get_all_books(session:AsyncSession=Depends(get_session)):
    all_books=await service.Book().get_all_books(session=session)
    return all_books


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Book)
async def create_book(book:schemas.BookCreate,session:AsyncSession=Depends(get_session)):
    # new_book=book.model_dump()
    # books.append(new_book)
    created_book=await service.Book().create_book(book,session)
    return created_book



@router.get("/{uid}",status_code=status.HTTP_200_OK,response_model=schemas.Book)
async def get_single_book(uid:uuid.UUID,session:AsyncSession=Depends(get_session)):
    single_book=await service.Book().get_single_book(uid,session)
    if single_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with id {uid} not found."
        )
    return single_book

@router.patch("/{uid}",status_code=status.HTTP_200_OK,response_model=schemas.Book)
async def update_book(uid:uuid.UUID,book_detail:schemas.BookUpdate,session:AsyncSession=Depends(get_session)):
    updated_book=await service.Book().update_book(uid,book_detail,session)
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with uid {uid} not found"
        )
    return updated_book


@router.delete("/{uid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(uid:uuid.UUID,session:AsyncSession=Depends(get_session)):
    deleted_book=await service.Book().delete_book(uid,session)
    if deleted_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {uid} not found"
    )

