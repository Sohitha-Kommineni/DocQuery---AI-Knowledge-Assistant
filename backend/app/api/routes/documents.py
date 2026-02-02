from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import AccessLevel, Document, DocumentChunk, User, UserRole
from app.schemas.documents import DocumentOut, DocumentUpdate
from app.services.ingestion import chunk_text, extract_text
from app.services.rag import embed_texts
from app.services.storage import upload_to_s3


router = APIRouter(prefix="/documents")


@router.get("", response_model=list[DocumentOut])
def list_documents(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[DocumentOut]:
    query = db.query(Document)
    if user.role == UserRole.admin:
        return query.order_by(Document.uploaded_at.desc()).all()
    if user.role == UserRole.manager:
        query = query.filter(
            (Document.access_level == AccessLevel.public)
            | (
                (Document.access_level == AccessLevel.department)
                & (Document.department == user.department)
            )
        )
        return query.order_by(Document.uploaded_at.desc()).all()
    query = query.filter(Document.access_level == AccessLevel.public)
    return query.order_by(Document.uploaded_at.desc()).all()


@router.post("/upload", response_model=DocumentOut)
def upload_document(
    file: UploadFile = File(...),
    tags: str | None = Form(default=None),
    department: str | None = Form(default=None),
    access_level: AccessLevel = Form(default=AccessLevel.public),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DocumentOut:
    if user.role == UserRole.employee and access_level != AccessLevel.public:
        raise HTTPException(status_code=403, detail="Only admins or managers can restrict access")

    file_bytes = file.file.read()
    s3_key = upload_to_s3(file_bytes, file.filename)
    text = extract_text(file_bytes, file.filename)
    chunks = list(chunk_text(text))
    embeddings = embed_texts(chunks)

    document = Document(
        name=file.filename,
        file_type=file.content_type or "unknown",
        s3_key=s3_key,
        department=department,
        access_level=access_level,
        tags=tags,
    )
    db.add(document)
    db.flush()

    for content, embedding in zip(chunks, embeddings):
        db.add(DocumentChunk(document_id=document.id, content=content, embedding=embedding))
    db.commit()
    db.refresh(document)
    return document


@router.patch("/{document_id}", response_model=DocumentOut)
def update_document(
    document_id: int,
    payload: DocumentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DocumentOut:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin only")
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(document, field, value)
    db.commit()
    db.refresh(document)
    return document
