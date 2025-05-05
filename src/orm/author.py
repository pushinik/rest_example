from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from orm.book_author import BookAuthor

class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(index=True, max_length=100)
    biography: Optional[str] = Field(default=None, max_length=2000)
    birth_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

    books: List["Book"] = Relationship(back_populates="authors", link_model=BookAuthor)
