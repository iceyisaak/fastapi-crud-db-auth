from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app=FastAPI()



class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int] = None

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
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/latest")
def get_latest_post():
    return {"data":my_posts[-1]}
    


@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    print(id)
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )

    print(post)
    return {"data":post}


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index=find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )
    post_dict=post.model_dump()  
    post_dict["id"]=id  
    my_posts[index]=post_dict
    return {"data":post_dict, "message":"post updated successfully"}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, response:Response):
    index=find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)





def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        


def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i