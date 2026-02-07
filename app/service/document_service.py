from fastapi import UploadFile
from pypdf import PdfReader
from app.database.chroma_db import store_chunks

def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap

    return chunks


async def process_and_store_document(file: UploadFile) -> int:
    text = ""

    # 📄 PDF handling
    if file.filename.lower().endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    # 📄 TXT handling
    else:
        content = await file.read()
        text = content.decode("utf-8")

    if not text.strip():
        raise ValueError("Document is empty or unreadable")

    chunks = chunk_text(text)

    store_chunks(chunks)

    return len(chunks)
