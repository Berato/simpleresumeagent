from fastapi import APIRouter, status
from app.models.job_description_models import JobDescriptionRequest
from app.services.job_description_service import JobDescriptionService
from app.models.job_description_models import JobDescriptionResponse

router = APIRouter()

@router.post("/", response_model=JobDescriptionResponse, status_code=status.HTTP_200_OK)
async def store_job_description(job_description: JobDescriptionRequest) -> JobDescriptionResponse:
    """Store job description from a URL"""
    job_description = await JobDescriptionService().extract_job_description(job_description)
    return JobDescriptionResponse(job_description=job_description, message="Job description extracted successfully")
    