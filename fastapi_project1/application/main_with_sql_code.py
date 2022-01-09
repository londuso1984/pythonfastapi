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
    #Get posts from posts table
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()

    return {'data':posts}


@app.get("/posts/latest")
def get_latest_post():
    latest_post=my_posts[len(my_posts)-1]
    return {"data":latest_post}


@app.get("/posts/{id}")
def get_post(id:int):

    #Get data by ID from posts table
    #Make sure you convert the id back to str before you use it in query
    cursor.execute("""SELECT * FROM posts WHERE id= %s""", (str(id)))
    post=cursor.fetchone()

    #Check if the post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    return {"post_details":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
  
    #Delete a post from posts table
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id)))
    deleted_post=cursor.fetchone()
    conn.commit()
   
    #Check if the id to delete exists
    if deleted_post==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"The data with id {id} you trying delete does not exist")
    
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
def create_posts(post:Post):

    #Insert Data in post table
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING * """,
    (post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()

    return {"data": new_post} 

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    
    cursor.execute("""UPDATE posts SET title=%s, content =%s, published=%s WHERE id=%s RETURNING * """,(post.title,post.content, 
    post.published, str(id)) )
    updated_post=cursor.fetchone()
    conn.commit()
   
    if updated_post==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"The id {id} does not exist")

    return {"data":updated_post}



