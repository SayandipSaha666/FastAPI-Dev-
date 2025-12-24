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
from fastapi.middleware.cors import CORSMiddleware
from .routers import post,user,auth,vote

# This is a SQLAlchemy command that creates all the database tables defined in your SQLAlchemy models if they do not already exist.
models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)