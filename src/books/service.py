from sqlmodel.ext.asyncio.session import AsyncSession
from . import schemas, models
from sqlmodel import select,desc
import uuid


class Book:

    async def get_all_books(self,session:AsyncSession):
        statement=select(models.Book).order_by(desc(models.Book.created_at))
        result=await session.exec(statement)
        all_books=result.all()
        return all_books

    async def get_single_book(self,uid:uuid.UUID,session:AsyncSession):
        statement=select(models.Book).where(models.Book.uid==uid)
        result=await session.exec(statement)
        single_book=result.first()
        return single_book

    async def create_book(self,book:schemas.BookCreate,session:AsyncSession):
        book_detail=book.model_dump()
        created_book=models.Book(
            **book_detail
        )
        session.add(created_book)
        await session.commit()
        await session.refresh(created_book)
        return created_book

    async def update_book(self,uid:uuid.UUID,book:schemas.BookUpdate,session:AsyncSession):
        updated_book=await self.get_single_book(uid,session)
        if updated_book is not None:
            book_detail=book.model_dump(exclude_unset=True)
            for key,value in book_detail.items():
                setattr(updated_book,key,value)
            await session.commit()
            await session.refresh(updated_book)
            return updated_book
        else:
            return None
        
    async def delete_book(self,uid:uuid.UUID,session:AsyncSession):
        deleted_book=await self.get_single_book(uid,session)
        if deleted_book is not None:
            await session.delete(deleted_book)
            await session.commit()
            return True
        else:
            return None