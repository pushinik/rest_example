from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

from orm.book_genre import BookGenre

class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)

    books: List["Book"] = Relationship(back_populates="genres", link_model=BookGenre)
