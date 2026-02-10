from fastapi import APIRouter, UploadFile, File, HTTPException
from app.service.document_service import process_and_store_document

router = APIRouter( tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )

    chunks_count = await process_and_store_document(file)

    return {
        "message": "Document uploaded and indexed successfully",
        "chunks_indexed": chunks_count,
        "filename": file.filename
    }
