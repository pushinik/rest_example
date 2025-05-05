from datetime import datetime
from typing import Optional
from sqlmodel import ForeignKey, SQLModel, Field

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(sa_type=ForeignKey("comment.id", ondelete="CASCADE"))
    user_id: int = Field(sa_type=ForeignKey("user.id", ondelete="CASCADE"))
    reason_text: str = Field(max_length=1000)
    created_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
