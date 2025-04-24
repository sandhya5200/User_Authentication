from pydantic import BaseModel, EmailStr, field_validator
import re

class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

    @field_validator("name")
    def name_length(name):
        if len(name) < 8:
            raise ValueError("Name must be atleast 8 characters")
        return name
    
    @field_validator("phone")
    def phone_valid(phone):
        pattern = r'^\+\d{1,4}\d{10}$'
        if not re.match(pattern,phone):
            raise ValueError("Phone number must include country code and then 10 digits")
        return phone
    
    @field_validator("password")
    def password_strength(password):
        if len(password) < 8:
            raise ValueError("Password should have atleast 8 characters")
        return password


class LoginSchema(BaseModel):
    phone: str
    password: str

class OTPVerifySchema(BaseModel):
    phone: str
    otp: str
