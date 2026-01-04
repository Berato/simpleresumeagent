from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import hello
from app.core.config import settings
from app.routes import job_description_routes

from app.services.browser_service import browser_service
from app.services.db_service import db_service
from app.routes import resume_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting up...")
    
    # Initialize Services
    await db_service.start()
    await browser_service.start()
    
    yield
    
    # Teardown logic
    print("Shutting down...")
    await browser_service.stop()
    await db_service.stop()

def get_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

    _app.include_router(hello.router, prefix="/hello", tags=["hello"])
    _app.include_router(job_description_routes.router, tags=["job-descriptions"])
    _app.include_router(resume_routes.router, prefix="/api/resumes", tags=["resumes"])

    @_app.get("/")
    def root():
        return {"message": "Welcome to the Simple Resume Agent API"}

    return _app

app = get_application()
