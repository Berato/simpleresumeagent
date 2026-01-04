from typing import Optional, List, Dict, Any
from beanie import PydanticObjectId
from app.models.job_description_models import JobDescription

class JobDescriptionRepository:
    """
    Repository for interacting with JobDescription documents in MongoDB.
    """
    
    async def create_job_description(self, job_description: JobDescription) -> JobDescription:
        """
        Create a new job description in the database.
        """
        await job_description.insert()
        return job_description

    async def get_job_description_by_id(self, id: str) -> Optional[JobDescription]:
        """
        Fetch a job description by its ID.
        """
        try:
            oid = PydanticObjectId(id)
            return await JobDescription.get(oid)
        except Exception:
            return None
            
    async def get_job_description_by_url(self, url: str) -> Optional[JobDescription]:
        """
        Fetch a job description by its unique URL.
        """
        return await JobDescription.find_one(JobDescription.url == url)

    async def get_all_job_descriptions(self) -> List[JobDescription]:
        """
        Fetch all job descriptions.
        """
        return await JobDescription.find_all().to_list()

    async def update_job_description(self, id: str, updates: Dict[str, Any]) -> Optional[JobDescription]:
        """
        Update a job description by its ID.
        """
        jd = await self.get_job_description_by_id(id)
        if not jd:
            return None
        
        await jd.set(updates)
        return jd

    async def delete_job_description(self, id: str) -> bool:
        """
        Delete a job description by its ID. Returns True if deleted, False if not found.
        """
        jd = await self.get_job_description_by_id(id)
        if not jd:
            return False
            
        await jd.delete()
        return True
