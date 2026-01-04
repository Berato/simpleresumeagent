from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.job_description_models import JobDescription
from app.models.resume_model import Resume
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DBService:
    def __init__(self):
        self._client: Optional[AsyncIOMotorClient] = None

    async def start(self):
        """Initialize MongoDB connection and Beanie"""
        if not self._client:
            logger.info("Initializing Database Service...")
            self._client = AsyncIOMotorClient(settings.MONGODB_URL)
            # Add all Beanie document models here
            document_models = [JobDescription, Resume]
            await init_beanie(database=self._client.get_default_database(), document_models=document_models)
            logger.info("Database Service initialized successfully.")

    async def stop(self):
        """Close MongoDB connection"""
        if self._client:
            logger.info("Closing Database Service...")
            self._client.close()
            self._client = None
            logger.info("Database Service closed.")

# Global instance
db_service = DBService()
