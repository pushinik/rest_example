from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import IntEnum

class Role(IntEnum):
    USER = 0
    EDITOR = 1
    MODERATOR = 2

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=100)
    last_name: str = Field(index=True, max_length=100)
    email: str = Field(index=True, unique=True, max_length=150)
    password: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    joined_at: datetime = Field(default_factory=datetime.now)
    role: Role = Field(default=Role.USER)
    is_active: bool = Field(default=True)
