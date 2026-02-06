from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List


books=[
        {
            "id": 1,
            "title": "Project Hail Mary",
            "author": "Andy Weir",
            "publisher": "Ballantine Books",
            "published_date": "2021-05-04",
            "page_count": 476,
            "language": "en"
        },
        {
            "id": 2,
            "title": "The Silent Patient",
            "author": "Alex Michaelides",
            "publisher": "Celadon Books",
            "published_date": "2019-02-05",
            "page_count": 336,
            "language": "en"
        },
        {
            "id": 3,
            "title": "Cien años de soledad",
            "author": "Gabriel García Márquez",
            "publisher": "Editorial Sudamericana",
            "published_date": "1967-05-30",
            "page_count": 417,
            "language": "es"
        },
        {
            "id": 4,
            "title": "Atomic Habits",
            "author": "James Clear",
            "publisher": "Avery",
            "published_date": "2018-10-16",
            "page_count": 320,
            "language": "en"
        },
        {
            "id": 5,
            "title": "The Seven Husbands of Evelyn Hugo",
            "author": "Taylor Jenkins Reid",
            "publisher": "Atria Books",
            "published_date": "2017-06-13",
            "page_count": 389,
            "language": "en"
        },
        {
            "id": 6,
            "title": "Le Petit Prince",
            "author": "Antoine de Saint-Exupéry",
            "publisher": "Reynal & Hitchcock",
            "published_date": "1943-04-06",
            "page_count": 96,
            "language": "fr"
        },
        {
            "id": 7,
            "title": "Dune",
            "author": "Frank Herbert",
            "publisher": "Chilton Books",
            "published_date": "1965-08-01",
            "page_count": 412,
            "language": "en"
        },
        {
            "id": 8,
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "publisher": "Chatto & Windus",
            "published_date": "1932-01-01",
            "page_count": 311,
            "language": "en"
        },
        {
            "id": 9,
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "publisher": "HarperTorch",
            "published_date": "1988-01-01",
            "page_count": 208,
            "language": "pt"
        },
        {
            "id": 10,
            "title": "Sapiens: A Brief History of Humankind",
            "author": "Yuval Noah Harari",
            "publisher": "Harper",
            "published_date": "2014-09-04",
            "page_count": 443,
            "language": "en"
        }
    ]




app=FastAPI()


class Book(BaseModel):
    id:int 
    title:str 
    author:str
    publisher:str 
    published_date:str 
    page_count:int 
    language:str 

class BookUpdate(BaseModel):
    title:str 
    author:str
    publisher:str 
    page_count:int 
    language:str 




@app.get("/books",status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_all_books():
    return books


@app.post("/books",status_code=status.HTTP_201_CREATED)
async def create_book(book:Book)->dict:
    new_book=book.model_dump()
    books.append(new_book)
    return new_book



@app.get("/books/{id}")
async def get_single_book(id:int)->dict:
    for book in books:
        if book["id"]==id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Book with id {id} not found."
        )



@app.patch("/books/{id}")
async def update_book(id:int,updated_book:BookUpdate)->dict:
    for book in books:
        if book["id"]==id:
            book["title"]=updated_book.title
            book["author"]=updated_book.author
            book["publisher"]=updated_book.publisher
            book["page_count"]=updated_book.page_count
            book["language"]=updated_book.language
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {id} not found"
    )


@app.delete("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id:int):
    for book in books:
        if book["id"]==id:
            books.remove(book)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with id {id} not found"
    )

