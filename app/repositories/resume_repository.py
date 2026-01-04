from typing import Optional, List, Dict, Any
from beanie import PydanticObjectId
from app.models.resume_model import Resume

class ResumeRepository:
    """
    Repository for interacting with Resume documents in MongoDB.
    """
    
    async def create_resume(self, resume: Resume) -> Resume:
        """
        Create a new resume in the database.
        """
        await resume.insert()
        return resume

    async def get_resume_by_id(self, resume_id: str) -> Optional[Resume]:
        """
        Fetch a resume by its ID.
        """
        try:
            oid = PydanticObjectId(resume_id)
            return await Resume.get(oid)
        except Exception:
            return None

    async def get_all_resumes(self) -> List[Resume]:
        """
        Fetch all resumes.
        """
        return await Resume.find_all().to_list()

    async def update_resume(self, resume_id: str, updates: Dict[str, Any]) -> Optional[Resume]:
        """
        Update a resume by its ID.
        """
        resume = await self.get_resume_by_id(resume_id)
        if not resume:
            return None
        
        # Determine how to clear specific fields if needed, 
        # but basic update is usually just setting fields
        # set(updates) is beanie syntax for update
        await resume.set(updates)
        return resume

    async def delete_resume(self, resume_id: str) -> bool:
        """
        Delete a resume by its ID. Returns True if deleted, False if not found.
        """
        resume = await self.get_resume_by_id(resume_id)
        if not resume:
            return False
            
        await resume.delete()
        return True
