from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.pdf_extractor import extract_resume_from_path

router = APIRouter(prefix="/extract-resume", tags=["extraction"])


class ExtractRequest(BaseModel):
    file_path: str


@router.post("")
def extract_resume(request: ExtractRequest):
    """
    Receives the absolute path of an uploaded PDF (written by NestJS),
    extracts and structures its text, and returns it to NestJS.
    """
    try:
        result = extract_resume_from_path(request.file_path)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found at provided path.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
