# Middle School Non-Academic Skills Measurement Engine

## Implementation PRD v1.0 (MVP Engineering Specification)

**Organization:** Flourish Schools  
**Project ID:** JnGyV0Xlx2AEiL31nu7J_1761530509243  
**Version:** 1.0 (Engineering Implementation)  
**Date:** November 10, 2025  
**Engineer Handoff Document**

---

## Executive Summary

This document provides **step-by-step technical specifications** for building the MVP of the Non-Academic Skills Measurement Engine. The MVP demonstrates an AI-powered system that analyzes student data (transcripts, reflections, peer feedback, notes) to assess 17 non-academic skills using a 4-level rubric (Emerging, Developing, Proficient, Advanced). The system includes a teacher dashboard for validation/correction and a student dashboard with gamified progress tracking.

**MVP Goal:** Demonstrate the complete AI inference → human-in-the-loop correction → student engagement pipeline using mock data spanning 3 months.

**Tech Stack:** Python FastAPI + PostgreSQL + Streamlit + OpenAI API

---

## Table of Contents

1. [Technical Architecture](#1-technical-architecture)
2. [Database Schema](#2-database-schema)
3. [Mock Data Specifications](#3-mock-data-specifications)
4. [AI Inference Pipeline](#4-ai-inference-pipeline)
5. [API Endpoints](#5-api-endpoints)
6. [Teacher Dashboard Requirements](#6-teacher-dashboard-requirements)
7. [Student Dashboard Requirements](#7-student-dashboard-requirements)
8. [Implementation Steps](#8-implementation-steps)
9. [Testing & Validation](#9-testing--validation)
10. [File Structure](#10-file-structure)

---

## 1. Technical Architecture

### 1.1 Stack Overview

| Component           | Technology                    | Purpose                                                   |
| ------------------- | ----------------------------- | --------------------------------------------------------- |
| **Backend API**     | FastAPI (Python 3.11+)        | RESTful API for data processing and AI inference          |
| **Database**        | PostgreSQL 15+ (Local/Docker) | Persistent storage for students, assessments, corrections |
| **AI Engine**       | OpenAI API (GPT-4)            | LLM-based skill inference using context engineering       |
| **Frontend (Demo)** | Streamlit 1.28+               | Rapid prototyping for both teacher and student dashboards |
| **Environment**     | Docker Compose                | Containerized development environment                     |

### 1.2 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT DASHBOARDS                     │
│  ┌──────────────────────┐      ┌───────────────────────┐   │
│  │  Teacher Dashboard   │      │  Student Dashboard    │   │
│  │  - Skill Trends      │      │  - Journey Map        │   │
│  │  - Correction UI     │      │  - Badge Collection   │   │
│  └──────────────────────┘      └───────────────────────┘   │
└───────────────────────┬──────────────────┬──────────────────┘
                        │                  │
                        ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Data Ingest  │  │ AI Inference │  │ Correction API   │  │
│  │   Endpoint   │  │   Pipeline   │  │    Endpoint      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   POSTGRESQL DATABASE                        │
│  Tables: students, teachers, data_entries, assessments,      │
│          teacher_corrections, skill_targets                  │
└─────────────────────────────────────────────────────────────┘
                        ▲
                        │
                  ┌─────┴──────┐
                  │ Mock Data  │
                  │ JSON Files │
                  └────────────┘
```

### 1.3 Development Environment Setup

**Prerequisites:**

- Docker Desktop installed
- Python 3.11+
- OpenAI API key

**Environment Variables (.env):**

```bash
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_USER=flourish_admin
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=skills_tracker_db
DATABASE_URL=postgresql://flourish_admin:secure_password_123@db:5432/skills_tracker_db
```

---

## 2. Database Schema

### 2.1 Entity Relationship Diagram

```
students (1) ──────< (N) data_entries
    │                       │
    │                       ├──> (N) assessments
    │                       │         │
    │                       │         └──> (1) teacher_corrections
    │                       │
    └──> (1) teachers      └──> (1) skill_targets
```

### 2.2 Table Definitions

#### **students**

```sql
CREATE TABLE students (
    id VARCHAR(10) PRIMARY KEY,           -- e.g., 'S001'
    name VARCHAR(100) NOT NULL,
    grade INTEGER NOT NULL,
    teacher_id VARCHAR(10) REFERENCES teachers(id),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **teachers**

```sql
CREATE TABLE teachers (
    id VARCHAR(10) PRIMARY KEY,           -- e.g., 'T001'
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **data_entries**

```sql
CREATE TABLE data_entries (
    id VARCHAR(20) PRIMARY KEY,           -- e.g., 'DE001'
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    teacher_id VARCHAR(10) REFERENCES teachers(id),
    type VARCHAR(50) NOT NULL,            -- 'group_discussion', 'reflection', etc.
    date DATE NOT NULL,
    content TEXT NOT NULL,                -- Full transcript/note text
    metadata JSONB,                       -- {duration, participants, topic, etc.}
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_student_date (student_id, date),
    INDEX idx_type (type)
);
```

**Supported `type` values:**

- `group_discussion_transcript`
- `peer_tutoring_transcript`
- `project_presentation_transcript`
- `reflection_journal`
- `peer_feedback`
- `teacher_observation_note`
- `parent_note`

#### **assessments**

```sql
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    data_entry_id VARCHAR(20) REFERENCES data_entries(id) ON DELETE CASCADE,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,     -- e.g., 'Self-Awareness'
    skill_category VARCHAR(50) NOT NULL,  -- 'SEL', 'EF', '21st_Century'
    level VARCHAR(20) NOT NULL,           -- 'Emerging', 'Developing', 'Proficient', 'Advanced'
    confidence_score DECIMAL(3,2),        -- 0.00 to 1.00 (optional)
    justification TEXT NOT NULL,          -- AI-generated explanation with quote
    source_quote TEXT NOT NULL,           -- Direct quote from data_entry.content
    data_point_count INTEGER DEFAULT 1,   -- Number of observations supporting this assessment
    rubric_version VARCHAR(10) DEFAULT '1.0',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (data_entry_id, skill_name),
    INDEX idx_student_skill (student_id, skill_name),
    INDEX idx_level (level)
);
```

#### **teacher_corrections**

```sql
CREATE TABLE teacher_corrections (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    original_level VARCHAR(20) NOT NULL,
    corrected_level VARCHAR(20) NOT NULL,
    original_justification TEXT,
    corrected_justification TEXT,
    teacher_notes TEXT,                   -- Optional notes explaining correction
    corrected_by VARCHAR(10) REFERENCES teachers(id),
    corrected_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_corrected_by (corrected_by)
);
```

#### **skill_targets**

```sql
CREATE TABLE skill_targets (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    assigned_by VARCHAR(10) REFERENCES teachers(id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    UNIQUE (student_id, skill_name, completed)
);
```

---

## 3. Mock Data Specifications

### 3.1 Student Personas

| Student ID | Name  | Teacher       | Grade | Arc Description                                                                                                          |
| ---------- | ----- | ------------- | ----- | ------------------------------------------------------------------------------------------------------------------------ |
| **S001**   | Eva   | Ms. Rodriguez | 7     | **The Steady Climber:** Consistent growth across all domains. Strong communicator from start, grows in self-management.  |
| **S002**   | Lucas | Ms. Rodriguez | 7     | **The Executive Function Champion:** Strong in SEL, initially weak in planning/organization, makes breakthrough mid-way. |
| **S003**   | Pat   | Mr. Thompson  | 7     | **The Late Bloomer:** Slow start, rapid acceleration in Month 3. Initially reserved in collaboration.                    |
| **S004**   | Mia   | Mr. Thompson  | 7     | **The Well-Rounded Leader:** Already strong, achieves Advanced in multiple skills. Natural peer mentor.                  |

### 3.2 Data Distribution Timeline

**3-Month Timeline: August - October 2025**

| Month         | Week | Data Entry Frequency | Rationale                |
| ------------- | ---- | -------------------- | ------------------------ |
| **August**    | 1-2  | 3 entries/student    | Baseline establishment   |
| **August**    | 3-4  | 2 entries/student    | Regular data collection  |
| **September** | 1-2  | 4 entries/student    | Peak project work        |
| **September** | 3-4  | 3 entries/student    | Mid-intervention check   |
| **October**   | 1-2  | 4 entries/student    | Final project push       |
| **October**   | 3-4  | 2 entries/student    | Reflection/consolidation |

**Total per student:** ~18-22 data entries over 3 months

### 3.3 Data Type Distribution

Each student should have a balanced mix across 7 data types:

| Data Type                    | Count/Student | Focus Skills                                                  |
| ---------------------------- | ------------- | ------------------------------------------------------------- |
| Group Discussion Transcripts | 3             | Collaboration, Communication, Relationship Skills             |
| Peer Tutoring Transcripts    | 3             | Social Awareness, Communication, Self-Management              |
| Project Presentations        | 3             | Communication, Critical Thinking, Creativity                  |
| Reflection Journals          | 3             | Self-Awareness, Self-Management, Metacognition                |
| Peer Feedback Forms          | 2             | Social Awareness, Relationship Skills                         |
| Teacher Observation Notes    | 3             | All skills, holistic view                                     |
| Parent Notes                 | 2             | Self-Management, Task Initiation, Organization (home context) |

**Total: 19 entries × 4 students = 76 data entries**

### 3.4 Mock Data File Structure

```
/mock_data/
├── config.json                          # Master configuration
├── students.json                        # Student and teacher definitions
├── transcripts/
│   ├── S001_group_disc_2025-08-15.md
│   ├── S001_peer_tutor_2025-08-22.md
│   ├── S001_presentation_2025-09-10.md
│   └── ...
├── reflections/
│   ├── S001_reflection_2025-08-18.md
│   └── ...
├── peer_feedback/
│   ├── S001_peer_fb_2025-09-05.json
│   └── ...
├── teacher_notes/
│   ├── S001_teacher_obs_2025-08-20.md
│   └── ...
└── parent_notes/
    ├── S001_parent_note_2025-09-15.md
    └── ...
```

### 3.5 config.json Schema

```json
{
  "project": {
    "name": "Flourish Skills Tracker MVP",
    "version": "1.0",
    "rubric_version": "1.0",
    "data_period": {
      "start": "2025-08-01",
      "end": "2025-10-31"
    }
  },
  "students": [
    {
      "id": "S001",
      "name": "Eva",
      "grade": 7,
      "teacher_id": "T001"
    }
  ],
  "teachers": [
    {
      "id": "T001",
      "name": "Ms. Rodriguez",
      "email": "rodriguez@flourishschools.edu"
    }
  ],
  "data_entries": [
    {
      "id": "DE001",
      "student_id": "S001",
      "teacher_id": "T001",
      "type": "group_discussion_transcript",
      "date": "2025-08-15",
      "file_path": "transcripts/S001_group_disc_2025-08-15.md",
      "metadata": {
        "duration_mins": 45,
        "participants": ["S001", "S002", "S003"],
        "topic": "Climate change solutions debate",
        "context": "Science class collaborative project"
      }
    }
  ]
}
```

### 3.6 Transcript Content Guidelines

**Group Discussion Transcript Example:**

```markdown
# Group Discussion: Climate Change Solutions

**Date:** August 15, 2025
**Participants:** Eva (S001), Lucas (S002), Jordan (S003)
**Duration:** 45 minutes
**Context:** Science class collaborative project

---

**Ms. Rodriguez:** "Alright team, today you're going to discuss potential solutions to climate change. Remember to listen to each other and build on ideas. Eva, would you like to start us off?"

**Eva:** "Sure! Um, I was thinking we could focus on renewable energy? Like, solar panels and wind turbines."

**Lucas:** _interrupts_ "That's boring! Everyone talks about that. We should do something about stopping people from wasting food."

**Eva:** _pauses, then responds calmly_ "I hear you, Lucas. Food waste is definitely important. Maybe we could look at both? They're kind of connected—like, food production uses a lot of energy."

**Lucas:** "Oh... I didn't think about that. Yeah, okay."

**Jordan:** _quietly_ "I also read that transportation is a big problem..."

**Eva:** "Great point, Jordan! Can you tell us more about what you found?"

[Transcript continues...]
```

**Key Behavioral Markers to Include:**

- **Emerging:** Interruptions, giving up quickly, off-task comments
- **Developing:** Responses with prompting, simple ideas, needs structure
- **Proficient:** Active listening, building on ideas, staying on task
- **Advanced:** Facilitating discussion, synthesizing ideas, mentoring peers

---

## 4. AI Inference Pipeline

### 4.1 Context Engineering Approach

The AI inference pipeline uses **Zero-Shot + Few-Shot Learning** with the full rubric embedded in the system prompt.

#### **System Prompt Template:**

````python
SYSTEM_PROMPT = """You are an Expert Educational Assessor specializing in middle school non-academic skill development. Your task is to analyze student data (transcripts, notes, reflections, feedback) and assess proficiency levels for specific skills based on a comprehensive behavioral rubric.

# YOUR ROLE
- Objective and unbiased
- Focus on observable behaviors, not assumptions
- Provide specific evidence for every assessment
- Use the EXACT proficiency levels defined in the rubric

# THE 17 SKILLS YOU ASSESS
[Full list of 17 skills from rubric inserted here]

# PROFICIENCY LEVELS
- **Emerging (E):** Needs significant, consistent support; skill application is inconsistent or absent.
- **Developing (D):** Applies the skill with frequent prompting or scaffolding; inconsistent success.
- **Proficient (P):** Applies the skill independently and consistently in familiar contexts; generally successful.
- **Advanced (A):** Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others.

# COMPLETE RUBRIC
[Full rubric for all 17 skills inserted here]

# ASSESSMENT RULES
1. **Evidence-Based:** Every assessment MUST include a direct quote from the source material.
2. **Specific Skill Focus:** Assess ONLY the skills that have observable evidence in the data.
3. **Level Justification:** Explain WHY the student is at that level using rubric criteria.
4. **Quote Selection:** Choose the MOST representative quote (1-3 sentences) that demonstrates the behavior.
5. **No Assumptions:** Do not infer beyond what is observable in the text.
6. **Confidence Threshold:** If there is insufficient evidence to assess a skill, mark it as "Insufficient Data."

# OUTPUT FORMAT
Return your assessment as a JSON array with the following structure:

```json
[
  {
    "skill_name": "Self-Awareness",
    "skill_category": "SEL",
    "level": "Developing",
    "confidence_score": 0.85,
    "justification": "The student can name basic emotions when prompted and is beginning to connect feelings to behavior. In the transcript, the student says 'I was feeling frustrated because...' after being asked by the teacher to reflect. This demonstrates D-level self-awareness: naming emotions with prompting.",
    "source_quote": "I was feeling frustrated because the group wasn't listening to my ideas, and that made me want to just stop participating.",
    "data_point_count": 1
  }
]
````

# FEW-SHOT EXAMPLES (If Available)

[Teacher-corrected examples inserted here as training data]

Now, analyze the following student data and provide assessments for ALL observable skills."""

````

### 4.2 Inference Pipeline Implementation

**File:** `backend/ai/inference_engine.py`

```python
import openai
import json
from typing import List, Dict, Any

class SkillInferenceEngine:
    def __init__(self, api_key: str, rubric: str, few_shot_examples: List[Dict] = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.rubric = rubric
        self.few_shot_examples = few_shot_examples or []

    def assess_skills(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Assess skills for a given student data entry.

        Args:
            student_data: {
                "content": "Full transcript or note text",
                "metadata": {"type": "group_discussion", "date": "2025-08-15", ...}
            }

        Returns:
            List of skill assessments in JSON format
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(student_data)

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Low temperature for consistency
            max_tokens=3000
        )

        assessments = json.loads(response.choices[0].message.content)
        return assessments

    def _build_system_prompt(self) -> str:
        # Build the full system prompt with rubric and few-shot examples
        prompt = SYSTEM_PROMPT_TEMPLATE  # From above

        if self.few_shot_examples:
            prompt += "\n\n# FEW-SHOT LEARNING EXAMPLES\n"
            prompt += "Here are examples of high-quality assessments corrected by teachers:\n\n"
            for example in self.few_shot_examples[-5:]:  # Use last 5 corrections
                prompt += f"**Example:**\n{json.dumps(example, indent=2)}\n\n"

        return prompt

    def _build_user_prompt(self, student_data: Dict[str, Any]) -> str:
        return f"""
# STUDENT DATA TO ANALYZE

**Type:** {student_data['metadata']['type']}
**Date:** {student_data['metadata']['date']}
**Context:** {student_data['metadata'].get('context', 'N/A')}

**Content:**
{student_data['content']}

---

Please assess all observable skills based on this data. Return ONLY the JSON array, no additional text.
"""
````

### 4.3 Few-Shot Learning Integration

**File:** `backend/ai/few_shot_manager.py`

```python
from typing import List, Dict
from backend.database import get_db_connection

class FewShotManager:
    """Manages teacher corrections for few-shot learning."""

    def get_recent_corrections(self, skill_name: str = None, limit: int = 5) -> List[Dict]:
        """
        Retrieve recent teacher corrections to use as few-shot examples.

        Args:
            skill_name: Optional skill filter (e.g., only corrections for "Self-Awareness")
            limit: Maximum number of examples to return

        Returns:
            List of correction examples in LLM-friendly format
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                a.skill_name,
                a.skill_category,
                tc.corrected_level,
                tc.corrected_justification,
                a.source_quote,
                tc.teacher_notes
            FROM teacher_corrections tc
            JOIN assessments a ON tc.assessment_id = a.id
            WHERE tc.teacher_notes IS NOT NULL
        """

        if skill_name:
            query += " AND a.skill_name = %s"
            cursor.execute(query + " ORDER BY tc.corrected_at DESC LIMIT %s", (skill_name, limit))
        else:
            cursor.execute(query + " ORDER BY tc.corrected_at DESC LIMIT %s", (limit,))

        corrections = cursor.fetchall()

        examples = []
        for correction in corrections:
            examples.append({
                "skill_name": correction[0],
                "skill_category": correction[1],
                "level": correction[2],
                "justification": correction[3],
                "source_quote": correction[4],
                "teacher_notes": correction[5]
            })

        return examples
```

### 4.4 Data Quality Confidence Scoring

**Implementation Logic:**

```python
def calculate_confidence_score(data_entry: Dict, assessment: Dict) -> float:
    """
    Calculate confidence score based on data quality indicators.

    Factors:
    - Quote length and specificity
    - Data entry length
    - Alignment with rubric language
    - Historical data availability
    """
    confidence = 0.5  # Base confidence

    # Factor 1: Source quote length (longer quotes indicate clearer evidence)
    quote_length = len(assessment['source_quote'].split())
    if quote_length >= 20:
        confidence += 0.15
    elif quote_length >= 10:
        confidence += 0.10

    # Factor 2: Rubric keyword matching
    rubric_keywords = ['independently', 'consistently', 'with prompting', 'struggles to']
    if any(keyword in assessment['justification'].lower() for keyword in rubric_keywords):
        confidence += 0.15

    # Factor 3: Data entry completeness
    if len(data_entry['content'].split()) > 200:
        confidence += 0.10

    # Factor 4: Historical data point count
    if assessment.get('data_point_count', 1) >= 3:
        confidence += 0.10

    return min(confidence, 1.0)  # Cap at 1.0
```

---

## 5. API Endpoints

### 5.1 FastAPI Application Structure

**File:** `backend/main.py`

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import logging

app = FastAPI(title="Flourish Skills Tracker API", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from backend.routers import data_ingest, assessments, corrections, students

app.include_router(data_ingest.router, prefix="/api/data", tags=["Data Ingestion"])
app.include_router(assessments.router, prefix="/api/assessments", tags=["Assessments"])
app.include_router(corrections.router, prefix="/api/corrections", tags=["Teacher Corrections"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])

@app.get("/")
def root():
    return {"message": "Flourish Skills Tracker API v1.0", "status": "operational"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
```

### 5.2 Core Endpoints

#### **POST /api/data/ingest**

Ingest mock data and trigger AI assessment.

**Request Body:**

```json
{
  "data_entry_id": "DE001",
  "student_id": "S001",
  "type": "group_discussion_transcript",
  "date": "2025-08-15",
  "content": "Full transcript text...",
  "metadata": {
    "duration_mins": 45,
    "participants": ["S001", "S002"],
    "topic": "Climate change"
  }
}
```

**Response:**

```json
{
  "data_entry_id": "DE001",
  "assessments_created": 5,
  "assessment_ids": [1, 2, 3, 4, 5],
  "status": "success"
}
```

#### **GET /api/assessments/student/{student_id}**

Retrieve all assessments for a student.

**Query Parameters:**

- `skill_name` (optional): Filter by specific skill
- `date_from` (optional): Filter by start date
- `date_to` (optional): Filter by end date

**Response:**

```json
{
  "student_id": "S001",
  "total_assessments": 25,
  "assessments": [
    {
      "id": 1,
      "skill_name": "Self-Awareness",
      "skill_category": "SEL",
      "level": "Developing",
      "confidence_score": 0.85,
      "justification": "Student demonstrates...",
      "source_quote": "I was feeling frustrated...",
      "date": "2025-08-15",
      "data_entry_type": "group_discussion_transcript",
      "corrected": false
    }
  ]
}
```

#### **GET /api/assessments/skill-trends/{student_id}**

Get skill progression over time for visualization.

**Response:**

```json
{
  "student_id": "S001",
  "skills": [
    {
      "skill_name": "Self-Awareness",
      "skill_category": "SEL",
      "trend": [
        { "date": "2025-08-15", "level": "Emerging", "level_numeric": 1 },
        { "date": "2025-09-10", "level": "Developing", "level_numeric": 2 },
        { "date": "2025-10-05", "level": "Proficient", "level_numeric": 3 }
      ],
      "current_level": "Proficient",
      "growth_direction": "positive"
    }
  ]
}
```

#### **POST /api/corrections/submit**

Submit teacher correction for an assessment.

**Request Body:**

```json
{
  "assessment_id": 1,
  "corrected_level": "Proficient",
  "corrected_justification": "Student actually demonstrates consistent skill application...",
  "teacher_notes": "The AI missed the context where Eva independently managed her emotions during conflict.",
  "corrected_by": "T001"
}
```

**Response:**

```json
{
  "correction_id": 1,
  "status": "success",
  "message": "Correction saved and added to few-shot training set"
}
```

#### **POST /api/students/{student_id}/target-skill**

Assign a target skill to a student.

**Request Body:**

```json
{
  "skill_name": "Self-Management",
  "assigned_by": "T001"
}
```

**Response:**

```json
{
  "target_id": 1,
  "student_id": "S001",
  "skill_name": "Self-Management",
  "assigned_at": "2025-10-15T10:30:00Z",
  "status": "assigned"
}
```

#### **GET /api/students/{student_id}/badges**

Retrieve earned badges for student dashboard.

**Response:**

```json
{
  "student_id": "S001",
  "total_badges": 3,
  "badges": [
    {
      "badge_id": 1,
      "skill_name": "Communication",
      "earned_date": "2025-10-01",
      "level_achieved": "Advanced",
      "badge_icon": "🎖️"
    }
  ]
}
```

---

## 6. Teacher Dashboard Requirements

### 6.1 Dashboard Pages

The Streamlit teacher dashboard consists of **4 main pages:**

1. **Student Overview** - Grid view of all students
2. **Skill Trends** - Individual student skill progression charts
3. **Assessment Review** - Validate/correct AI assessments
4. **Target Assignment** - Assign next target skills

### 6.2 Page 1: Student Overview

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  👩‍🏫 Teacher Dashboard - Ms. Rodriguez                       │
├─────────────────────────────────────────────────────────────┤
│  [Student Overview] [Skill Trends] [Assessment Review]      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  My Students (4)                                            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Eva          │  │ Lucas        │  │ Pat          │ ... │
│  │ 23 Assess.   │  │ 19 Assess.   │  │ 21 Assess.   │     │
│  │ ▲ Trending   │  │ ▲ Trending   │  │ → Stable     │     │
│  │ [View]       │  │ [View]       │  │ [View]       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation (Streamlit):**

```python
import streamlit as st
import requests

st.set_page_config(page_title="Teacher Dashboard", layout="wide")

st.title("👩‍🏫 Teacher Dashboard")

# Fetch students
teacher_id = st.session_state.get("teacher_id", "T001")
response = requests.get(f"http://backend:8000/api/students?teacher_id={teacher_id}")
students = response.json()

st.header(f"My Students ({len(students)})")

cols = st.columns(4)
for idx, student in enumerate(students):
    with cols[idx % 4]:
        st.subheader(student['name'])
        st.metric("Total Assessments", student['assessment_count'])
        st.metric("Growth Trend", student['trend_indicator'])
        if st.button(f"View {student['name']}", key=f"view_{student['id']}"):
            st.session_state.selected_student = student['id']
            st.switch_page("pages/02_Skill_Trends.py")
```

### 6.3 Page 2: Skill Trends

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  Skill Trends - Eva                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SEL Skills Progress                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Self-Awareness:  E ─→ D ─→ P                         │  │
│  │ Self-Management: E ─→ D ─→ D                         │  │
│  │ Social Awareness: D ─→ P ─→ P                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  Detailed Chart: Self-Awareness                             │
│  [Line chart showing progression Aug-Oct]                   │
│                                                              │
│  Recent Data Points (5 most recent)                         │
│  - Aug 15: Group Discussion → Developing                    │
│  - Sep 10: Reflection → Developing                          │
│  - Oct 5: Peer Feedback → Proficient                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import streamlit as st
import plotly.express as px
import pandas as pd

student_id = st.session_state.get("selected_student", "S001")

# Fetch skill trends
response = requests.get(f"http://backend:8000/api/assessments/skill-trends/{student_id}")
trends = response.json()

st.title(f"Skill Trends - {trends['student_name']}")

# Display by category
for category in ["SEL", "EF", "21st_Century"]:
    st.header(f"{category} Skills Progress")

    category_skills = [s for s in trends['skills'] if s['skill_category'] == category]

    for skill in category_skills:
        # Create mini timeline
        timeline_str = " → ".join([f"{t['level'][0]}" for t in skill['trend']])
        st.write(f"**{skill['skill_name']}:** {timeline_str}")

        # Detailed chart
        if st.checkbox(f"Show detailed chart for {skill['skill_name']}", key=skill['skill_name']):
            df = pd.DataFrame(skill['trend'])
            fig = px.line(df, x='date', y='level_numeric',
                          title=f"{skill['skill_name']} Progression",
                          labels={'level_numeric': 'Proficiency Level', 'date': 'Date'},
                          markers=True)
            st.plotly_chart(fig)
```

### 6.4 Page 3: Assessment Review (Correction Workflow)

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  Assessment Review - Pending Corrections                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Filter: [All Students ▼] [All Skills ▼] [Low Conf Only ✓] │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Assessment #47 - Eva - Self-Management                 │ │
│  │ Date: Oct 5, 2025 | Source: Reflection Journal        │ │
│  │                                                         │ │
│  │ AI Assessment: Developing (Confidence: 78%)            │ │
│  │ Justification: "Student uses simple coping strategies  │ │
│  │ when prompted and can sustain effort on short tasks..."│ │
│  │                                                         │ │
│  │ Source Quote: "I took a deep breath like Ms. Rodriguez│ │
│  │ taught us when I got frustrated with my math homework."│ │
│  │                                                         │ │
│  │ ┌─ Rubric Reference (Developing) ──────────────────┐   │ │
│  │ │ Uses simple coping strategies when prompted;      │   │ │
│  │ │ can sustain effort on short tasks with reminders  │   │ │
│  │ └───────────────────────────────────────────────────┘   │ │
│  │                                                         │ │
│  │ Your Assessment:                                        │ │
│  │ Level: [Developing ▼] ← Change to: [Proficient ▼]     │ │
│  │                                                         │ │
│  │ Justification (optional correction):                   │ │
│  │ [Text area for teacher input]                          │ │
│  │                                                         │ │
│  │ Notes (explain your correction):                       │ │
│  │ [Text area for teacher notes]                          │ │
│  │                                                         │ │
│  │ [✓ Approve as-is] [📝 Submit Correction] [⏭️ Skip]    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import streamlit as st

st.title("Assessment Review")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    selected_student = st.selectbox("Student", ["All Students", "Eva", "Lucas", "Pat", "Mia"])
with col2:
    selected_skill = st.selectbox("Skill", ["All Skills"] + SKILL_LIST)
with col3:
    low_conf_only = st.checkbox("Low Confidence Only (< 80%)")

# Fetch pending assessments
params = {
    "corrected": False,
    "confidence_threshold": 0.8 if low_conf_only else 0.0
}
response = requests.get("http://backend:8000/api/assessments/pending", params=params)
assessments = response.json()

st.write(f"**Pending Reviews:** {len(assessments)}")

# Display assessments one at a time
if assessments:
    current_idx = st.session_state.get("review_index", 0)
    assessment = assessments[current_idx]

    with st.container():
        st.subheader(f"Assessment #{assessment['id']} - {assessment['student_name']} - {assessment['skill_name']}")
        st.caption(f"Date: {assessment['date']} | Source: {assessment['data_entry_type']}")

        # Display AI assessment
        st.info(f"**AI Assessment:** {assessment['level']} (Confidence: {assessment['confidence_score']*100:.0f}%)")
        st.write("**Justification:**")
        st.write(assessment['justification'])

        st.write("**Source Quote:**")
        st.code(assessment['source_quote'])

        # Show rubric reference
        with st.expander(f"📖 Rubric Reference - {assessment['level']}"):
            st.write(get_rubric_text(assessment['skill_name'], assessment['level']))

        # Correction form
        st.write("---")
        st.write("**Your Assessment:**")

        corrected_level = st.selectbox(
            "Level",
            options=["Emerging", "Developing", "Proficient", "Advanced"],
            index=["Emerging", "Developing", "Proficient", "Advanced"].index(assessment['level']),
            key=f"level_{assessment['id']}"
        )

        corrected_justification = st.text_area(
            "Justification (optional correction)",
            value=assessment['justification'],
            key=f"just_{assessment['id']}"
        )

        teacher_notes = st.text_area(
            "Notes (explain your correction)",
            placeholder="e.g., 'The AI missed the independent initiative shown in the second paragraph...'",
            key=f"notes_{assessment['id']}"
        )

        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("✓ Approve as-is", key=f"approve_{assessment['id']}"):
                # Approve without changes
                requests.post(f"http://backend:8000/api/assessments/{assessment['id']}/approve")
                st.success("Assessment approved!")
                st.session_state.review_index = current_idx + 1
                st.rerun()

        with col2:
            if st.button("📝 Submit Correction", key=f"correct_{assessment['id']}"):
                # Submit correction
                correction_data = {
                    "assessment_id": assessment['id'],
                    "corrected_level": corrected_level,
                    "corrected_justification": corrected_justification,
                    "teacher_notes": teacher_notes,
                    "corrected_by": st.session_state.teacher_id
                }
                requests.post("http://backend:8000/api/corrections/submit", json=correction_data)
                st.success("Correction submitted and added to training set!")
                st.session_state.review_index = current_idx + 1
                st.rerun()

        with col3:
            if st.button("⏭️ Skip", key=f"skip_{assessment['id']}"):
                st.session_state.review_index = current_idx + 1
                st.rerun()
```

### 6.5 Page 4: Target Assignment

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  Target Skill Assignment                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Student: [Eva ▼]                                           │
│                                                              │
│  Current Target: Self-Management (Assigned Sep 15)          │
│  Progress: Developing → Proficient (Completed ✓)            │
│                                                              │
│  Suggested Next Skills (Based on Rubric Dependencies):      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. Task Initiation (EF)                                │ │
│  │    Current: Developing | Prerequisite: Self-Management │ │
│  │    [Assign]                                            │ │
│  │                                                         │ │
│  │ 2. Planning & Prioritization (EF)                      │ │
│  │    Current: Emerging | Prerequisite: Organization      │ │
│  │    [Assign]                                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Or manually select a skill:                                │
│  [Skill Dropdown] [Assign]                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Student Dashboard Requirements

### 7.1 Dashboard Pages

The Streamlit student dashboard consists of **3 main pages:**

1. **My Journey Map** - Animated skill progression visualization
2. **Badge Collection** - Display earned badges
3. **Current Goal** - Show assigned target skill

### 7.2 Page 1: My Journey Map

**Visual Concept:**

- Horizontal path from left (start) to right (mastery)
- Student avatar moves along the path as skills improve
- Each skill has 4 milestones: E → D → P → A
- Current position highlighted
- Celebratory animation when advancement occurs

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  🎒 Eva's Skill Journey                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Self-Awareness Journey                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  E ─────→ D ─────→ [P] ─────→ A                       │ │
│  │  Aug     Sep      🎉 YOU!     Goal                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Self-Management Journey                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  E ─────→ [D] ─────→ P ─────→ A                       │ │
│  │  Aug     🎉 YOU!    Goal      Future                   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [Show All Skills ▼]                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="My Journey", page_icon="🎒", layout="wide")

st.title("🎒 My Skill Journey")

student_id = st.session_state.get("student_id", "S001")

# Fetch student progress
response = requests.get(f"http://backend:8000/api/students/{student_id}/progress")
progress = response.json()

st.write(f"Welcome back, **{progress['student_name']}**! 🌟")

# Display each skill journey
for skill in progress['skills']:
    st.subheader(f"{skill['skill_name']} Journey")

    # Create visual progress bar
    levels = ["Emerging", "Developing", "Proficient", "Advanced"]
    current_level_idx = levels.index(skill['current_level'])

    cols = st.columns(4)
    for idx, level in enumerate(levels):
        with cols[idx]:
            if idx < current_level_idx:
                st.success(f"✅ {level}")
            elif idx == current_level_idx:
                st.info(f"🎉 **YOU ARE HERE!**\n\n{level}")
                # Trigger celebration animation if new level
                if skill.get('recently_advanced', False):
                    st.balloons()
            else:
                st.write(f"⬜ {level}\n\n(Future Goal)")

    st.write("---")

# Show celebration for recently earned badges
if st.session_state.get("new_badge_earned"):
    st.success("🎖️ Congratulations! You earned a new badge!")
    st.balloons()
```

### 7.3 Page 2: Badge Collection

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  🏆 My Badge Collection                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Badges Earned: 3 / 17                                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   🎖️         │  │   🎖️         │  │   🎖️         │     │
│  │ Communication│  │ Collaboration│  │Social Awareness│    │
│  │   ADVANCED   │  │  PROFICIENT  │  │  PROFICIENT  │     │
│  │ Earned 10/15 │  │ Earned 9/20  │  │ Earned 10/01 │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  In Progress (14 skills remaining)                          │
│  [Show locked badges ▼]                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
import streamlit as st

st.title("🏆 My Badge Collection")

student_id = st.session_state.student_id
response = requests.get(f"http://backend:8000/api/students/{student_id}/badges")
badges = response.json()

st.metric("Badges Earned", f"{badges['earned_count']} / 17")

# Display earned badges
st.subheader("🎖️ Earned Badges")
cols = st.columns(3)
for idx, badge in enumerate(badges['earned']):
    with cols[idx % 3]:
        st.image(badge['icon'], width=100)  # Badge icon
        st.write(f"**{badge['skill_name']}**")
        st.caption(f"Level: {badge['level_achieved']}")
        st.caption(f"Earned: {badge['earned_date']}")

# Show locked badges (optional)
if st.checkbox("Show locked badges"):
    st.subheader("🔒 Locked Badges")
    for skill in badges['locked']:
        st.write(f"- {skill['skill_name']} (Current: {skill['current_level']})")
```

### 7.3 Page 3: Current Goal

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 My Current Goal                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Your teacher assigned you a new skill to focus on!        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │           🎯 SELF-MANAGEMENT 🎯                        │ │
│  │                                                         │ │
│  │  Current Level: Developing                             │ │
│  │  Goal: Reach Proficient                                │ │
│  │                                                         │ │
│  │  What this means:                                      │ │
│  │  "Independently use strategies to manage emotions      │ │
│  │   and stress; set and work toward short-term goals;   │ │
│  │   demonstrate persistence on challenging tasks."       │ │
│  │                                                         │ │
│  │  Tips to improve:                                      │ │
│  │  ✓ Practice taking deep breaths when frustrated       │ │
│  │  ✓ Break big tasks into smaller steps                 │ │
│  │  ✓ Celebrate small wins along the way                 │ │
│  │                                                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Progress Updates:                                          │
│  - Sep 20: Group Discussion → Still Developing             │
│  - Oct 5: Reflection → Moving toward Proficient! 🎉        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Implementation Steps

### Step-by-Step Implementation Guide

#### **Phase 1: Environment Setup (Day 1)**

**1.1 Create Project Structure**

```bash
mkdir flourish-skills-tracker
cd flourish-skills-tracker

mkdir -p backend/{ai,database,routers,models}
mkdir -p frontend/pages
mkdir -p mock_data/{transcripts,reflections,peer_feedback,teacher_notes,parent_notes}
mkdir -p scripts
```

**1.2 Initialize Docker Environment**

Create `docker-compose.yml`:

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

  backend:
    build: ./backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
      - ./mock_data:/app/mock_data
    ports:
      - "8000:8000"
    depends_on:
      - db
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
    command: streamlit run Home.py --server.port 8501

volumes:
  postgres_data:
```

**1.3 Create `.env` File**

```bash
OPENAI_API_KEY=your_api_key_here
POSTGRES_USER=flourish_admin
POSTGRES_PASSWORD=secure_password_123
POSTGRES_DB=skills_tracker_db
DATABASE_URL=postgresql://flourish_admin:secure_password_123@db:5432/skills_tracker_db
```

**1.4 Start Environment**

```bash
docker-compose up -d
```

#### **Phase 2: Database Setup (Day 1)**

**2.1 Create Database Schema**

File: `backend/database/init.sql`

```sql
-- [Insert full schema from Section 2.2]
```

**2.2 Create Database Helper**

File: `backend/database/connection.py`

```python
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )
```

#### **Phase 3: Mock Data Generation (Day 2)**

**3.1 Create Mock Data Generator Script**

File: `scripts/generate_mock_data.py`

```python
import json
from datetime import datetime, timedelta
import random

STUDENTS = [
    {"id": "S001", "name": "Eva", "teacher_id": "T001", "archetype": "steady_climber"},
    {"id": "S002", "name": "Lucas", "teacher_id": "T001", "archetype": "ef_champion"},
    {"id": "S003", "name": "Pat", "teacher_id": "T002", "archetype": "late_bloomer"},
    {"id": "S004", "name": "Mia", "teacher_id": "T002", "archetype": "leader"}
]

TEACHERS = [
    {"id": "T001", "name": "Ms. Rodriguez", "email": "rodriguez@flourishschools.edu"},
    {"id": "T002", "name": "Mr. Thompson", "email": "thompson@flourishschools.edu"}
]

DATA_TYPES = [
    "group_discussion_transcript",
    "peer_tutoring_transcript",
    "project_presentation_transcript",
    "reflection_journal",
    "peer_feedback",
    "teacher_observation_note",
    "parent_note"
]

def generate_transcript_content(student, archetype, data_type, date, month_num):
    """
    Generate realistic transcript content based on student archetype and progression.
    """
    # [Implementation to generate appropriate content based on archetype]
    # Month 1: Baseline (more Emerging/Developing behaviors)
    # Month 2: Growth (more Developing/Proficient behaviors)
    # Month 3: Advanced (more Proficient/Advanced behaviors)

    pass  # Full implementation required

def generate_mock_data():
    data_entries = []
    entry_id = 1

    start_date = datetime(2025, 8, 1)

    # Distribution: [Week 1-2, Week 3-4, Sep Week 1-2, Sep Week 3-4, Oct Week 1-2, Oct Week 3-4]
    entries_per_period = [3, 2, 4, 3, 4, 2]  # Total: 18 per student

    for student in STUDENTS:
        period_idx = 0
        current_date = start_date

        for month in range(3):  # Aug, Sep, Oct
            for half in range(2):  # First half, second half
                num_entries = entries_per_period[period_idx]

                for _ in range(num_entries):
                    # Select data type (ensure balance)
                    data_type = random.choice(DATA_TYPES)

                    # Generate content
                    content = generate_transcript_content(
                        student,
                        student['archetype'],
                        data_type,
                        current_date,
                        month + 1
                    )

                    entry = {
                        "id": f"DE{entry_id:03d}",
                        "student_id": student['id'],
                        "teacher_id": student['teacher_id'],
                        "type": data_type,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "content": content,
                        "metadata": {
                            "duration_mins": random.randint(20, 60),
                            "context": f"Month {month+1} - {data_type.replace('_', ' ').title()}"
                        }
                    }

                    data_entries.append(entry)
                    entry_id += 1

                    # Increment date by 3-5 days
                    current_date += timedelta(days=random.randint(3, 5))

                period_idx += 1

    # Write to config.json
    config = {
        "project": {
            "name": "Flourish Skills Tracker MVP",
            "version": "1.0",
            "rubric_version": "1.0",
            "data_period": {
                "start": "2025-08-01",
                "end": "2025-10-31"
            }
        },
        "students": STUDENTS,
        "teachers": TEACHERS,
        "data_entries": data_entries
    }

    with open("mock_data/config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Generated {len(data_entries)} mock data entries!")

if __name__ == "__main__":
    generate_mock_data()
```

**3.2 Run Mock Data Generation**

```bash
python scripts/generate_mock_data.py
```

#### **Phase 4: AI Inference Pipeline (Day 3-4)**

**4.1 Implement Inference Engine**

File: `backend/ai/inference_engine.py`

```python
# [Insert full implementation from Section 4.2]
```

**4.2 Implement Few-Shot Manager**

File: `backend/ai/few_shot_manager.py`

```python
# [Insert full implementation from Section 4.3]
```

**4.3 Create Rubric Loader**

File: `backend/ai/rubric_loader.py`

```python
def load_rubric():
    """Load the full rubric from markdown file."""
    with open("backend/ai/rubric.md", "r") as f:
        return f.read()
```

#### **Phase 5: Backend API (Day 4-5)**

**5.1 Create FastAPI Application**

File: `backend/main.py`

```python
# [Insert full implementation from Section 5.1]
```

**5.2 Implement Data Ingestion Router**

File: `backend/routers/data_ingest.py`

```python
from fastapi import APIRouter, HTTPException
from backend.ai.inference_engine import SkillInferenceEngine
from backend.database.connection import get_db_connection

router = APIRouter()

@router.post("/ingest")
def ingest_data(data_entry: dict):
    """
    Ingest a data entry and trigger AI assessment.
    """
    # 1. Insert data_entry into database
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO data_entries (id, student_id, teacher_id, type, date, content, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data_entry['id'],
        data_entry['student_id'],
        data_entry['teacher_id'],
        data_entry['type'],
        data_entry['date'],
        data_entry['content'],
        json.dumps(data_entry['metadata'])
    ))
    conn.commit()

    # 2. Run AI inference
    engine = SkillInferenceEngine(
        api_key=os.getenv("OPENAI_API_KEY"),
        rubric=load_rubric()
    )

    assessments = engine.assess_skills({
        "content": data_entry['content'],
        "metadata": data_entry['metadata']
    })

    # 3. Insert assessments into database
    assessment_ids = []
    for assessment in assessments:
        cursor.execute("""
            INSERT INTO assessments
            (data_entry_id, student_id, skill_name, skill_category, level,
             confidence_score, justification, source_quote, rubric_version)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data_entry['id'],
            data_entry['student_id'],
            assessment['skill_name'],
            assessment['skill_category'],
            assessment['level'],
            assessment['confidence_score'],
            assessment['justification'],
            assessment['source_quote'],
            '1.0'
        ))
        assessment_ids.append(cursor.fetchone()['id'])

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "data_entry_id": data_entry['id'],
        "assessments_created": len(assessment_ids),
        "assessment_ids": assessment_ids,
        "status": "success"
    }
```

**5.3 Implement Additional Routers**

- `backend/routers/assessments.py` - Assessment retrieval endpoints
- `backend/routers/corrections.py` - Teacher correction endpoints
- `backend/routers/students.py` - Student data endpoints

#### **Phase 6: Teacher Dashboard (Day 6-7)**

**6.1 Create Streamlit Home Page**

File: `frontend/Home.py`

```python
# [Insert implementation from Section 6.2]
```

**6.2 Create Dashboard Pages**

- `frontend/pages/01_Student_Overview.py`
- `frontend/pages/02_Skill_Trends.py`
- `frontend/pages/03_Assessment_Review.py`
- `frontend/pages/04_Target_Assignment.py`

#### **Phase 7: Student Dashboard (Day 7-8)**

**7.1 Create Student Pages**

- `frontend/pages/Student_01_Journey_Map.py`
- `frontend/pages/Student_02_Badge_Collection.py`
- `frontend/pages/Student_03_Current_Goal.py`

#### **Phase 8: Data Ingestion & Testing (Day 8-9)**

**8.1 Bulk Ingest Mock Data**

File: `scripts/ingest_all_data.py`

```python
import json
import requests

with open("mock_data/config.json", "r") as f:
    config = json.load(f)

for entry in config['data_entries']:
    response = requests.post("http://localhost:8000/api/data/ingest", json=entry)
    print(f"Ingested {entry['id']}: {response.json()['assessments_created']} assessments created")
```

**8.2 Run Full Ingestion**

```bash
python scripts/ingest_all_data.py
```

#### **Phase 9: Testing & Refinement (Day 9-10)**

**9.1 Test AI Accuracy**

- Manually review 10-15 assessments
- Calculate initial TAR (Teacher Agreement Rate)

**9.2 Submit Teacher Corrections**

- Use correction workflow to add 5-10 corrections
- Verify few-shot learning integration

**9.3 Test Dashboard Flows**

- Verify all visualizations render correctly
- Test skill trend charts
- Confirm badge system works

---

## 9. Testing & Validation

### 9.1 Test Cases

| Test ID  | Category            | Test Case                                              | Expected Outcome                            |
| -------- | ------------------- | ------------------------------------------------------ | ------------------------------------------- |
| **T001** | Data Ingestion      | Ingest single transcript                               | Data entry + assessments created in DB      |
| **T002** | AI Inference        | Assess group discussion with clear Proficient behavior | Level = Proficient, Confidence > 0.8        |
| **T003** | AI Inference        | Assess reflection with limited data                    | Insufficient Data flag or low confidence    |
| **T004** | Correction Workflow | Submit teacher correction                              | Correction saved, few-shot examples updated |
| **T005** | Skill Trends        | View student progression chart                         | Chart shows E→D→P progression               |
| **T006** | Target Assignment   | Assign target skill to student                         | Skill visible in student dashboard          |
| **T007** | Badge System        | Student reaches Advanced level                         | Badge earned and displayed                  |
| **T008** | Journey Map         | Skill level increases                                  | Avatar moves on journey map                 |

### 9.2 Performance Benchmarks

| Metric                           | Target                         | Measurement Method              |
| -------------------------------- | ------------------------------ | ------------------------------- |
| **API Response Time**            | < 2s for assessment generation | FastAPI logging                 |
| **TAR (Teacher Agreement Rate)** | ≥ 85%                          | Manual review of 20 assessments |
| **Dashboard Load Time**          | < 3s                           | Streamlit profiling             |
| **Database Query Performance**   | < 500ms for trend queries      | PostgreSQL EXPLAIN ANALYZE      |

### 9.3 Validation Checklist

**Before Demo:**

- [ ] All 76 mock data entries ingested successfully
- [ ] At least 300 assessments generated (avg 4 skills per entry)
- [ ] All 4 students show clear progression over 3 months
- [ ] Teacher dashboard renders all views without errors
- [ ] Student dashboard shows animated journey maps
- [ ] At least 5 teacher corrections submitted and integrated
- [ ] Badge system awards badges for Advanced achievements
- [ ] Target assignment workflow functional

---

## 10. File Structure

```
flourish-skills-tracker/
│
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                     # FastAPI app entry point
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── inference_engine.py     # Core LLM inference logic
│   │   ├── few_shot_manager.py     # Teacher correction integration
│   │   ├── rubric_loader.py        # Rubric loading utility
│   │   └── rubric.md               # Full rubric text
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── init.sql                # Database schema
│   │   └── connection.py           # DB connection helper
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── data_ingest.py          # Data ingestion endpoints
│   │   ├── assessments.py          # Assessment retrieval
│   │   ├── corrections.py          # Teacher corrections
│   │   └── students.py             # Student data endpoints
│   │
│   └── models/
│       ├── __init__.py
│       └── schemas.py              # Pydantic models
│
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── Home.py                     # Streamlit home page
│   │
│   ├── pages/
│   │   ├── 01_Student_Overview.py
│   │   ├── 02_Skill_Trends.py
│   │   ├── 03_Assessment_Review.py
│   │   ├── 04_Target_Assignment.py
│   │   ├── Student_01_Journey_Map.py
│   │   ├── Student_02_Badge_Collection.py
│   │   └── Student_03_Current_Goal.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── api_client.py           # Backend API wrapper
│
├── mock_data/
│   ├── config.json                 # Master configuration
│   ├── students.json               # (Optional) Separate student file
│   │
│   ├── transcripts/
│   │   ├── S001_group_disc_2025-08-15.md
│   │   ├── S001_peer_tutor_2025-08-22.md
│   │   └── ...
│   │
│   ├── reflections/
│   │   ├── S001_reflection_2025-08-18.md
│   │   └── ...
│   │
│   ├── peer_feedback/
│   │   ├── S001_peer_fb_2025-09-05.json
│   │   └── ...
│   │
│   ├── teacher_notes/
│   │   ├── S001_teacher_obs_2025-08-20.md
│   │   └── ...
│   │
│   └── parent_notes/
│       ├── S001_parent_note_2025-09-15.md
│       └── ...
│
├── scripts/
│   ├── generate_mock_data.py      # Mock data generation
│   ├── ingest_all_data.py         # Bulk data ingestion
│   └── test_ai_accuracy.py        # AI validation script
│
└── docs/
    ├── Implementation_PRD_v1.0.md  # This document
    └── API_Documentation.md        # Auto-generated API docs
```

---

## Appendix A: Quick Start Commands

```bash
# Clone repository (if applicable)
git clone <repository-url>
cd flourish-skills-tracker

# Setup environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Start all services
docker-compose up -d

# Generate mock data
docker-compose exec backend python scripts/generate_mock_data.py

# Ingest all mock data
docker-compose exec backend python scripts/ingest_all_data.py

# Access dashboards
# Teacher Dashboard: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

---

## Appendix B: Dependencies

**Backend (`backend/requirements.txt`):**

```
fastapi==0.104.1
uvicorn==0.24.0
psycopg2-binary==2.9.9
openai==1.3.0
pydantic==2.5.0
python-dotenv==1.0.0
```

**Frontend (`frontend/requirements.txt`):**

```
streamlit==1.28.0
plotly==5.17.0
pandas==2.1.0
requests==2.31.0
streamlit-lottie==0.0.5
```

---

## Appendix C: Key Decisions & Rationale

| Decision                                 | Rationale                                                          |
| ---------------------------------------- | ------------------------------------------------------------------ |
| **Streamlit over React for MVP**         | Rapid prototyping, 80% faster development, sufficient for demo     |
| **Context Engineering over Fine-Tuning** | No labeled data yet, more flexible, easier to iterate              |
| **PostgreSQL over NoSQL**                | Structured data with clear relationships, need for complex queries |
| **Local Docker over AWS for MVP**        | Faster setup, lower costs, easier debugging                        |
| **JSON + Markdown for mock data**        | Human-readable, easy to edit, version control friendly             |
| **Teacher-in-the-loop corrections**      | Ensures accuracy, builds training dataset, maintains trust         |

---

## Contact & Support

**Project Lead:** Flourish Schools  
**Technical Questions:** [Contact email]  
**Documentation:** See `docs/` folder for additional resources

---

**END OF IMPLEMENTATION PRD v1.0**
