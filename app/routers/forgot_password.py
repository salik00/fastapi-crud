from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app import database, oauth2, models, schemas, utils
# from database import reset_token
from datetime import datetime, timedelta
router = APIRouter()

@router.post("/forgot-password")
def forgot_password(email: str, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user with this email not found")
    #create a reset token
    token = oauth2.create_reset_token(user.id)
    #optionally store reset token in dtabse(if desired)
    user.reset_token = token
    user.reset_token_expiry = datetime.now()+timedelta(minutes=15)
    db.commit()
    #send reset token to users email
    reset_link = f"http://127.0.0.1:8000/reset-password?token={token}"
    utils.send_email(
        recipient_email = user.email,
        subject="Password Reset Request",
        body=f"Click the link to reset your password: {reset_link}"
    )
    return {"message": "Password reset link sent to your email."}

@router.post("/reset-password")
def reset_password(token:str, new_password:str, db:Session=Depends(database.get_db)):
    token_data = oauth2.verify_reset_token(token)
    
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user or user.reset_token!=token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= "invalid or expired token") 
    if user.reset_token_expiry and user.reset_token_expiry < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Token has expired.")

    #reset users password
    hashed_password = utils.hash(new_password)
    user.password = hashed_password
    #invalidate the token
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    return {"message": "Password reset successfully.."}