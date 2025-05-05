from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    user_id: int = Field(foreign_key="user.id")
    comment_text: str = Field(max_length=2000)
    rating: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    is_approved: bool = Field(default=False)
