from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT:str
    DATABASE_NAME:str
    DATABASE_PASSWORD:str
    DATABASE_USERNAME: str
    JWT_SECRET_KEY:str
    ALGORITHIM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    #this allows this class access .env file and use it
    class Config:
        env_file=".env"

settings=Settings()