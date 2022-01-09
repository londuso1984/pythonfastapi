from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from sqlalchemy.orm.session import Session
from .. import schemas, database_conn, models, oauth2

router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(database_conn.get_db), current_user=Depends(oauth2.get_current_user)):

    #Check if the post exist before voting
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {vote.post_id} does not exist")

    #query for user vote for a post
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()

    #Check if the user has already voted for a given post

    if(vote.vote_dir==1):
        if(found_vote!=None):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already liked on post {vote.post_id}")

        #Othewise create vote
        vote_for_post=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.begin()
        db.add(vote_for_post)
        db.commit()
        return {"message":"Successful Liked the Post"}
    else:
        #Check if vote found
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        #Delete the vote or unlike the post
        db.begin()
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully Deleted vote or unliked post"}
    

