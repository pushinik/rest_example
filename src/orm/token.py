from datetime import datetime
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field

from orm.user import User

class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    token: str = Field(max_length=100, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=False)

    user: User = Relationship()
