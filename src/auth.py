from hashlib import sha256
from http.client import HTTPException
import random
import string
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from db import get_session
from orm.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_by_token(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    existing_token = session.exec(
        select(Token).where(Token.token == token)
    ).first()
    if not existing_token or not existing_token.is_active:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return existing_token.user

def get_current_active_user(user: Annotated[Token, Depends(get_user_by_token)],):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

def generate_random_token(length=100):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def verify_password(plain_password: str, hashed_password: str):
    return sha256(plain_password.encode("utf-8")).hexdigest() == hashed_password

def hash_password(plain_password: str):
    return sha256(plain_password.encode("utf-8")).hexdigest()
