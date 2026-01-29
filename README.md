# BimaBot
BimaBot is a Insurance Claim Audit System

## 🚀 Getting Started

### 1. Frontend (React + Vite)
The frontend is located in the root directory.

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

### 2. Backend (FastAPI)
The backend is located in `bima-bot-backend/`.

```bash
# Navigate to backend folder
cd bima-bot-backend

# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```
