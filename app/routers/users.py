from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..schemas import (UserSchema, 
                      UserCreateResponseSchema, UserGetResponseSchema)
from ..utils import hash_password

router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserCreateResponseSchema)
def create_users(user: UserSchema, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.UsersModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=list[UserGetResponseSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UsersModel).all()
    return users

@router.get('/{id}', response_model=UserGetResponseSchema)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UsersModel).filter(models.UsersModel.id==id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} not found!")
    return user