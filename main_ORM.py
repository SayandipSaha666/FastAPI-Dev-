# For documentation head over to http://127.0.0.1:8000/redoc or http://127.0.0.1:8000/docs route

from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session

from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,Schemas,utils
from .database import engine,get_db


# This is a SQLAlchemy command that creates all the database tables defined in your SQLAlchemy models if they do not already exist.
models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # rating: Optional[int] = None

# if commented use post: Schemas.Post else only post: Post in case of create_post/, update_post/
    
while True:
    try:
        connection = psycopg2.connect(host='localhost',database='FastAPI_Tutorial_Database',user='postgres',password='Saha@06122004')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print('Error: ',error)
        time.sleep(2)
        break

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts",response_model=List[Schemas.PostResponse])
async def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/create_post",status_code=status.HTTP_201_CREATED,response_model=Schemas.PostResponse)
async def create_post(post: Schemas.Post,db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/posts/latest',response_model = Schemas.PostResponse)
async def get_latest_post(db: Session = Depends(get_db),status_code=status.HTTP_200_OK):
    latest_post_query = db.query(models.Post).order_by(models.Post.id.desc())
    if not latest_post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        latest_post = latest_post_query.first()
        return latest_post

@app.get('/posts/{id}',response_model = Schemas.PostResponse)
async def get_post(id: int, response: Response,db: Session = Depends(get_db),status_code=status.HTTP_200_OK):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        return post

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}',status_code=status.HTTP_202_ACCEPTED,response_model = Schemas.PostResponse)
async def update_post(id: int,post: Schemas.Post,db: Session = Depends(get_db)):
    update_post_query = db.query(models.Post).filter(models.Post.id == id)
    if not update_post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    update_post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return  update_post_query.first()

@app.get('/users',status_code=status.HTTP_200_OK,response_model = List[Schemas.UserResponse])
async def get_user(user: Schemas.UserSignup,db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    else:
        return users

@app.post('/create_user',status_code=status.HTTP_201_CREATED,response_model = Schemas.UserResponse)
async def create_user(user: Schemas.UserSignup,db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users/{id}',status_code=status.HTTP_200_OK,response_model = Schemas.UserResponse)
async def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    else:
        return user

