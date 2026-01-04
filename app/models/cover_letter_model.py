from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from beanie import Document
from pydantic import BaseModel, Field
from app.models.cover_letter_data import CoverLetterData

class CoverLetter(Document):
    """
    Cover Letter document model.
    Contains metadata and the embedded CoverLetterData content.
    """
    content: CoverLetterData
    resume_id: str
    job_profile_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    class Settings:
        name = "cover_letters"

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "content": {
                    "title": "Software Engineer Cover Letter",
                    "clientName": "Acme Corp",
                    "wordCount": 300
                },
                "resume_id": "60d5ecb8b5c9e62c1c8f1f11"
            }
        }

class CoverLetterCreate(BaseModel):
    # Flattened input for DX, mapped to structure in Service/Router
    title: str
    client_name: str = Field(alias="clientName")
    hiring_manager: Optional[str] = Field(None, alias="hiringManager")
    job_details: Dict[str, Any] = Field(default_factory=dict, alias="jobDetails")
    resume_id: str
    job_profile_id: Optional[str] = None
    word_count: int = Field(0, alias="wordCount")
    opening_paragraph: Optional[str] = Field(None, alias="openingParagraph")
    body_paragraphs: Optional[List[str]] = Field(None, alias="bodyParagraphs")
    company_connection: Optional[str] = Field(None, alias="companyConnection")
    closing_paragraph: Optional[str] = Field(None, alias="closingParagraph")

class CoverLetterUpdate(BaseModel):
    title: Optional[str] = None
    client_name: Optional[str] = Field(None, alias="clientName")
    hiring_manager: Optional[str] = Field(None, alias="hiringManager")
    job_details: Optional[Dict[str, Any]] = Field(None, alias="jobDetails")
    resume_id: Optional[str] = None
    job_profile_id: Optional[str] = None
    word_count: Optional[int] = Field(None, alias="wordCount")
    opening_paragraph: Optional[str] = Field(None, alias="openingParagraph")
    body_paragraphs: Optional[List[str]] = Field(None, alias="bodyParagraphs")
    company_connection: Optional[str] = Field(None, alias="companyConnection")
    closing_paragraph: Optional[str] = Field(None, alias="closingParagraph")
