# Shard 1: Database & Infrastructure Setup

**Owner:** Backend Engineer
**Estimated Time:** 1 day
**Dependencies:** None
**Priority:** P0 (Critical Path)

---

## Objective

Set up the foundational infrastructure: PostgreSQL database, Docker environment, and database schema with all tables, indexes, and relationships.

---

## Inputs

1. [Docs/PRD.md](../Docs/PRD.md) - Section 2: Database Schema
2. [Docs/Curriculum.md](../Docs/Curriculum.md) - 17 skills reference
3. [Docs/Rubric.md](../Docs/Rubric.md) - Proficiency levels

---

## Deliverables

### 1. Docker Environment

**File:** `docker-compose.yml`

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      OPENAI_MODEL: gpt-4o
      USE_LLM_CONFIDENCE: "false"
    volumes:
      - ./backend:/app
      - ./mock_data:/app/mock_data
      - ./Docs:/app/Docs
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    environment:
      BACKEND_URL: http://backend:8000
    volumes:
      - ./frontend:/app
    ports:
      - "8501:8501"
    depends_on:
      - backend
    command: streamlit run Home.py --server.port 8501 --server.address 0.0.0.0

volumes:
  postgres_data:
```

### 2. Environment Configuration

**File:** `.env`

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Database Configuration
POSTGRES_USER=flourish_admin
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=skills_tracker_db
DATABASE_URL=postgresql://flourish_admin:secure_password_123@db:5432/skills_tracker_db

# Feature Flags
USE_LLM_CONFIDENCE=false
```

**File:** `.env.example` (for version control)

```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
POSTGRES_USER=flourish_admin
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=skills_tracker_db
DATABASE_URL=postgresql://flourish_admin:secure_password_123@db:5432/skills_tracker_db
USE_LLM_CONFIDENCE=false
```

### 3. Database Schema

**File:** `backend/database/init.sql`

```sql
-- Flourish Skills Tracker Database Schema
-- Version: 1.0
-- Date: November 10, 2025

-- Enable UUID extension (if needed in future)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- TEACHERS TABLE
-- ============================================================================
CREATE TABLE teachers (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- STUDENTS TABLE
-- ============================================================================
CREATE TABLE students (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    grade INTEGER NOT NULL,
    teacher_id VARCHAR(10) REFERENCES teachers(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- DATA ENTRIES TABLE
-- ============================================================================
CREATE TABLE data_entries (
    id VARCHAR(20) PRIMARY KEY,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    teacher_id VARCHAR(10) REFERENCES teachers(id),
    type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for data_entries
CREATE INDEX idx_data_entries_student_date ON data_entries(student_id, date);
CREATE INDEX idx_data_entries_type ON data_entries(type);
CREATE INDEX idx_data_entries_date ON data_entries(date);

-- ============================================================================
-- ASSESSMENTS TABLE
-- ============================================================================
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    data_entry_id VARCHAR(20) REFERENCES data_entries(id) ON DELETE CASCADE,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL,
    confidence_score DECIMAL(3,2),
    justification TEXT NOT NULL,
    source_quote TEXT NOT NULL,
    data_point_count INTEGER DEFAULT 1,
    rubric_version VARCHAR(10) DEFAULT '1.0',
    corrected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for assessments (REMOVED UNIQUE constraint per clarification 3.1)
CREATE INDEX idx_assessments_student_skill ON assessments(student_id, skill_name);
CREATE INDEX idx_assessments_level ON assessments(level);
CREATE INDEX idx_assessments_data_entry ON assessments(data_entry_id);
CREATE INDEX idx_assessments_pending ON assessments(student_id, created_at) WHERE corrected = FALSE;

-- ============================================================================
-- TEACHER CORRECTIONS TABLE
-- ============================================================================
CREATE TABLE teacher_corrections (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    original_level VARCHAR(20) NOT NULL,
    corrected_level VARCHAR(20) NOT NULL,
    original_justification TEXT,
    corrected_justification TEXT,
    teacher_notes TEXT,
    corrected_by VARCHAR(10) REFERENCES teachers(id),
    corrected_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for teacher_corrections
CREATE INDEX idx_corrections_corrected_by ON teacher_corrections(corrected_by);
CREATE INDEX idx_corrections_assessment ON teacher_corrections(assessment_id);
CREATE INDEX idx_corrections_date ON teacher_corrections(corrected_at DESC);

-- ============================================================================
-- SKILL TARGETS TABLE (Updated per clarification 3.2)
-- ============================================================================
CREATE TABLE skill_targets (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    starting_level VARCHAR(20),
    target_level VARCHAR(20),
    assigned_by VARCHAR(10) REFERENCES teachers(id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    UNIQUE (student_id, skill_name, completed)
);

-- Indexes for skill_targets
CREATE INDEX idx_targets_student ON skill_targets(student_id);
CREATE INDEX idx_targets_active ON skill_targets(student_id, skill_name) WHERE completed = FALSE;

-- ============================================================================
-- BADGES TABLE (NEW - per clarification 4.1)
-- ============================================================================
CREATE TABLE badges (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(50) NOT NULL,
    level_achieved VARCHAR(20) NOT NULL,
    badge_type VARCHAR(20) NOT NULL, -- 'bronze', 'silver', 'gold'
    granted_by VARCHAR(10) REFERENCES teachers(id),
    earned_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (student_id, skill_name, level_achieved)
);

-- Indexes for badges
CREATE INDEX idx_badges_student ON badges(student_id);
CREATE INDEX idx_badges_earned_date ON badges(earned_date DESC);

-- ============================================================================
-- SEED DATA
-- ============================================================================

-- Insert Teachers
INSERT INTO teachers (id, name, email) VALUES
('T001', 'Ms. Rodriguez', 'rodriguez@flourishschools.edu'),
('T002', 'Mr. Thompson', 'thompson@flourishschools.edu');

-- Insert Students
INSERT INTO students (id, name, grade, teacher_id) VALUES
('S001', 'Eva', 7, 'T001'),
('S002', 'Lucas', 7, 'T001'),
('S003', 'Pat', 7, 'T002'),
('S004', 'Mia', 7, 'T002');

-- ============================================================================
-- HELPER VIEWS
-- ============================================================================

-- View: Latest assessment per student per skill
CREATE VIEW latest_assessments AS
SELECT DISTINCT ON (student_id, skill_name)
    id,
    student_id,
    skill_name,
    skill_category,
    level,
    confidence_score,
    created_at
FROM assessments
ORDER BY student_id, skill_name, created_at DESC;

-- View: Student progress summary
CREATE VIEW student_progress_summary AS
SELECT
    s.id AS student_id,
    s.name AS student_name,
    COUNT(DISTINCT a.skill_name) AS skills_assessed,
    COUNT(a.id) AS total_assessments,
    COUNT(CASE WHEN a.level = 'Advanced' THEN 1 END) AS advanced_count,
    COUNT(CASE WHEN a.level = 'Proficient' THEN 1 END) AS proficient_count,
    COUNT(CASE WHEN a.level = 'Developing' THEN 1 END) AS developing_count,
    COUNT(CASE WHEN a.level = 'Emerging' THEN 1 END) AS emerging_count
FROM students s
LEFT JOIN assessments a ON s.id = a.student_id
GROUP BY s.id, s.name;

-- ============================================================================
-- TRIGGER: Update assessments.corrected on correction
-- ============================================================================
CREATE OR REPLACE FUNCTION mark_assessment_corrected()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE assessments
    SET corrected = TRUE, updated_at = NOW()
    WHERE id = NEW.assessment_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_mark_corrected
AFTER INSERT ON teacher_corrections
FOR EACH ROW
EXECUTE FUNCTION mark_assessment_corrected();

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check table creation
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Check seed data
SELECT 'Teachers' AS table_name, COUNT(*) AS row_count FROM teachers
UNION ALL
SELECT 'Students', COUNT(*) FROM students;
```

### 4. Database Connection Module

**File:** `backend/database/connection.py`

```python
"""
Database connection utility for Flourish Skills Tracker.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Create and return a database connection.

    Returns:
        psycopg2 connection object with RealDictCursor

    Raises:
        psycopg2.OperationalError: If connection fails
    """
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise


def test_connection() -> bool:
    """
    Test database connectivity.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] == 1
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False


def get_student_count() -> int:
    """Helper to verify seed data loaded."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM students")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['count']
```

**File:** `backend/database/__init__.py`

```python
from .connection import get_db_connection, test_connection, get_student_count

__all__ = ['get_db_connection', 'test_connection', 'get_student_count']
```

### 5. Backend Dockerfile

**File:** `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File:** `backend/requirements.txt`

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
openai==1.3.7
pydantic==2.5.0
python-dotenv==1.0.0
```

### 6. Frontend Dockerfile

**File:** `frontend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command (overridden by docker-compose)
CMD ["streamlit", "run", "Home.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

**File:** `frontend/requirements.txt`

```
streamlit==1.28.0
plotly==5.17.0
pandas==2.1.3
requests==2.31.0
streamlit-lottie==0.0.5
```

### 7. Project Structure Setup Script

**File:** `scripts/setup_project_structure.sh`

```bash
#!/bin/bash

echo "Creating Flourish Skills Tracker project structure..."

# Create main directories
mkdir -p backend/{ai,database,routers,models}
mkdir -p frontend/{pages,utils,assets/badges}
mkdir -p mock_data/{transcripts,reflections,peer_feedback,teacher_notes,parent_notes}
mkdir -p scripts
mkdir -p Docs
mkdir -p Implementation_Shards

# Create __init__.py files
touch backend/__init__.py
touch backend/ai/__init__.py
touch backend/database/__init__.py
touch backend/routers/__init__.py
touch backend/models/__init__.py
touch frontend/__init__.py
touch frontend/utils/__init__.py

# Create placeholder files
touch backend/main.py
touch frontend/Home.py
touch .gitignore

echo "✅ Project structure created successfully!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and add your OpenAI API key"
echo "2. Run: docker-compose up -d"
echo "3. Verify database connection"
```

### 8. .gitignore

**File:** `.gitignore`

```
# Environment
.env
*.env
!.env.example

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Docker
postgres_data/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Testing
.pytest_cache/
htmlcov/
.coverage
```

---

## Acceptance Criteria

- [ ] Docker Compose starts all 3 services (db, backend, frontend) successfully
- [ ] PostgreSQL database is accessible on port 5432
- [ ] All 6 tables created: `students`, `teachers`, `data_entries`, `assessments`, `teacher_corrections`, `skill_targets`, `badges`
- [ ] All indexes created successfully
- [ ] Seed data loaded: 2 teachers, 4 students
- [ ] Database connection test passes from backend
- [ ] Views created: `latest_assessments`, `student_progress_summary`
- [ ] Trigger `mark_assessment_corrected` fires correctly
- [ ] Backend accessible on http://localhost:8000
- [ ] Frontend accessible on http://localhost:8501

---

## Testing Commands

```bash
# Start services
docker-compose up -d

# Check service health
docker-compose ps

# Test database connection
docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "SELECT COUNT(*) FROM students;"

# Expected output: 4

# Check backend connectivity
curl http://localhost:8000/health

# Expected: {"status": "healthy", "database": "connected"}

# View logs
docker-compose logs -f backend
```

---

## Troubleshooting

### Issue: Database connection refused
**Solution:** Ensure PostgreSQL container is healthy before backend starts
```bash
docker-compose logs db
```

### Issue: Port already in use
**Solution:** Change ports in docker-compose.yml or stop conflicting services

### Issue: Permission denied on init.sql
**Solution:** Check file permissions
```bash
chmod 644 backend/database/init.sql
```

---

## Dependencies for Next Shards

Once this shard is complete, the following shards can begin:
- **Shard 2**: Mock Data Generation (needs DB schema reference)
- **Shard 3**: AI Inference Pipeline (needs DB connection)
- **Shard 4**: Backend API (needs DB tables)

---

**Completion Checklist:**
- [ ] All files created
- [ ] Docker environment running
- [ ] Database schema deployed
- [ ] Seed data verified
- [ ] Connection tests pass
- [ ] Documentation complete

**Sign-off:** _____________________
**Date:** _____________________
