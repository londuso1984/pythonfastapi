from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session


from .. import models, schemas, utils,database_conn,oauth2

router=APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/",response_model=schemas.Token)
def authenticate(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database_conn.get_db)):
    """
     Note: When using OAuth2PasswordRequestForm the credentials are not compared 
     from the schema but they come from the library which return username and password field

     Therefore the function auntenticate will have recieve the values from the fastapi lib[OAuth2PasswordRequestForm] as
     authenticate(user_credential:OAuth2PasswordRequestForm=Depends()) instead of authenticate(user_credential:schemas.userAuthenticate) 

     Then after that change user_credential.email to user_credential.username since that field will store the email

     Then for you to call it in the Postman the api expects data from form-data and not from body
     
    """
    user=db.query(models.User).filter(models.User.email==user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    verify_user=utils.verify_credentials(user_credential.password,user.password)

    if not verify_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    # # Create and return Token
    access_token=oauth2.create_jwt_access_token(data={"id":user.id}) #payload we decided to user id . You can also use role or position
    return {"access_token":access_token,"token_type":"bearer"}

    
