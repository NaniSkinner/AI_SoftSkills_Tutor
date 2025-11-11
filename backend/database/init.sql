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
