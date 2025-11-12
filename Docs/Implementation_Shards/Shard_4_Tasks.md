# Shard 4 Tasks: Backend API Layer

**Status:** ✅ Completed
**Priority:** P0 (Critical Path)
**Dependencies:** Shards 1, 3 (Database + AI Pipeline)

---

## Overview

Build FastAPI REST API with 15+ endpoints for data ingestion, assessment retrieval, teacher corrections, student progress tracking, and badge management. Implement request validation, error handling, and database transaction management.

---

## Prerequisites Checklist

- [x] Shard 1 completed (Database running)
- [x] Shard 3 completed (AI inference engine functional)
- [x] FastAPI and Pydantic packages installed
- [x] Understanding of REST API design principles
- [x] PostgreSQL connection working
- [x] OpenAI API integration tested

---

## Tasks

### 1. Pydantic Models (Schemas)

- [x] Create `backend/models/schemas.py` file

#### 1.1 Data Ingestion Schemas
- [x] Import `pydantic.BaseModel`, `pydantic.Field`
- [x] Import `datetime.date`
- [x] Import `typing.Optional`, `typing.Dict`, `typing.Any`

- [x] Create `DataEntryRequest` schema
  - [x] `data_entry_id: str`
  - [x] `student_id: str`
  - [x] `teacher_id: str`
  - [x] `type: str` (field with choices validation)
  - [x] `date: str` (YYYY-MM-DD format)
  - [x] `content: str`
  - [x] `metadata: Dict[str, Any]`
  - [x] Add field validators for date format
  - [x] Add field validators for type enum

- [x] Create `DataEntryResponse` schema
  - [x] `success: bool`
  - [x] `data_entry_id: str`
  - [x] `assessments_created: int`
  - [x] `assessment_ids: list[int]`

#### 1.2 Assessment Schemas
- [x] Create `AssessmentResponse` schema
  - [x] `id: int`
  - [x] `data_entry_id: str`
  - [x] `student_id: str`
  - [x] `skill_name: str`
  - [x] `skill_category: str`
  - [x] `level: str`
  - [x] `confidence_score: float`
  - [x] `justification: str`
  - [x] `source_quote: str`
  - [x] `data_point_count: int`
  - [x] `rubric_version: str`
  - [x] `corrected: bool`
  - [x] `created_at: str`

- [x] Create `SkillTrendResponse` schema
  - [x] `skill_name: str`
  - [x] `skill_category: str`
  - [x] `assessments: list[dict]` (date, level, confidence)

#### 1.3 Correction Schemas
- [x] Create `CorrectionRequest` schema
  - [x] `assessment_id: int`
  - [x] `corrected_level: str`
  - [x] `corrected_justification: Optional[str]`
  - [x] `teacher_notes: Optional[str]`
  - [x] `corrected_by: str` (teacher_id)

- [x] Create `CorrectionResponse` schema
  - [x] `success: bool`
  - [x] `correction_id: int`
  - [x] `message: str`

- [x] Create `ApprovalRequest` schema
  - [x] `assessment_id: int`
  - [x] `approved_by: str` (teacher_id)

#### 1.4 Student & Target Schemas
- [x] Create `StudentResponse` schema
  - [x] `id: str`
  - [x] `name: str`
  - [x] `grade: int`
  - [x] `teacher_id: str`
  - [x] `created_at: str`

- [x] Create `StudentProgressResponse` schema
  - [x] `student_id: str`
  - [x] `student_name: str`
  - [x] `total_assessments: int`
  - [x] `total_badges: int`
  - [x] `active_targets: int`
  - [x] `recent_growth: list[dict]`

- [x] Create `TargetAssignmentRequest` schema
  - [x] `student_id: str`
  - [x] `skill_name: str`
  - [x] `starting_level: str`
  - [x] `target_level: str`
  - [x] `assigned_by: str` (teacher_id)

- [x] Create `TargetResponse` schema
  - [x] `id: int`
  - [x] `student_id: str`
  - [x] `skill_name: str`
  - [x] `starting_level: str`
  - [x] `target_level: str`
  - [x] `assigned_by: str`
  - [x] `assigned_at: str`
  - [x] `completed: bool`
  - [x] `completed_at: Optional[str]`

#### 1.5 Badge Schemas
- [x] Create `BadgeResponse` schema
  - [x] `id: int`
  - [x] `student_id: str`
  - [x] `skill_name: str`
  - [x] `skill_category: str`
  - [x] `level_achieved: str`
  - [x] `badge_type: str` (bronze/silver/gold)
  - [x] `granted_by: str`
  - [x] `earned_date: str`
  - [x] `created_at: str`

- [x] Create `BadgeGrantRequest` schema
  - [x] `student_id: str`
  - [x] `skill_name: str`
  - [x] `skill_category: str`
  - [x] `level_achieved: str`
  - [x] `granted_by: str` (teacher_id)
  - [x] `earned_date: str`

- [x] Create `BadgeCollectionResponse` schema
  - [x] `student_id: str`
  - [x] `earned_badges: list[BadgeResponse]`
  - [x] `locked_badges: list[dict]` (skill_name, level, badge_type)
  - [x] `total_earned: int`
  - [x] `total_possible: int`

---

### 2. Data Ingestion Router

- [x] Create `backend/routers/data_ingest.py` file

#### 2.1 Router Setup
- [x] Import `fastapi.APIRouter`, `fastapi.HTTPException`
- [x] Import schemas from `backend.models.schemas`
- [x] Import `get_db_connection` from `backend.database.connection`
- [x] Import `SkillInferenceEngine`, `load_rubric` from `backend.ai`
- [x] Import `os`, `logging`
- [x] Create router instance with prefix="/api/data" and tag="Data Ingestion"
- [x] Create logger

#### 2.2 POST /ingest Endpoint - Setup
- [x] Create `@router.post("/ingest", response_model=DataEntryResponse)` decorator
- [x] Write `ingest_data_entry(entry: DataEntryRequest)` async function
- [x] Add docstring explaining endpoint purpose

#### 2.3 POST /ingest Endpoint - Database Insertion
- [x] Get database connection
- [x] Create cursor
- [x] Begin transaction (set autocommit=False)
- [x] Write INSERT INTO data_entries SQL
  - [x] Insert id, student_id, teacher_id, type, date, content, metadata
  - [x] Use parameterized query to prevent SQL injection
- [x] Execute INSERT with try-except block
- [x] Catch IntegrityError for duplicate entry_id
  - [x] Return HTTPException 400 if duplicate
- [x] Commit transaction

#### 2.4 POST /ingest Endpoint - AI Inference
- [x] Load rubric using `load_rubric()`
- [x] Get OpenAI API key from environment
- [x] Create SkillInferenceEngine instance
- [x] Prepare student_data dictionary with content and metadata
- [x] Call `engine.assess_skills(student_data)`
- [x] Store assessments result

#### 2.5 POST /ingest Endpoint - Assessment Storage
- [x] Loop through assessments
  - [x] Write INSERT INTO assessments SQL
  - [x] Insert data_entry_id, student_id, skill_name, skill_category, level, confidence_score, justification, source_quote, data_point_count
  - [x] Execute INSERT RETURNING id
  - [x] Collect assessment_ids
- [x] Commit transaction
- [x] Close cursor and connection

#### 2.6 POST /ingest Endpoint - Response
- [x] Return DataEntryResponse with:
  - [x] success=True
  - [x] data_entry_id
  - [x] assessments_created count
  - [x] assessment_ids list

#### 2.7 POST /ingest Endpoint - Error Handling
- [x] Add global exception handler
- [x] Rollback transaction on error
- [x] Log error details
- [x] Return HTTPException 500 with error message

---

### 3. Assessments Router

- [x] Create `backend/routers/assessments.py` file

#### 3.1 Router Setup
- [x] Import required modules (APIRouter, HTTPException, schemas, database)
- [x] Create router with prefix="/api/assessments" and tag="Assessments"

#### 3.2 GET /student/{student_id} Endpoint
- [x] Create `@router.get("/student/{student_id}")` decorator
- [x] Write `get_student_assessments(student_id: str)` function
- [x] Get database connection
- [x] Query assessments table WHERE student_id = ?
- [x] Order by created_at DESC
- [x] Fetch all results
- [x] Convert to AssessmentResponse list
- [x] Return results
- [x] Add error handling for database errors

#### 3.3 GET /skill-trends/{student_id} Endpoint
- [x] Create `@router.get("/skill-trends/{student_id}")` decorator
- [x] Write `get_skill_trends(student_id: str)` function
- [x] Get database connection
- [x] Query assessments grouped by skill_name
- [x] Order by date ASC within each skill
- [x] Fetch all results
- [x] Group results by skill_name into dictionary
- [x] For each skill, create list of {date, level, confidence}
- [x] Convert levels to numeric for charting (E=1, D=2, P=3, A=4)
- [x] Return SkillTrendResponse list
- [x] Add error handling

#### 3.4 GET /pending Endpoint
- [x] Create `@router.get("/pending")` decorator
- [x] Write `get_pending_assessments(limit: int = 50)` function
- [x] Get database connection
- [x] Query assessments WHERE corrected = FALSE
- [x] Order by confidence_score ASC, created_at DESC
- [x] LIMIT to specified limit (default 50)
- [x] Optional query parameter: min_confidence (filter < threshold)
- [x] Fetch results
- [x] Return AssessmentResponse list
- [x] Add error handling

#### 3.5 GET /{assessment_id} Endpoint
- [x] Create `@router.get("/{assessment_id}")` decorator
- [x] Write `get_assessment_by_id(assessment_id: int)` function
- [x] Get database connection
- [x] Query assessments WHERE id = ?
- [x] Fetch one result
- [x] If not found, raise HTTPException 404
- [x] Return AssessmentResponse
- [x] Add error handling

---

### 4. Corrections Router

- [x] Create `backend/routers/corrections.py` file

#### 4.1 Router Setup
- [x] Import required modules
- [x] Create router with prefix="/api/corrections" and tag="Teacher Corrections"

#### 4.2 POST /submit Endpoint - Setup
- [x] Create `@router.post("/submit", response_model=CorrectionResponse)` decorator
- [x] Write `submit_correction(correction: CorrectionRequest)` function
- [x] Add docstring

#### 4.3 POST /submit Endpoint - Validation
- [x] Get database connection
- [x] Query assessments to verify assessment_id exists
- [x] If not found, raise HTTPException 404
- [x] Store original_level from assessment

#### 4.4 POST /submit Endpoint - Insert Correction
- [x] Write INSERT INTO teacher_corrections SQL
  - [x] assessment_id
  - [x] original_level
  - [x] corrected_level
  - [x] original_justification (from assessment)
  - [x] corrected_justification (from request, or use original if None)
  - [x] teacher_notes
  - [x] corrected_by
- [x] Execute INSERT RETURNING id
- [x] Store correction_id

#### 4.5 POST /submit Endpoint - Update Assessment
- [x] Write UPDATE assessments SET corrected = TRUE WHERE id = ?
- [x] Execute UPDATE
- [x] Commit transaction
- [x] Close cursor and connection

#### 4.6 POST /submit Endpoint - Response
- [x] Return CorrectionResponse with:
  - [x] success=True
  - [x] correction_id
  - [x] message="Correction submitted successfully"

#### 4.7 POST /submit Endpoint - Error Handling
- [x] Add exception handlers for database errors
- [x] Rollback on error
- [x] Return HTTPException 500

#### 4.8 POST /assessments/{id}/approve Endpoint
- [x] Create endpoint for approving assessment as-is
- [x] Require ApprovalRequest body
- [x] UPDATE assessments SET corrected = TRUE WHERE id = ?
- [x] Return success response
- [x] Add error handling

#### 4.9 GET /recent Endpoint
- [x] Create `@router.get("/recent")` decorator
- [x] Write `get_recent_corrections(limit: int = 10)` function
- [x] Query teacher_corrections with JOIN to assessments
- [x] Order by corrected_at DESC
- [x] LIMIT to specified limit
- [x] Return list of correction objects
- [x] Add error handling

---

### 5. Students Router

- [x] Create `backend/routers/students.py` file

#### 5.1 Router Setup
- [x] Import required modules
- [x] Create router with prefix="/api/students" and tag="Students"

#### 5.2 GET / Endpoint
- [x] Create `@router.get("/")` decorator
- [x] Write `get_students(teacher_id: Optional[str] = None)` function
- [x] Get database connection
- [x] Query students table
- [x] If teacher_id provided, add WHERE teacher_id = ?
- [x] Order by name ASC
- [x] Fetch all results
- [x] Return StudentResponse list
- [x] Add error handling

#### 5.3 GET /{student_id}/progress Endpoint
- [x] Create `@router.get("/{student_id}/progress")` decorator
- [x] Write `get_student_progress(student_id: str)` function
- [x] Get database connection
- [x] Query student info from students table
- [x] Query total assessments COUNT
- [x] Query total badges COUNT
- [x] Query active targets COUNT WHERE completed = FALSE
- [x] Query recent growth (last 5 assessments with level changes)
- [x] Combine results into StudentProgressResponse
- [x] Return response
- [x] Add error handling for student not found

#### 5.4 POST /{student_id}/target-skill Endpoint
- [x] Create `@router.post("/{student_id}/target-skill")` decorator
- [x] Write `assign_target_skill(student_id: str, target: TargetAssignmentRequest)` function
- [x] Validate student_id matches request body
- [x] Get database connection
- [x] Check if active target already exists for this skill
- [x] If exists and not completed, raise HTTPException 400
- [x] Write INSERT INTO skill_targets SQL
  - [x] student_id
  - [x] skill_name
  - [x] starting_level
  - [x] target_level
  - [x] assigned_by
  - [x] assigned_at (NOW())
- [x] Execute INSERT RETURNING id
- [x] Return TargetResponse
- [x] Add error handling

#### 5.5 GET /{student_id}/targets Endpoint
- [x] Create `@router.get("/{student_id}/targets")` decorator
- [x] Write `get_student_targets(student_id: str, completed: Optional[bool] = None)` function
- [x] Get database connection
- [x] Query skill_targets WHERE student_id = ?
- [x] If completed parameter provided, add WHERE completed = ?
- [x] Order by assigned_at DESC
- [x] Fetch all results
- [x] Return TargetResponse list
- [x] Add error handling

#### 5.6 PUT /targets/{target_id}/complete Endpoint
- [x] Create `@router.put("/targets/{target_id}/complete")` decorator
- [x] Write `complete_target(target_id: int)` function
- [x] Get database connection
- [x] UPDATE skill_targets SET completed = TRUE, completed_at = NOW()
- [x] WHERE id = ?
- [x] Execute UPDATE
- [x] Return success response
- [x] Add error handling

---

### 6. Badges Router

- [x] Create `backend/routers/badges.py` file

#### 6.1 Router Setup
- [x] Import required modules
- [x] Create router with prefix="/api/badges" and tag="Badges"

#### 6.2 GET /students/{student_id}/badges Endpoint
- [x] Create `@router.get("/students/{student_id}/badges")` decorator
- [x] Write `get_student_badges(student_id: str)` function
- [x] Get database connection
- [x] Query badges table WHERE student_id = ?
- [x] Order by earned_date DESC
- [x] Fetch earned badges
- [x] Generate locked badges list (all 17 skills at 3 levels = 51 possible)
- [x] Filter out earned badges from locked list
- [x] Calculate total_earned and total_possible
- [x] Return BadgeCollectionResponse
- [x] Add error handling

#### 6.3 POST /grant Endpoint - Setup
- [x] Create `@router.post("/grant")` decorator
- [x] Write `grant_badge(badge: BadgeGrantRequest)` function
- [x] Add docstring explaining teacher-only action

#### 6.4 POST /grant Endpoint - Validation
- [x] Validate level_achieved is one of: Developing, Proficient, Advanced
- [x] Determine badge_type based on level:
  - [x] Developing → bronze
  - [x] Proficient → silver
  - [x] Advanced → gold
- [x] Get database connection

#### 6.5 POST /grant Endpoint - Check Existing Badge
- [x] Query badges WHERE student_id = ? AND skill_name = ? AND level_achieved = ?
- [x] If badge already exists, raise HTTPException 400 "Badge already granted"

#### 6.6 POST /grant Endpoint - Insert Badge
- [x] Write INSERT INTO badges SQL
  - [x] student_id
  - [x] skill_name
  - [x] skill_category
  - [x] level_achieved
  - [x] badge_type
  - [x] granted_by
  - [x] earned_date
- [x] Execute INSERT RETURNING id
- [x] Commit transaction
- [x] Return BadgeResponse
- [x] Add error handling

#### 6.7 GET /students/{student_id}/badge-progress Endpoint
- [x] Create endpoint to calculate badge progress
- [x] Count earned badges by category (SEL, EF, 21st Century)
- [x] Count by badge type (bronze, silver, gold)
- [x] Return progress metrics
- [x] Add error handling

---

### 7. Main FastAPI Application

- [x] Open/create `backend/main.py` file

#### 7.1 Imports
- [x] Import `fastapi.FastAPI`
- [x] Import `fastapi.middleware.cors.CORSMiddleware`
- [x] Import all routers (data_ingest, assessments, corrections, students, badges)
- [x] Import `logging`
- [x] Import `os` for environment variables

#### 7.2 Logger Setup
- [x] Configure logging with INFO level
- [x] Create logger instance

#### 7.3 FastAPI App Initialization
- [x] Create FastAPI instance with:
  - [x] title="Flourish Skills Tracker API"
  - [x] version="1.0.0"
  - [x] description="AI-powered soft skills assessment API"
- [x] Add docstring to app

#### 7.4 CORS Middleware
- [x] Add CORSMiddleware to app
  - [x] allow_origins=["http://localhost:8501", "http://frontend:8501"]
  - [x] allow_credentials=True
  - [x] allow_methods=["*"]
  - [x] allow_headers=["*"]
- [x] Add comment explaining CORS for Streamlit

#### 7.5 Router Inclusion
- [x] Include data_ingest router
- [x] Include assessments router
- [x] Include corrections router
- [x] Include students router
- [x] Include badges router

#### 7.6 Root Endpoint
- [x] Create `@app.get("/")` endpoint
- [x] Return JSON with:
  - [x] message="Flourish Skills Tracker API"
  - [x] version="1.0.0"
  - [x] docs_url="/docs"

#### 7.7 Health Check Endpoint
- [x] Create `@app.get("/health")` endpoint
- [x] Test database connection using `test_connection()`
- [x] Return JSON with:
  - [x] status="healthy"
  - [x] database="connected" or "disconnected"
  - [x] version="1.0.0"
- [x] Add error handling

#### 7.8 Startup Event
- [x] Create `@app.on_event("startup")` handler
- [x] Log "FastAPI server starting..."
- [x] Test database connection
- [x] Log database connection status
- [x] Test OpenAI API key exists
- [x] Log OpenAI integration status

#### 7.9 Shutdown Event
- [x] Create `@app.on_event("shutdown")` handler
- [x] Log "FastAPI server shutting down..."
- [x] Close any open connections

---

### 8. API Documentation Enhancement

#### 8.1 Schema Examples
- [x] Add example values to Pydantic schemas using `Field(..., example=...)`
- [x] Add examples for DataEntryRequest
- [x] Add examples for CorrectionRequest
- [x] Add examples for TargetAssignmentRequest
- [x] Add examples for BadgeGrantRequest

#### 8.2 Endpoint Descriptions
- [x] Add detailed descriptions to each endpoint using docstrings
- [x] Add summary and description to router decorators
- [x] Add response_description to endpoints
- [x] Add tags for endpoint organization

#### 8.3 Error Response Models
- [x] Create HTTPErrorResponse schema for consistent error formatting
- [x] Add responses parameter to endpoints for 400, 404, 500 errors
- [x] Document common error scenarios

---

## Testing Checklist

### Router Testing (Individual)

#### Data Ingestion Router
- [x] Test POST /api/data/ingest with valid data
  ```bash
  curl -X POST http://localhost:8000/api/data/ingest \
    -H "Content-Type: application/json" \
    -d @mock_data/test_entry.json
  ```
  - [x] Verify 200 response
  - [x] Verify assessments created
  - [x] Check database for data_entry and assessments

- [x] Test duplicate data_entry_id rejection
- [x] Test malformed JSON handling
- [x] Test missing required fields

#### Assessments Router
- [x] Test GET /api/assessments/student/{student_id}
  ```bash
  curl http://localhost:8000/api/assessments/student/S001
  ```
  - [x] Verify returns list of assessments
  - [x] Verify correct student_id filter

- [x] Test GET /api/assessments/skill-trends/S001
  - [x] Verify grouped by skill
  - [x] Verify chronological order within skill

- [x] Test GET /api/assessments/pending
  - [x] Verify only uncorrected assessments returned
  - [x] Verify sorted by confidence score

#### Corrections Router
- [x] Test POST /api/corrections/submit
  ```bash
  curl -X POST http://localhost:8000/api/corrections/submit \
    -H "Content-Type: application/json" \
    -d '{"assessment_id": 1, "corrected_level": "Proficient", "teacher_notes": "Test", "corrected_by": "T001"}'
  ```
  - [x] Verify correction saved
  - [x] Verify assessment marked as corrected

- [x] Test POST /api/assessments/{id}/approve
  - [x] Verify assessment approved without correction

- [x] Test GET /api/corrections/recent
  - [x] Verify recent corrections returned

#### Students Router
- [x] Test GET /api/students
  - [x] Verify all students returned
  - [x] Test teacher_id filter

- [x] Test GET /api/students/S001/progress
  - [x] Verify progress metrics calculated

- [x] Test POST /api/students/S001/target-skill
  - [x] Verify target assigned
  - [x] Verify duplicate target rejected

- [x] Test GET /api/students/S001/targets
  - [x] Verify targets returned
  - [x] Test completed filter

#### Badges Router
- [x] Test GET /api/badges/students/S001/badges
  - [x] Verify earned and locked badges returned

- [x] Test POST /api/badges/grant
  - [x] Verify badge granted
  - [x] Verify duplicate badge rejected
  - [x] Verify badge_type calculated correctly

### Integration Testing

- [x] Test full ingestion workflow
  1. Ingest data entry
  2. Verify assessments created
  3. Retrieve assessments via API
  4. Submit correction
  5. Verify correction saved
  6. Check few-shot manager retrieves correction

- [x] Test target assignment workflow
  1. Assign target to student
  2. Retrieve targets
  3. Complete target
  4. Verify completion saved

- [x] Test badge workflow
  1. Grant badge
  2. Retrieve badges
  3. Verify badge in collection

### Error Handling Testing

- [x] Test invalid student_id (404)
- [x] Test invalid assessment_id (404)
- [x] Test database connection failure (500)
- [x] Test OpenAI API failure (500)
- [x] Test malformed JSON (422)
- [x] Test missing required fields (422)
- [x] Test duplicate entries (400)

### Performance Testing

- [x] Test ingestion endpoint response time
  - [x] Average < 3 seconds

- [x] Test assessment retrieval response time
  - [x] Average < 500ms

- [x] Test concurrent requests (10 simultaneous)
  - [x] No timeouts
  - [x] No database deadlocks

### API Documentation Testing

- [x] Open http://localhost:8000/docs
- [x] Verify all 15+ endpoints listed
- [x] Test each endpoint via Swagger UI
- [x] Verify request/response examples shown
- [x] Verify error responses documented

---

## Acceptance Criteria

- [x] FastAPI application created and functional
- [x] All 5 routers implemented (data_ingest, assessments, corrections, students, badges)
- [x] All 15+ endpoints functional
- [x] Pydantic schemas defined for all request/response types
- [x] CORS configured for Streamlit frontend
- [x] Database transactions properly managed (commit/rollback)
- [x] Error handling returns appropriate HTTP status codes
- [x] AI inference integrated into ingestion endpoint
- [x] Badge system enforces unique constraint
- [x] Target assignment includes starting_level and target_level fields
- [x] API documentation auto-generated at /docs
- [x] Health check endpoint functional
- [x] Logging implemented for all endpoints
- [x] All tests pass
- [x] No security vulnerabilities (SQL injection prevented)

---

## Notes

- Use parameterized queries everywhere to prevent SQL injection
- All database operations should have proper error handling and rollback
- Response models ensure consistent API contract
- CORS is required for frontend to call backend from different port
- Few-shot learning automatically incorporates corrections into future inferences
- Badge type calculation: D=bronze, P=silver, A=gold, E=no badge

**Next Shards:** [Shard 5: Teacher Dashboard](Shard_5_Tasks.md) and [Shard 6: Student Dashboard](Shard_6_Tasks.md) (can work in parallel)
