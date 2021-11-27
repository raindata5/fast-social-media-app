from os import stat
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy import func

import time

from pydantic import utils
from .. import models, schemas, utils, oauth2
from ..db import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts'])

@router.get("/", response_model= List[schemas.PostFavoriteModelResponseSchema])
def get_posts( limit: int = 10, offset: int = 0, keyword: Optional[str] = "", db: Session = Depends(get_db)):
    # cursor.execute('select * from public."Post" ')
    # posts = cursor.fetchall()
    # posts = db.query(models.PostModelORM).filter(models.PostModelORM.title.contains(keyword)).limit(limit).offset(offset).all()
    results = db.query(models.PostModelORM, func.count(models.FavoriteModelORM.PostID).label("votes")).join(models.FavoriteModelORM,
     models.PostModelORM.id == models.FavoriteModelORM.PostID, isouter=True).group_by(models.PostModelORM.id).filter(
         models.PostModelORM.title.contains(keyword)).limit(limit).offset(offset).all()
    return results
    

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PostModelResponseSchema)
def create_post(data: schemas.PostModelCreateSchema, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user) ):
    # cursor.execute('insert into public."Post" (title, content, published) VALUES (%s, %s, %s) RETURNING *', (data.title, data.content, data.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.PostModelORM(UserID=user.id ,**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostFavoriteModelResponseSchema)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # having connected to db
    # cursor = conn.cursor()
    # query = 'select * from public."Post" where id=%s'
    # cursor.execute(query, (id,))
    # post = cursor.fetchone()
    # using in memory data store
    # post = next(filter(lambda x: x["id"] == id , in_mem_posts), None)
    # post1 = [row for row in in_mem_posts if row["id"] == id ]
    # post = db.query(models.PostModelORM).filter(models.PostModelORM.id == id).first()
    post = db.query(models.PostModelORM, func.count(models.FavoriteModelORM.PostID).label("votes")).join(models.FavoriteModelORM,
    models.PostModelORM.id == models.FavoriteModelORM.PostID, isouter=True).group_by(models.PostModelORM.id).filter(models.PostModelORM.id == id).first()
    if post is None:
        # response.status_code = status.HTTP_400_BAD_REQUEST
        # return {"msg": f"post with {id} as id not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} as id not found")
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def del_posts(id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # global in_mem_posts
    # posts = [row for row in in_mem_posts if row["id"] != id ]    
    # in_mem_posts = posts
    # cursor = conn.cursor()
    # query = 'DELETE from public."Post" where id=%s returning *'
    # cursor.execute(query, (id,))
    # del_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.PostModelORM).filter(models.PostModelORM.id == id)   
    post = post_query.first()
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} as id not found")

    if post.UserID != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostModelResponseSchema)
def update_posts(id: int, data: schemas.PostModelCreateSchema, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # data = data.dict()
    # post = next(filter(lambda x: x["id"] == id , in_mem_posts), None)
    # post.update(data)
    # cursor = conn.cursor()
    # query = 'UPDATE public."Post" SET title = %s, content = %s, published=%s where id=%s returning *'
    # cursor.execute(query, (data.title, data.content, data.published, id))
    # up_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.PostModelORM).filter(models.PostModelORM.id == id)   
    post = post_query.first()
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} as id not found")

    if post.UserID != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform requested action")
        
    post_query.update(data.dict(), synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post