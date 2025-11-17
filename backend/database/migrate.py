"""
Database Migration Module

Automatically initializes database schema and seed data on startup.
This ensures that deployments to Render (or other managed database services)
have the necessary tables and sample data without manual intervention.
"""

import os
import time
import psycopg2
from psycopg2 import extensions
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Cache to track if we've already verified migrations in this session
_migration_verified = False


def check_tables_exist(cursor) -> bool:
    """
    Check if the core database tables exist.

    Returns:
        bool: True if students table exists, False otherwise
    """
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'students'
        )
    """)
    return cursor.fetchone()[0]


def check_seed_data_exists(cursor) -> bool:
    """
    Check if seed data (students and teachers) exists.

    Returns:
        bool: True if seed students exist, False otherwise
    """
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    return student_count > 0


def check_sample_assessments_exist(cursor) -> bool:
    """
    Check if sample assessments have been loaded.

    Returns:
        bool: True if assessments exist, False otherwise
    """
    cursor.execute("SELECT COUNT(*) FROM assessments")
    assessment_count = cursor.fetchone()[0]
    return assessment_count > 0


def run_sql_file(cursor, conn, sql_file_path: Path, description: str):
    """
    Execute a SQL file with statement timeout.

    Args:
        cursor: Database cursor
        conn: Database connection
        sql_file_path: Path to SQL file
        description: Description of what this SQL file does (for logging)
    """
    if not sql_file_path.exists():
        logger.error(f"SQL file not found: {sql_file_path}")
        raise FileNotFoundError(f"SQL file not found: {sql_file_path}")

    logger.info(f"Executing {description}: {sql_file_path.name}")
    start_time = time.time()

    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Set statement timeout to prevent hanging (60 seconds)
    cursor.execute("SET statement_timeout = '60s'")

    # Execute the entire script
    cursor.execute(sql_script)
    conn.commit()

    # Reset statement timeout
    cursor.execute("RESET statement_timeout")

    elapsed = time.time() - start_time
    logger.info(f"✓ {description} completed successfully in {elapsed:.2f}s")


def run_migrations():
    """
    Main migration function - runs database initialization if needed.

    This function is idempotent and safe to run multiple times.
    It will:
    1. Check if tables exist
    2. If not, create schema from init.sql
    3. Check if sample assessments exist
    4. If not, load seed_assessments.sql

    This runs automatically on backend startup to ensure database is ready.

    Uses session cache to skip expensive checks on subsequent calls.
    """
    global _migration_verified

    # Skip full migration check if already verified in this session
    if _migration_verified:
        logger.info("✓ Database migrations already verified in this session - skipping check")
        return

    start_time = time.time()
    logger.info("=" * 70)
    logger.info("DATABASE MIGRATION CHECK")
    logger.info("=" * 70)

    conn = None
    cursor = None

    try:
        # Connect to database with timeout
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.error("DATABASE_URL environment variable not set!")
            raise ValueError("DATABASE_URL not configured")

        conn = psycopg2.connect(database_url, connect_timeout=10)
        # Set default statement timeout for all queries in this connection
        conn.set_session(
            isolation_level=extensions.ISOLATION_LEVEL_READ_COMMITTED,
            readonly=False,
            deferrable=False,
            autocommit=False
        )
        cursor = conn.cursor()
        cursor.execute("SET statement_timeout = '30s'")

        # Get SQL file paths
        db_dir = Path(__file__).parent
        init_sql = db_dir / "init.sql"
        seed_sql = db_dir / "seed_assessments.sql"

        # Step 1: Check if tables exist
        tables_exist = check_tables_exist(cursor)

        if not tables_exist:
            logger.warning("⚠ Database tables not found - initializing schema...")
            run_sql_file(cursor, conn, init_sql, "schema initialization (init.sql)")
            logger.info("✓ Database schema created successfully!")
        else:
            logger.info("✓ Database tables already exist - skipping schema creation")

        # Step 2: Check if seed data exists
        seed_exists = check_seed_data_exists(cursor)

        if not seed_exists:
            logger.warning("⚠ Seed data (students/teachers) not found")
            logger.info("  Note: init.sql should have created seed data")
            logger.info("  This might indicate init.sql was not fully executed")
        else:
            logger.info("✓ Seed data (students/teachers) exists")

        # Step 3: Load sample assessments if they don't exist
        # Use idempotent check - only load if seed data is missing
        cursor.execute("SELECT COUNT(*) FROM assessments WHERE data_entry_id LIKE 'S00%_202%'")
        seed_count = cursor.fetchone()[0]

        if seed_count == 0:
            logger.info("Loading longitudinal seed data (6 months of progress)...")
            run_sql_file(cursor, conn, seed_sql, "sample assessments (seed_assessments.sql)")
        else:
            logger.info(f"✓ Sample assessments already exist ({seed_count} found) - skipping seed load")

        # Verify assessments were loaded
        cursor.execute("SELECT COUNT(*) FROM assessments")
        count = cursor.fetchone()[0]
        logger.info(f"✓ Loaded {count} sample assessments successfully!")

        # Final summary
        logger.info("=" * 70)
        logger.info("DATABASE MIGRATION COMPLETE")

        # Log database statistics (lightweight counts)
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM data_entries")
        entry_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM assessments")
        assessment_count = cursor.fetchone()[0]

        logger.info(f"  Teachers: {teacher_count}")
        logger.info(f"  Students: {student_count}")
        logger.info(f"  Data Entries: {entry_count}")
        logger.info(f"  Assessments: {assessment_count}")

        total_elapsed = time.time() - start_time
        logger.info(f"  Total migration time: {total_elapsed:.2f}s")
        logger.info("=" * 70)

        # Mark migrations as verified for this session
        _migration_verified = True

    except Exception as e:
        logger.error(f"✗ Migration failed: {e}", exc_info=True)
        if conn:
            conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    # Allow running migrations manually for testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    run_migrations()
