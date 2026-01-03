from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import hello
from app.core.config import settings
from app.routes import job_description_routes

from app.services.browser_service import browser_service

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.job_description_models import JobDescription

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up...")
    
    # Initialize Beanie
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client.get_default_database(), document_models=[JobDescription])
    
    await browser_service.start()
    yield
    # Teardown logic
    print("Shutting down...")
    await browser_service.stop()

def get_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

    _app.include_router(hello.router, prefix="/hello", tags=["hello"])
    _app.include_router(job_description_routes.router, tags=["job-descriptions"])

    @_app.get("/")
    def root():
        return {"message": "Welcome to the Simple Resume Agent API"}

    return _app

app = get_application()
