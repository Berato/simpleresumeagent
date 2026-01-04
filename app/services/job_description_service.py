from bs4 import BeautifulSoup
from app.models.job_description_models import JobDescription, JobDescriptionRequest
from app.models.job_description_models import JobDescription, JobDescriptionRequest
from app.services.browser_service import browser_service
from app.services.llm_extraction_service import LLMExtractionService
from app.repositories.job_description_repository import JobDescriptionRepository

class JobDescriptionService:
    def __init__(self):
        self.browser_service = browser_service
        self.llm_service = LLMExtractionService()
        self.repository = JobDescriptionRepository()

    async def extract_job_description(self, job_description_request: JobDescriptionRequest) -> JobDescription:
        """Extract job description using Playwright and BeautifulSoup"""
        html = await self.browser_service.fetch_html(job_description_request.url)
        soup = BeautifulSoup(html, "html.parser")
    
        title = soup.title.string if soup.title else None
    
        # Try to find a reasonable description (some heuristics)
        # This is a basic implementation, can be improved with better selectors
        description = ""
        main_content = soup.find('main') or soup.find('article') or soup.body
        if main_content:
            description = main_content.get_text(separator="\n", strip=True)

        # Extract structured data
        try:
            structured_data = await self.llm_service.extract_job_description_data(description)
        except Exception as e:
            print(f"LLM Extraction failed for JD: {e}")
            structured_data = None

        job_desc = JobDescription(
            url=job_description_request.url,
            title=title,
            description=description,
            structured_data=structured_data
        )

        # Store in MongoDB via Repository
        try:
            await self.repository.create_job_description(job_desc)
        except Exception as e:
            # If it already exists, we might want to update it or just return the existing one
            # For now, let's just log and continue, or fetch existing
            existing = await self.repository.get_job_description_by_url(job_description_request.url)
            if existing:
                # Update existing with new data if applicable? 
                # For now just return existing
                job_desc = existing
        
        return job_desc