from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CoverLetterData(BaseModel):
    """
    Pure Pydantic model for Cover Letter data content.
    Used for ADK compatibility and separation of concerns.
    """
    title: str
    client_name: str = Field(alias="clientName")
    hiring_manager: Optional[str] = Field(None, alias="hiringManager")
    job_details: Dict[str, Any] = Field(default_factory=dict, alias="jobDetails")
    opening_paragraph: Optional[str] = Field(None, alias="openingParagraph")
    body_paragraphs: Optional[List[str]] = Field(None, alias="bodyParagraphs")
    company_connection: Optional[str] = Field(None, alias="companyConnection")
    closing_paragraph: Optional[str] = Field(None, alias="closingParagraph")
    word_count: int = Field(0, alias="wordCount")

    class Config:
        populate_by_name = True
