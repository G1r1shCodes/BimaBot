from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "BimaBot Backend"
    debug: bool = True
    
    # File storage
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 10
    
    # AWS Configuration (Phase 4.2)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    s3_bucket_name: Optional[str] = None
    
    # AWS Bedrock Configuration (RAG + AI Services)
    bedrock_kb_id: Optional[str] = None
    bedrock_model_arn: Optional[str] = None
    
    class Config:
        env_file = ".env"


settings = Settings()
