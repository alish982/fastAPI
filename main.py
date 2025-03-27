from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username:str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/user/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get('/user/', status_code=status.HTTP_200_OK)
async def get_users(db:db_dependency):
    user = db.query(models.User).all()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"No New Users"
        )
    return user

@app.get('/user/{user_id}', status_code=status.HTTP_200_OK)
async def get_users(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail=f"User of ID {user_id} not found"
        )
    return user

@app.post('/post/', status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get('/post', status_code=status.HTTP_200_OK)
async def read_post(db: db_dependency):
    post = db.query(models.Post).all()
    if post is None:
        raise HTTPException(
            status_code=404,
            detail=f"No Newer Posts"
        )
    return post

@app.get('/post/{user_id}', status_code=status.HTTP_200_OK)
async def get_post(user_id: int, db:db_dependency):
    post = db.query(models.Post).filter(models.Post.id == user_id).first()
    if post is None:
        raise HTTPException(
            status_code= 404, 
            detail=f"No ID found for {user_id}"
        )
    return post

@app.get('/user/post/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_post(user_id: int, db: db_dependency):
    jointData = db.query(models.Post).filter(models.Post.user_id == user_id).all() 

    if not jointData:  
        raise HTTPException(
            status_code=404, 
            detail="Posts not found"
        )

    return jointData

@app.delete('/user/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id:int, db:db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=404, 
            detail=f"User Id {user_id} not found"
        )
    db.delete(db_user)
    db.commit()

    return {f"message: User ID {user_id} deleted successfully"}

@app.delete('/post/{post_id}', status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db:db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with Post ID: {post_id} not found"
        )
    db.delete(post)
    db.commit()

    return {"message: post delete successfully"}