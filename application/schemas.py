from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime

from pydantic.types import conint

class UserCreate(BaseModel):
    email:EmailStr
    password: str

class UserReponseOutPut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    #The Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model(or any other arbitrary object with attibutes)
    class Config:
        orm_mode=True

class UserAuthenticate(BaseModel):
    email:EmailStr
    password:str

class PostBase (BaseModel):
    title: str
    content: str
    published: bool=True  #This is optional but when user does not provide data it will default to 'True'
    #rating: Optional[int]=None #this field is fully optional and if user does not provide it will store no data

    
class PostCreate (PostBase):
    #this keyword helps pass all the things from base class to child class
    pass

class PostResponse(PostBase):
    id: int
    owner_id:int
    created_at: datetime
    post_owner:UserReponseOutPut

    """We can Inherit these fields from the Base class(PostBase)
        title: str
        content: str
        published: bool 
    """
    
    #The Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model(or any other arbitrary object with attibutes)
    class Config:
        orm_mode=True

class PostVoteResponse(BaseModel):
    Post:PostResponse 
    votes: int
    class Config:
        orm_mode=True

class Vote(BaseModel):
    post_id:int
    vote_dir: conint(le=1)# allows 1 and less than 1

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str]=None