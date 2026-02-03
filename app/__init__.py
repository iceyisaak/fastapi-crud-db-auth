from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from random import randrange
from contextlib import asynccontextmanager
from psycopg_pool import ConnectionPool
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os


load_dotenv() 



class Post(BaseModel):
    title:str
    content:str
    published:bool=True




@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    try:
        pool = ConnectionPool(
            kwargs={
                "host": os.getenv('DB_HOST'),
                "port": os.getenv('DB_PORT'),
                "dbname": os.getenv('DB_NAME'),
                "user": os.getenv('DB_USERNAME'),
                "password": os.getenv('DB_PASSWORD')
            },
            min_size=1,
            max_size=10
        )
        print("Database Connection Pool Created")
    except Exception as e:
        print(f"Failed to create database connection pool: {e}")
        pool = None
    
    yield
    
    if pool:
        pool.close()



app=FastAPI(lifespan=lifespan)



# Custom exception handler
@app.exception_handler(psycopg.OperationalError)
async def db_exception_handler(request: Request, exc: psycopg.OperationalError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "Database service unavailable", "detail": str(exc)}
    )




my_posts = [{
    "title":"Title of post 1",
    "content":"Content of post 1",
    "id":1
},
{
    "title":"Favourite Food",
    "content":"I love pizza",
    "id":2
}]



@app.get("/")
def root():
    return {"message": "fastapi-crud-db-auth"}


@app.get("/posts")
def get_posts():
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": "Database connection pool not available"}
        )
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""SELECT * FROM posts""")
            posts = cursor.fetchall()
            return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": "Database connection pool not available"}
        )
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                INSERT INTO posts (title, content, published)
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (post.title,post.content,post.published))
            new_post=cursor.fetchone()
            conn.commit()
            return {"data":new_post}
        



@app.get("/posts/latest")
def get_latest_post():
    return {"data":my_posts[-1]}
    


@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": "Database connection pool not available"}
        )
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT * FROM posts
                WHERE id=%s;
            """,(id,))
            post=cursor.fetchone()
            
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Post with ID: {id} does not exist"
                )
            return {"data":post}


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": "Database connection pool not available"}
        )
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                UPDATE posts
                SET 
                    title=%s,
                    content=%s,
                    published=%s
                WHERE id=%s
                RETURNING *;
            """,(post.title,post.content,post.published,id))
            updated_post=cursor.fetchone()
            conn.commit()
            if updated_post == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Post with ID: {id} does not exist"
                )
    return {"data":updated_post, "message":"Post updated successfully"}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"message": "Database connection pool not available"}
        )
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                DELETE FROM posts
                WHERE id=%s
                RETURNING *;
            """,(id,))
            deleted_post=cursor.fetchone()
            conn.commit()
            if deleted_post == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Post with ID: {id} does not exist"
                )
    return {"message":f"Post with ID:{id} deleted successfully"}





def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i