# For documentation head over to http://127.0.0.1:8000/redoc or http://127.0.0.1:8000/docs route

from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", 
             "content": "content of post 1", 
             "id": 1
            }, 
            {
                "title": "favorite foods", 
                "content": "I like pizza", 
                "id": 2
            }]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def delete_post(id: int):
    new_post = []
    for p in my_posts:
        if(p["id"] != id):
            new_post.append(p)
    return new_post 

def get_index(id):
    for i,p in enumerate(my_posts):
        if(p["id"] == id):
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {
        "status": "success",
        "user_id": 1,
        "posts":my_posts
    }
@app.post("/create_post",status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)
    return {"message": "New post created!",
            "post": post_dict
            }

@app.get('/posts/latest')
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post": post}


@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}
    else:
        return {"post": post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # posts = delete_post(id)
    index = get_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int,post: Post):
    index = get_index(id)
    if(index == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {'message': 'post updated','post': post_dict}