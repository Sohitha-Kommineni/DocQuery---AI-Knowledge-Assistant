from datetime import datetime

from pydantic import BaseModel

from app.db.models import AccessLevel


class DocumentOut(BaseModel):
    id: int
    name: str
    file_type: str
    department: str | None
    access_level: AccessLevel
    tags: str | None
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    tags: str | None = None
    department: str | None = None
    access_level: AccessLevel | None = None
