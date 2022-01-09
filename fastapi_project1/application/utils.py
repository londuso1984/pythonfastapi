from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session
from . import database_conn, models

password_context=CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password:str):
    return password_context.hash(password)

def verify_credentials(plain_blurred_password, hashed_password):
    return password_context.verify(plain_blurred_password,hashed_password)

def verify_email_exists(user_email,db: Session=Depends(database_conn.get_db())):

    user_email=db.query(models.User).filter(models.User.email==user_email).first()

    if user_email !=None:
        return True

    return False
