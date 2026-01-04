from typing import Optional, List, Dict, Any
from beanie import PydanticObjectId
from app.models.cover_letter_model import CoverLetter
from datetime import datetime, timezone

class CoverLetterRepository:
    """
    Repository for interacting with CoverLetter documents.
    """
    
    async def create(self, cover_letter: CoverLetter) -> CoverLetter:
        """
        Create a new cover letter.
        """
        await cover_letter.insert()
        return cover_letter

    async def get_by_id(self, id: str) -> Optional[CoverLetter]:
        """
        Get a cover letter by ID.
        """
        try:
            return await CoverLetter.get(PydanticObjectId(id))
        except Exception:
            return None

    async def get_all(self) -> List[CoverLetter]:
        """
        Get all cover letters.
        """
        return await CoverLetter.find_all().to_list()

    async def update(self, id: str, updates: Dict[str, Any]) -> Optional[CoverLetter]:
        """
        Update a cover letter.
        """
        cover_letter = await self.get_by_id(id)
        if not cover_letter:
            return None
        
        updates['updated_at'] = datetime.now(timezone.utc)
        await cover_letter.set(updates)
        return cover_letter

    async def delete(self, id: str) -> bool:
        """
        Delete a cover letter.
        """
        cover_letter = await self.get_by_id(id)
        if not cover_letter:
            return False
            
        await cover_letter.delete()
        return True
