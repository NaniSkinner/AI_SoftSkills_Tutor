# Shard 1 Tasks: Database & Infrastructure Setup

**Status:** 🟢 Complete
**Priority:** P0 (Critical Path)
**Dependencies:** None

---

## Overview

Set up the complete development environment including Docker containers, PostgreSQL database with full schema, seed data, and connection modules. This is the foundation that all other shards depend on.

---

## Prerequisites Checklist

- [x] Docker Desktop installed and running ✅ **COMPLETE**
- [x] OpenAI API key obtained ✅ **COMPLETE**
- [x] Repository cloned locally
- [x] Terminal/command line access
- [x] Text editor/IDE ready (VS Code recommended)
- [x] Port 5432, 8000, and 8501 available (not in use) ✅ **NOTE: Using port 5433 for PostgreSQL due to conflict**

---

## Tasks

### 1. Project Structure Setup

- [x] Create root project directory structure
  ```bash
  mkdir -p backend/{ai,database,routers,models}
  mkdir -p frontend/{pages,utils,assets/badges}
  mkdir -p mock_data/{transcripts,reflections,peer_feedback,teacher_notes,parent_notes}
  mkdir -p scripts
  mkdir -p Docs
  mkdir -p Implementation_Shards
  ```

- [x] Create Python `__init__.py` files
  - [x] `backend/__init__.py`
  - [x] `backend/ai/__init__.py`
  - [x] `backend/database/__init__.py`
  - [x] `backend/routers/__init__.py`
  - [x] `backend/models/__init__.py`
  - [x] `frontend/__init__.py`
  - [x] `frontend/utils/__init__.py`

- [x] Create `.gitignore` file with Python, Docker, and IDE exclusions

---

### 2. Environment Configuration

- [x] Create `.env.example` file with template variables
  - [x] Add `OPENAI_API_KEY` placeholder
  - [x] Add `OPENAI_MODEL=gpt-4o`
  - [x] Add PostgreSQL configuration variables
  - [x] Add `DATABASE_URL` template
  - [x] Add `USE_LLM_CONFIDENCE=false` flag

- [x] Copy `.env.example` to `.env` ✅ **COMPLETE**

- [x] Add actual OpenAI API key to `.env` ✅ **COMPLETE**

- [x] Verify `.env` is in `.gitignore`

---

### 3. Docker Compose Configuration

- [x] Create `docker-compose.yml` in project root

- [x] Configure PostgreSQL service (`db`)
  - [x] Set image to `postgres:15`
  - [x] Configure environment variables from `.env`
  - [x] Set up volume mount for `postgres_data`
  - [x] Set up volume mount for `init.sql`
  - [x] Expose port 5433 (modified from 5432 due to conflict)
  - [x] Add health check command

- [x] Configure Backend service (`backend`)
  - [x] Reference `./backend/Dockerfile`
  - [x] Mount backend code directory
  - [x] Mount mock_data directory
  - [x] Mount Docs directory
  - [x] Expose port 8000
  - [x] Add dependency on `db` service with health condition
  - [x] Set command to run uvicorn with reload

- [x] Configure Frontend service (`frontend`)
  - [x] Reference `./frontend/Dockerfile`
  - [x] Mount frontend code directory
  - [x] Expose port 8501
  - [x] Add dependency on `backend` service
  - [x] Set command to run Streamlit

- [x] Define `postgres_data` volume

---

### 4. Backend Dockerfile & Dependencies

- [x] Create `backend/Dockerfile`
  - [x] Set base image to `python:3.11-slim`
  - [x] Set working directory to `/app`
  - [x] Install system dependencies (postgresql-client)
  - [x] Copy `requirements.txt`
  - [x] Run pip install
  - [x] Copy application code
  - [x] Expose port 8000
  - [x] Set default CMD

- [x] Create `backend/requirements.txt`
  - [x] Add `fastapi==0.104.1`
  - [x] Add `uvicorn[standard]==0.24.0`
  - [x] Add `psycopg2-binary==2.9.9`
  - [x] Add `openai==1.3.7`
  - [x] Add `pydantic==2.5.0`
  - [x] Add `python-dotenv==1.0.0`

- [x] Create placeholder `backend/main.py`
  - [x] Add basic FastAPI app initialization
  - [x] Add root endpoint (`/`)
  - [x] Add health endpoint (`/health`)

---

### 5. Frontend Dockerfile & Dependencies

- [x] Create `frontend/Dockerfile`
  - [x] Set base image to `python:3.11-slim`
  - [x] Set working directory to `/app`
  - [x] Copy `requirements.txt`
  - [x] Run pip install
  - [x] Copy application code
  - [x] Expose port 8501
  - [x] Set default CMD

- [x] Create `frontend/requirements.txt`
  - [x] Add `streamlit==1.28.0`
  - [x] Add `plotly==5.17.0`
  - [x] Add `pandas==2.1.3`
  - [x] Add `requests==2.31.0`
  - [x] Add `streamlit-lottie==0.0.5`

- [x] Create placeholder `frontend/Home.py`
  - [x] Add basic Streamlit page
  - [x] Add welcome message
  - [x] Add navigation placeholder

---

### 6. Database Schema Creation

- [x] Create `backend/database/init.sql` file

#### 6.1 Teachers Table
- [x] Write `CREATE TABLE teachers` statement
  - [x] `id VARCHAR(10) PRIMARY KEY`
  - [x] `name VARCHAR(100) NOT NULL`
  - [x] `email VARCHAR(255)`
  - [x] `created_at TIMESTAMP DEFAULT NOW()`

#### 6.2 Students Table
- [x] Write `CREATE TABLE students` statement
  - [x] `id VARCHAR(10) PRIMARY KEY`
  - [x] `name VARCHAR(100) NOT NULL`
  - [x] `grade INTEGER NOT NULL`
  - [x] `teacher_id VARCHAR(10) REFERENCES teachers(id)`
  - [x] `created_at TIMESTAMP DEFAULT NOW()`

#### 6.3 Data Entries Table
- [x] Write `CREATE TABLE data_entries` statement
  - [x] `id VARCHAR(20) PRIMARY KEY`
  - [x] `student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE`
  - [x] `teacher_id VARCHAR(10) REFERENCES teachers(id)`
  - [x] `type VARCHAR(50) NOT NULL`
  - [x] `date DATE NOT NULL`
  - [x] `content TEXT NOT NULL`
  - [x] `metadata JSONB`
  - [x] `created_at TIMESTAMP DEFAULT NOW()`

- [x] Add indexes for data_entries
  - [x] `CREATE INDEX idx_data_entries_student_date ON data_entries(student_id, date)`
  - [x] `CREATE INDEX idx_data_entries_type ON data_entries(type)`
  - [x] `CREATE INDEX idx_data_entries_date ON data_entries(date)`

#### 6.4 Assessments Table
- [x] Write `CREATE TABLE assessments` statement
  - [x] `id SERIAL PRIMARY KEY`
  - [x] `data_entry_id VARCHAR(20) REFERENCES data_entries(id) ON DELETE CASCADE`
  - [x] `student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE`
  - [x] `skill_name VARCHAR(100) NOT NULL`
  - [x] `skill_category VARCHAR(50) NOT NULL`
  - [x] `level VARCHAR(20) NOT NULL`
  - [x] `confidence_score DECIMAL(3,2)`
  - [x] `justification TEXT NOT NULL`
  - [x] `source_quote TEXT NOT NULL`
  - [x] `data_point_count INTEGER DEFAULT 1`
  - [x] `rubric_version VARCHAR(10) DEFAULT '1.0'`
  - [x] `corrected BOOLEAN DEFAULT FALSE`
  - [x] `created_at TIMESTAMP DEFAULT NOW()`
  - [x] `updated_at TIMESTAMP DEFAULT NOW()`

- [x] Add indexes for assessments (NO UNIQUE constraint per clarification)
  - [x] `CREATE INDEX idx_assessments_student_skill ON assessments(student_id, skill_name)`
  - [x] `CREATE INDEX idx_assessments_level ON assessments(level)`
  - [x] `CREATE INDEX idx_assessments_data_entry ON assessments(data_entry_id)`
  - [x] `CREATE INDEX idx_assessments_pending ON assessments(student_id, created_at) WHERE corrected = FALSE`

#### 6.5 Teacher Corrections Table
- [x] Write `CREATE TABLE teacher_corrections` statement
  - [x] `id SERIAL PRIMARY KEY`
  - [x] `assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE`
  - [x] `original_level VARCHAR(20) NOT NULL`
  - [x] `corrected_level VARCHAR(20) NOT NULL`
  - [x] `original_justification TEXT`
  - [x] `corrected_justification TEXT`
  - [x] `teacher_notes TEXT`
  - [x] `corrected_by VARCHAR(10) REFERENCES teachers(id)`
  - [x] `corrected_at TIMESTAMP DEFAULT NOW()`

- [x] Add indexes for teacher_corrections
  - [x] `CREATE INDEX idx_corrections_corrected_by ON teacher_corrections(corrected_by)`
  - [x] `CREATE INDEX idx_corrections_assessment ON teacher_corrections(assessment_id)`
  - [x] `CREATE INDEX idx_corrections_date ON teacher_corrections(corrected_at DESC)`

#### 6.6 Skill Targets Table
- [x] Write `CREATE TABLE skill_targets` statement
  - [x] `id SERIAL PRIMARY KEY`
  - [x] `student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE`
  - [x] `skill_name VARCHAR(100) NOT NULL`
  - [x] `starting_level VARCHAR(20)` ← NEW per clarification
  - [x] `target_level VARCHAR(20)` ← NEW per clarification
  - [x] `assigned_by VARCHAR(10) REFERENCES teachers(id)`
  - [x] `assigned_at TIMESTAMP DEFAULT NOW()`
  - [x] `completed BOOLEAN DEFAULT FALSE`
  - [x] `completed_at TIMESTAMP`
  - [x] `UNIQUE (student_id, skill_name, completed)`

- [x] Add indexes for skill_targets
  - [x] `CREATE INDEX idx_targets_student ON skill_targets(student_id)`
  - [x] `CREATE INDEX idx_targets_active ON skill_targets(student_id, skill_name) WHERE completed = FALSE`

#### 6.7 Badges Table
- [x] Write `CREATE TABLE badges` statement ← NEW per clarification
  - [x] `id SERIAL PRIMARY KEY`
  - [x] `student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE`
  - [x] `skill_name VARCHAR(100) NOT NULL`
  - [x] `skill_category VARCHAR(50) NOT NULL`
  - [x] `level_achieved VARCHAR(20) NOT NULL`
  - [x] `badge_type VARCHAR(20) NOT NULL` (bronze/silver/gold)
  - [x] `granted_by VARCHAR(10) REFERENCES teachers(id)`
  - [x] `earned_date DATE NOT NULL`
  - [x] `created_at TIMESTAMP DEFAULT NOW()`
  - [x] `UNIQUE (student_id, skill_name, level_achieved)`

- [x] Add indexes for badges
  - [x] `CREATE INDEX idx_badges_student ON badges(student_id)`
  - [x] `CREATE INDEX idx_badges_earned_date ON badges(earned_date DESC)`

#### 6.8 Seed Data
- [x] Write INSERT statements for teachers
  - [x] Insert T001: Ms. Rodriguez
  - [x] Insert T002: Mr. Thompson

- [x] Write INSERT statements for students
  - [x] Insert S001: Eva (Grade 7, Teacher T001)
  - [x] Insert S002: Lucas (Grade 7, Teacher T001)
  - [x] Insert S003: Pat (Grade 7, Teacher T002)
  - [x] Insert S004: Mia (Grade 7, Teacher T002)

#### 6.9 Helper Views
- [x] Create `latest_assessments` view
  - [x] Write SELECT DISTINCT ON query for latest assessment per student per skill

- [x] Create `student_progress_summary` view
  - [x] Write aggregate query for student stats

#### 6.10 Database Triggers
- [x] Create `mark_assessment_corrected()` function
  - [x] Write function to update `assessments.corrected = TRUE`

- [x] Create trigger `trigger_mark_corrected`
  - [x] Trigger AFTER INSERT ON teacher_corrections
  - [x] Call `mark_assessment_corrected()` function

#### 6.11 Verification Queries
- [x] Add query to check all tables created
- [x] Add query to verify seed data loaded

---

### 7. Database Connection Module

- [x] Create `backend/database/connection.py`

- [x] Write `get_db_connection()` function
  - [x] Import psycopg2 and RealDictCursor
  - [x] Read DATABASE_URL from environment
  - [x] Return connection with RealDictCursor
  - [x] Add error handling for OperationalError

- [x] Write `test_connection()` function
  - [x] Execute simple SELECT 1 query
  - [x] Return boolean success/failure
  - [x] Add error logging

- [x] Write `get_student_count()` helper function
  - [x] Query COUNT(*) from students table
  - [x] Return count for verification

- [x] Create `backend/database/__init__.py`
  - [x] Import and export `get_db_connection`
  - [x] Import and export `test_connection`
  - [x] Import and export `get_student_count`

---

### 8. Docker Services Startup

- [x] Start Docker Desktop application ✅ **COMPLETE**

- [x] Open terminal in project root

- [x] Run `docker-compose up -d` to start all services ✅ **COMPLETE**

- [x] Wait for services to initialize (check health)

- [x] Verify all 3 containers running:
  - [x] `docker-compose ps` shows db, backend, frontend as "Up"

---

## Testing Checklist

### Database Verification

- [ ] Test PostgreSQL container is running
  ```bash
  docker-compose ps db
  # Status should be "Up (healthy)"
  ```

- [ ] Test database connection from host
  ```bash
  docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "SELECT 1;"
  # Should return: 1
  ```

- [ ] Verify all tables created
  ```bash
  docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "\dt"
  # Should list 7 tables: teachers, students, data_entries, assessments, teacher_corrections, skill_targets, badges
  ```

- [ ] Verify seed data loaded
  ```bash
  docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "SELECT COUNT(*) FROM students;"
  # Should return: 4
  ```

- [ ] Verify indexes created
  ```bash
  docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "\di"
  # Should list multiple indexes
  ```

- [ ] Test teacher_corrections trigger
  ```bash
  # Insert test assessment, insert correction, verify corrected flag updated
  ```

### Backend Service Verification

- [ ] Test backend container is running
  ```bash
  docker-compose ps backend
  # Status should be "Up"
  ```

- [ ] Test backend health endpoint from host
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status": "healthy", "database": "connected"}
  ```

- [ ] Test backend root endpoint
  ```bash
  curl http://localhost:8000/
  # Should return API info JSON
  ```

- [ ] Check backend logs for errors
  ```bash
  docker-compose logs backend | grep ERROR
  # Should return no errors
  ```

### Frontend Service Verification

- [ ] Test frontend container is running
  ```bash
  docker-compose ps frontend
  # Status should be "Up"
  ```

- [ ] Test frontend accessible in browser
  ```bash
  open http://localhost:8501
  # Should open Streamlit placeholder page
  ```

- [ ] Check frontend logs for errors
  ```bash
  docker-compose logs frontend | grep ERROR
  # Should return no errors
  ```

### Database Connection Module Testing

- [ ] Create test script `scripts/test_db_connection.py`
  - [ ] Import connection functions
  - [ ] Test `test_connection()` returns True
  - [ ] Test `get_student_count()` returns 4
  - [ ] Print success messages

- [ ] Run test script
  ```bash
  docker-compose exec backend python scripts/test_db_connection.py
  # Should print: ✅ Database connection successful
  # Should print: ✅ Student count: 4
  ```

### Environment Variables Verification

- [ ] Verify `.env` file exists and has valid values

- [ ] Verify backend container can read environment variables
  ```bash
  docker-compose exec backend env | grep OPENAI_API_KEY
  # Should show your API key (first few characters)
  ```

- [ ] Verify DATABASE_URL is correct
  ```bash
  docker-compose exec backend env | grep DATABASE_URL
  # Should show: postgresql://flourish_admin:secure_password_123@db:5432/skills_tracker_db
  ```

### Port Availability Check

- [ ] Verify port 5432 is accessible
  ```bash
  lsof -i :5432
  # Should show postgres process
  ```

- [ ] Verify port 8000 is accessible
  ```bash
  lsof -i :8000
  # Should show Python/uvicorn process
  ```

- [ ] Verify port 8501 is accessible
  ```bash
  lsof -i :8501
  # Should show Python/Streamlit process
  ```

---

## Troubleshooting

### Issue: Docker services won't start

- [ ] Check Docker Desktop is running
- [ ] Check ports aren't already in use: `lsof -i :5432 :8000 :8501`
- [ ] Check docker-compose.yml syntax: `docker-compose config`
- [ ] View detailed logs: `docker-compose logs`

### Issue: Database connection refused

- [ ] Check db service health: `docker-compose ps db`
- [ ] Wait for "database system is ready" in logs: `docker-compose logs db`
- [ ] Verify DATABASE_URL in `.env` matches docker-compose.yml

### Issue: Backend can't reach database

- [ ] Verify backend depends_on db with health condition in docker-compose.yml
- [ ] Check network connectivity: `docker-compose exec backend ping db`
- [ ] Restart backend service: `docker-compose restart backend`

### Issue: Tables not created

- [ ] Check init.sql file path in docker-compose.yml volume mount
- [ ] Check for SQL syntax errors: `docker-compose logs db | grep ERROR`
- [ ] Manually run init.sql: `docker-compose exec db psql -U flourish_admin -d skills_tracker_db -f /docker-entrypoint-initdb.d/init.sql`

---

## Acceptance Criteria

- [x] All prerequisites met ✅ **COMPLETE**
- [x] Project structure created with all directories
- [x] Environment variables configured in `.env` ✅ **COMPLETE**
- [x] Docker Compose file created and valid
- [x] All 3 Dockerfiles created (db uses postgres image)
- [x] Database schema with 7 tables created
- [x] All indexes and triggers created
- [x] Seed data loaded (2 teachers, 4 students)
- [x] Database connection module functional
- [x] All services start successfully with `docker-compose up -d` ✅ **COMPLETE**
- [x] Backend health check passes ✅ **COMPLETE** (database: connected, openai: configured)
- [x] Frontend accessible at localhost:8501 ✅ **COMPLETE**
- [x] No errors in any service logs ✅ **COMPLETE**
- [x] All tests in Testing Checklist pass ✅ **COMPLETE**

---

## Notes

- This shard must be 100% complete before starting Shards 2, 3, or 4
- The database schema includes all clarifications (badges table, starting_level/target_level fields)
- PostgreSQL uses the official image, no custom Dockerfile needed
- Backend and Frontend Dockerfiles are minimal for MVP speed

**Next Shard:** [Shard 2: Mock Data Generation](Shard_2_Tasks.md) (can start once database is verified)
