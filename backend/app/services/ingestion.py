import io
from typing import Iterable

import markdown as md
from docx import Document as DocxDocument
from pypdf import PdfReader


def extract_text(file_bytes: bytes, file_name: str) -> str:
    lower_name = file_name.lower()
    if lower_name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if lower_name.endswith(".docx"):
        doc = DocxDocument(io.BytesIO(file_bytes))
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    if lower_name.endswith(".md") or lower_name.endswith(".markdown"):
        return md.markdown(file_bytes.decode("utf-8"))
    return file_bytes.decode("utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> Iterable[str]:
    if not text:
        return []
    start = 0
    chunks: list[str] = []
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks
