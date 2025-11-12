# Shard 8 Tasks: Integration Testing & Validation

**Status:** ✅ Completed (Core Tests)
**Priority:** P1 (High Priority)
**Dependencies:** All shards (1-7)

---

## Overview

Perform comprehensive end-to-end integration testing, test all user workflows, verify performance benchmarks, and ensure demo readiness. This validates the core system functionality before stakeholder demo.

**Note:** TAR (Teacher Agreement Rate) testing was deferred as it requires pre-labeled expected skills in the mock data configuration.

---

## Prerequisites Checklist

- [x] All Shards 1-7 completed
- [x] All services running without errors
- [x] All 32 data entries ingested (modified scope)
- [x] 31 assessments generated
- [x] Teacher dashboard accessible and functional
- [x] Teacher corrections functional (1 correction submitted during testing)
- [x] Backend API documentation accessible at /docs

---

## Tasks

### 1. TAR (Teacher Agreement Rate) Testing Script

- [ ] Create `scripts/test_ai_accuracy.py` file

#### 1.1 Imports and Setup
- [ ] Import `json`
- [ ] Import `sys`, `os`
- [ ] Add parent directory to path
- [ ] Import `get_db_connection` from backend.database.connection
- [ ] Import `logging`
- [ ] Configure logging

#### 1.2 Load Expected Skills from Config
- [ ] Write `load_expected_skills() -> dict` function
- [ ] Load mock_data/config.json
- [ ] Extract data_entries with 'expected_skills' field
- [ ] Return dictionary: {entry_id: [expected_skills]}
- [ ] Log count of validation entries

#### 1.3 Calculate TAR Function - Setup
- [ ] Write `calculate_tar() -> tuple` function
- [ ] Load expected skills
- [ ] Initialize counters:
  - [ ] total_comparisons = 0
  - [ ] exact_matches = 0
  - [ ] close_matches = 0 (within 1 level)
  - [ ] mismatches = []

#### 1.4 Calculate TAR Function - Query Assessments
- [ ] Get database connection
- [ ] For each entry with expected_skills:
  - [ ] Query assessments WHERE data_entry_id = ?
  - [ ] Get AI-generated skill_name and level
  - [ ] Store in dictionary

#### 1.5 Calculate TAR Function - Compare Levels
- [ ] For each expected skill:
  - [ ] Get expected_level
  - [ ] Get AI level from query results
  - [ ] If AI assessment exists:
    - [ ] Increment total_comparisons
    - [ ] If levels match exactly: increment exact_matches
    - [ ] If levels within 1 (e.g., D vs P): increment close_matches
    - [ ] If mismatch: append to mismatches list
  - [ ] If AI assessment missing:
    - [ ] Log warning: "Skill not assessed by AI"

#### 1.6 Calculate TAR Function - Calculate Rates
- [ ] Calculate exact_tar = (exact_matches / total_comparisons) * 100
- [ ] Calculate close_tar = ((exact_matches + close_matches) / total_comparisons) * 100
- [ ] Return (exact_tar, close_tar, mismatches, total_comparisons)

#### 1.7 Print TAR Report Function
- [ ] Write `print_tar_report(exact_tar, close_tar, mismatches, total)` function
- [ ] Print formatted report:
  - [ ] Header with separator
  - [ ] "Teacher Agreement Rate (TAR) Report"
  - [ ] Total Comparisons
  - [ ] Exact Matches count and percentage
  - [ ] Close Matches count and percentage
  - [ ] Total TAR (exact + close)
  - [ ] Target: >= 85%
  - [ ] Result: PASS or FAIL

#### 1.8 Print Mismatches Function
- [ ] Write `print_mismatches(mismatches: list)` function
- [ ] If mismatches list not empty:
  - [ ] Print "Mismatches Found:"
  - [ ] For each mismatch:
    - [ ] Print entry_id, skill_name
    - [ ] Print Expected: level
    - [ ] Print AI Generated: level
    - [ ] Print Justification (truncated)

#### 1.9 Script Entry Point
- [ ] Add `if __name__ == "__main__":` block
- [ ] Call calculate_tar()
- [ ] Call print_tar_report()
- [ ] If mismatches, call print_mismatches()
- [ ] Exit with code 0 if TAR >= 85%, else 1

---

### 2. End-to-End Workflow Tests

#### 2.1 Test Case 1: Teacher Correction Workflow

- [ ] Create `scripts/test_workflow_correction.py` file

##### Setup
- [ ] Import required modules
- [ ] Import APIClient or use requests directly
- [ ] Configure test constants

##### Step 1: Fetch Pending Assessment
- [ ] Call GET /api/assessments/pending
- [ ] Select first assessment
- [ ] Store assessment_id, original_level
- [ ] Log assessment details

##### Step 2: Submit Correction
- [ ] Build correction payload:
  - [ ] assessment_id
  - [ ] corrected_level (change from original)
  - [ ] corrected_justification
  - [ ] teacher_notes
  - [ ] corrected_by: "T001"
- [ ] Call POST /api/corrections/submit
- [ ] Verify response success
- [ ] Store correction_id

##### Step 3: Verify Correction Saved
- [ ] Query database:
  ```sql
  SELECT * FROM teacher_corrections WHERE id = ?
  ```
- [ ] Verify correction exists
- [ ] Verify corrected_level matches request

##### Step 4: Verify Assessment Marked Corrected
- [ ] Query database:
  ```sql
  SELECT corrected FROM assessments WHERE id = ?
  ```
- [ ] Verify corrected = TRUE

##### Step 5: Verify Few-Shot Retrieval
- [ ] Import FewShotManager
- [ ] Call get_recent_corrections()
- [ ] Verify submitted correction appears in results
- [ ] Log few-shot example

##### Step 6: Test Few-Shot Learning
- [ ] Create similar test data entry
- [ ] Ingest via API
- [ ] Check if AI assessment closer to correction
- [ ] Log comparison

##### Assertions
- [ ] Assert correction saved
- [ ] Assert assessment marked corrected
- [ ] Assert few-shot manager retrieves correction
- [ ] Print "✅ Correction Workflow Test PASSED"

---

#### 2.2 Test Case 2: Target Assignment & Student View

- [ ] Create `scripts/test_workflow_target.py` file

##### Setup
- [ ] Import required modules
- [ ] Select test student: "S001" (Eva)
- [ ] Select test skill: "Self-Management"

##### Step 1: Assign Target
- [ ] Build target assignment payload:
  - [ ] student_id: "S001"
  - [ ] skill_name: "Self-Management"
  - [ ] starting_level: "D"
  - [ ] target_level: "P"
  - [ ] assigned_by: "T001"
- [ ] Call POST /api/students/S001/target-skill
- [ ] Verify response success
- [ ] Store target_id

##### Step 2: Verify Target Saved
- [ ] Query database:
  ```sql
  SELECT * FROM skill_targets WHERE id = ?
  ```
- [ ] Verify target exists
- [ ] Verify starting_level = "D"
- [ ] Verify target_level = "P"
- [ ] Verify completed = FALSE

##### Step 3: Retrieve Targets via API
- [ ] Call GET /api/students/S001/targets?completed=false
- [ ] Verify target appears in response
- [ ] Verify format includes starting_level → target_level

##### Step 4: Simulate Student Dashboard View
- [ ] Call GET /api/students/S001/targets
- [ ] Parse response
- [ ] Format display: "Self-Management: D → P"
- [ ] Log formatted display

##### Step 5: Mark Target Complete
- [ ] Call PUT /api/targets/{target_id}/complete
- [ ] Verify response success

##### Step 6: Verify Completion
- [ ] Query database:
  ```sql
  SELECT completed, completed_at FROM skill_targets WHERE id = ?
  ```
- [ ] Verify completed = TRUE
- [ ] Verify completed_at is set

##### Assertions
- [ ] Assert target assigned successfully
- [ ] Assert starting_level and target_level saved correctly
- [ ] Assert API returns correct format
- [ ] Assert target can be marked complete
- [ ] Print "✅ Target Assignment Workflow Test PASSED"

---

#### 2.3 Test Case 3: Badge Granting

- [ ] Create `scripts/test_workflow_badge.py` file

##### Setup
- [ ] Import required modules
- [ ] Select test student: "S004" (Mia)
- [ ] Select test skill: "Communication"

##### Step 1: Verify Student Has Proficient Assessment
- [ ] Query assessments for S004, Communication
- [ ] Filter for level = "Proficient"
- [ ] If no Proficient, create test assessment
- [ ] Store assessment_id

##### Step 2: Grant Badge
- [ ] Build badge grant payload:
  - [ ] student_id: "S004"
  - [ ] skill_name: "Communication"
  - [ ] skill_category: "21st Century"
  - [ ] level_achieved: "Proficient"
  - [ ] granted_by: "T001"
  - [ ] earned_date: today
- [ ] Call POST /api/badges/grant
- [ ] Verify response success
- [ ] Verify badge_type = "silver" (Proficient)
- [ ] Store badge_id

##### Step 3: Verify Badge Saved
- [ ] Query database:
  ```sql
  SELECT * FROM badges WHERE id = ?
  ```
- [ ] Verify badge exists
- [ ] Verify badge_type = "silver"
- [ ] Verify level_achieved = "Proficient"

##### Step 4: Test Duplicate Prevention
- [ ] Attempt to grant same badge again
- [ ] Verify response is 400 error
- [ ] Verify error message mentions duplicate

##### Step 5: Retrieve Student Badges
- [ ] Call GET /api/badges/students/S004/badges
- [ ] Verify granted badge appears in earned_badges
- [ ] Verify badge has correct color/type

##### Step 6: Verify Locked Badges
- [ ] Check locked_badges in response
- [ ] Verify unearnedskills appear as locked
- [ ] Verify total count = earned + locked

##### Assertions
- [ ] Assert badge granted successfully
- [ ] Assert badge_type calculated correctly (silver for Proficient)
- [ ] Assert duplicate prevention works
- [ ] Assert badge appears in collection
- [ ] Print "✅ Badge Granting Workflow Test PASSED"

---

#### 2.4 Test Case 4: Skill Progression Tracking

- [ ] Create `scripts/test_workflow_progression.py` file

##### Setup
- [ ] Import required modules
- [ ] Select test student: "S001" (Eva)
- [ ] Select test skill: "Self-Awareness"

##### Step 1: Query Initial Assessments
- [ ] Call GET /api/assessments/skill-trends/S001
- [ ] Filter for Self-Awareness
- [ ] Store initial assessments
- [ ] Log initial level (should be Developing or Proficient)

##### Step 2: Ingest New Data Entry (Simulated)
- [ ] Create test data entry showing higher-level behavior
- [ ] Call POST /api/data/ingest
- [ ] Verify assessments created

##### Step 3: Query Updated Assessments
- [ ] Call GET /api/assessments/skill-trends/S001 again
- [ ] Verify new assessment added
- [ ] Check if level increased

##### Step 4: Verify Chart Data
- [ ] Convert levels to numeric (E=1, D=2, P=3, A=4)
- [ ] Verify chronological order
- [ ] Verify progression or stability

##### Step 5: Verify Dashboard Display
- [ ] Simulate Teacher Dashboard Skill Trends page
- [ ] Verify chart shows progression
- [ ] Verify dates align with data

##### Step 6: Verify Student Dashboard Journey Map
- [ ] Simulate Student Dashboard Journey Map
- [ ] Verify current level highlighted
- [ ] Verify completed stages show checkmarks
- [ ] Verify future stages locked

##### Assertions
- [ ] Assert skill trends retrieved correctly
- [ ] Assert progression visible
- [ ] Assert chronological order maintained
- [ ] Print "✅ Skill Progression Tracking Test PASSED"

---

### 3. Performance Benchmarking

#### 3.1 API Endpoint Benchmarks

- [ ] Create `scripts/benchmark_api.py` file

##### Benchmark Ingestion Endpoint
- [ ] Write `benchmark_ingestion(num_requests: int = 10)` function
- [ ] Load sample data entry
- [ ] Make num_requests POST requests
- [ ] Time each request
- [ ] Calculate statistics: avg, min, max, p50, p95
- [ ] Verify avg < 3 seconds
- [ ] Log results

##### Benchmark Assessment Retrieval
- [ ] Write `benchmark_retrieval(num_requests: int = 100)` function
- [ ] Make num_requests GET requests to /api/assessments/student/S001
- [ ] Time each request
- [ ] Calculate statistics
- [ ] Verify avg < 500ms
- [ ] Log results

##### Benchmark Skill Trends
- [ ] Write `benchmark_skill_trends(num_requests: int = 50)` function
- [ ] Make num_requests GET requests to /api/assessments/skill-trends/S001
- [ ] Time each request
- [ ] Calculate statistics
- [ ] Verify avg < 500ms
- [ ] Log results

##### Benchmark Dashboard Load
- [ ] Write `benchmark_dashboard_load()` function
- [ ] Use requests to load Streamlit pages
- [ ] Measure response time
- [ ] Verify < 3 seconds
- [ ] Log results

##### Print Benchmark Report
- [ ] Write `print_benchmark_report(results: dict)` function
- [ ] Display table with:
  - [ ] Endpoint
  - [ ] Avg Time
  - [ ] Min Time
  - [ ] Max Time
  - [ ] P95 Time
  - [ ] Target
  - [ ] Status (PASS/FAIL)

#### 3.2 Database Query Performance

- [ ] Create `scripts/benchmark_database.py` file

##### Benchmark Assessment Queries
- [ ] Test query: SELECT * FROM assessments WHERE student_id = ?
- [ ] Run EXPLAIN ANALYZE
- [ ] Verify execution time < 100ms
- [ ] Log query plan

##### Benchmark Skill Trends Query
- [ ] Test skill trends query (grouped by skill, ordered by date)
- [ ] Run EXPLAIN ANALYZE
- [ ] Verify execution time < 200ms
- [ ] Verify indexes used

##### Benchmark Pending Assessments Query
- [ ] Test query: SELECT * FROM assessments WHERE corrected = FALSE ORDER BY confidence_score ASC
- [ ] Run EXPLAIN ANALYZE
- [ ] Verify idx_assessments_pending index used
- [ ] Verify execution time < 100ms

##### Check Index Usage
- [ ] Query pg_stat_user_indexes
- [ ] Verify all defined indexes being used
- [ ] Log unused indexes (if any)

---

### 4. Data Quality Validation

#### 4.1 Comprehensive Data Quality Script

- [ ] Create `scripts/validate_data_quality.py` file

##### Check 1: No Duplicate Assessments
- [ ] Query for duplicates (same student, skill, data_entry)
- [ ] Verify count = 0
- [ ] Log result

##### Check 2: Confidence Scores in Range
- [ ] Query for confidence_score < 0.5 or > 1.0
- [ ] Verify count = 0
- [ ] Log result

##### Check 3: All Required Fields Populated
- [ ] Query for NULL justification or source_quote
- [ ] Verify count = 0
- [ ] Log result

##### Check 4: Growth Trajectories Realistic
- [ ] For each student:
  - [ ] Verify not all Emerging
  - [ ] Verify some progression visible
  - [ ] Verify at least 3 skills at D or higher
- [ ] Log per-student results

##### Check 5: Mia Has Advanced Assessments
- [ ] Query S004 for Advanced level assessments
- [ ] Verify count >= 3
- [ ] Log result

##### Check 6: Eva Shows Steady Growth
- [ ] Query S001 assessments ordered by date
- [ ] Verify progression from D to P in multiple skills
- [ ] Log result

##### Check 7: Lucas Shows EF Breakthrough
- [ ] Query S002 for Planning & Prioritization
- [ ] Verify progression from E to D or P
- [ ] Query S002 for Organization
- [ ] Verify progression visible
- [ ] Log result

##### Check 8: Pat Shows Late Bloom
- [ ] Query S003 assessments
- [ ] Verify early assessments mostly D/E
- [ ] Verify October assessments include P
- [ ] Log result

##### Print Quality Report
- [ ] Display comprehensive quality report
- [ ] List all checks with PASS/FAIL
- [ ] Provide recommendations if failures

---

### 5. Demo Readiness Checklist

- [ ] Create `scripts/demo_readiness.py` file

#### 5.1 Service Health Checks
- [ ] Write `check_services()` function
- [ ] Verify docker containers running:
  - [ ] `docker-compose ps` all "Up"
- [ ] Verify backend health endpoint
- [ ] Verify frontend accessible
- [ ] Verify database connectable
- [ ] Return True if all pass

#### 5.2 Data Completeness Checks
- [ ] Write `check_data_completeness()` function
- [ ] Verify 76 data entries
- [ ] Verify 300+ assessments
- [ ] Verify all 4 students have data
- [ ] Verify all 17 skills represented
- [ ] Return True if all pass

#### 5.3 Dashboard Functionality Checks
- [ ] Write `check_dashboards()` function
- [ ] Test Teacher Dashboard pages:
  - [ ] Student Overview loads
  - [ ] Skill Trends loads
  - [ ] Assessment Review loads
  - [ ] Target Assignment loads
- [ ] Test Student Dashboard pages:
  - [ ] Journey Map loads
  - [ ] Badge Collection loads
  - [ ] Current Goal loads
- [ ] Return True if all load without errors

#### 5.4 Workflow Checks
- [ ] Write `check_workflows()` function
- [ ] Verify correction workflow functional
- [ ] Verify target assignment functional
- [ ] Verify badge granting functional
- [ ] Return True if all pass

#### 5.5 Performance Checks
- [ ] Write `check_performance()` function
- [ ] Verify API response times meet targets
- [ ] Verify dashboard load times acceptable
- [ ] Return True if all meet targets

#### 5.6 AI Accuracy Check
- [ ] Write `check_ai_accuracy()` function
- [ ] Calculate TAR
- [ ] Verify TAR >= 85%
- [ ] Return True if passes

#### 5.7 Main Readiness Check
- [ ] Write `main()` function
- [ ] Run all check functions
- [ ] Aggregate results
- [ ] Print readiness report:
  - [ ] Service Health: PASS/FAIL
  - [ ] Data Completeness: PASS/FAIL
  - [ ] Dashboard Functionality: PASS/FAIL
  - [ ] Workflows: PASS/FAIL
  - [ ] Performance: PASS/FAIL
  - [ ] AI Accuracy: PASS/FAIL
  - [ ] Overall: DEMO READY / NOT READY
- [ ] Exit with code 0 if ready, 1 if not

---

### 6. Test Execution Orchestration

- [ ] Create `scripts/run_all_tests.sh` bash script

#### 6.1 Script Header
- [ ] Add shebang: `#!/bin/bash`
- [ ] Add description comments
- [ ] Set -e flag (exit on error)

#### 6.2 Service Check
- [ ] Echo "Checking services..."
- [ ] Run docker-compose ps
- [ ] Verify all services up
- [ ] Echo "✅ Services running"

#### 6.3 Data Validation
- [ ] Echo "Running data validation..."
- [ ] Run python scripts/validate_ingestion.py
- [ ] Check exit code
- [ ] Echo result

#### 6.4 Data Quality
- [ ] Echo "Running data quality checks..."
- [ ] Run python scripts/validate_data_quality.py
- [ ] Check exit code
- [ ] Echo result

#### 6.5 AI Accuracy
- [ ] Echo "Testing AI accuracy (TAR)..."
- [ ] Run python scripts/test_ai_accuracy.py
- [ ] Check exit code
- [ ] Echo result

#### 6.6 Workflow Tests
- [ ] Echo "Running workflow tests..."
- [ ] Run python scripts/test_workflow_correction.py
- [ ] Run python scripts/test_workflow_target.py
- [ ] Run python scripts/test_workflow_badge.py
- [ ] Run python scripts/test_workflow_progression.py
- [ ] Check exit codes
- [ ] Echo results

#### 6.7 Performance Benchmarks
- [ ] Echo "Running performance benchmarks..."
- [ ] Run python scripts/benchmark_api.py
- [ ] Run python scripts/benchmark_database.py
- [ ] Check exit codes
- [ ] Echo results

#### 6.8 Demo Readiness
- [ ] Echo "Checking demo readiness..."
- [ ] Run python scripts/demo_readiness.py
- [ ] Check exit code
- [ ] Echo result

#### 6.9 Final Summary
- [ ] Echo separator line
- [ ] Echo "ALL TESTS COMPLETE"
- [ ] Echo pass/fail counts
- [ ] Exit with appropriate code

---

### 7. Manual Testing Protocol

- [ ] Create `docs/Manual_Testing_Protocol.md` file

#### 7.1 Teacher Dashboard Testing
- [ ] Document step-by-step testing procedure
- [ ] Include screenshots (optional)
- [ ] List expected outcomes
- [ ] Include test data to use

#### 7.2 Student Dashboard Testing
- [ ] Document step-by-step testing procedure
- [ ] Include expected UI elements
- [ ] List animation triggers to verify

#### 7.3 Error Scenario Testing
- [ ] Document how to test error handling
- [ ] Include invalid inputs to try
- [ ] Verify error messages are user-friendly

---

### 8. Final Validation Checklist

- [ ] Create `docs/Final_Validation_Checklist.md` file

#### 8.1 Data Checklist
- [ ] 76 data entries ingested
- [ ] 300+ assessments generated
- [ ] All 4 students have data
- [ ] Eva shows steady growth
- [ ] Lucas shows EF breakthrough
- [ ] Pat shows late bloom
- [ ] Mia has 5+ Advanced skills

#### 8.2 Functionality Checklist
- [ ] All API endpoints functional
- [ ] Teacher correction workflow works
- [ ] Target assignment works
- [ ] Badge granting works
- [ ] Few-shot learning works
- [ ] Dashboard navigation works

#### 8.3 Quality Checklist
- [ ] TAR >= 85%
- [ ] No duplicate assessments
- [ ] All confidence scores valid
- [ ] All fields populated
- [ ] Realistic growth trajectories

#### 8.4 Performance Checklist
- [ ] API response times meet targets
- [ ] Dashboard loads < 3s
- [ ] No timeout errors
- [ ] Database queries optimized

#### 8.5 Demo Checklist
- [ ] All services start with docker-compose up
- [ ] Teacher dashboard navigable
- [ ] Student dashboard engaging
- [ ] No console errors
- [ ] Representative data visible

---

## Testing Checklist

### TAR Testing
- [ ] Run test_ai_accuracy.py:
  ```bash
  python scripts/test_ai_accuracy.py
  ```
- [ ] Verify TAR >= 85%
- [ ] Review mismatches
- [ ] If TAR < 85%:
  - [ ] Review mismatched assessments
  - [ ] Check if rubric alignment issues
  - [ ] Add more few-shot examples
  - [ ] Re-test

### Workflow Testing
- [ ] Run all workflow tests:
  ```bash
  python scripts/test_workflow_correction.py
  python scripts/test_workflow_target.py
  python scripts/test_workflow_badge.py
  python scripts/test_workflow_progression.py
  ```
- [ ] Verify all print "✅ PASSED"
- [ ] Review any failures

### Performance Testing
- [ ] Run benchmark scripts:
  ```bash
  python scripts/benchmark_api.py
  python scripts/benchmark_database.py
  ```
- [ ] Verify all targets met
- [ ] Review performance report
- [ ] Note any slow queries

### Data Quality Testing
- [ ] Run validate_data_quality.py:
  ```bash
  python scripts/validate_data_quality.py
  ```
- [ ] Verify all checks pass
- [ ] Review any quality issues

### Demo Readiness
- [ ] Run demo_readiness.py:
  ```bash
  python scripts/demo_readiness.py
  ```
- [ ] Verify overall status: DEMO READY
- [ ] Fix any failing checks
- [ ] Re-run until ready

### Manual Testing
- [ ] Follow Manual Testing Protocol
- [ ] Test Teacher Dashboard:
  - [ ] Student Overview
  - [ ] Skill Trends
  - [ ] Assessment Review
  - [ ] Target Assignment
- [ ] Test Student Dashboard:
  - [ ] Journey Map
  - [ ] Badge Collection
  - [ ] Current Goal
- [ ] Verify animations work
- [ ] Verify error handling

### Full Test Suite
- [ ] Run run_all_tests.sh:
  ```bash
  bash scripts/run_all_tests.sh
  ```
- [ ] Monitor output
- [ ] Verify all sections pass
- [ ] Review summary

### API Documentation
- [ ] Open http://localhost:8000/docs
- [ ] Test each endpoint via Swagger UI
- [ ] Verify examples work
- [ ] Verify response schemas correct

### Browser Console Check
- [ ] Open Teacher Dashboard in browser
- [ ] Open Developer Tools (F12)
- [ ] Check Console tab for errors
- [ ] Navigate all pages
- [ ] Verify no JavaScript errors
- [ ] Repeat for Student Dashboard

### Log Review
- [ ] Check backend logs:
  ```bash
  docker-compose logs backend --tail=100
  ```
- [ ] Verify no ERROR level logs (or only acceptable ones)
- [ ] Check frontend logs:
  ```bash
  docker-compose logs frontend --tail=100
  ```
- [ ] Verify no errors

---

## Acceptance Criteria

### AI Accuracy
- [ ] TAR (Teacher Agreement Rate) >= 85%
- [ ] Confidence scores align with assessment quality
- [ ] Few-shot learning demonstrates improvement after corrections

### Workflows
- [ ] Teacher correction workflow functional end-to-end
- [ ] Target assignment works with starting_level → target_level format
- [ ] Badge granting functional, duplicate prevention works
- [ ] Student journey map accurately shows progression

### Performance
- [ ] Ingestion API < 3s average response time
- [ ] Assessment retrieval < 500ms average
- [ ] Skill trends query < 500ms average
- [ ] Dashboard loads < 3s
- [ ] No performance degradation with full dataset

### Data Quality
- [ ] No duplicate assessments
- [ ] No malformed data (NULL required fields)
- [ ] All students show realistic growth trajectories
- [ ] All 17 skills represented across dataset
- [ ] Level distribution reasonable (mix of E, D, P, A)

### Demo Readiness
- [ ] All services start successfully with `docker-compose up`
- [ ] Teacher dashboard navigable without errors
- [ ] Student dashboard engaging and accurate
- [ ] No console errors or warnings in browser
- [ ] Representative data for each student archetype
- [ ] At least 5 teacher corrections submitted for demo
- [ ] Badges displayed correctly (bronze/silver/gold)
- [ ] Faded badges shown for locked skills
- [ ] Target assignments display correct format
- [ ] Charts render correctly in Skill Trends
- [ ] Journey Map animations trigger appropriately

---

## Notes

- TAR target of 85% represents strong AI accuracy while allowing for some expected variance
- Few-shot learning effectiveness should be demonstrated by improved assessments after corrections
- Performance benchmarks ensure good user experience
- Manual testing verifies edge cases and UI/UX quality
- Demo readiness script provides final go/no-go decision
- All test results should be documented for stakeholder review

**Final Step:** Demo rehearsal and stakeholder presentation preparation
