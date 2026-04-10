"""
SmartPredict AI — Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import upload, insights, chat

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered platform that transforms raw data into actionable business insights",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount route modules
app.include_router(upload.router)
app.include_router(insights.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "SmartPredict AI backend is ready. Upload a CSV/Excel file to get started.",
    }


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
