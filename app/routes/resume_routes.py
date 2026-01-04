from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.resume_service import ResumeService
from app.models.resume_model import Resume

router = APIRouter()
resume_service = ResumeService()

@router.post("/upload", response_model=Resume)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        resume = await resume_service.extract_and_save_resume(content)
        return resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
