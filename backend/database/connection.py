"""
Database connection utility for Flourish Skills Tracker.

Uses connection pooling to efficiently manage database connections
and prevent connection exhaustion on free tier (max 20 connections).
"""
import os
import time
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global connection pool (initialized on first import)
_connection_pool: Optional[pool.SimpleConnectionPool] = None


def init_connection_pool():
    """
    Initialize the connection pool with retry logic.

    Called automatically on first connection request.
    Safe to call multiple times (idempotent).

    Retries with exponential backoff to handle database startup delays.
    """
    global _connection_pool

    if _connection_pool is not None:
        return  # Already initialized

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")

    # Retry configuration for database startup
    max_retries = 5
    retry_delay = 1  # Start with 1 second

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Initializing database connection pool (attempt {attempt}/{max_retries})...")

            # Create connection pool
            # Free tier PostgreSQL on Render has ~20 max connections
            # Use conservative limits to avoid exhaustion
            _connection_pool = pool.SimpleConnectionPool(
                minconn=2,   # Keep 2 connections warm
                maxconn=10,  # Max 10 connections (safe for free tier)
                dsn=database_url,
                cursor_factory=RealDictCursor,
                connect_timeout=10  # 10 second connection timeout
            )
            logger.info("✓ Database connection pool initialized (2-10 connections)")
            return  # Success!

        except (psycopg2.OperationalError, psycopg2.DatabaseError) as e:
            if attempt < max_retries:
                logger.warning(f"Connection attempt {attempt} failed: {e}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 16)  # Exponential backoff, max 16s
            else:
                logger.error(f"Failed to initialize connection pool after {max_retries} attempts: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error initializing connection pool: {e}")
            raise


def get_db_connection():
    """
    Get a connection from the pool.

    Returns:
        psycopg2 connection object with RealDictCursor

    Raises:
        psycopg2.OperationalError: If connection fails

    Note:
        Caller MUST call putconn() to return connection to pool,
        or use the connection context manager.
    """
    global _connection_pool

    # Initialize pool on first use
    if _connection_pool is None:
        init_connection_pool()

    try:
        conn = _connection_pool.getconn()
        return conn
    except Exception as e:
        logger.error(f"Failed to get connection from pool: {e}")
        raise


def return_db_connection(conn):
    """
    Return a connection to the pool.

    Args:
        conn: Connection to return
    """
    global _connection_pool

    if _connection_pool is not None and conn is not None:
        _connection_pool.putconn(conn)


def test_connection() -> bool:
    """
    Test database connectivity using connection pool.

    Returns:
        bool: True if connection successful, False otherwise
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        return_db_connection(conn)
        return result['test'] == 1
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        if conn:
            return_db_connection(conn)
        return False


def get_student_count() -> int:
    """Helper to verify seed data loaded."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM students")
        result = cursor.fetchone()
        cursor.close()
        return_db_connection(conn)
        return result['count']
    except Exception as e:
        if conn:
            return_db_connection(conn)
        raise


def close_all_connections():
    """
    Close all connections in the pool.

    Called during application shutdown.
    """
    global _connection_pool

    if _connection_pool is not None:
        _connection_pool.closeall()
        logger.info("✓ All database connections closed")
        _connection_pool = None
