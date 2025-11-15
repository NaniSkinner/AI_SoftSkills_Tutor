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
    """Health check endpoint with database connectivity and schema verification"""
    from database.connection import get_db_connection

    db_status = "disconnected"
    tables_exist = False
    student_count = 0
    assessment_count = 0

    try:
        if test_connection():
            db_status = "connected"

            # Check if tables exist and get counts
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'students'
                )
            """)
            tables_exist = cursor.fetchone()[0]

            if tables_exist:
                cursor.execute("SELECT COUNT(*) FROM students")
                student_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM assessments")
                assessment_count = cursor.fetchone()[0]

            cursor.close()
            conn.close()
    except Exception as e:
        logger.error(f"Health check error: {e}")

    return {
        "status": "healthy" if db_status == "connected" and tables_exist else "degraded",
        "database": db_status,
        "schema_initialized": tables_exist,
        "students": student_count,
        "assessments": assessment_count,
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
        # Run the ingestion script with auto-confirm flag for non-interactive execution
        result = subprocess.run(
            ["python", "scripts/ingest_all_data.py", "--backend-url", "http://localhost:8000", "--auto-confirm"],
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
            # Provide meaningful error message even if stderr is empty
            error_msg = result.stderr or result.stdout or "Script failed with no output"
            logger.error(f"Data initialization failed: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail=f"Data initialization failed: {error_msg}"
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

    # Run database migrations first (creates schema and loads seed data if needed)
    try:
        from database.migrate import run_migrations
        run_migrations()
    except Exception as e:
        logger.error(f"✗ Database migration failed: {e}")
        logger.error("  Backend may not function correctly!")

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
