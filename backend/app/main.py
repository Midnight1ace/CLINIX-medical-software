"""
AI Patient Record Intelligence - FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.api.auth import router as auth_router
from app.api.patients import router as patients_router
from app.api.records import router as records_router
from app.api.ai_summary import router as ai_summary_router
from app.api.pharmacy import router as pharmacy_router
from app.api.clinic import router as clinic_router
from app.api.audit import router as audit_router

# Database
from app.database.connection import init_db

def create_application() -> FastAPI:
    """Create FastAPI application"""

    app = FastAPI(
        title="AI Patient Record Intelligence",
        description="Doctor-first, safety-critical patient record system",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS middleware
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize database
    init_db()

    # Include routers
    app.include_router(auth_router, prefix="/api/v1", tags=["Authentication"])
    app.include_router(patients_router, prefix="/api/v1", tags=["Patients"])
    app.include_router(records_router, prefix="/api/v1", tags=["Records"])
    app.include_router(ai_summary_router, prefix="/api/v1", tags=["AI Summary"])
    app.include_router(pharmacy_router, prefix="/api/v1", tags=["Pharmacy"])
    app.include_router(clinic_router, prefix="/api/v1", tags=["Clinic"])
    app.include_router(audit_router, prefix="/api/v1", tags=["Audit"])

    return app