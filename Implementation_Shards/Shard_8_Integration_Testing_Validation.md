# Shard 8: Integration Testing & Validation

**Owner:** QA Lead / Integration Engineer
**Estimated Time:** 2 days
**Dependencies:** All shards (1-7)
**Priority:** P1 (High Priority)

---

## Objective

Perform end-to-end integration testing, validate AI accuracy (TAR - Teacher Agreement Rate), test all user workflows, and verify demo readiness.

---

## Test Categories

### 1. AI Accuracy Validation (TAR Testing)

**Goal:** Achieve ≥85% Teacher Agreement Rate

**Approach:**
- Use `expected_skills` from config.json (validation dataset)
- Compare AI assessments vs expected levels
- Calculate TAR = (matching assessments / total assessments) × 100

**File:** `scripts/test_ai_accuracy.py`

```python
"""Calculate Teacher Agreement Rate for AI assessments."""
import json
from backend.database.connection import get_db_connection

def calculate_tar():
    """Calculate TAR by comparing AI assessments to expected levels."""
    config = json.load(open('mock_data/config.json'))

    matches = 0
    total = 0

    for entry in config['data_entries']:
        if 'expected_skills' not in entry:
            continue

        # Get AI assessments for this data entry
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT skill_name, level
            FROM assessments
            WHERE data_entry_id = %s
        """, (entry['id'],))

        ai_assessments = {row['skill_name']: row['level'] for row in cursor.fetchall()}

        # Compare to expected
        for expected in entry['expected_skills']:
            skill = expected['skill']
            expected_level = expected['expected_level']

            if skill in ai_assessments:
                total += 1
                if ai_assessments[skill] == expected_level:
                    matches += 1
                else:
                    print(f"❌ Mismatch: {entry['id']} - {skill}")
                    print(f"   Expected: {expected_level}, Got: {ai_assessments[skill]}")

        cursor.close()
        conn.close()

    tar = (matches / total * 100) if total > 0 else 0
    print(f"\n{'='*60}")
    print(f"Teacher Agreement Rate (TAR): {tar:.1f}%")
    print(f"Matches: {matches}/{total}")
    print(f"{'='*60}\n")

    return tar >= 85  # Pass if TAR ≥ 85%
```

### 2. End-to-End Workflow Testing

#### Test Case 1: Teacher Correction Workflow
**Steps:**
1. Login as Ms. Rodriguez (T001)
2. Navigate to Assessment Review
3. Filter for Low Confidence assessments
4. Review assessment for Eva - Self-Management
5. Change level from Developing → Proficient
6. Add teacher notes explaining correction
7. Submit correction
8. Verify correction saved in database
9. Check few-shot manager retrieves correction
10. Re-run inference on similar data
11. Verify AI improved (uses correction in few-shot)

**Expected Result:** Correction workflow functional, few-shot learning works

#### Test Case 2: Target Assignment & Student View
**Steps:**
1. Teacher assigns target: Eva - Self-Management (D → P)
2. Navigate to Student Dashboard
3. Select Eva
4. Check Current Goal page shows "Self-Management: D → P"
5. Verify tips and progress updates display
6. Teacher later marks target as completed
7. Student sees celebration animation

**Expected Result:** Target assignment and student goal view functional

#### Test Case 3: Badge Granting
**Steps:**
1. Teacher reviews Eva's assessments
2. Eva reaches Proficient in Communication
3. Teacher grants Silver badge
4. Student Dashboard shows new badge
5. Badge collection displays silver-colored badge
6. Locked badges show faded with lock icon

**Expected Result:** Badge system functional, colors correct

#### Test Case 4: Skill Progression Tracking
**Steps:**
1. View Eva's Skill Trends for August
2. Note Self-Awareness at Developing
3. Ingest September data (already done)
4. Check Self-Awareness progressed to Proficient
5. Verify chart shows E → D → P timeline
6. Check Journey Map reflects progression

**Expected Result:** Skill tracking shows authentic growth over time

### 3. Performance Testing

**Metrics to Measure:**

| Metric | Target | Test Method |
|--------|--------|-------------|
| API Response Time (Ingestion) | < 3s | Time 10 ingestion requests |
| Dashboard Load Time | < 3s | Measure Streamlit page load |
| Database Query Time (Trends) | < 500ms | EXPLAIN ANALYZE on trend queries |
| Confidence Score Calculation | < 50ms | Profile heuristic function |

**File:** `scripts/performance_test.py`

```python
import time
import requests

def test_ingestion_performance():
    """Test ingestion endpoint performance."""
    times = []

    for i in range(10):
        start = time.time()
        response = requests.post("http://localhost:8000/api/data/ingest", json=test_payload)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Request {i+1}: {elapsed:.2f}s")

    avg_time = sum(times) / len(times)
    print(f"\nAverage: {avg_time:.2f}s")
    print(f"Max: {max(times):.2f}s")

    return avg_time < 3.0  # Pass if avg < 3s
```

### 4. Data Quality Checks

**Checks to Perform:**

- [ ] No duplicate assessments (same student, skill, data_entry)
- [ ] All confidence scores between 0.5 and 1.0
- [ ] All assessments have non-null justification and source_quote
- [ ] All students show growth trajectory (not all Emerging)
- [ ] At least 3 Advanced-level assessments for Mia
- [ ] Skill distribution balanced (not all Communication, neglecting EF)

**File:** `scripts/data_quality_check.py`

```python
def check_data_quality():
    """Run data quality checks."""
    conn = get_db_connection()
    cursor = conn.cursor()

    issues = []

    # Check for nulls
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM assessments
        WHERE justification IS NULL OR source_quote IS NULL
    """)
    null_count = cursor.fetchone()['count']
    if null_count > 0:
        issues.append(f"Found {null_count} assessments with null justification/quote")

    # Check confidence score range
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM assessments
        WHERE confidence_score < 0.5 OR confidence_score > 1.0
    """)
    invalid_conf = cursor.fetchone()['count']
    if invalid_conf > 0:
        issues.append(f"Found {invalid_conf} assessments with invalid confidence scores")

    # Check Mia has Advanced assessments
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM assessments
        WHERE student_id = 'S004' AND level = 'Advanced'
    """)
    mia_advanced = cursor.fetchone()['count']
    if mia_advanced < 3:
        issues.append(f"Mia only has {mia_advanced} Advanced assessments (expected ≥3)")

    cursor.close()
    conn.close()

    if issues:
        print("❌ Data Quality Issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All data quality checks passed")
        return True
```

---

## Acceptance Criteria

### AI Accuracy
- [ ] TAR (Teacher Agreement Rate) ≥ 85%
- [ ] Confidence scores align with assessment quality
- [ ] Few-shot learning improves assessments after corrections

### Workflows
- [ ] Teacher correction workflow functional
- [ ] Target assignment works with starting_level → target_level
- [ ] Badge granting and display functional
- [ ] Student journey map shows progression accurately

### Performance
- [ ] Ingestion API < 3s average response time
- [ ] Dashboard loads < 3s
- [ ] Trend queries < 500ms
- [ ] No performance degradation with full dataset

### Data Quality
- [ ] No duplicate or malformed assessments
- [ ] All students show realistic growth trajectories
- [ ] All 17 skills represented across dataset
- [ ] Level distribution reasonable (mix of E/D/P/A)

### Demo Readiness
- [ ] All services start successfully with `docker-compose up`
- [ ] Teacher dashboard navigable without errors
- [ ] Student dashboard engaging and accurate
- [ ] No console errors or warnings
- [ ] Representative data for each student archetype

---

## Final Validation Checklist

**Before demo, verify:**

- [ ] 76 data entries ingested
- [ ] 300+ assessments generated
- [ ] All 4 students have complete data
- [ ] Eva shows steady growth (Emerging → Proficient)
- [ ] Lucas shows EF breakthrough (Planning: Emerging → Proficient)
- [ ] Pat shows late bloom (Month 3 acceleration)
- [ ] Mia has 5+ Advanced skills
- [ ] At least 5 teacher corrections submitted
- [ ] Badge system awards bronze/silver/gold correctly
- [ ] Faded badges shown for Emerging skills
- [ ] Target assignments display D → P format
- [ ] Charts render correctly in Skill Trends
- [ ] Journey Map animations trigger
- [ ] API docs accessible at /docs
- [ ] No errors in logs

---

## Test Execution Commands

```bash
# Run all tests
cd scripts
python test_ai_accuracy.py
python performance_test.py
python data_quality_check.py
python validate_ingestion.py

# Manual testing
open http://localhost:8501  # Teacher Dashboard
open http://localhost:8501  # Student Dashboard (different tab)
open http://localhost:8000/docs  # API Docs

# Check logs for errors
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep ERROR
```

---

## Issue Triage

**If TAR < 85%:**
1. Review mismatched assessments
2. Check if rubric alignment issues
3. Add more few-shot examples
4. Adjust system prompt if needed

**If Performance Issues:**
1. Check database query plans (EXPLAIN ANALYZE)
2. Add missing indexes
3. Consider caching frequently accessed data
4. Optimize confidence score calculation

**If Dashboard Errors:**
1. Check API connectivity
2. Verify session state management
3. Review Streamlit error traceback
4. Check browser console for JS errors

---

**Completion Checklist:**
- [ ] TAR ≥ 85% achieved
- [ ] All workflows tested
- [ ] Performance benchmarks met
- [ ] Data quality verified
- [ ] Demo rehearsal successful
- [ ] Documentation complete
- [ ] Handoff to stakeholders ready

**Sign-off:** _____________________
**Date:** _____________________
