from datetime import datetime
from typing import Optional
from sqlmodel import ForeignKey, SQLModel, Field

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(sa_type=ForeignKey("book.id", ondelete="CASCADE"))
    user_id: int = Field(sa_type=ForeignKey("user.id", ondelete="CASCADE"))
    comment_text: str = Field(max_length=2000)
    rating: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)
    is_approved: bool = Field(default=False)
