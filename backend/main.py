"""
Flourish Skills Tracker - Backend API

Complete REST API for AI-powered soft skills assessment.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import subprocess
from database import test_connection

# Import all routers
from routers import data_ingest, assessments, corrections, students, badges

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Flourish Skills Tracker API",
    description="AI-powered soft skills assessment system with 15+ endpoints for data ingestion, assessment retrieval, teacher corrections, student progress, and badge management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for Streamlit frontend
# Get allowed origins from environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else [
    "http://localhost:8501",
    "http://frontend:8501",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(data_ingest.router)
app.include_router(assessments.router)
app.include_router(corrections.router)
app.include_router(students.router)
app.include_router(badges.router)

logger.info("All routers registered successfully")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Flourish Skills Tracker API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test"""
    db_status = "connected" if test_connection() else "disconnected"

    return {
        "status": "healthy",
        "database": db_status,
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "version": "1.0.0"
    }


@app.post("/api/admin/initialize-data")
async def initialize_data(admin_key: str):
    """
    One-time initialization endpoint to load mock data into the database.

    This endpoint runs the data ingestion script to populate the database
    with all student data, assessments, and related information from the
    mock_data directory.

    Args:
        admin_key: Secret key to prevent unauthorized access

    Returns:
        Success message with data loaded count

    Usage:
        POST /api/admin/initialize-data?admin_key=your-secret-key
    """
    # Verify admin key
    expected_key = os.getenv("ADMIN_INIT_KEY", "flourish-admin-2024")
    if admin_key != expected_key:
        logger.warning(f"Unauthorized data initialization attempt")
        raise HTTPException(status_code=403, detail="Unauthorized - Invalid admin key")

    logger.info("Starting data initialization...")

    try:
        # Run the ingestion script
        result = subprocess.run(
            ["python", "scripts/ingest_all_data.py", "--backend-url", "http://localhost:8000"],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd="/app"  # Ensure we're in the app directory
        )

        if result.returncode == 0:
            logger.info("Data initialization completed successfully")
            return {
                "success": True,
                "message": "Data initialization completed successfully",
                "output": result.stdout,
                "details": "All students and their data have been loaded into the database"
            }
        else:
            logger.error(f"Data initialization failed: {result.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Data initialization failed: {result.stderr}"
            )

    except subprocess.TimeoutExpired:
        logger.error("Data initialization timed out after 5 minutes")
        raise HTTPException(
            status_code=500,
            detail="Data initialization timed out after 5 minutes"
        )
    except Exception as e:
        logger.error(f"Data initialization error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Data initialization error: {str(e)}"
        )


@app.on_event("startup")
async def startup_event():
    """Startup event handler - runs when the API starts"""
    logger.info("=" * 80)
    logger.info("Flourish Skills Tracker API Starting...")
    logger.info("=" * 80)

    # Test database connection
    if test_connection():
        logger.info("✓ Database connection successful")
    else:
        logger.error("✗ Database connection failed!")

    # Check OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        logger.info("✓ OpenAI API key configured")
        if api_key.startswith('sk-or-v1-'):
            logger.info("  → Using OpenRouter endpoint")
    else:
        logger.warning("✗ OpenAI API key not configured!")

    # Log available endpoints
    logger.info("Available routers:")
    logger.info("  → Data Ingestion: /api/data/ingest")
    logger.info("  → Assessments: /api/assessments/*")
    logger.info("  → Corrections: /api/corrections/*")
    logger.info("  → Students: /api/students/*")
    logger.info("  → Badges: /api/badges/*")
    logger.info("=" * 80)
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("=" * 80)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler - runs when the API stops"""
    logger.info("=" * 80)
    logger.info("Flourish Skills Tracker API Shutting Down...")
    logger.info("=" * 80)
