from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Simple Resume Agent"
    API_V1_STR: str = "/api/v1"
    MONGODB_URL: str = "mongodb://admin:password@localhost:27018/simpleresume?authSource=admin"

    class Config:
        case_sensitive = True

settings = Settings()
