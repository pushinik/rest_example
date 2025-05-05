from sqlmodel import ForeignKey, SQLModel, Field

class BookAuthor(SQLModel, table=True):
    book_id: int = Field(sa_type=ForeignKey("book.id", ondelete="CASCADE"), primary_key=True)
    author_id: int = Field(sa_type=ForeignKey("author.id", ondelete="CASCADE"), primary_key=True)
