from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from  .. import models,Schemas, database,oauth2
from sqlalchemy.orm import session
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(user_vote:Schemas.Vote,db: session = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    get_post = db.query(models.Post).filter(models.Post.id == user_vote.post_id).first()
    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Pos                                                                   t does not exist')
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == user_vote.post_id,models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(user_vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f' User with id {current_user.id} has already voted on post with id {user_vote.post_id}')
        else:
            new_vote = models.Vote(user_id = current_user.id,post_id = user_vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return f'Successfully added vote'
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Vote does not exist')
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return f'Successfully deleted vote'