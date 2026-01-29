from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import audit, health
from app.config import settings

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title=settings.app_name, debug=settings.debug)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, tags=["Health"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])


@app.get("/")
def root():
    return {
        "message": "BimaBot Backend API",
        "docs": "/docs",
        "health": "/health"
    }
