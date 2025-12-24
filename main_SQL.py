# For documentation head over to http://127.0.0.1:8000/redoc or http://127.0.0.1:8000/docs route

from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None

    
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
    return {"data": posts}


@app.get("/posts")
async def get_posts():
    cursor.execute('SELECT * FROM "Social_Media"')
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/create_post",status_code=status.HTTP_201_CREATED)
async def create_post(post: models.Post):
    cursor.execute('INSERT INTO "Social_Media" ("title","content","published") VALUES (%s,%s,%s) RETURNING *',(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"data": new_post}

@app.get('/posts/latest')
async def get_latest_post():
    cursor.execute('SELECT * FROM "Social_Media" ORDER BY "id" DESC LIMIT 1 RETURNING *')
    latest_post = cursor.fetchone()
    return {"data": latest_post}

@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    cursor.execute('SELECT * FROM "Social_Media" WHERE "id" = %s',str(id))
    post =  cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        return {"data": post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute('DELETE FROM "Social_Media" WHERE "id" = %s RETURNING *',str(id))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int,post: models.Post):
    cursor.execute('UPDATE "Social_Media" SET title = %s, content = %s, published = %s WHERE "id" = %s RETURNING *',(post.title,post.content,post.published,str(id)))
    update_post = cursor.fetchone()
    if not update_post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    connection.commit()
    return {"data": update_post}

