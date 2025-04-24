from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from models import User
from database import get_db
from schemas import SignupSchema
from fastapi_mail import FastMail, MessageSchema
from mail_config import conf

router = APIRouter()

@router.post("/signup")
async def signup(user: SignupSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")

    hashed_pwd = bcrypt.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_pwd,
        status="pending"
    )
    db.add(new_user)
    db.commit()

    verification_url = f"http://localhost:8000/verify-email?email={user.email}"
    email_body = f"Hi This is Sandhya Konda,Don't worry this is just for testing Click the link to verify your email: <a href='{verification_url}'>Verify Email</a>"

    message = MessageSchema(
        subject="Email Verification By Sandhya Konda",
        recipients=[user.email],  #the person to whom we want to send fetches from db
        body=email_body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "Verification email sent"}

@router.get("/verify-email")
def verify_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == "verified":
        return {"message": "Already verified"}

    user.status = "verified"
    db.commit()

    return {"message": "Email verified successfully"}


