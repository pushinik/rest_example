from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_active_user
from db import get_session
from orm.author import Author
from orm.book import Book
from orm.comment import Comment
from orm.book_author import BookAuthor
from orm.book_genre import BookGenre
from orm.genre import Genre
from orm.publisher import Publisher
from orm.user import User, Role

book_router = APIRouter()

class BookCreate(BaseModel):
    title: str
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    publisher_id: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    publisher_id: Optional[int] = None

class BookWithAuthors(BaseModel):
    id: int
    title: str
    publication_year: Optional[int]
    page_count: Optional[int]
    description: Optional[str]
    image_url: Optional[str]
    publisher_id: Optional[int]
    created_at: datetime
    authors: List[Author]
    comments: List[Comment]
    publisher: Optional[Publisher] = None

class CommentCreate(BaseModel):
    comment_text: str
    rating: Optional[int] = None

@book_router.post("/books", response_model=Book)
def create_book(
    book: BookCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    existing_publisher = session.exec(
        select(Publisher).where(Publisher.id == book.publisher_id)
    ).first()
    if not existing_publisher:
        raise HTTPException(status_code=400, detail="Publisher not found")

    db_book = Book(**book.model_dump())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@book_router.put("/books/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: BookUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    existing_publisher = session.exec(
        select(Publisher).where(Publisher.id == book.publisher_id)
    ).first()
    if not existing_publisher:
        raise HTTPException(status_code=400, detail="Publisher not found")

    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = book.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@book_router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(db_book)
    session.commit()
    return { "ok": True }

@book_router.get("/books", response_model=List[BookWithAuthors])
def get_books(
    current_user: Annotated[User, Depends(get_current_active_user)],
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session)
):
    books = session.exec(
        select(Book)
        .offset(offset)
        .limit(10)
    ).all()

    result = []
    for book in books:
        publisher = None
        if book.publisher_id:
            publisher = session.get(Publisher, book.publisher_id)

        authors = session.exec(
            select(Author)
            .join(BookAuthor)
            .where(BookAuthor.book_id == book.id)
        ).all()

        comments = session.exec(
            select(Comment)
            .where((Comment.book_id == book.id) & ((Comment.is_approved == True) | (current_user.role in [Role.MODERATOR])))
        ).all()

        book_dict = book.model_dump()
        book_dict["authors"] = [author.model_dump() for author in authors]
        book_dict["comments"] = [comment.model_dump() for comment in comments]
        book_dict["publisher"] = publisher.model_dump()
        result.append(book_dict)

    return result

@book_router.post("/books/{book_id}/authors/{author_id}")
def add_author_to_book(
    book_id: int,
    author_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    existing = session.exec(
        select(BookAuthor).where(
            BookAuthor.book_id == book_id,
            BookAuthor.author_id == author_id
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    book_author = BookAuthor(book_id=book_id, author_id=author_id)
    session.add(book_author)
    session.commit()
    return {"ok": True}

@book_router.post("/books/{book_id}/genres/{genre_id}")
def add_genre_to_book(
    book_id: int,
    genre_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.EDITOR, Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    genre = session.get(Genre, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    existing = session.exec(
        select(BookGenre).where(
            BookGenre.book_id == book_id,
            BookGenre.genre_id == genre_id
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    book_genre = BookGenre(book_id=book_id, genre_id=genre_id)
    session.add(book_genre)
    session.commit()
    return { "ok": True }

@book_router.post("/books/{book_id}/comments", response_model=Comment)
def add_comment(
    book_id: int,
    comment: CommentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_comment = Comment(
        book_id=book_id,
        user_id=current_user.id,
        comment_text=comment.comment_text,
        rating=comment.rating,
        is_approved=current_user.role in [Role.EDITOR, Role.MODERATOR]
    )
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment
