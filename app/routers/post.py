from fastapi import FastAPI, Request, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List 


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    posts=db.query(models.Post).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:str=Depends(oauth2.get_current_user)):
    # print(current_user.email)
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def get_post(id:int, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   post=db.query(models.Post).filter(models.Post.id==id).first()
   print(post)
   if not post:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Post with id {id} does not exist"
        )
   return post


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post_to_update=post_query.first()
    if post_to_update== None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )
    post_data = post.model_dump()
    for key, value in post_data.items():
        setattr(post_to_update, key, value)
    db.commit()
    db.refresh(post_to_update)
    return post_to_update


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )
    post_query.delete(synchronize_session=False)   
    db.commit() 
