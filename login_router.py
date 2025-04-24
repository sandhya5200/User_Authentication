from schemas import OTPVerifySchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from redis_client import r
from schemas import LoginSchema
import random
from twilio_config import send_sms
from passlib.hash import bcrypt

router = APIRouter()

# Login route
@router.post("/login")
def login_user(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.phone == data.phone)).first()

    if not user or not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.status != "verified":
        raise HTTPException(status_code=403, detail="Email not verified")

    otp = str(random.randint(100000, 999999))
    r.setex(f"otp:{user.phone}", 300, otp)
    print(f"Generated OTP: {otp} for {user.phone}")


    send_sms(user.phone, f"Your OTP for login is: {otp}")
    return {"message": "OTP sent to your phone number"}

# Verify OTP route
@router.post("/verify-otp")
def verify_otp(data: OTPVerifySchema, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User).filter_by(phone=data.phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Phone number is not registered")

    # Verify OTP only if user exists
    stored_otp = r.get(f"otp:{data.phone}")
    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Delete OTP after successful verification
    r.delete(f"otp:{data.phone}")

    return {"message": f"Login successful. Welcome, {user.name}!"}
