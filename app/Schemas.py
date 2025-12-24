from pydantic import BaseModel,ConfigDict,EmailStr
from typing import Optional,Literal
from datetime import datetime
from pydantic.types import conint


# class to handle data validation for data from user to backend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_no: str
    model_config = ConfigDict(from_attributes=True) # It will tell pydantic response_model to read the data even if not a dict but an ORM model


#  For handling data validation for data from backend -> user 
class PostResponse(Post):
    id: int
    user_id: int
    owner: UserResponse
    pass
    # time: datetime
    model_config = ConfigDict(from_attributes=True) # instaed of class Config: orm_mode = True

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_no: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    # model_config = ConfigDict(from_attributes=True)

class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]

class PostVote(BaseModel):
    post: PostResponse
    votes: int
    model_config = ConfigDict(from_attributes=True)