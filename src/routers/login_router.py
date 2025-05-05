from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from auth import generate_random_token, verify_password
from db import get_session
from orm.user import User
from orm.token import Token

login_router = APIRouter()

@login_router.post("/login")
async def post_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = generate_random_token()
    token = Token(
        token=access_token,
        user_id=user.id,
        is_active=True
    )
    session.add(token)
    session.commit()
    session.refresh(token)
    return { "access_token": access_token }
