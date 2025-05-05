from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=100)
    publication_year: Optional[int] = None
    page_count: Optional[int] = None
    description: Optional[str] = Field(default=None, max_length=2000)
    image_url: Optional[str] = Field(default=None, max_length=200)
    publisher_id: Optional[int] = Field(default=None, foreign_key="publisher.id")
    created_at: datetime = Field(default_factory=datetime.now)
