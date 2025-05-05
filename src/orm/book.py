from datetime import datetime
from typing import List, Optional
from sqlmodel import ForeignKey, Relationship, SQLModel, Field

from orm.book_author import BookAuthor
from orm.book_genre import BookGenre

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=100)
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    description: Optional[str] = Field(default=None, max_length=2000)
    image_url: Optional[str] = Field(default=None, max_length=200)
    publisher_id: Optional[int] = Field(default=None, sa_type=ForeignKey("publisher.id", ondelete="SET NULL"))
    created_at: datetime = Field(default_factory=datetime.now)

    genres: List["Genre"] = Relationship(back_populates="books", link_model=BookGenre)
    authors: List["Author"] = Relationship(back_populates="books", link_model=BookAuthor)
    publisher: Optional["Publisher"] = Relationship(back_populates="books")
