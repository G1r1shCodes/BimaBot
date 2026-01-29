# AWS Setup Guide for BimaBot

## Prerequisites

1. **AWS Account** with access to:
   - Amazon S3
   - Amazon Textract
   - IAM permissions to create access keys

2. **S3 Bucket**: `bima-bot-hackathon-2026` (must exist and be in `us-east-1`)

---

## Option 1: Using Environment Variables (Recommended for Local Development)

### Step 1: Create `.env` file

Create a file named `.env` in the `bima-bot-backend` directory:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=AKIA...your_access_key...
AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
AWS_REGION=us-east-1
S3_BUCKET_NAME=bima-bot-hackathon-2026
```

### Step 2: Install python-dotenv

```bash
pip install python-dotenv
```

### Step 3: Update main.py to load environment variables

Add this at the top of `app/main.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 4: Restart backend

The server should now have access to AWS credentials.

---

## Option 2: Using AWS CLI Configuration

### Step 1: Install AWS CLI

**Windows**:
Download from: https://aws.amazon.com/cli/

Or use winget:
```powershell
winget install Amazon.AWSCLI
```

**Verify installation**:
```bash
aws --version
```

### Step 2: Configure credentials

```bash
aws configure
```

Enter when prompted:
- AWS Access Key ID: `AKIA...`
- AWS Secret Access Key: `your_secret_key`
- Default region: `us-east-1`
- Default output format: `json`

### Step 3: Test S3 access

```bash
aws s3 ls s3://bima-bot-hackathon-2026/
```

---

## Option 3: Testing Without Real AWS (Development Mode)

If you don't have AWS credentials yet, you can test with **mock AWS services**:

### Install moto (AWS mocking library)

```bash
pip install moto[s3,textract]
```

### Use the test script

Run `test_aws_mock.py` (see separate file) to test without real AWS.

---

## Verification Steps

After setting up credentials, verify the integration:

### 1. Check S3 Connectivity

Run this Python script:

```python
import boto3

s3 = boto3.client('s3', region_name='us-east-1')
try:
    response = s3.list_objects_v2(Bucket='bima-bot-hackathon-2026', MaxKeys=1)
    print("✅ S3 connection successful!")
    print(f"Bucket: bima-bot-hackathon-2026 is accessible")
except Exception as e:
    print(f"❌ S3 connection failed: {e}")
```

### 2. Test File Upload

```python
import boto3
from pathlib import Path

s3 = boto3.client('s3', region_name='us-east-1')

# Create a test file
test_file = Path("test.txt")
test_file.write_text("Hello from BimaBot!")

try:
    s3.upload_file(str(test_file), 'bima-bot-hackathon-2026', 'test/test.txt')
    print("✅ Upload successful!")
    
    # Cleanup
    s3.delete_object(Bucket='bima-bot-hackathon-2026', Key='test/test.txt')
    test_file.unlink()
    print("✅ Cleanup successful!")
except Exception as e:
    print(f"❌ Upload failed: {e}")
```

### 3. Run BimaBot Audit

1. Start backend: `python -m uvicorn app.main:app --reload --port 8000`
2. Start frontend: `npm run dev`
3. Navigate to http://localhost:5173
4. Click "View Sample Bill & Audit"
5. Run sample audit

**Expected behavior**:
- ✅ Audit completes successfully
- ✅ Backend logs show: `"✅ Uploaded ... to s3://..."`
- ✅ Backend logs show: `"🗑️ Deleted ... from S3"`

---

## Troubleshooting

### Error: "NoCredentialsError: Unable to locate credentials"

**Solution**: Credentials not found. Use Option 1 or 2 above.

### Error: "An error occurred (AccessDenied) when calling the ..."

**Solution**: Your AWS account doesn't have permissions. Check IAM policies.

### Error: "An error occurred (NoSuchBucket) when calling the ListObjectsV2 operation"

**Solution**: Create the S3 bucket:
```bash
aws s3 mb s3://bima-bot-hackathon-2026 --region us-east-1
```

### Error: "botocore.exceptions.ClientError: ... InvalidAccessKeyId"

**Solution**: Your access keys are invalid or expired. Generate new ones in AWS Console → IAM → Users → Security Credentials.

---

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `.env` file to git (it's already in `.gitignore`)
- Never share your AWS credentials
- Use IAM roles in production (not access keys)
- Rotate access keys regularly
- Use least-privilege IAM policies
