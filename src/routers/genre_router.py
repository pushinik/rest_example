from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_active_user
from db import get_session
from orm.genre import Genre
from orm.user import User, Role

genre_router = APIRouter()

class GenreCreate(BaseModel):
    name: str
    description: Optional[str] = None

class GenreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

@genre_router.post("/genres", response_model=Genre)
def create_genre(
    genre: GenreCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_genre = Genre(**genre.model_dump())
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre

@genre_router.put("/genres/{genre_id}", response_model=Genre)
def update_genre(
    genre_id: int,
    genre: GenreUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    genre_data = genre.model_dump(exclude_unset=True)
    for key, value in genre_data.items():
        setattr(db_genre, key, value)

    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre

@genre_router.delete("/genres/{genre_id}")
def delete_genre(
    genre_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    session.delete(db_genre)
    session.commit()
    return { "ok": True }

@genre_router.get("/genres/", response_model=List[Genre])
def get_genres(
    current_user: Annotated[User, Depends(get_current_active_user)],
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session)
):
    genres = session.exec(
        select(Genre)
        .offset(offset)
        .limit(10)
    ).all()
    return genres
