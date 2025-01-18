from fastapi import status, HTTPException, Response, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import Optional, List
from .. import  schemas, models, oauth2

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
    )

# @router.get("/", response_model=list[schemas.PostOut])
@router.get("/", response_model = List[schemas.PostOut])
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit : int = 10, skip : int = 0, search: Optional[str] = ""):
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).all()
    
    return result
   
    # return result
       
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id= current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()  
    # post = result.first()
    print(post)
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f" post with id {id} not found...")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
    #                         detail= f"Sorry! Not authorized to perform requested action")
    return post


@router.delete("/{id}", response_model = schemas.Post)
def delete_post(id: int, db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)   
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Sorry! Not authorized to perform requested action")
    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: str, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Sorry! Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()
    return post_query.first()