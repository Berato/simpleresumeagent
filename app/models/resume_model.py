from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from app.models.resume_data import ResumeData

class Resume(Document):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    content: ResumeData  # Embed the extraction result here
    original_text: str   # Store raw extracted text for reference

    class Settings:
        name = "resumes"
