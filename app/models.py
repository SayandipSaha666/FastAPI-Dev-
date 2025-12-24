from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,text,ForeignKey
from sqlalchemy.sql.expression import null
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "Social_Media_Table_Relational"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False,default=null)
    content = Column(String,nullable=False,default=null)
    published = Column(Boolean,default=True)
    time = Column(TIMESTAMP(timezone=True),server_default=text("now()"),nullable=True)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE",onupdate="NO ACTION"),nullable=False)
    owner = relationship("User",back_populates="posts") # Referencing User class
    # phone_no = Column(String,ForeignKey("Users.phone_no",ondelete="CASCADE",onupdate="NO ACTION"),nullable=False)


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    username = Column(String,nullable=False,unique=True)
    time = Column(TIMESTAMP(timezone=True),server_default=text("now()"),nullable=True)
    phone_no = Column(String,nullable=False,unique=True)
    posts = relationship("Post",back_populates="owner")
    

class Vote(Base):
    __tablename__ = "Votes"
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE",onupdate="NO ACTION"),primary_key=True)
    post_id = Column(Integer,ForeignKey("Social_Media_Table_Relational.id",ondelete="CASCADE",onupdate="NO ACTION"),primary_key=True)
    