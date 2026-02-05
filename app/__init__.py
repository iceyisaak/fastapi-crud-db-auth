from fastapi import FastAPI
from contextlib import asynccontextmanager
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import os
from app.database import engine, Base
from .routers import post, user, auth

load_dotenv() 

Base.metadata.create_all(bind=engine)


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


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "fastapi-crud-db-auth"}


#######################################################

