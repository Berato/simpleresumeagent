from pydantic import BaseModel, Field
from typing import List, Optional

class JobDescriptionData(BaseModel):
    role: str = Field(description="The job title or role name")
    company: str = Field(description="The name of the company hiring")
    summary: str = Field(description="A brief summary of the job")
    responsibilities: List[str] = Field(default_factory=list, description="List of job responsibilities")
    requirements: List[str] = Field(default_factory=list, description="List of job requirements or qualifications")
    benefits: List[str] = Field(default_factory=list, description="List of benefits offered")
    tech_stack: List[str] = Field(default_factory=list, description="List of technologies mentioned")
