from fastapi import status, HTTPException, Depends, APIRouter
from .. import models,schemas,oauth2
from sqlalchemy import or_,func
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional 


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)






# @router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.Post])
@router.get("/",status_code=status.HTTP_200_OK,response_model=List[schemas.PostInfo])
def get_posts(
    db:Session=Depends(get_db),
    current_user:schemas.User=Depends(oauth2.get_current_user),
    limit:int=10,
    skip:int=0,
    search:Optional[str]=""
):
    # posts=db.query(models.Post).all()
    # posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    query = db.query(models.Post)

    if search:
        # Case-insensitive search for multiple keywords (OR logic)
        keywords = search.split()
        search_conditions = [
            func.lower(models.Post.title).contains(keyword.lower()) 
            for keyword in keywords
        ]
        query = query.filter(or_(*search_conditions))
    
    # posts = query.limit(limit).offset(skip).all()
    
    # print(f"Search: '{search}', Found: {len(posts)} posts")

    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    # results = query.join(
    # models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    # ).group_by(models.Post.id).with_entities(
    #     models.Post, func.count(models.Vote.post_id).label("votes")
    # ).limit(limit).offset(skip).all()

    # Transform results into the expected format
    return posts
    # print(results)
    # return results





@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostInfo)
def get_post(
    id:int, 
    db:Session=Depends(get_db),
    current_user:schemas.User=Depends(oauth2.get_current_user)
):
    # post=db.query(models.Post).filter(models.Post.id==id).first()

    # post_query = db.query(models.Post).filter(
    #     models.Post.id == id,
    #     models.Post.owner_id == current_user.id
    # )
    # post = post_query.first()

    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True
    ).group_by(models.Post.id).filter(models.Post.id==id).first()


    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )



    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int, 
    updated_post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(
        models.Post.id == id,
        models.Post.owner_id == current_user.id  # Authorization in query
    )
    post_to_update = post_query.first()
    
    if post_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )
    
    # Update the post
    post_data = updated_post.model_dump()
    for key, value in post_data.items():
        setattr(post_to_update, key, value)
    
    db.commit()
    db.refresh(post_to_update)
    return post_to_update


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id:int, 
    db:Session=Depends(get_db),
    current_user:models.User=Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(
        models.Post.id == id,
        models.Post.owner_id == current_user.id
    )
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with ID: {id} does not exist"
        )
    post_query.delete(synchronize_session=False)   
    db.commit() 
