# Shard 4 Tasks: Backend API Layer

**Status:** 🔴 Not Started
**Priority:** P0 (Critical Path)
**Dependencies:** Shards 1, 3 (Database + AI Pipeline)

---

## Overview

Build FastAPI REST API with 15+ endpoints for data ingestion, assessment retrieval, teacher corrections, student progress tracking, and badge management. Implement request validation, error handling, and database transaction management.

---

## Prerequisites Checklist

- [ ] Shard 1 completed (Database running)
- [ ] Shard 3 completed (AI inference engine functional)
- [ ] FastAPI and Pydantic packages installed
- [ ] Understanding of REST API design principles
- [ ] PostgreSQL connection working
- [ ] OpenAI API integration tested

---

## Tasks

### 1. Pydantic Models (Schemas)

- [ ] Create `backend/models/schemas.py` file

#### 1.1 Data Ingestion Schemas
- [ ] Import `pydantic.BaseModel`, `pydantic.Field`
- [ ] Import `datetime.date`
- [ ] Import `typing.Optional`, `typing.Dict`, `typing.Any`

- [ ] Create `DataEntryRequest` schema
  - [ ] `data_entry_id: str`
  - [ ] `student_id: str`
  - [ ] `teacher_id: str`
  - [ ] `type: str` (field with choices validation)
  - [ ] `date: str` (YYYY-MM-DD format)
  - [ ] `content: str`
  - [ ] `metadata: Dict[str, Any]`
  - [ ] Add field validators for date format
  - [ ] Add field validators for type enum

- [ ] Create `DataEntryResponse` schema
  - [ ] `success: bool`
  - [ ] `data_entry_id: str`
  - [ ] `assessments_created: int`
  - [ ] `assessment_ids: list[int]`

#### 1.2 Assessment Schemas
- [ ] Create `AssessmentResponse` schema
  - [ ] `id: int`
  - [ ] `data_entry_id: str`
  - [ ] `student_id: str`
  - [ ] `skill_name: str`
  - [ ] `skill_category: str`
  - [ ] `level: str`
  - [ ] `confidence_score: float`
  - [ ] `justification: str`
  - [ ] `source_quote: str`
  - [ ] `data_point_count: int`
  - [ ] `rubric_version: str`
  - [ ] `corrected: bool`
  - [ ] `created_at: str`

- [ ] Create `SkillTrendResponse` schema
  - [ ] `skill_name: str`
  - [ ] `skill_category: str`
  - [ ] `assessments: list[dict]` (date, level, confidence)

#### 1.3 Correction Schemas
- [ ] Create `CorrectionRequest` schema
  - [ ] `assessment_id: int`
  - [ ] `corrected_level: str`
  - [ ] `corrected_justification: Optional[str]`
  - [ ] `teacher_notes: Optional[str]`
  - [ ] `corrected_by: str` (teacher_id)

- [ ] Create `CorrectionResponse` schema
  - [ ] `success: bool`
  - [ ] `correction_id: int`
  - [ ] `message: str`

- [ ] Create `ApprovalRequest` schema
  - [ ] `assessment_id: int`
  - [ ] `approved_by: str` (teacher_id)

#### 1.4 Student & Target Schemas
- [ ] Create `StudentResponse` schema
  - [ ] `id: str`
  - [ ] `name: str`
  - [ ] `grade: int`
  - [ ] `teacher_id: str`
  - [ ] `created_at: str`

- [ ] Create `StudentProgressResponse` schema
  - [ ] `student_id: str`
  - [ ] `student_name: str`
  - [ ] `total_assessments: int`
  - [ ] `total_badges: int`
  - [ ] `active_targets: int`
  - [ ] `recent_growth: list[dict]`

- [ ] Create `TargetAssignmentRequest` schema
  - [ ] `student_id: str`
  - [ ] `skill_name: str`
  - [ ] `starting_level: str`
  - [ ] `target_level: str`
  - [ ] `assigned_by: str` (teacher_id)

- [ ] Create `TargetResponse` schema
  - [ ] `id: int`
  - [ ] `student_id: str`
  - [ ] `skill_name: str`
  - [ ] `starting_level: str`
  - [ ] `target_level: str`
  - [ ] `assigned_by: str`
  - [ ] `assigned_at: str`
  - [ ] `completed: bool`
  - [ ] `completed_at: Optional[str]`

#### 1.5 Badge Schemas
- [ ] Create `BadgeResponse` schema
  - [ ] `id: int`
  - [ ] `student_id: str`
  - [ ] `skill_name: str`
  - [ ] `skill_category: str`
  - [ ] `level_achieved: str`
  - [ ] `badge_type: str` (bronze/silver/gold)
  - [ ] `granted_by: str`
  - [ ] `earned_date: str`
  - [ ] `created_at: str`

- [ ] Create `BadgeGrantRequest` schema
  - [ ] `student_id: str`
  - [ ] `skill_name: str`
  - [ ] `skill_category: str`
  - [ ] `level_achieved: str`
  - [ ] `granted_by: str` (teacher_id)
  - [ ] `earned_date: str`

- [ ] Create `BadgeCollectionResponse` schema
  - [ ] `student_id: str`
  - [ ] `earned_badges: list[BadgeResponse]`
  - [ ] `locked_badges: list[dict]` (skill_name, level, badge_type)
  - [ ] `total_earned: int`
  - [ ] `total_possible: int`

---

### 2. Data Ingestion Router

- [ ] Create `backend/routers/data_ingest.py` file

#### 2.1 Router Setup
- [ ] Import `fastapi.APIRouter`, `fastapi.HTTPException`
- [ ] Import schemas from `backend.models.schemas`
- [ ] Import `get_db_connection` from `backend.database.connection`
- [ ] Import `SkillInferenceEngine`, `load_rubric` from `backend.ai`
- [ ] Import `os`, `logging`
- [ ] Create router instance with prefix="/api/data" and tag="Data Ingestion"
- [ ] Create logger

#### 2.2 POST /ingest Endpoint - Setup
- [ ] Create `@router.post("/ingest", response_model=DataEntryResponse)` decorator
- [ ] Write `ingest_data_entry(entry: DataEntryRequest)` async function
- [ ] Add docstring explaining endpoint purpose

#### 2.3 POST /ingest Endpoint - Database Insertion
- [ ] Get database connection
- [ ] Create cursor
- [ ] Begin transaction (set autocommit=False)
- [ ] Write INSERT INTO data_entries SQL
  - [ ] Insert id, student_id, teacher_id, type, date, content, metadata
  - [ ] Use parameterized query to prevent SQL injection
- [ ] Execute INSERT with try-except block
- [ ] Catch IntegrityError for duplicate entry_id
  - [ ] Return HTTPException 400 if duplicate
- [ ] Commit transaction

#### 2.4 POST /ingest Endpoint - AI Inference
- [ ] Load rubric using `load_rubric()`
- [ ] Get OpenAI API key from environment
- [ ] Create SkillInferenceEngine instance
- [ ] Prepare student_data dictionary with content and metadata
- [ ] Call `engine.assess_skills(student_data)`
- [ ] Store assessments result

#### 2.5 POST /ingest Endpoint - Assessment Storage
- [ ] Loop through assessments
  - [ ] Write INSERT INTO assessments SQL
  - [ ] Insert data_entry_id, student_id, skill_name, skill_category, level, confidence_score, justification, source_quote, data_point_count
  - [ ] Execute INSERT RETURNING id
  - [ ] Collect assessment_ids
- [ ] Commit transaction
- [ ] Close cursor and connection

#### 2.6 POST /ingest Endpoint - Response
- [ ] Return DataEntryResponse with:
  - [ ] success=True
  - [ ] data_entry_id
  - [ ] assessments_created count
  - [ ] assessment_ids list

#### 2.7 POST /ingest Endpoint - Error Handling
- [ ] Add global exception handler
- [ ] Rollback transaction on error
- [ ] Log error details
- [ ] Return HTTPException 500 with error message

---

### 3. Assessments Router

- [ ] Create `backend/routers/assessments.py` file

#### 3.1 Router Setup
- [ ] Import required modules (APIRouter, HTTPException, schemas, database)
- [ ] Create router with prefix="/api/assessments" and tag="Assessments"

#### 3.2 GET /student/{student_id} Endpoint
- [ ] Create `@router.get("/student/{student_id}")` decorator
- [ ] Write `get_student_assessments(student_id: str)` function
- [ ] Get database connection
- [ ] Query assessments table WHERE student_id = ?
- [ ] Order by created_at DESC
- [ ] Fetch all results
- [ ] Convert to AssessmentResponse list
- [ ] Return results
- [ ] Add error handling for database errors

#### 3.3 GET /skill-trends/{student_id} Endpoint
- [ ] Create `@router.get("/skill-trends/{student_id}")` decorator
- [ ] Write `get_skill_trends(student_id: str)` function
- [ ] Get database connection
- [ ] Query assessments grouped by skill_name
- [ ] Order by date ASC within each skill
- [ ] Fetch all results
- [ ] Group results by skill_name into dictionary
- [ ] For each skill, create list of {date, level, confidence}
- [ ] Convert levels to numeric for charting (E=1, D=2, P=3, A=4)
- [ ] Return SkillTrendResponse list
- [ ] Add error handling

#### 3.4 GET /pending Endpoint
- [ ] Create `@router.get("/pending")` decorator
- [ ] Write `get_pending_assessments(limit: int = 50)` function
- [ ] Get database connection
- [ ] Query assessments WHERE corrected = FALSE
- [ ] Order by confidence_score ASC, created_at DESC
- [ ] LIMIT to specified limit (default 50)
- [ ] Optional query parameter: min_confidence (filter < threshold)
- [ ] Fetch results
- [ ] Return AssessmentResponse list
- [ ] Add error handling

#### 3.5 GET /{assessment_id} Endpoint
- [ ] Create `@router.get("/{assessment_id}")` decorator
- [ ] Write `get_assessment_by_id(assessment_id: int)` function
- [ ] Get database connection
- [ ] Query assessments WHERE id = ?
- [ ] Fetch one result
- [ ] If not found, raise HTTPException 404
- [ ] Return AssessmentResponse
- [ ] Add error handling

---

### 4. Corrections Router

- [ ] Create `backend/routers/corrections.py` file

#### 4.1 Router Setup
- [ ] Import required modules
- [ ] Create router with prefix="/api/corrections" and tag="Teacher Corrections"

#### 4.2 POST /submit Endpoint - Setup
- [ ] Create `@router.post("/submit", response_model=CorrectionResponse)` decorator
- [ ] Write `submit_correction(correction: CorrectionRequest)` function
- [ ] Add docstring

#### 4.3 POST /submit Endpoint - Validation
- [ ] Get database connection
- [ ] Query assessments to verify assessment_id exists
- [ ] If not found, raise HTTPException 404
- [ ] Store original_level from assessment

#### 4.4 POST /submit Endpoint - Insert Correction
- [ ] Write INSERT INTO teacher_corrections SQL
  - [ ] assessment_id
  - [ ] original_level
  - [ ] corrected_level
  - [ ] original_justification (from assessment)
  - [ ] corrected_justification (from request, or use original if None)
  - [ ] teacher_notes
  - [ ] corrected_by
- [ ] Execute INSERT RETURNING id
- [ ] Store correction_id

#### 4.5 POST /submit Endpoint - Update Assessment
- [ ] Write UPDATE assessments SET corrected = TRUE WHERE id = ?
- [ ] Execute UPDATE
- [ ] Commit transaction
- [ ] Close cursor and connection

#### 4.6 POST /submit Endpoint - Response
- [ ] Return CorrectionResponse with:
  - [ ] success=True
  - [ ] correction_id
  - [ ] message="Correction submitted successfully"

#### 4.7 POST /submit Endpoint - Error Handling
- [ ] Add exception handlers for database errors
- [ ] Rollback on error
- [ ] Return HTTPException 500

#### 4.8 POST /assessments/{id}/approve Endpoint
- [ ] Create endpoint for approving assessment as-is
- [ ] Require ApprovalRequest body
- [ ] UPDATE assessments SET corrected = TRUE WHERE id = ?
- [ ] Return success response
- [ ] Add error handling

#### 4.9 GET /recent Endpoint
- [ ] Create `@router.get("/recent")` decorator
- [ ] Write `get_recent_corrections(limit: int = 10)` function
- [ ] Query teacher_corrections with JOIN to assessments
- [ ] Order by corrected_at DESC
- [ ] LIMIT to specified limit
- [ ] Return list of correction objects
- [ ] Add error handling

---

### 5. Students Router

- [ ] Create `backend/routers/students.py` file

#### 5.1 Router Setup
- [ ] Import required modules
- [ ] Create router with prefix="/api/students" and tag="Students"

#### 5.2 GET / Endpoint
- [ ] Create `@router.get("/")` decorator
- [ ] Write `get_students(teacher_id: Optional[str] = None)` function
- [ ] Get database connection
- [ ] Query students table
- [ ] If teacher_id provided, add WHERE teacher_id = ?
- [ ] Order by name ASC
- [ ] Fetch all results
- [ ] Return StudentResponse list
- [ ] Add error handling

#### 5.3 GET /{student_id}/progress Endpoint
- [ ] Create `@router.get("/{student_id}/progress")` decorator
- [ ] Write `get_student_progress(student_id: str)` function
- [ ] Get database connection
- [ ] Query student info from students table
- [ ] Query total assessments COUNT
- [ ] Query total badges COUNT
- [ ] Query active targets COUNT WHERE completed = FALSE
- [ ] Query recent growth (last 5 assessments with level changes)
- [ ] Combine results into StudentProgressResponse
- [ ] Return response
- [ ] Add error handling for student not found

#### 5.4 POST /{student_id}/target-skill Endpoint
- [ ] Create `@router.post("/{student_id}/target-skill")` decorator
- [ ] Write `assign_target_skill(student_id: str, target: TargetAssignmentRequest)` function
- [ ] Validate student_id matches request body
- [ ] Get database connection
- [ ] Check if active target already exists for this skill
- [ ] If exists and not completed, raise HTTPException 400
- [ ] Write INSERT INTO skill_targets SQL
  - [ ] student_id
  - [ ] skill_name
  - [ ] starting_level
  - [ ] target_level
  - [ ] assigned_by
  - [ ] assigned_at (NOW())
- [ ] Execute INSERT RETURNING id
- [ ] Return TargetResponse
- [ ] Add error handling

#### 5.5 GET /{student_id}/targets Endpoint
- [ ] Create `@router.get("/{student_id}/targets")` decorator
- [ ] Write `get_student_targets(student_id: str, completed: Optional[bool] = None)` function
- [ ] Get database connection
- [ ] Query skill_targets WHERE student_id = ?
- [ ] If completed parameter provided, add WHERE completed = ?
- [ ] Order by assigned_at DESC
- [ ] Fetch all results
- [ ] Return TargetResponse list
- [ ] Add error handling

#### 5.6 PUT /targets/{target_id}/complete Endpoint
- [ ] Create `@router.put("/targets/{target_id}/complete")` decorator
- [ ] Write `complete_target(target_id: int)` function
- [ ] Get database connection
- [ ] UPDATE skill_targets SET completed = TRUE, completed_at = NOW()
- [ ] WHERE id = ?
- [ ] Execute UPDATE
- [ ] Return success response
- [ ] Add error handling

---

### 6. Badges Router

- [ ] Create `backend/routers/badges.py` file

#### 6.1 Router Setup
- [ ] Import required modules
- [ ] Create router with prefix="/api/badges" and tag="Badges"

#### 6.2 GET /students/{student_id}/badges Endpoint
- [ ] Create `@router.get("/students/{student_id}/badges")` decorator
- [ ] Write `get_student_badges(student_id: str)` function
- [ ] Get database connection
- [ ] Query badges table WHERE student_id = ?
- [ ] Order by earned_date DESC
- [ ] Fetch earned badges
- [ ] Generate locked badges list (all 17 skills at 3 levels = 51 possible)
- [ ] Filter out earned badges from locked list
- [ ] Calculate total_earned and total_possible
- [ ] Return BadgeCollectionResponse
- [ ] Add error handling

#### 6.3 POST /grant Endpoint - Setup
- [ ] Create `@router.post("/grant")` decorator
- [ ] Write `grant_badge(badge: BadgeGrantRequest)` function
- [ ] Add docstring explaining teacher-only action

#### 6.4 POST /grant Endpoint - Validation
- [ ] Validate level_achieved is one of: Developing, Proficient, Advanced
- [ ] Determine badge_type based on level:
  - [ ] Developing → bronze
  - [ ] Proficient → silver
  - [ ] Advanced → gold
- [ ] Get database connection

#### 6.5 POST /grant Endpoint - Check Existing Badge
- [ ] Query badges WHERE student_id = ? AND skill_name = ? AND level_achieved = ?
- [ ] If badge already exists, raise HTTPException 400 "Badge already granted"

#### 6.6 POST /grant Endpoint - Insert Badge
- [ ] Write INSERT INTO badges SQL
  - [ ] student_id
  - [ ] skill_name
  - [ ] skill_category
  - [ ] level_achieved
  - [ ] badge_type
  - [ ] granted_by
  - [ ] earned_date
- [ ] Execute INSERT RETURNING id
- [ ] Commit transaction
- [ ] Return BadgeResponse
- [ ] Add error handling

#### 6.7 GET /students/{student_id}/badge-progress Endpoint
- [ ] Create endpoint to calculate badge progress
- [ ] Count earned badges by category (SEL, EF, 21st Century)
- [ ] Count by badge type (bronze, silver, gold)
- [ ] Return progress metrics
- [ ] Add error handling

---

### 7. Main FastAPI Application

- [ ] Open/create `backend/main.py` file

#### 7.1 Imports
- [ ] Import `fastapi.FastAPI`
- [ ] Import `fastapi.middleware.cors.CORSMiddleware`
- [ ] Import all routers (data_ingest, assessments, corrections, students, badges)
- [ ] Import `logging`
- [ ] Import `os` for environment variables

#### 7.2 Logger Setup
- [ ] Configure logging with INFO level
- [ ] Create logger instance

#### 7.3 FastAPI App Initialization
- [ ] Create FastAPI instance with:
  - [ ] title="Flourish Skills Tracker API"
  - [ ] version="1.0.0"
  - [ ] description="AI-powered soft skills assessment API"
- [ ] Add docstring to app

#### 7.4 CORS Middleware
- [ ] Add CORSMiddleware to app
  - [ ] allow_origins=["http://localhost:8501", "http://frontend:8501"]
  - [ ] allow_credentials=True
  - [ ] allow_methods=["*"]
  - [ ] allow_headers=["*"]
- [ ] Add comment explaining CORS for Streamlit

#### 7.5 Router Inclusion
- [ ] Include data_ingest router
- [ ] Include assessments router
- [ ] Include corrections router
- [ ] Include students router
- [ ] Include badges router

#### 7.6 Root Endpoint
- [ ] Create `@app.get("/")` endpoint
- [ ] Return JSON with:
  - [ ] message="Flourish Skills Tracker API"
  - [ ] version="1.0.0"
  - [ ] docs_url="/docs"

#### 7.7 Health Check Endpoint
- [ ] Create `@app.get("/health")` endpoint
- [ ] Test database connection using `test_connection()`
- [ ] Return JSON with:
  - [ ] status="healthy"
  - [ ] database="connected" or "disconnected"
  - [ ] version="1.0.0"
- [ ] Add error handling

#### 7.8 Startup Event
- [ ] Create `@app.on_event("startup")` handler
- [ ] Log "FastAPI server starting..."
- [ ] Test database connection
- [ ] Log database connection status
- [ ] Test OpenAI API key exists
- [ ] Log OpenAI integration status

#### 7.9 Shutdown Event
- [ ] Create `@app.on_event("shutdown")` handler
- [ ] Log "FastAPI server shutting down..."
- [ ] Close any open connections

---

### 8. API Documentation Enhancement

#### 8.1 Schema Examples
- [ ] Add example values to Pydantic schemas using `Field(..., example=...)`
- [ ] Add examples for DataEntryRequest
- [ ] Add examples for CorrectionRequest
- [ ] Add examples for TargetAssignmentRequest
- [ ] Add examples for BadgeGrantRequest

#### 8.2 Endpoint Descriptions
- [ ] Add detailed descriptions to each endpoint using docstrings
- [ ] Add summary and description to router decorators
- [ ] Add response_description to endpoints
- [ ] Add tags for endpoint organization

#### 8.3 Error Response Models
- [ ] Create HTTPErrorResponse schema for consistent error formatting
- [ ] Add responses parameter to endpoints for 400, 404, 500 errors
- [ ] Document common error scenarios

---

## Testing Checklist

### Router Testing (Individual)

#### Data Ingestion Router
- [ ] Test POST /api/data/ingest with valid data
  ```bash
  curl -X POST http://localhost:8000/api/data/ingest \
    -H "Content-Type: application/json" \
    -d @mock_data/test_entry.json
  ```
  - [ ] Verify 200 response
  - [ ] Verify assessments created
  - [ ] Check database for data_entry and assessments

- [ ] Test duplicate data_entry_id rejection
- [ ] Test malformed JSON handling
- [ ] Test missing required fields

#### Assessments Router
- [ ] Test GET /api/assessments/student/{student_id}
  ```bash
  curl http://localhost:8000/api/assessments/student/S001
  ```
  - [ ] Verify returns list of assessments
  - [ ] Verify correct student_id filter

- [ ] Test GET /api/assessments/skill-trends/S001
  - [ ] Verify grouped by skill
  - [ ] Verify chronological order within skill

- [ ] Test GET /api/assessments/pending
  - [ ] Verify only uncorrected assessments returned
  - [ ] Verify sorted by confidence score

#### Corrections Router
- [ ] Test POST /api/corrections/submit
  ```bash
  curl -X POST http://localhost:8000/api/corrections/submit \
    -H "Content-Type: application/json" \
    -d '{"assessment_id": 1, "corrected_level": "Proficient", "teacher_notes": "Test", "corrected_by": "T001"}'
  ```
  - [ ] Verify correction saved
  - [ ] Verify assessment marked as corrected

- [ ] Test POST /api/assessments/{id}/approve
  - [ ] Verify assessment approved without correction

- [ ] Test GET /api/corrections/recent
  - [ ] Verify recent corrections returned

#### Students Router
- [ ] Test GET /api/students
  - [ ] Verify all students returned
  - [ ] Test teacher_id filter

- [ ] Test GET /api/students/S001/progress
  - [ ] Verify progress metrics calculated

- [ ] Test POST /api/students/S001/target-skill
  - [ ] Verify target assigned
  - [ ] Verify duplicate target rejected

- [ ] Test GET /api/students/S001/targets
  - [ ] Verify targets returned
  - [ ] Test completed filter

#### Badges Router
- [ ] Test GET /api/badges/students/S001/badges
  - [ ] Verify earned and locked badges returned

- [ ] Test POST /api/badges/grant
  - [ ] Verify badge granted
  - [ ] Verify duplicate badge rejected
  - [ ] Verify badge_type calculated correctly

### Integration Testing

- [ ] Test full ingestion workflow
  1. Ingest data entry
  2. Verify assessments created
  3. Retrieve assessments via API
  4. Submit correction
  5. Verify correction saved
  6. Check few-shot manager retrieves correction

- [ ] Test target assignment workflow
  1. Assign target to student
  2. Retrieve targets
  3. Complete target
  4. Verify completion saved

- [ ] Test badge workflow
  1. Grant badge
  2. Retrieve badges
  3. Verify badge in collection

### Error Handling Testing

- [ ] Test invalid student_id (404)
- [ ] Test invalid assessment_id (404)
- [ ] Test database connection failure (500)
- [ ] Test OpenAI API failure (500)
- [ ] Test malformed JSON (422)
- [ ] Test missing required fields (422)
- [ ] Test duplicate entries (400)

### Performance Testing

- [ ] Test ingestion endpoint response time
  - [ ] Average < 3 seconds

- [ ] Test assessment retrieval response time
  - [ ] Average < 500ms

- [ ] Test concurrent requests (10 simultaneous)
  - [ ] No timeouts
  - [ ] No database deadlocks

### API Documentation Testing

- [ ] Open http://localhost:8000/docs
- [ ] Verify all 15+ endpoints listed
- [ ] Test each endpoint via Swagger UI
- [ ] Verify request/response examples shown
- [ ] Verify error responses documented

---

## Acceptance Criteria

- [ ] FastAPI application created and functional
- [ ] All 5 routers implemented (data_ingest, assessments, corrections, students, badges)
- [ ] All 15+ endpoints functional
- [ ] Pydantic schemas defined for all request/response types
- [ ] CORS configured for Streamlit frontend
- [ ] Database transactions properly managed (commit/rollback)
- [ ] Error handling returns appropriate HTTP status codes
- [ ] AI inference integrated into ingestion endpoint
- [ ] Badge system enforces unique constraint
- [ ] Target assignment includes starting_level and target_level fields
- [ ] API documentation auto-generated at /docs
- [ ] Health check endpoint functional
- [ ] Logging implemented for all endpoints
- [ ] All tests pass
- [ ] No security vulnerabilities (SQL injection prevented)

---

## Notes

- Use parameterized queries everywhere to prevent SQL injection
- All database operations should have proper error handling and rollback
- Response models ensure consistent API contract
- CORS is required for frontend to call backend from different port
- Few-shot learning automatically incorporates corrections into future inferences
- Badge type calculation: D=bronze, P=silver, A=gold, E=no badge

**Next Shards:** [Shard 5: Teacher Dashboard](Shard_5_Tasks.md) and [Shard 6: Student Dashboard](Shard_6_Tasks.md) (can work in parallel)
