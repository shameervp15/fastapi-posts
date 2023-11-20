from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostSchema(BaseModel):
    title : str
    content : str
    published: bool

class PostResponseSchema(PostSchema): #for get posts; use list[schema]
    created_at: datetime
    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime

class UserCreateResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserGetResponseSchema(BaseModel):
    id: int
    email: str
    created_at: datetime

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    id: Optional[str]