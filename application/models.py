from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import column, null, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database_conn import Base

class Post(Base):
    __tablename__='posts'

    id=Column(Integer,primary_key=True,nullable=False)
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #How to add a foreigner key for posts and users id
    title=Column(String,nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean,server_default='TRUE', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    #get user information from users table. 
    post_owner=relationship('User')
    
    """
    get user information from users table. Pass the user class model in the SQLAlchemy 'relationship('user)
    With just one line of code you are able to get info from another table in your API response and you can now use it on the Front End.
    """
    
    
class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String, nullable=False, unique=True)
    phone_number=Column(String,nullable=True, server_default=text('0722988766987'))
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__='votes'
    user_id=Column(Integer,ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id=Column(Integer,ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)