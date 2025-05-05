from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(foreign_key="comment.id")
    user_id: int = Field(foreign_key="user.id")
    reason_text: str = Field(max_length=1000)
    created_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
