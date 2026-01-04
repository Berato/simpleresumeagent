from typing import List, Optional, Dict, Any
from app.models.cover_letter_model import CoverLetter
from app.repositories.cover_letter_repository import CoverLetterRepository

class CoverLetterService:
    def __init__(self):
        self.repository = CoverLetterRepository()

    async def create_cover_letter(self, data: CoverLetter) -> CoverLetter:
        return await self.repository.create(data)

    async def get_cover_letter(self, id: str) -> Optional[CoverLetter]:
        return await self.repository.get_by_id(id)

    async def get_all_cover_letters(self) -> List[CoverLetter]:
        return await self.repository.get_all()

    async def update_cover_letter(self, id: str, updates: Dict[str, Any]) -> Optional[CoverLetter]:
        return await self.repository.update(id, updates)

    async def delete_cover_letter(self, id: str) -> bool:
        return await self.repository.delete(id)
