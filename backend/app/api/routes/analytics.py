from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import Document, QueryLog, User
from app.schemas.analytics import AnalyticsOverview


router = APIRouter(prefix="/analytics")


@router.get("/overview", response_model=AnalyticsOverview)
def overview(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AnalyticsOverview:
    document_count = db.query(func.count(Document.id)).scalar() or 0
    query_count = db.query(func.count(QueryLog.id)).filter(QueryLog.user_id == user.id).scalar() or 0
    recent_questions = [
        q.question
        for q in (
            db.query(QueryLog)
            .filter(QueryLog.user_id == user.id)
            .order_by(QueryLog.created_at.desc())
            .limit(5)
            .all()
        )
    ]
    frequent_questions = [
        row[0]
        for row in (
            db.query(QueryLog.question, func.count(QueryLog.id).label("count"))
            .filter(QueryLog.user_id == user.id)
            .group_by(QueryLog.question)
            .order_by(func.count(QueryLog.id).desc())
            .limit(5)
            .all()
        )
    ]
    unanswered_questions = [
        q.question
        for q in (
            db.query(QueryLog)
            .filter(QueryLog.user_id == user.id)
            .filter(QueryLog.confidence < 0.3)
            .order_by(QueryLog.created_at.desc())
            .limit(5)
            .all()
        )
    ]
    return AnalyticsOverview(
        document_count=document_count,
        query_count=query_count,
        recent_questions=recent_questions,
        frequent_questions=frequent_questions,
        unanswered_questions=unanswered_questions,
    )
