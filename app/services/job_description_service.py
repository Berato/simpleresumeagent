from bs4 import BeautifulSoup
from app.models.job_description_models import JobDescription, JobDescriptionRequest
from app.services.browser_service import browser_service

class JobDescriptionService:
    def __init__(self):
        self.browser_service = browser_service

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

        job_desc = JobDescription(
            url=job_description_request.url,
            title=title,
            description=description
        )

        # Store in MongoDB
        try:
            await job_desc.insert()
        except Exception as e:
            # If it already exists, we might want to update it or just return the existing one
            # For now, let's just log and continue, or fetch existing
            existing = await JobDescription.find_one(JobDescription.url == job_description_request.url)
            if existing:
                job_desc = existing

        return job_desc
    