from pydantic import BaseModel
from typing import Optional
from beanie import Document, Indexed
from app.models.job_description_data import JobDescriptionData

class JobDescription(Document):
    url: Indexed(str, unique=True)
    title: Optional[str] = None
    description: Optional[str] = None
    structured_data: Optional[JobDescriptionData] = None

    class Settings:
        name = "job_descriptions"

class JobDescriptionRequest(BaseModel):
    url: str

class JobDescriptionResponse(BaseModel):
    message: Optional[str] = None   
    job_description: Optional[JobDescription] = None