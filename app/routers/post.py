# For documentation head over to http://127.0.0.1:8000/redoc or http://127.0.0.1:8000/docs route

from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,Schemas,oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[Schemas.PostVote])
async def get_posts(db:Session = Depends(get_db),limit:int = 5,skip:int = 0,search:Optional["str"] = ""): # Query parameter: {{URL}}posts?limit=2&skip=0&search=north
    # ,current_user:int = Depends(oauth2.get_current_user)
    # posts = db.query(models.Post).filter(func.lower(models.Post.title).contains(search.lower())).limit(limit).offset(skip).all() # Limit to limit results and skip first n results
    # return posts
    rows = (
        db.query(models.Post, func.count(models.Vote.user_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(func.lower(models.Post.title).contains(search.lower())).limit(limit).offset(skip).all()
    )
    return [{"post": row[0], "votes": row[1]} for row in rows]

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Schemas.PostResponse)
async def create_post(post: Schemas.Post,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # print(current_user.username)
    new_post = models.Post(user_id=current_user.id,**post.model_dump()) # post.model_dump() -> {title,content,published}
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/latest',response_model = Schemas.PostResponse)
async def get_latest_post(db: Session = Depends(get_db),status_code=status.HTTP_200_OK,current_user:int = Depends(oauth2.get_current_user)):
    latest_post_query = db.query(models.Post).order_by(models.Post.id.desc())
    if not latest_post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        latest_post = latest_post_query.first()
        return latest_post

@router.get('/{id}',response_model = Schemas.PostVote) # initially Schemas.PostResponse
async def get_post(id: int, response: Response,db: Session = Depends(get_db),status_code=status.HTTP_200_OK,current_user:int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    post_obj = {"post": post[0],"votes": post[1]}
    if not post_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        return post_obj

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db),status_code=status.HTTP_204_NO_CONTENT,current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        if (post.user_id !=  current_user.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to delete this post")
        post_query.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model = Schemas.PostResponse)
async def update_post(id: int,post: Schemas.Post,db: Session = Depends(get_db),status_code=status.HTTP_202_ACCEPTED,current_user:int = Depends(oauth2.get_current_user)):
    update_post_query = db.query(models.Post).filter(models.Post.id == id)
    if not update_post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    else:
        if(update_post_query.first().user_id != current_user.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to update this post")
        update_post_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
        return  update_post_query.first()