from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_active_user
from db import get_session
from orm.author import Author
from orm.user import User, Role

author_router = APIRouter()

class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    biography: Optional[str] = None
    birth_date: Optional[datetime] = None

@author_router.post("/authors", response_model=Author)
def create_author(
    author: AuthorCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_author = Author(**author.model_dump())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@author_router.put("/authors/{author_id}", response_model=Author)
def update_author(
    author_id: int,
    author: AuthorUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    author_data = author.model_dump(exclude_unset=True)
    for key, value in author_data.items():
        setattr(db_author, key, value)

    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@author_router.delete("/authors/{author_id}")
def delete_author(
    author_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    session.delete(db_author)
    session.commit()
    return { "ok": True }

@author_router.get("/authors/", response_model=List[Author])
def get_authors(
    current_user: Annotated[User, Depends(get_current_active_user)],
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session)
):
    authors = session.exec(
        select(Author)
        .offset(offset)
        .limit(10)
    ).all()
    return authors
