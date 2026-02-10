from fastapi import APIRouter, status, HTTPException,Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from . import schemas,services
from ..auth import dependencies
from src.db.main import get_session
import uuid



router=APIRouter()
book_service=services.Book()
access_token_bearer = dependencies.AccessTokenBearer()
role_checker=Depends(dependencies.RoleChecker(["admin","user"]))


@router.get(
        "/",
        status_code=status.HTTP_200_OK, 
        response_model=List[schemas.Book],
        dependencies=[role_checker]
    )
async def get_all_books(
    session:AsyncSession=Depends(get_session),
    user_details=Depends(access_token_bearer),
):  
    print(user_details)
    all_books=await book_service.get_all_books(session=session)
    return all_books


@router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=schemas.Book,
        dependencies=[role_checker]
    )
async def create_book(
    book:schemas.BookCreate,
    session:AsyncSession=Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    # new_book=book.model_dump()
    # books.append(new_book)
    created_book=await services.Book().create_book(book,session)
    return created_book



@router.get(
        "/{uid}",
        status_code=status.HTTP_200_OK,
        response_model=schemas.Book,
        dependencies=[role_checker]
    )
async def get_single_book(
    uid:uuid.UUID,
    session:AsyncSession=Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    single_book=await services.Book().get_single_book(uid,session)
    if single_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with id {uid} not found."
        )
    return single_book


@router.patch(
        "/{uid}",
        status_code=status.HTTP_200_OK,
        response_model=schemas.Book,
        dependencies=[role_checker]
    )
async def update_book(
    uid:uuid.UUID,
    book_detail:schemas.BookUpdate,
    session:AsyncSession=Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    updated_book=await services.Book().update_book(uid,book_detail,session)
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with uid {uid} not found"
        )
    return updated_book


@router.delete(
        "/{uid}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[role_checker]
    )
async def delete_book(
    uid:uuid.UUID,
    session:AsyncSession=Depends(get_session),
    user_details=Depends(access_token_bearer)
):
    deleted_book=await services.Book().delete_book(uid,session)
    if deleted_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {uid} not found"
    )

