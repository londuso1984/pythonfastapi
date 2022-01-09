from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
#from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor #this helps access column names for tables
import time

app=FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True  #This is optional but when user does not provide data it will default to 'True'
    #rating: Optional[int]=None #this field is fully optional and if user does not provide it will store no data

while True:
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi', user="postgres",password="@Compassion123", cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database was successfully connected")
        break
    except Exception as error:
        print("Database failed to connect")
        print("Error :" , error)
        time.sleep(2)


my_posts=[{"id":1,"title":"Mombasa Beaches","content":"SouthCoast has some nice beautiful beaches"},
           {"id":2,"title":"Kisumu Beaches","content":"Lake Victoria some old beaches"}
          ]



@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    
    return {'data':posts}


@app.get("/posts/latest")
def get_latest_post():
    latest_post=my_posts[len(my_posts)-1]
    return {"data":latest_post}


@app.get("/posts/{id}")
def get_post(id:int):

    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    return {"post_details":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #deleting a post logic
    #find the index of the post in a dictionary/array
    #my_posts.pop(index)

    get_index=find_index_by_id(id)

    if get_index==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"The data with id {id} you trying delete does not exist")
    my_posts.pop(get_index)

    return {"message": f"The post of id {id} was susccessfully deleted"}

def find_index_by_id(id):
    for index, post in enumerate(my_posts):
        if post['id'] is id:
            return index


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:Post):
    #extracting all the post content/data
         #print(new_post)

    #extracting some properties from the pydantic model
         #print(new_post.rating)

    #Converting pydantic model to dictionary
    post_dictionary=new_post.dict()

    post_dictionary['id']=randrange(0,1000000)

    my_posts.append(post_dictionary)

    return {"data":post_dictionary} # Sending data as dictionary

@app.put("/posts/{id}")
def update_post(id:int,post:Post):

    index=find_index_by_id(id)
    if index==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"The id {id} does not exist")

    update_dictionary=post.dict()
    update_dictionary['id']=id
    my_posts[index]=update_dictionary

    return {"data":my_posts}

# @app.post("/createposts")
# def create_posts(payload_data:dict=Body(...)):

#     print(payload_data)

#     return {"new_post": f"title:{payload_data['title']}, content:{payload_data['content']}"}

