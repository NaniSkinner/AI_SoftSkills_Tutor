#!/usr/bin/env python3
"""
Bulk Data Ingestion Script - Flourish Skills Tracker

Ingests all 32 mock data entries from the mock_data directory and triggers
AI assessment generation for each entry via the backend API.

Usage:
    python scripts/ingest_all_data.py [--backend-url URL] [--dry-run]
"""

import json
import requests
import time
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, List
import argparse
import os
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_BACKEND_URL = "http://localhost:8000"
# In Docker, mock_data is mounted at /app/mock_data; locally it's in parent dir
MOCK_DATA_DIR = Path("/app/mock_data") if Path("/app/mock_data").exists() else Path(__file__).parent.parent.parent / "mock_data"
CONFIG_PATH = MOCK_DATA_DIR / "config.json"
RATE_LIMIT_PAUSE_EVERY = 10
RATE_LIMIT_PAUSE_SECONDS = 5
MAX_RETRIES = 3
RETRY_DELAY = 2


def load_config() -> dict:
    """Load configuration from config.json"""
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Loaded configuration from {CONFIG_PATH}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {CONFIG_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        sys.exit(1)


def generate_stable_id(student_id: str, date: str, filename: str) -> str:
    """
    Generate a stable, unique ID from file metadata using SHA-256 hash.

    This ensures:
    - Same file always generates same ID (stable)
    - Different files generate different IDs (unique)
    - Idempotent ingestion (safe to re-run)

    Args:
        student_id: Student identifier (e.g., S001)
        date: Date string (e.g., 2025-08-15)
        filename: Source filename (e.g., S001_group_disc_2025-08-15.md)

    Returns:
        ID string in format: DE_<12-char-hash> (e.g., DE_a3f7c9e2b1d4)
    """
    hash_input = f"{student_id}_{date}_{filename}"
    hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
    return f"DE_{hash_digest}"


def discover_data_entries() -> List[Dict]:
    """
    Discover all data entry files in mock_data directory and build entry manifests

    Scans transcripts/, reflections/, teacher_notes/, peer_feedback/ etc.
    """
    data_entries = []

    # Map subdirectories to data types
    type_mapping = {
        "transcripts": "Group Discussion",
        "reflections": "Reflection Journal",
        "teacher_notes": "Teacher Observation",
        "peer_feedback": "Peer Feedback",
        "parent_notes": "Parent Communication"
    }

    for subdir, data_type in type_mapping.items():
        subdir_path = MOCK_DATA_DIR / subdir
        if not subdir_path.exists():
            continue

        for file_path in sorted(subdir_path.glob("*.md")):
            # Parse filename: S001_group_disc_2025-08-15.md
            filename = file_path.stem
            parts = filename.split("_")

            if len(parts) < 3:
                logger.warning(f"Skipping file with unexpected format: {filename}")
                continue

            student_id = parts[0]  # S001
            date = parts[-1]  # 2025-08-15

            # Determine teacher_id from student
            config = load_config()
            teacher_id = "T001"  # default
            for student in config.get("students", []):
                if student["id"] == student_id:
                    teacher_id = student["teacher_id"]
                    break

            # More specific data types based on filename patterns
            # Must match exact types from backend API validation
            if "group" in filename or "disc" in filename:
                specific_type = "Group Discussion Transcript"
            elif "presentation" in filename:
                specific_type = "Project Presentation"
            elif "reflection" in filename:
                specific_type = "Reflection Journal"
            elif "observation" in filename:
                specific_type = "Teacher Observation"
            elif "peer" in filename:
                specific_type = "Peer Feedback"
            elif "parent" in filename:
                specific_type = "Parent Note"
            else:
                specific_type = data_type

            # Generate stable hash-based ID from file metadata
            stable_id = generate_stable_id(student_id, date, file_path.name)

            data_entry = {
                "id": stable_id,
                "student_id": student_id,
                "teacher_id": teacher_id,
                "type": specific_type,
                "date": date,
                "file_path": str(file_path.relative_to(MOCK_DATA_DIR.parent)),
                "metadata": {
                    "source_file": file_path.name,
                    "data_type": specific_type
                }
            }

            data_entries.append(data_entry)

    logger.info(f"Discovered {len(data_entries)} data entry files")
    return data_entries


def load_data_entry_content(file_path: str) -> str:
    """Load content from a data entry file"""
    try:
        full_path = Path(file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content.strip():
            logger.warning(f"File is empty: {file_path}")

        return content
    except FileNotFoundError:
        logger.error(f"Data entry file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise


def ingest_single_entry(entry: Dict, backend_url: str, retry_count: int = 0) -> Dict:
    """
    Ingest a single data entry via the backend API

    Args:
        entry: Data entry dictionary with id, student_id, teacher_id, type, date, file_path
        backend_url: Backend API base URL
        retry_count: Current retry attempt (0-indexed)

    Returns:
        Response dictionary with success status and assessment_ids
    """
    entry_id = entry['id']
    logger.info(f"Ingesting {entry_id} ({entry['student_id']}, {entry['type']}, {entry['date']})...")

    try:
        # Load content
        content = load_data_entry_content(entry['file_path'])

        # Build payload
        payload = {
            "data_entry_id": entry['id'],
            "student_id": entry['student_id'],
            "teacher_id": entry['teacher_id'],
            "type": entry['type'],
            "date": entry['date'],
            "content": content,
            "metadata": entry['metadata']
        }

        # Make API call
        url = f"{backend_url}/api/data/ingest"
        response = requests.post(url, json=payload, timeout=60)

        # Handle response
        if response.status_code in [200, 201]:
            result = response.json()
            logger.info(f"✅ {entry_id}: Successfully ingested, {result.get('assessments_created', 0)} assessments created")
            return result

        elif response.status_code == 400:
            # Client error - don't retry
            logger.error(f"❌ {entry_id}: Client error (400): {response.text}")
            return {"success": False, "error": "client_error", "message": response.text}

        elif response.status_code >= 500:
            # Server error - retry
            if retry_count < MAX_RETRIES:
                retry_count += 1
                delay = RETRY_DELAY * retry_count
                logger.warning(f"⚠️  {entry_id}: Server error (500), retrying in {delay}s ({retry_count}/{MAX_RETRIES})...")
                time.sleep(delay)
                return ingest_single_entry(entry, backend_url, retry_count)
            else:
                logger.error(f"❌ {entry_id}: Max retries exceeded")
                return {"success": False, "error": "max_retries", "message": response.text}

        else:
            logger.error(f"❌ {entry_id}: Unexpected status {response.status_code}: {response.text}")
            return {"success": False, "error": "unexpected_status", "message": response.text}

    except requests.exceptions.Timeout:
        logger.error(f"❌ {entry_id}: Request timeout")
        if retry_count < MAX_RETRIES:
            retry_count += 1
            logger.warning(f"⚠️  Retrying ({retry_count}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY * retry_count)
            return ingest_single_entry(entry, backend_url, retry_count)
        return {"success": False, "error": "timeout"}

    except Exception as e:
        logger.error(f"❌ {entry_id}: Unexpected error: {e}")
        return {"success": False, "error": "exception", "message": str(e)}


def ingest_all(backend_url: str, dry_run: bool = False, auto_confirm: bool = False) -> Dict:
    """
    Ingest all data entries

    Args:
        backend_url: Backend API base URL
        dry_run: If True, only discover and list entries without ingesting

    Returns:
        Summary statistics dictionary
    """
    logger.info("=" * 60)
    logger.info("Flourish Skills Tracker - Bulk Data Ingestion")
    logger.info("=" * 60)

    # Discover data entries
    data_entries = discover_data_entries()

    if not data_entries:
        logger.error("No data entries found!")
        return {"success": False, "error": "no_entries"}

    logger.info(f"\nFound {len(data_entries)} data entries to ingest")
    logger.info(f"Estimated API calls: {len(data_entries) * 17} (17 skills per entry)")
    logger.info(f"Estimated cost: ~$9.00 (based on GPT-4o pricing)\n")

    if dry_run:
        logger.info("DRY RUN MODE - Listing entries without ingestion:\n")
        for entry in data_entries:
            logger.info(f"  {entry['id']}: {entry['student_id']} - {entry['type']} ({entry['date']})")
        logger.info(f"\nTotal: {len(data_entries)} entries")
        return {"success": True, "dry_run": True, "total_entries": len(data_entries)}

    # Confirm before proceeding (skip if auto_confirm is True)
    if not auto_confirm:
        confirm = input(f"\nProceed with ingestion of {len(data_entries)} entries? (yes/no): ")
        if confirm.lower() not in ['yes', 'y']:
            logger.info("Ingestion cancelled by user")
            return {"success": False, "error": "user_cancelled"}
    else:
        logger.info(f"Auto-confirm enabled - proceeding with ingestion of {len(data_entries)} entries")

    # Ingest all entries
    results = []
    start_time = time.time()

    for i, entry in enumerate(data_entries, 1):
        logger.info(f"\n[{i}/{len(data_entries)}] Processing {entry['id']}...")

        result = ingest_single_entry(entry, backend_url)
        results.append({
            "entry": entry,
            "result": result
        })

        # Rate limiting
        if i % RATE_LIMIT_PAUSE_EVERY == 0 and i < len(data_entries):
            logger.info(f"⏸️  Rate limit pause: {RATE_LIMIT_PAUSE_SECONDS}s...")
            time.sleep(RATE_LIMIT_PAUSE_SECONDS)

    # Calculate statistics
    elapsed_time = time.time() - start_time
    successful = len([r for r in results if r['result'].get('success', False)])
    failed = len(results) - successful
    total_assessments = sum(r['result'].get('assessments_created', 0) for r in results)

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total entries processed: {len(results)}")
    logger.info(f"✅ Successful: {successful}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"📊 Total assessments created: {total_assessments}")
    logger.info(f"⏱️  Time elapsed: {elapsed_time:.1f}s ({elapsed_time/60:.1f} minutes)")
    logger.info(f"⚡ Average time per entry: {elapsed_time/len(results):.1f}s")

    if failed > 0:
        logger.info("\nFailed entries:")
        for r in results:
            if not r['result'].get('success', False):
                entry = r['entry']
                error = r['result'].get('error', 'unknown')
                logger.info(f"  - {entry['id']}: {error}")

    logger.info("=" * 60)

    return {
        "success": successful == len(results),
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "total_assessments": total_assessments,
        "elapsed_time": elapsed_time,
        "results": results
    }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Bulk ingest mock data for Flourish Skills Tracker")
    parser.add_argument(
        '--backend-url',
        default=os.getenv('BACKEND_URL', DEFAULT_BACKEND_URL),
        help=f'Backend API URL (default: {DEFAULT_BACKEND_URL})'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='List entries without ingesting'
    )
    parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='Skip interactive confirmation prompt (for API/automation use)'
    )

    args = parser.parse_args()

    # Test backend connectivity with longer timeout for Render deployment
    try:
        response = requests.get(f"{args.backend_url}/health", timeout=30)
        if response.status_code == 200:
            logger.info(f"✅ Backend connected: {args.backend_url}")
        else:
            logger.error(f"❌ Backend health check failed: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Cannot connect to backend at {args.backend_url}: {e}")
        sys.exit(1)

    # Run ingestion
    summary = ingest_all(args.backend_url, args.dry_run, args.auto_confirm)

    # Exit with appropriate code
    if summary.get('success', False):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
