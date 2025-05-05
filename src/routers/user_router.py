from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from auth import generate_random_token, get_current_active_user, hash_password
from db import get_session
from mailer import send_email
from orm.token import Token
from orm.user import User

user_router = APIRouter()

class ResetPasswordRequest(BaseModel):
    email: EmailStr

class UpdatePasswordRequest(BaseModel):
    password_token: str

@user_router.get("/user")
def get_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.phone
    }

@user_router.post("/reset_password")
def post_reset_password(request_data: Annotated[ResetPasswordRequest, Form()], session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(User.email == request_data.email)
    ).first()
    if user:
        access_token = generate_random_token()
        token = Token(
            token=access_token,
            user_id=user.id
        )
        session.add(token)
        session.commit()
        session.refresh(token)
        send_email(request_data.email, "Password Reset Key", f"Your password reset key: {token.token}")
    return { "message": "Password reset key sent to your email if registered on the site" }

@user_router.post("/update_password")
def post_reset_password(request_data: Annotated[UpdatePasswordRequest, Form()], session: Session = Depends(get_session)):
    token = session.exec(
        select(Token).where(Token.token == request_data.password_token)
    ).first()
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    session.delete(token)
    password = generate_random_token(6)
    token.user.password = hash_password(password)
    session.commit()
    send_email(token.user.email, "New Password", f"Your new password: {password}")
    return { "message": "Your new password has been sent to your email" }
