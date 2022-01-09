from sqlalchemy import create_engine, engine
from sqlalchemy.engine import base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor #this helps access column names for tables
import time
from .config import settings

"""
    Connection URL string format
    SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip_address>/hostname>/<database_name>'
"""
"""Connect to DB using SQLAlchemy library--------------------------------------------------------------------------------------------------------"""
#Create database connection url and create_engine. Pass the variables from the pydantic class that have .env file with variables
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit='false',autoflush='false',bind=engine)

Base=declarative_base() #all our model classes will extend this

#this functions helps us connect to database and create a session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""Connect to db via psycog2 library---------------------------------------------------------------------------------------------------------"""

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost', database='fastapi', user="postgres",password="Compassion123", cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database was successfully connected")
#         break
#     except Exception as error:
#         print("Database failed to connect")
#         print("Error :" , error)
#         time.sleep(2)