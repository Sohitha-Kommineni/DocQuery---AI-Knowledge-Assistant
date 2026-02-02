from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    document_count: int
    query_count: int
    recent_questions: list[str]
    frequent_questions: list[str]
    unanswered_questions: list[str]
