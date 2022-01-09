from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, models, database_conn
from .config import settings


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='auth') #tokenUrl is the auth or login end point

"""
  To create the JWT token we need the following
    -SECRET KEY
    -ALGORITHIM
    -EXPIRATION TIME
"""
#variables from the pyndantic model file/class that has the .env file with enveironment variables
SECRET_KEY=settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHIM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_jwt_access_token(data:dict):

    data_to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data_to_encode.update({"exp": expire})
    
    encoded_jwt=jwt.encode(data_to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        #decode the token/data and extract the user id from the token
        decode_payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id:str=decode_payload.get("id")

        #if incorect id throw exception otherwise get the user id
        if user_id is None:
            raise credentials_exception

        token_data=schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data

#This function will now be exposed to any end point that requires user to be authenticated b4 accessing end point and gets you user which you can use to do other operations
def get_current_user(token:str=Depends(oauth2_scheme), db: Session=Depends(database_conn.get_db)):

    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    user_token=verify_access_token(token,credentials_exception)

    user=db.query(models.User).filter(models.User.id==user_token.id).first()

    return user

    
