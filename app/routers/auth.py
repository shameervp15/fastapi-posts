from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import get_db
from ..schemas import UserLoginSchema
from ..models import UsersModel
from ..utils import verify_password
from ..oauth2 import create_access_token

router = APIRouter(
    prefix='/auth',
    tags=['Authentication'],
)

@router.post('/login')
#OAuth2PasswordRequestForm - returns a form to fill in user credentials(username,password) :OAuth2PasswordRequestForm = Depends()
def login_user(user_credentials: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UsersModel).filter(UsersModel.email==user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials!")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials!")
    
    access_token = create_access_token(data={"user_id":user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
    