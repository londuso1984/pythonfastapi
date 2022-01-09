from application import oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database_conn import get_db
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostVoteResponse])
#@router.get("/")
def get_posts(db:Session=Depends(get_db), current_user=Depends(oauth2.get_current_user),limit:int=10, skip:int=0, search:Optional[str]=""):
    #Get posts from posts table
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    """
      -Left Outer Join with SQLAlchemy lib [By default SQLalchemy gives Left Inner Join]. Therefor isouter=True to get Outer join
      -Then 'Group by' with SQLAlchemy
      -The Count results with SQLalchemy [For this you have to import func from SqlAlchemy lib: from sqlalchemy import func]. To rename the count column name [.lable('votes)]
    """
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return post


@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id:int,db:Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    #Get data by ID from posts table
    #Make sure you convert the id back to str before you use it in query
    """
      cursor.execute('''SELECT * FROM posts WHERE id= %s''', (str(id)))
      post=cursor.fetchone()
    """

    #SQLalchemy orm way the raw select where sql query
    #post=db.query(models.Post).filter(models.Post.id==id).first()

    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    #Check if the post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
  
    #Delete a post from posts table
    '''
      cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(str(id)))
      deleted_post=cursor.fetchone()
      conn.commit()
    '''
    #Using SQLAlchmy ORM way to delete a post
    post_query=db.query(models.Post).filter(models.Post.id==id)
    
    post=post_query.first()

    #Check if the id to delete exists
    if post==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"The data with id {id} you trying delete does not exist")
    
    #check to ensure a user can only delete his post and not someone else post
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to delete other user's post")

    db.begin()
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"The post of id {id} was susccessfully deleted"}


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db:Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):

   

    #print(user_id)
    ''' Raw SQL query for inserting data
            cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING * """,
            (post.title,post.content,post.published))
            new_post=cursor.fetchone()
            conn.commit()
    '''
    #Insert Data in post table using SQLAlchemy db functions
    
    db.begin()
    #add owner id and get columns name using dictionary and then use ** to unpack the dictionary
    
    new_post=models.Post(owner_id=current_user.id, **post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #this implements RETURNING * piece in the raw sql
           
    return new_post 

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.PostCreate, db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    '''   
    cursor.execute("""UPDATE posts SET title=%s, content =%s, published=%s WHERE id=%s RETURNING * """,(post.title,post.content, 
    post.published, str(id)) )
    updated_post=cursor.fetchone()
    conn.commit()
    '''
    update_query=db.query(models.Post).filter(models.Post.id==id)
    update_post=update_query.first()
    
    if update_post==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"The id {id} does not exist")

    if update_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized to update other people's post")

    db.begin()
    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(update_post)

    return update_post
