"""
SME Financial Compass - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.config import settings
from app.routers import (
    auth_router,
    upload_router,
    analysis_router,
    forecast_router,
    reports_router,
    business_router,
    banking_router,
    insights_router
)
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Initializing database...")
    await init_db()
    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Application shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="SME Financial Compass API",
    description="AI-powered financial health assessment platform for SMEs",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(upload_router, prefix="/api/upload", tags=["Upload"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(forecast_router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(reports_router, prefix="/api/reports", tags=["Reports"])
app.include_router(business_router, prefix="/api/business", tags=["Business"])
app.include_router(banking_router, prefix="/api/banking", tags=["Banking"])
app.include_router(insights_router, prefix="/api/insights", tags=["Insights"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SME Financial Compass API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sme-financial-compass",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
