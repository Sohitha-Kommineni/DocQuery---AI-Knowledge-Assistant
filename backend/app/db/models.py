from datetime import datetime
from enum import Enum

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

from app.core.config import settings
from app.core.security import hash_password


class Base(DeclarativeBase):
    pass


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"


class AccessLevel(str, Enum):
    public = "public"
    department = "department"
    admin_only = "admin_only"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.employee)
    department: Mapped[str | None] = mapped_column(String(120), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    queries: Mapped[list["QueryLog"]] = relationship(back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(50))
    s3_key: Mapped[str] = mapped_column(String(512))
    department: Mapped[str | None] = mapped_column(String(120), default=None)
    access_level: Mapped[AccessLevel] = mapped_column(SqlEnum(AccessLevel), default=AccessLevel.public)
    tags: Mapped[str | None] = mapped_column(String(255), default=None)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.vector_dimension))

    document: Mapped["Document"] = relationship(back_populates="chunks")


class QueryLog(Base):
    __tablename__ = "query_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)
    response_time_ms: Mapped[int] = mapped_column(Integer)
    citations: Mapped[list[dict]] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="queries")


def ensure_seed_data(db: Session) -> None:
    if db.query(User).filter(User.username == "admin").first():
        return
    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),
        role=UserRole.admin,
        department="IT",
    )
    db.add(admin)
    db.commit()
