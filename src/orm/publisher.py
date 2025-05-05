from datetime import datetime
from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field

class Publisher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    address: Optional[str] = Field(default=None, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=20)
    created_at: datetime = Field(default_factory=datetime.now)

    books: List["Book"] = Relationship(back_populates="publisher")
