from passlib.context import CryptContext # type: ignore
import smtplib
from email.mime.text import MIMEText

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def send_email(recipient_email, subject, body):
    sender_email = "casinoacegames@gmail.com"
    sender_password = "l0ttery@$#*"
    
    #create the email message
    msg = MIMEText(body)
    msg["Subject"]=subject
    msg["From"]=sender_email
    msg["To"]=recipient_email
    
    #send the mail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        
    