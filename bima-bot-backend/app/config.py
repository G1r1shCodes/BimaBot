from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "BimaBot Backend"
    debug: bool = True
    
    # File storage
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 10
    
    # OCR (Phase 4)
    tesseract_path: Optional[str] = None
    
    # AI (Phase 5)
    llm_model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    llm_api_key: Optional[str] = None
    
    # AWS Configuration (Phase 4.2)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()
