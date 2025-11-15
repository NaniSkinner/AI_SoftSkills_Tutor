#!/usr/bin/env python3
"""
Generate Sample Data - Create a small set of assessments for seed data

This script ingests 4 selected mock data files to generate ~50-70 assessments
for use as permanent seed data in the database.
"""

import json
import requests
import time
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BACKEND_URL = "http://localhost:8000"

# Selected files for sample data (diverse mix of data types and students)
SAMPLE_FILES = [
    "mock_data/transcripts/S001_group_disc_2025-08-15.md",
    "mock_data/transcripts/S002_group_disc_2025-08-16.md",
    "mock_data/reflections/S001_reflection_2025-08-18.md",
    "mock_data/transcripts/S003_group_disc_2025-09-16.md",
]

def read_markdown_file(filepath: Path) -> str:
    """Read markdown file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def parse_filename(filename: str) -> tuple:
    """Parse student ID, type, and date from filename"""
    # Format: S001_description_2025-08-15.md
    parts = filename.stem.split('_')
    student_id = parts[0]
    type_abbr = parts[1]  # group_disc, reflection, etc.
    date = parts[-1]  # Last part is the date
    return student_id, type_abbr, date

def ingest_file(filepath: Path, file_index: int) -> bool:
    """Ingest a single file and trigger assessment generation"""
    try:
        student_id, type_abbr, date = parse_filename(filepath)
        content = read_markdown_file(filepath)

        # Determine data type from directory
        # Must match exact enum values from schema
        dir_name = filepath.parent.name
        type_map = {
            "transcripts": "Group Discussion Transcript",
            "reflections": "Reflection Journal",
            "teacher_notes": "Teacher Observation",
            "peer_feedback": "Peer Feedback",
            "parent_notes": "Parent Note"
        }
        data_type = type_map.get(dir_name, "Teacher Observation")

        # Default teacher is T001 (Ms. Rodriguez)
        teacher_id = "T001"

        # Create short ID (max 20 chars): S001_20250815_1
        date_short = date.replace('-', '')
        data_entry_id = f"{student_id}_{date_short}_{file_index}"

        payload = {
            "data_entry_id": data_entry_id,
            "student_id": student_id,
            "teacher_id": teacher_id,
            "type": data_type,
            "content": content,
            "date": date,
            "metadata": {}
        }

        logger.info(f"Ingesting {filepath.name} (student: {student_id}, type: {data_type})...")

        response = requests.post(
            f"{BACKEND_URL}/api/data/ingest",
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            logger.info(f"✓ Success: {result['assessments_created']} assessments created")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            logger.warning(f"⚠ Entry already exists, skipping")
            return True
        else:
            logger.error(f"✗ Failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.error(f"✗ Error ingesting {filepath}: {e}")
        return False

def main():
    """Generate sample data from selected files"""
    base_path = Path(__file__).parent.parent

    logger.info("=" * 60)
    logger.info("SAMPLE DATA GENERATION")
    logger.info("=" * 60)
    logger.info(f"Selected {len(SAMPLE_FILES)} files for sample data")
    logger.info("")

    # Check backend connectivity
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code != 200:
            logger.error("Backend health check failed!")
            return
        logger.info("✓ Backend is healthy")
    except Exception as e:
        logger.error(f"Cannot connect to backend: {e}")
        return

    # Ingest each file
    success_count = 0
    for idx, file_path_str in enumerate(SAMPLE_FILES, start=1):
        filepath = base_path / file_path_str
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            continue

        if ingest_file(filepath, idx):
            success_count += 1

        # Small delay between requests
        time.sleep(1)

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"COMPLETED: {success_count}/{len(SAMPLE_FILES)} files processed")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
