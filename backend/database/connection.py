"""
Database connection utility for Flourish Skills Tracker.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Create and return a database connection.

    Returns:
        psycopg2 connection object with RealDictCursor

    Raises:
        psycopg2.OperationalError: If connection fails
    """
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise


def test_connection() -> bool:
    """
    Test database connectivity.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['test'] == 1
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False


def get_student_count() -> int:
    """Helper to verify seed data loaded."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM students")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['count']
