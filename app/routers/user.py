from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body


import time

from pydantic import utils
from .. import models  , schemas, utils
from ..db import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserModelResponseSchema)
def create_user(user: schemas.UserModelCreateSchema, db: Session = Depends(get_db)):
    # hashing password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.UserModelORM(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserModelResponseSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModelORM).filter(models.UserModelORM.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user id {id} does not exist")
    return user