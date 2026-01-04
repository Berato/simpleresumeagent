from pydantic import BaseModel, Field
from typing import List, Optional

class Education(BaseModel):
    institution: str
    degree: Optional[str] = None
    date: Optional[str] = None

class WorkExperience(BaseModel):
    company: str
    role: str
    date: Optional[str] = None
    description: List[str] = [] # Bullet points
    location: Optional[str] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = []
    url: Optional[str] = None

class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None

class ResumeData(BaseModel):
    full_name: str
    summary: Optional[str] = None
    contact: ContactInfo = Field(default_factory=ContactInfo)
    skills: List[str] = []
    education: List[Education] = []
    experience: List[WorkExperience] = []
    projects: List[Project] = []
