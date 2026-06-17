import io
from fastapi import APIRouter, HTTPException, File, UploadFile
from services.pdf_extractor import extract_resume_from_stream

router = APIRouter(prefix="/extract-resume", tags=["extraction"])


@router.post("")
async def extract_resume(file: UploadFile = File(...)):
    """
    Receives an uploaded PDF file stream, extracts and structures its text,
    and returns it to NestJS.
    """
    try:
        content = await file.read()
        pdf_stream = io.BytesIO(content)
        result = extract_resume_from_stream(pdf_stream)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
