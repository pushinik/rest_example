from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel, Field, EmailStr
from sqlmodel import Session, select

from auth import hash_password
from db import get_session
from orm.user import User

register_router = APIRouter()

class RegisterUser(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: Optional[str] = Field(max_length=20)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

@register_router.post("/register")
def post_register(user_data: Annotated[RegisterUser, Form()], session: Session = Depends(get_session)):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user_data.password)
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        email=user_data.email,
        password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return { "message": "User registered successfully" }
