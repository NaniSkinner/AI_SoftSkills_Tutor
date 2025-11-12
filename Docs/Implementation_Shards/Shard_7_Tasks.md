# Shard 7 Tasks: Data Ingestion & Testing

**Status:** ✅ Completed
**Priority:** P1 (High Priority)
**Dependencies:** Shards 2, 4 (Mock Data + Backend API)

---

## Overview

Bulk ingest all 32 mock data entries (modified scope from 76), trigger AI assessments for each entry, validate the complete data pipeline from ingestion through inference to storage, and verify dashboard display accuracy. Includes performance testing and data quality validation.

---

## Prerequisites Checklist

- [x] Shard 2 completed (32 mock data files created, config.json ready)
- [x] Shard 4 completed (Backend API functional)
- [x] All services running (docker-compose up)
- [x] Backend health check passes
- [x] OpenAI API key configured and valid
- [x] Database ready for bulk ingestion

---

## Tasks

### 1. Bulk Ingestion Script

- [ ] Create `scripts/ingest_all_data.py` file

#### 1.1 Imports and Setup
- [ ] Import `json`
- [ ] Import `requests`
- [ ] Import `time`
- [ ] Import `logging`
- [ ] Import `pathlib.Path`
- [ ] Import `sys`
- [ ] Import `typing.Optional`
- [ ] Configure logging with INFO level
- [ ] Create logger instance

#### 1.2 Configuration Constants
- [ ] Define `BACKEND_URL` (default "http://localhost:8000")
- [ ] Define `CONFIG_PATH` ("mock_data/config.json")
- [ ] Define `RATE_LIMIT_PAUSE_EVERY` (10 requests)
- [ ] Define `RATE_LIMIT_PAUSE_SECONDS` (5 seconds)
- [ ] Define `MAX_RETRIES` (3)
- [ ] Define `RETRY_DELAY` (2 seconds)

#### 1.3 Load Config Function
- [ ] Write `load_config() -> dict` function
  - [ ] Open CONFIG_PATH
  - [ ] Parse JSON
  - [ ] Return config dictionary
  - [ ] Add error handling for file not found
  - [ ] Add error handling for invalid JSON

#### 1.4 Load Data Entry Content Function
- [ ] Write `load_data_entry_content(file_path: str) -> str` function
  - [ ] Construct full path: Path("mock_data") / file_path
  - [ ] Open file in read mode with UTF-8 encoding
  - [ ] Read and return content
  - [ ] Add error handling for file not found
  - [ ] Log warning if file is empty

#### 1.5 Ingest Single Entry Function - Setup
- [ ] Write `ingest_single_entry(entry: dict, retry_count: int = 0) -> dict` function
  - [ ] Add comprehensive docstring
  - [ ] Log: "Ingesting {entry_id}..."

#### 1.6 Ingest Single Entry Function - Prepare Payload
- [ ] Load content from file using `load_data_entry_content()`
- [ ] Build payload dictionary:
  - [ ] "data_entry_id": entry['id']
  - [ ] "student_id": entry['student_id']
  - [ ] "teacher_id": entry['teacher_id']
  - [ ] "type": entry['type']
  - [ ] "date": entry['date']
  - [ ] "content": content
  - [ ] "metadata": entry['metadata']

#### 1.7 Ingest Single Entry Function - API Call
- [ ] Build URL: f"{BACKEND_URL}/api/data/ingest"
- [ ] Make POST request with JSON payload
- [ ] Set timeout to 30 seconds
- [ ] Capture response

#### 1.8 Ingest Single Entry Function - Response Handling
- [ ] Check response.status_code
- [ ] If 200-299: Parse and return JSON
- [ ] If 400: Log error, don't retry (client error)
- [ ] If 500-599: Retry if retry_count < MAX_RETRIES
- [ ] Raise HTTPError for other errors

#### 1.9 Ingest Single Entry Function - Retry Logic
- [ ] If retry needed:
  - [ ] Increment retry_count
  - [ ] Sleep for RETRY_DELAY * retry_count
  - [ ] Log: "Retrying ({retry_count}/{MAX_RETRIES})..."
  - [ ] Recursively call ingest_single_entry()
- [ ] If max retries exceeded, raise exception

#### 1.10 Main Ingestion Function - Setup
- [ ] Write `main()` function
- [ ] Load config
- [ ] Get data_entries list
- [ ] Log: "Starting ingestion of {len(entries)} data entries..."

#### 1.11 Main Ingestion Function - Results Tracking
- [ ] Initialize results dictionary:
  - [ ] "total_entries": len(entries)
  - [ ] "successful": 0
  - [ ] "failed": 0
  - [ ] "total_assessments": 0
  - [ ] "errors": []
  - [ ] "start_time": time.time()

#### 1.12 Main Ingestion Function - Processing Loop
- [ ] Loop through entries with enumerate (start at 1)
- [ ] Try-except block for each entry:
  - [ ] Log: "[{idx}/{total}] Ingesting {entry_id}..."
  - [ ] Call ingest_single_entry()
  - [ ] On success:
    - [ ] Increment results["successful"]
    - [ ] Add result["assessments_created"] to total_assessments
    - [ ] Log: "✅ Created {count} assessments"
  - [ ] On failure:
    - [ ] Increment results["failed"]
    - [ ] Append error to results["errors"]
    - [ ] Log: "❌ Failed: {error_message}"

#### 1.13 Main Ingestion Function - Rate Limiting
- [ ] After each successful ingestion, check if idx % RATE_LIMIT_PAUSE_EVERY == 0
- [ ] If so:
  - [ ] Log: "⏸️  Pausing for rate limiting..."
  - [ ] Sleep for RATE_LIMIT_PAUSE_SECONDS

#### 1.14 Main Ingestion Function - Summary
- [ ] Calculate total elapsed time
- [ ] Log summary:
  - [ ] "=" separator line
  - [ ] "INGESTION COMPLETE"
  - [ ] Total Entries
  - [ ] Successful
  - [ ] Failed
  - [ ] Total Assessments Created
  - [ ] Total Time
  - [ ] Average Time per Entry

#### 1.15 Main Ingestion Function - Error Report
- [ ] If errors list not empty:
  - [ ] Log: "{len(errors)} errors occurred:"
  - [ ] Loop through errors
  - [ ] Log each: "- {entry_id}: {error_message}"

#### 1.16 Main Ingestion Function - Save Results
- [ ] Save results to `scripts/ingestion_results.json`
- [ ] Use json.dump with indent=2
- [ ] Log: "Results saved to scripts/ingestion_results.json"

#### 1.17 Script Entry Point
- [ ] Add `if __name__ == "__main__":` block
- [ ] Call main()
- [ ] Wrap in try-except for keyboard interrupt
- [ ] Handle Ctrl+C gracefully

---

### 2. Validation Script

- [ ] Create `scripts/validate_ingestion.py` file

#### 2.1 Imports and Setup
- [ ] Import `psycopg2`
- [ ] Import `psycopg2.extras.RealDictCursor`
- [ ] Import `os`
- [ ] Import `json`
- [ ] Import `logging`
- [ ] Import `sys`
- [ ] Add parent directory to path
- [ ] Import `get_db_connection` from backend.database.connection
- [ ] Configure logging
- [ ] Create logger

#### 2.2 Get Database Connection Function
- [ ] Write `get_db_connection()` wrapper
- [ ] Use DATABASE_URL from environment
- [ ] Return connection with RealDictCursor
- [ ] Add error handling

#### 2.3 Run Validation Checks Function - Setup
- [ ] Write `run_validation_checks() -> dict` function
- [ ] Get database connection
- [ ] Create cursor
- [ ] Initialize results dictionary with keys:
  - [ ] "total_data_entries"
  - [ ] "total_assessments"
  - [ ] "assessments_per_student"
  - [ ] "skills_assessed"
  - [ ] "level_distribution"
  - [ ] "confidence_stats"
  - [ ] "validation_passed"

#### 2.4 Check 1: Total Data Entries
- [ ] Execute: `SELECT COUNT(*) as count FROM data_entries`
- [ ] Store result in results["total_data_entries"]
- [ ] Verify count == 76
- [ ] If not, log error and set validation_passed = False

#### 2.5 Check 2: Total Assessments
- [ ] Execute: `SELECT COUNT(*) as count FROM assessments`
- [ ] Store result in results["total_assessments"]
- [ ] Verify count >= 300 (expected avg 4+ per entry)
- [ ] If < 300, log warning

#### 2.6 Check 3: Assessments Per Student
- [ ] Execute query:
  ```sql
  SELECT student_id, COUNT(*) as count
  FROM assessments
  GROUP BY student_id
  ORDER BY student_id
  ```
- [ ] Loop through results
- [ ] Store in results["assessments_per_student"] dictionary
- [ ] Verify each student has > 50 assessments
- [ ] If any student < 50, log warning

#### 2.7 Check 4: All 17 Skills Represented
- [ ] Execute query:
  ```sql
  SELECT DISTINCT skill_name
  FROM assessments
  ORDER BY skill_name
  ```
- [ ] Fetch all skill names
- [ ] Store count in results["skills_assessed"]["total_unique"]
- [ ] Store list in results["skills_assessed"]["list"]
- [ ] Verify count >= 17
- [ ] If < 17, log error and list missing skills

#### 2.8 Check 5: Level Distribution
- [ ] Execute query:
  ```sql
  SELECT level, COUNT(*) as count
  FROM assessments
  GROUP BY level
  ORDER BY level
  ```
- [ ] Loop through results
- [ ] Store in results["level_distribution"] dictionary
- [ ] Verify all 4 levels present (E, D, P, A)
- [ ] Calculate percentages
- [ ] Verify reasonable distribution (no level > 60%)

#### 2.9 Check 6: Confidence Score Statistics
- [ ] Execute query:
  ```sql
  SELECT
    AVG(confidence_score) as avg,
    MIN(confidence_score) as min,
    MAX(confidence_score) as max,
    STDDEV(confidence_score) as stddev
  FROM assessments
  ```
- [ ] Store results in results["confidence_stats"]
- [ ] Verify min >= 0.5 (confidence scoring minimum)
- [ ] Verify max <= 1.0
- [ ] Verify avg between 0.7 and 0.9

#### 2.10 Check 7: No Null Values
- [ ] Execute query:
  ```sql
  SELECT COUNT(*) as count
  FROM assessments
  WHERE justification IS NULL OR source_quote IS NULL
  ```
- [ ] Verify count == 0
- [ ] If > 0, log error and set validation_passed = False

#### 2.11 Check 8: Student Growth Trajectories
- [ ] For each student, query assessments ordered by date
- [ ] Check for level progression (not all Emerging)
- [ ] Verify at least some skills show D or P
- [ ] Store growth indicators in results

#### 2.12 Check 9: Mia Advanced Assessments
- [ ] Execute query:
  ```sql
  SELECT COUNT(*) as count
  FROM assessments
  WHERE student_id = 'S004' AND level = 'Advanced'
  ```
- [ ] Verify count >= 3 (Mia is advanced student)
- [ ] If < 3, log warning

#### 2.13 Finalization
- [ ] Close cursor and connection
- [ ] Return results dictionary

#### 2.14 Print Validation Report Function
- [ ] Write `print_validation_report(results: dict)` function
- [ ] Print formatted report:
  - [ ] Header with separator
  - [ ] Total Data Entries
  - [ ] Total Assessments
  - [ ] Assessments per Student (table)
  - [ ] Skills Assessed count
  - [ ] Level Distribution (with percentages)
  - [ ] Confidence Score Statistics
  - [ ] Validation Status (PASSED/FAILED)

#### 2.15 Script Entry Point
- [ ] Add `if __name__ == "__main__":` block
- [ ] Call run_validation_checks()
- [ ] Call print_validation_report()
- [ ] Exit with code 0 if passed, 1 if failed

---

### 3. Data Quality Check Script

- [ ] Create `scripts/data_quality_check.py` file

#### 3.1 Setup
- [ ] Import required modules
- [ ] Import get_db_connection
- [ ] Configure logging

#### 3.2 Check for Duplicates
- [ ] Write `check_duplicate_assessments() -> list` function
- [ ] Query for duplicate assessments:
  ```sql
  SELECT student_id, skill_name, data_entry_id, COUNT(*) as count
  FROM assessments
  GROUP BY student_id, skill_name, data_entry_id
  HAVING COUNT(*) > 1
  ```
- [ ] Return list of duplicates
- [ ] Log each duplicate found

#### 3.3 Check Confidence Score Range
- [ ] Write `check_confidence_scores() -> dict` function
- [ ] Query for invalid confidence scores:
  ```sql
  SELECT id, confidence_score
  FROM assessments
  WHERE confidence_score < 0.5 OR confidence_score > 1.0
  ```
- [ ] Return count and list of invalid scores
- [ ] Log errors

#### 3.4 Check All Fields Populated
- [ ] Write `check_null_fields() -> dict` function
- [ ] Check for nulls in required fields:
  - [ ] justification
  - [ ] source_quote
  - [ ] skill_name
  - [ ] level
- [ ] Return counts per field
- [ ] Log errors

#### 3.5 Check Skill Distribution
- [ ] Write `check_skill_distribution() -> dict` function
- [ ] Query assessment count per skill
- [ ] Verify no skill has < 10 assessments
- [ ] Verify no skill dominates (> 30% of total)
- [ ] Return distribution stats

#### 3.6 Check Student Progress Realism
- [ ] Write `check_student_progress(student_id: str) -> bool` function
- [ ] For each student, verify:
  - [ ] Not all skills at Emerging
  - [ ] Some progression visible (level changes)
  - [ ] At least 3 skills at Developing or higher
- [ ] Return True if realistic

#### 3.7 Main Quality Check Function
- [ ] Write `main()` function
- [ ] Call all check functions
- [ ] Aggregate issues
- [ ] Print quality report
- [ ] Return True if all checks pass

---

### 4. Performance Testing Script

- [ ] Create `scripts/performance_test.py` file

#### 4.1 Imports and Setup
- [ ] Import `time`
- [ ] Import `requests`
- [ ] Import `statistics`
- [ ] Import `logging`
- [ ] Configure logging

#### 4.2 Test Ingestion Performance
- [ ] Write `test_ingestion_performance(num_requests: int = 10) -> dict` function
- [ ] Load sample data entry from mock_data
- [ ] Loop num_requests times:
  - [ ] Record start time
  - [ ] Make POST to /api/data/ingest
  - [ ] Record end time
  - [ ] Calculate elapsed time
  - [ ] Store in list
- [ ] Calculate statistics:
  - [ ] Average time
  - [ ] Min time
  - [ ] Max time
  - [ ] Standard deviation
- [ ] Return stats dictionary
- [ ] Log results

#### 4.3 Test Assessment Retrieval Performance
- [ ] Write `test_retrieval_performance(student_id: str = "S001") -> dict` function
- [ ] Make 10 requests to /api/assessments/student/{student_id}
- [ ] Time each request
- [ ] Calculate stats
- [ ] Verify average < 500ms
- [ ] Return stats

#### 4.4 Test Skill Trends Performance
- [ ] Write `test_skill_trends_performance(student_id: str = "S001") -> dict` function
- [ ] Make 10 requests to /api/assessments/skill-trends/{student_id}
- [ ] Time each request
- [ ] Calculate stats
- [ ] Verify average < 500ms
- [ ] Return stats

#### 4.5 Test Concurrent Requests
- [ ] Write `test_concurrent_requests(num_concurrent: int = 5) -> dict` function
- [ ] Use threading or asyncio
- [ ] Make num_concurrent simultaneous requests
- [ ] Measure total time
- [ ] Verify no timeouts
- [ ] Verify no errors
- [ ] Return results

#### 4.6 Main Performance Test
- [ ] Write `main()` function
- [ ] Run all performance tests
- [ ] Print performance report
- [ ] Highlight any tests that fail thresholds

---

### 5. Test Data Entry Creation

- [ ] Create `scripts/create_test_entry.py` file

#### 5.1 Generate Test Entry Function
- [ ] Write function to create minimal test data entry
- [ ] Include all required fields
- [ ] Use short sample content
- [ ] Save to `mock_data/test_entry.json`
- [ ] Use for quick testing without full ingestion

---

### 6. Database Reset Script

- [ ] Create `scripts/reset_database.py` file

#### 6.1 Truncate Tables Function
- [ ] Write `truncate_tables()` function
- [ ] Truncate in correct order (respect foreign keys):
  - [ ] teacher_corrections
  - [ ] assessments
  - [ ] data_entries
  - [ ] badges
  - [ ] skill_targets
- [ ] Use CASCADE where appropriate
- [ ] Log each truncation

#### 6.2 Verify Empty Function
- [ ] Write `verify_empty()` function
- [ ] Query count for each table
- [ ] Verify all counts == 0
- [ ] Log results

#### 6.3 Confirmation Prompt
- [ ] Add interactive confirmation before truncating
- [ ] Require typing "CONFIRM" to proceed
- [ ] Add --force flag to skip confirmation

---

### 7. Execution Instructions Document

- [ ] Create `scripts/README.md` file

#### 7.1 Document Script Purposes
- [ ] List all scripts with descriptions
- [ ] Explain execution order
- [ ] Document prerequisites

#### 7.2 Document Execution Steps
- [ ] Step 1: Ensure services running
- [ ] Step 2: Verify backend health
- [ ] Step 3: Run ingestion script
- [ ] Step 4: Run validation script
- [ ] Step 5: Run quality checks
- [ ] Step 6: Run performance tests

#### 7.3 Document Expected Results
- [ ] Expected ingestion time: 30-45 minutes
- [ ] Expected assessments: 300-400
- [ ] Expected validation: All checks pass
- [ ] Expected performance: < 3s per ingestion

#### 7.4 Troubleshooting Guide
- [ ] OpenAI rate limit errors → increase pause
- [ ] Database connection timeouts → check max_connections
- [ ] Missing assessments → check API logs
- [ ] Slow performance → check database indexes

---

### 8. Manual Spot Check Procedure

#### 8.1 Create Spot Check Checklist
- [ ] Create `scripts/manual_spot_check.md` file
- [ ] List manual verification steps:
  - [ ] Open Teacher Dashboard
  - [ ] Select Ms. Rodriguez
  - [ ] View Eva's profile
  - [ ] Check Skill Trends show progression
  - [ ] Open Assessment Review
  - [ ] Verify pending assessments load
  - [ ] Submit test correction
  - [ ] Verify correction saved

#### 8.2 Dashboard Verification
- [ ] Document steps to verify each dashboard page
- [ ] Include expected outcomes
- [ ] Include screenshots (optional)

---

## Testing Checklist

### Pre-Ingestion Setup
- [ ] Verify all services running: `docker-compose ps`
- [ ] All services show "Up" status
- [ ] Test backend health: `curl http://localhost:8000/health`
- [ ] Response shows database connected
- [ ] Verify OpenAI API key set: `docker-compose exec backend env | grep OPENAI_API_KEY`
- [ ] Key present and non-empty

### Ingestion Execution
- [ ] Run ingestion script:
  ```bash
  python scripts/ingest_all_data.py
  ```
- [ ] Monitor output for errors
- [ ] Verify progress updates appear
- [ ] Verify rate limiting pauses occur
- [ ] Wait for completion message
- [ ] Check ingestion_results.json created
- [ ] Verify total_entries == 76
- [ ] Verify successful >= 70 (allow some failures)
- [ ] Verify total_assessments >= 300

### Validation Execution
- [ ] Run validation script:
  ```bash
  python scripts/validate_ingestion.py
  ```
- [ ] Verify all checks pass
- [ ] Review validation report
- [ ] Check total_data_entries == 76
- [ ] Check total_assessments >= 300
- [ ] Check all 17 skills present
- [ ] Check level distribution reasonable
- [ ] Check confidence scores in range

### Data Quality Checks
- [ ] Run data quality script:
  ```bash
  python scripts/data_quality_check.py
  ```
- [ ] Verify no duplicates found
- [ ] Verify no null justifications/quotes
- [ ] Verify all confidence scores valid
- [ ] Verify student progress realistic

### Performance Testing
- [ ] Run performance test script:
  ```bash
  python scripts/performance_test.py
  ```
- [ ] Verify average ingestion time < 3s
- [ ] Verify average retrieval time < 500ms
- [ ] Verify concurrent requests succeed
- [ ] Review performance report

### Manual Dashboard Verification
- [ ] Open Teacher Dashboard: http://localhost:8501
- [ ] Select Teacher: Ms. Rodriguez
- [ ] Navigate to Student Overview
  - [ ] Verify 2 students displayed (Eva, Lucas)
- [ ] Click on Eva
- [ ] Navigate to Skill Trends
  - [ ] Verify skills displayed
  - [ ] Verify charts render
  - [ ] Verify progression visible
- [ ] Navigate to Assessment Review
  - [ ] Verify pending assessments load
  - [ ] Filter for Low Confidence
  - [ ] Verify assessments displayed
- [ ] Open Student Dashboard
- [ ] Select Eva
- [ ] Navigate to Journey Map
  - [ ] Verify skills displayed
  - [ ] Verify progress stages shown
- [ ] Navigate to Badge Collection
  - [ ] Verify badges displayed
- [ ] Navigate to Current Goal
  - [ ] Verify goal displayed (if assigned)

### Database Direct Verification
- [ ] Connect to database:
  ```bash
  docker-compose exec db psql -U flourish_admin -d skills_tracker_db
  ```
- [ ] Check data_entries count:
  ```sql
  SELECT COUNT(*) FROM data_entries;
  ```
  - [ ] Result: 76
- [ ] Check assessments count:
  ```sql
  SELECT COUNT(*) FROM assessments;
  ```
  - [ ] Result: >= 300
- [ ] Check students have assessments:
  ```sql
  SELECT student_id, COUNT(*) FROM assessments GROUP BY student_id;
  ```
  - [ ] All 4 students listed
- [ ] Check all skills present:
  ```sql
  SELECT DISTINCT skill_name FROM assessments ORDER BY skill_name;
  ```
  - [ ] 17 skills listed

### Error Log Review
- [ ] Check backend logs for errors:
  ```bash
  docker-compose logs backend | grep ERROR
  ```
- [ ] Verify no errors (or only acceptable errors)
- [ ] Check frontend logs:
  ```bash
  docker-compose logs frontend | grep ERROR
  ```
- [ ] Verify no errors

---

## Acceptance Criteria

- [ ] All 76 data entries ingested successfully
- [ ] 300+ assessments generated (average 4+ per entry)
- [ ] All 4 students have assessments
- [ ] All 17 skills represented in assessments
- [ ] Level distribution reasonable (mix of E, D, P, A)
- [ ] Confidence scores all within 0.5-1.0 range
- [ ] No duplicate assessments
- [ ] No null justifications or source_quotes
- [ ] Teacher dashboard displays data correctly
- [ ] Student dashboard shows progression accurately
- [ ] API response times meet performance targets:
  - [ ] Ingestion < 3s average
  - [ ] Retrieval < 500ms average
- [ ] Validation script passes all checks
- [ ] Data quality script passes all checks
- [ ] Manual spot checks completed successfully
- [ ] No errors in service logs
- [ ] ingestion_results.json saved with summary

---

## Notes

- Ingestion takes 30-45 minutes due to OpenAI API calls
- Rate limiting (5s pause every 10 requests) prevents API throttling
- Retry logic handles transient failures
- Validation should be run after ingestion completes
- Manual spot checks ensure end-to-end functionality
- Database reset script useful for re-testing
- Save ingestion_results.json for documentation

**Next Shard:** [Shard 8: Integration Testing & Validation](Shard_8_Tasks.md)
