from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..schemas import (PostSchema, PostResponseSchema)
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)

@router.get('/', response_model=list[PostResponseSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.PostsModel).all() #while running db.query(models.PostsModel) => returns the sqlquery
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
def create_posts(post: PostSchema, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    new_post = models.PostsModel(**post.model_dump()) #lot cleaner rather than adding each and every field; refer docs
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #refresh does the same thing as we did in the sqlquery "RETURNING *"
    return new_post 

@router.get('/{id}', response_model=PostResponseSchema)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostsModel).filter(models.PostsModel.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found!")
    return post

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostsModel).filter(models.PostsModel.id==id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found!")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('//{id}', response_model=PostResponseSchema)
def update_post(id: int, post: PostSchema, db: Session = Depends(get_db)):
    post_query = db.query(models.PostsModel).filter(models.PostsModel.id==id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} not found!")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post