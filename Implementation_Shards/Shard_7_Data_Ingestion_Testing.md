# Shard 7: Data Ingestion & Testing

**Owner:** QA/Integration Engineer
**Estimated Time:** 2 days
**Dependencies:** Shards 2, 4 (Mock Data + Backend API)
**Priority:** P1 (High Priority)

---

## Objective

Bulk ingest all 76 mock data entries, trigger AI assessments, and validate the complete data pipeline from ingestion → inference → storage → dashboard display.

---

## Key Scripts

### 1. Bulk Data Ingestion

**File:** `scripts/ingest_all_data.py`

```python
"""Bulk ingest all mock data entries and trigger AI assessments."""
import json
import requests
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = "http://localhost:8000"
CONFIG_PATH = "mock_data/config.json"

def load_config():
    """Load mock data configuration."""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def load_data_entry_content(file_path: str) -> str:
    """Load content from data entry file."""
    full_path = Path("mock_data") / file_path
    with open(full_path, 'r') as f:
        return f.read()

def ingest_single_entry(entry: dict) -> dict:
    """Ingest single data entry via API."""
    # Load content from file
    content = load_data_entry_content(entry['file_path'])

    payload = {
        "data_entry_id": entry['id'],
        "student_id": entry['student_id'],
        "teacher_id": entry['teacher_id'],
        "type": entry['type'],
        "date": entry['date'],
        "content": content,
        "metadata": entry['metadata']
    }

    response = requests.post(f"{BACKEND_URL}/api/data/ingest", json=payload)
    response.raise_for_status()
    return response.json()

def main():
    config = load_config()
    entries = config['data_entries']

    logger.info(f"Starting ingestion of {len(entries)} data entries...")

    results = {
        "total_entries": len(entries),
        "successful": 0,
        "failed": 0,
        "total_assessments": 0,
        "errors": []
    }

    for idx, entry in enumerate(entries, 1):
        try:
            logger.info(f"[{idx}/{len(entries)}] Ingesting {entry['id']}...")
            result = ingest_single_entry(entry)

            results["successful"] += 1
            results["total_assessments"] += result["assessments_created"]

            logger.info(f"  ✅ Created {result['assessments_created']} assessments")

            # Rate limiting to avoid overwhelming OpenAI API
            if idx % 10 == 0:
                logger.info("  ⏸️  Pausing for rate limiting...")
                time.sleep(5)

        except Exception as e:
            results["failed"] += 1
            results["errors"].append({
                "entry_id": entry['id'],
                "error": str(e)
            })
            logger.error(f"  ❌ Failed: {e}")

    # Summary
    logger.info("\n" + "="*50)
    logger.info("INGESTION COMPLETE")
    logger.info("="*50)
    logger.info(f"Total Entries: {results['total_entries']}")
    logger.info(f"Successful: {results['successful']}")
    logger.info(f"Failed: {results['failed']}")
    logger.info(f"Total Assessments Created: {results['total_assessments']}")

    if results["errors"]:
        logger.warning(f"\n{len(results['errors'])} errors occurred:")
        for error in results["errors"]:
            logger.warning(f"  - {error['entry_id']}: {error['error']}")

    # Save results
    with open("scripts/ingestion_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    logger.info("\nResults saved to scripts/ingestion_results.json")

if __name__ == "__main__":
    main()
```

### 2. Data Validation

**File:** `scripts/validate_ingestion.py`

```python
"""Validate ingested data meets acceptance criteria."""
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )

def run_validation_checks():
    """Run comprehensive validation checks."""
    conn = get_db_connection()
    cursor = conn.cursor()

    results = {
        "total_data_entries": 0,
        "total_assessments": 0,
        "assessments_per_student": {},
        "skills_assessed": {},
        "avg_assessments_per_entry": 0,
        "level_distribution": {},
        "confidence_stats": {},
        "validation_passed": True
    }

    # Check 1: Total data entries
    cursor.execute("SELECT COUNT(*) as count FROM data_entries")
    results["total_data_entries"] = cursor.fetchone()['count']
    if results["total_data_entries"] != 76:
        print(f"❌ Expected 76 data entries, found {results['total_data_entries']}")
        results["validation_passed"] = False

    # Check 2: Total assessments
    cursor.execute("SELECT COUNT(*) as count FROM assessments")
    results["total_assessments"] = cursor.fetchone()['count']
    if results["total_assessments"] < 300:
        print(f"⚠️  Expected ≥300 assessments, found {results['total_assessments']}")

    # Check 3: Assessments per student
    cursor.execute("""
        SELECT student_id, COUNT(*) as count
        FROM assessments
        GROUP BY student_id
        ORDER BY student_id
    """)
    for row in cursor.fetchall():
        results["assessments_per_student"][row['student_id']] = row['count']

    # Check 4: All 17 skills represented
    cursor.execute("""
        SELECT DISTINCT skill_name
        FROM assessments
        ORDER BY skill_name
    """)
    skills = [row['skill_name'] for row in cursor.fetchall()]
    results["skills_assessed"]["total_unique"] = len(skills)
    results["skills_assessed"]["list"] = skills

    if len(skills) < 17:
        print(f"❌ Expected 17 skills, found {len(skills)}")
        results["validation_passed"] = False

    # Check 5: Level distribution
    cursor.execute("""
        SELECT level, COUNT(*) as count
        FROM assessments
        GROUP BY level
        ORDER BY level
    """)
    for row in cursor.fetchall():
        results["level_distribution"][row['level']] = row['count']

    # Check 6: Confidence score stats
    cursor.execute("""
        SELECT
            AVG(confidence_score) as avg,
            MIN(confidence_score) as min,
            MAX(confidence_score) as max
        FROM assessments
    """)
    stats = cursor.fetchone()
    results["confidence_stats"] = {
        "average": float(stats['avg']),
        "min": float(stats['min']),
        "max": float(stats['max'])
    }

    cursor.close()
    conn.close()

    return results

def print_validation_report(results):
    """Print human-readable validation report."""
    print("\n" + "="*60)
    print("VALIDATION REPORT")
    print("="*60)

    print(f"\n✅ Total Data Entries: {results['total_data_entries']}")
    print(f"✅ Total Assessments: {results['total_assessments']}")

    print(f"\nAssessments per Student:")
    for student_id, count in results['assessments_per_student'].items():
        print(f"  - {student_id}: {count} assessments")

    print(f"\nSkills Assessed: {results['skills_assessed']['total_unique']}/17")

    print(f"\nLevel Distribution:")
    for level, count in results['level_distribution'].items():
        percentage = (count / results['total_assessments']) * 100
        print(f"  - {level}: {count} ({percentage:.1f}%)")

    print(f"\nConfidence Score Statistics:")
    print(f"  - Average: {results['confidence_stats']['average']:.2f}")
    print(f"  - Min: {results['confidence_stats']['min']:.2f}")
    print(f"  - Max: {results['confidence_stats']['max']:.2f}")

    print("\n" + "="*60)
    if results['validation_passed']:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED - See errors above")
    print("="*60 + "\n")

if __name__ == "__main__":
    results = run_validation_checks()
    print_validation_report(results)
```

---

## Execution Plan

### Step 1: Prepare Environment
```bash
# Ensure all services running
docker-compose up -d

# Wait for backend to be ready
curl http://localhost:8000/health
```

### Step 2: Run Bulk Ingestion
```bash
python scripts/ingest_all_data.py
```

**Expected Duration:** ~30-45 minutes (depending on OpenAI API rate limits)

### Step 3: Validate Results
```bash
python scripts/validate_ingestion.py
```

### Step 4: Manual Spot Checks
1. Open Teacher Dashboard: http://localhost:8501
2. Select Teacher: Ms. Rodriguez
3. Check Eva's skill trends show progression
4. Verify Assessment Review has pending assessments
5. Open Student Dashboard
6. Select Eva
7. Check Journey Map shows correct levels

---

## Acceptance Criteria

- [ ] All 76 data entries ingested successfully
- [ ] At least 300 assessments generated (avg 4+ per entry)
- [ ] All 4 students have assessments
- [ ] All 17 skills represented in assessments
- [ ] Level distribution reasonable (mix of E/D/P/A)
- [ ] Confidence scores within 0.5-1.0 range
- [ ] Teacher dashboard displays data correctly
- [ ] Student dashboard shows progression
- [ ] No duplicate data entries in database
- [ ] API response times < 3s per ingestion

---

## Troubleshooting

### OpenAI Rate Limit Errors
**Solution:** Increase sleep interval in ingestion script
```python
if idx % 5 == 0:  # Pause more frequently
    time.sleep(10)  # Longer pause
```

### Database Connection Timeouts
**Solution:** Check PostgreSQL max_connections
```sql
SHOW max_connections;
ALTER SYSTEM SET max_connections = 100;
```

### Missing Assessments
**Solution:** Check API logs
```bash
docker-compose logs backend | grep ERROR
```

---

**Completion Checklist:**
- [ ] Ingestion script runs successfully
- [ ] Validation script passes all checks
- [ ] Manual spot checks completed
- [ ] Performance acceptable
- [ ] Error handling tested
- [ ] Results documented

**Sign-off:** _____________________
