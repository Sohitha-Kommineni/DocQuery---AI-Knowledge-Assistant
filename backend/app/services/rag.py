import time
from typing import Iterable

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import AccessLevel, Document, DocumentChunk, User, UserRole


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    texts_list = list(texts)
    if not texts_list:
        return []
    if settings.llm_provider != "openai" or not settings.openai_api_key:
        return [[0.0] * settings.vector_dimension for _ in texts_list]
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(model=settings.openai_embedding_model, input=texts_list)
    return [item.embedding for item in response.data]


def _role_filters(user: User):
    if user.role == UserRole.admin:
        return None
    if user.role == UserRole.manager:
        return (
            (Document.access_level == AccessLevel.public)
            | ((Document.access_level == AccessLevel.department) & (Document.department == user.department))
        )
    return Document.access_level == AccessLevel.public


def retrieve_relevant_chunks(db: Session, user: User, query_embedding: list[float], limit: int = 6):
    filters = _role_filters(user)
    stmt = select(DocumentChunk, Document).join(Document, Document.id == DocumentChunk.document_id)
    if filters is not None:
        stmt = stmt.where(filters)
    stmt = stmt.order_by(DocumentChunk.embedding.cosine_distance(query_embedding)).limit(limit)
    return db.execute(stmt).all()


def generate_answer(
    question: str,
    chunks: list[tuple[DocumentChunk, Document]],
) -> tuple[str, list[dict], float]:
    if not chunks:
        return "I don't know.", [], 0.0

    context = "\n\n".join(
        f"[{doc.id}] {doc.name}\n{chunk.content}" for chunk, doc in chunks
    )
    citations = [
        {"document_id": doc.id, "document_name": doc.name, "snippet": chunk.content[:240]}
        for chunk, doc in chunks
    ]

    if settings.llm_provider != "openai" or not settings.openai_api_key:
        answer = f"Based on {len(chunks)} document excerpts: {citations[0]['snippet']}"
        return answer, citations, 0.4

    client = OpenAI(api_key=settings.openai_api_key)
    prompt = (
        "You are an enterprise knowledge assistant. "
        "Answer using only the provided context. "
        "If the answer is not contained, say \"I don't know.\".\n\n"
        f"Context:\n{context}\n\nQuestion:\n{question}\nAnswer:"
    )
    response = client.responses.create(
        model=settings.openai_model,
        input=prompt,
        temperature=0.1,
    )
    answer = response.output_text.strip() if response.output_text else "I don't know."
    confidence = 0.75 if answer != "I don't know." else 0.1
    return answer, citations, confidence


def run_rag(db: Session, user: User, question: str):
    start = time.time()
    query_embedding = embed_texts([question])[0]
    results = retrieve_relevant_chunks(db, user, query_embedding)
    chunks = [(row[0], row[1]) for row in results]
    answer, citations, confidence = generate_answer(question, chunks)
    response_time_ms = int((time.time() - start) * 1000)
    return answer, citations, confidence, response_time_ms
