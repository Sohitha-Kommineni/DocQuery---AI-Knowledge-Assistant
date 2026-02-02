from datetime import datetime

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class Citation(BaseModel):
    document_id: int
    document_name: str
    snippet: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float
    response_time_ms: int


class QueryLogOut(BaseModel):
    id: int
    question: str
    response: str
    response_time_ms: int
    citations: list[dict]
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True
