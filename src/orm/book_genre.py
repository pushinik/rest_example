from sqlmodel import SQLModel, Field

class BookGenre(SQLModel, table=True):
    book_id: int = Field(foreign_key="book.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)
