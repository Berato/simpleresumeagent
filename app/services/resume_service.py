from app.services.pdf_service import PdfService
from app.services.llm_extraction_service import LLMExtractionService
from app.models.resume_model import Resume
from fastapi import UploadFile

from app.repositories.resume_repository import ResumeRepository

class ResumeService:
    def __init__(self):
        self.pdf_service = PdfService()
        self.llm_service = LLMExtractionService()
        self.resume_repository = ResumeRepository()

    

    async def extract_and_save_resume(self, file_content: bytes) -> Resume:
        """
        Orchestrates the resume extraction process:
        1. Extract text from PDF
        2. Extract structured data using LLM
        3. Save to database
        """
        # 1. Extract text
        raw_text = self.pdf_service.extract_text_from_pdf(file_content)
        
        # 2. Extract structured data
        # Note: In a real scenario, you might want to handle potential LLM failures
        try:
            resume_data = await self.llm_service.extract_resume_data(raw_text)
        except Exception as e:
            # Fallback or re-raise. For now, we allow it to fail but this could be improved
            raise ValueError(f"LLM Extraction failed: {str(e)}")
        
        # 3. Save to database
        resume = Resume(
            content=resume_data,
            original_text=raw_text
        )
        return await self.resume_repository.create_resume(resume)
        
        return resume