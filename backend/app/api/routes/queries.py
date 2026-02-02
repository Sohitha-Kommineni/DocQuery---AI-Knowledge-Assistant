from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import QueryLog, User
from app.schemas.queries import QueryLogOut, QueryRequest, QueryResponse
from app.services.rag import run_rag


router = APIRouter(prefix="/queries")


@router.post("/ask", response_model=QueryResponse)
def ask_question(
    payload: QueryRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> QueryResponse:
    answer, citations, confidence, response_time_ms = run_rag(db, user, payload.question)
    log = QueryLog(
        user_id=user.id,
        question=payload.question,
        response=answer,
        response_time_ms=response_time_ms,
        citations=citations,
        confidence=confidence,
    )
    db.add(log)
    db.commit()
    return QueryResponse(
        answer=answer,
        citations=citations,
        confidence=confidence,
        response_time_ms=response_time_ms,
    )


@router.get("", response_model=list[QueryLogOut])
def list_queries(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[QueryLogOut]:
    return (
        db.query(QueryLog)
        .filter(QueryLog.user_id == user.id)
        .order_by(QueryLog.created_at.desc())
        .limit(50)
        .all()
    )
