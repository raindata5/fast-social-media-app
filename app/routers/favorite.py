from os import stat
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
import time
from pydantic import utils
from .. import models, schemas, utils, oauth2
from ..db import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Favorite"], prefix="/favorite")


@router.post("/", status_code=status.HTTP_201_CREATED)
def favorite_post(favorite: schemas.FavoriteCreateSchema, db: Session = Depends(get_db), user: models.UserModelORM = Depends(oauth2.get_current_user)):
    post = db.query(models.PostModelORM).filter(models.PostModelORM.id==favorite.PostID).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {favorite.PostID} not found")
    check_query = db.query(models.FavoriteModelORM).filter(models.FavoriteModelORM.PostID == favorite.PostID, models.FavoriteModelORM.UserID == user.id)
    found = check_query.first()
    if favorite.dir == 1:
        if found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user {user.id} has already favorited the following post {favorite.PostID}')
        new_favorite = models.FavoriteModelORM(PostID = favorite.PostID, UserID= user.id)
        db.add(new_favorite)
        db.commit()
        return {"msg": "favorite received"}
    else:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="information provided isn't registered" )

        check_query.delete()
        db.commit()
        return {"msg": "vote deleted"}