from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint
from app.db import Base

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    # publisher: Optional[int] = None

class PostModelBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True
    # publisher: Optional[int] = None

class PostModelCreateSchema(PostModelBaseSchema):
    pass

class UserModelCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class FavoriteCreateSchema(BaseModel):
    PostID: int
    # How to place constraint on integer
    # dir: conint()
    dir: bool

class TokenData(BaseModel):
    id: Optional[str] = None



# reponsedata


class UserModelResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class PostModelResponseSchema(PostModelBaseSchema):
    id: int
    created_at: datetime
    UserID: int
    user: UserModelResponseSchema
    class Config:
        orm_mode = True

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str

# problem with this model is that it repeats 3 fields twice name the ones in PostModelBaseSchema 
# I can confirm by switching the default value for publish in and out
# class PostFavoriteModelResponseSchema(PostModelBaseSchema):
#     PostModelORM: PostModelResponseSchema
#     votes: int

#this class solves the issue
class PostFavoriteModelResponseSchema(BaseModel):
    PostModelORM: PostModelResponseSchema
    votes: int