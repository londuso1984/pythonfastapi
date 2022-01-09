from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database_conn import get_db

router=APIRouter(
    prefix="/users",
    tags=["Users"] #Helps grouping the swaggerUI documentation
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserReponseOutPut)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    #Check if email exists
    # email_exist=utils.verify_email_exists(user.email)
    # if email_exist==True:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Email already exists")
    
    #Hash the password
    hashed_user_password=utils.hash(user.password)
    user.password=hashed_user_password

    #save the user in the users table
    db.begin()
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.UserReponseOutPut)
def get_user(id:int, db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"The user of id {id} does not exist")
        
    return user
