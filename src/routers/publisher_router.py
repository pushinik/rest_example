from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_active_user
from db import get_session
from orm.publisher import Publisher
from orm.user import User, Role

publisher_router = APIRouter()

class PublisherCreate(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None

@publisher_router.post("/publishers/", response_model=Publisher)
def create_publisher(
    publisher: PublisherCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_publisher = Publisher(**publisher.model_dump())
    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return db_publisher

@publisher_router.put("/publishers/{publisher_id}", response_model=Publisher)
def update_publisher(
    publisher_id: int,
    publisher: PublisherUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_publisher = session.get(Publisher, publisher_id)
    if not db_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    publisher_data = publisher.model_dump(exclude_unset=True)
    for key, value in publisher_data.items():
        setattr(db_publisher, key, value)

    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return db_publisher

@publisher_router.delete("/publishers/{publisher_id}")
def delete_publisher(
    publisher_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_publisher = session.get(Publisher, publisher_id)
    if not db_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    session.delete(db_publisher)
    session.commit()
    return { "ok": True }

@publisher_router.get("/genres/", response_model=List[Publisher])
def get_publishers(
    current_user: Annotated[User, Depends(get_current_active_user)],
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session)
):
    publishers = session.exec(
        select(Publisher)
        .offset(offset)
        .limit(10)
    ).all()
    return publishers
