
from application.routers.auth import authenticate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database_conn import engine
from .routers import post, user,auth,vote
from .config import settings

#models.Base.metadata.create_all(bind=engine)#Creates the schemas/tables in database

app=FastAPI()


#origins=['https://compassion-africa.org','https://www.google.com', 'https://www.youtube.com']

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]

)

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI Cooooool 2022"}

#this goes and find the path operetion API and work normally
app.include_router(post.router) 
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

