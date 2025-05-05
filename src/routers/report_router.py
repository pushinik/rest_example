from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_active_user
from db import get_session
from orm.comment import Comment
from orm.report import Report
from orm.user import User, Role

report_router = APIRouter()

class ReportCreate(BaseModel):
    reason_text: str

@report_router.post("/comments/{comment_id}/reports", response_model=Report)
def report_comment(
    comment_id: int,
    report: ReportCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    existing = session.exec(
        select(Report).where(
            Report.comment_id == comment_id,
            Report.user_id == current_user.id
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You already reported this comment")

    db_report = Report(
        comment_id=comment_id,
        user_id=current_user.id,
        reason_text=report.reason_text
    )
    session.add(db_report)
    session.commit()
    session.refresh(db_report)
    return db_report

@report_router.get("/reports/", response_model=List[Report])
def list_reports(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    reports = session.exec(select(Report).where(Report.resolved_at == None)).all()
    return reports

@report_router.post("/reports/{report_id}/approve")
def approve_report(
    report_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    comment = session.get(Comment, report.comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    report.resolved_at = datetime.now()

    session.delete(comment)

    session.add(report)
    session.commit()
    return { "ok": True }

@report_router.post("/comments/{comment_id}/approve")
def approve_comment(
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.is_approved = True
    session.add(comment)
    session.commit()
    return { "ok": True }

@report_router.post("/users/{user_id}/block")
def block_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.role not in [Role.MODERATOR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == Role.MODERATOR:
        raise HTTPException(status_code=403, detail="Cannot block moderator")

    user.is_active = False
    session.add(user)
    session.commit()
    return { "ok": True }
