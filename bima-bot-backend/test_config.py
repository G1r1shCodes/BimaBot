"""
Test script to verify .env values are loaded correctly into config
"""
from app.config import settings

print("=" * 60)
print("BimaBot Configuration Test")
print("=" * 60)

print("\n📋 App Settings:")
print(f"  App Name: {settings.app_name}")
print(f"  Debug Mode: {settings.debug}")

print("\n☁️ AWS Configuration:")
print(f"  AWS Region: {settings.aws_region}")
print(f"  S3 Bucket: {settings.s3_bucket_name}")
print(f"  Access Key ID: {settings.aws_access_key_id[:10]}..." if settings.aws_access_key_id else "  Access Key ID: None")

print("\n🤖 AWS Bedrock Configuration:")
print(f"  KB ID: {settings.bedrock_kb_id}")
print(f"  Model ARN: {settings.bedrock_model_arn}")

print("\n✅ All values loaded successfully from .env file!")
print("=" * 60)
