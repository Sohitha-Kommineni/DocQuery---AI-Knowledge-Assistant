from pydantic import BaseModel

from app.db.models import UserRole


class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole
    department: str | None

    class Config:
        from_attributes = True
