# Rubric Documentation Index

This index helps you navigate all rubric-related information in the codebase.

## Quick Navigation

### For Quick Lookups
Start here for a rapid overview of all 17 skills and their proficiency descriptors.
- **File:** `RUBRIC_QUICK_REFERENCE.md`
- **What it contains:**
  - All 17 skills organized by category (SEL, EF, 21st Century)
  - All 68 skill descriptors (17 skills × 4 proficiency levels)
  - SQL query examples
  - Level-to-badge mapping
  - Summary statistics

### For Complete Architecture
Detailed technical documentation on how rubric data is stored and used throughout the system.
- **File:** `RUBRIC_STORAGE_ANALYSIS.md`
- **What it contains:**
  - Primary storage locations (Docs/Rubric.md)
  - Database schema for all rubric-related tables
  - Python model schemas for API validation
  - AI inference engine and prompt injection
  - Data flow from ingestion to assessment
  - API endpoints for rubric data access
  - Versioning and future updates strategy
  - Frontend integration details

### The Master Rubric
The authoritative source document containing all rubric content.
- **File:** `Rubric.md`
- **What it contains:**
  - Complete behavioral indicators for all 17 skills
  - Formatted as markdown tables for easy reading
  - Proficiency levels: Emerging (E), Developing (D), Proficient (P), Advanced (A)
  - Version 1.0 (current)

### Curriculum Context
Supporting document explaining why each skill is important for middle school students.
- **File:** `Curriculum.md`
- **What it contains:**
  - Developmental appropriateness research
  - Rationale for each skill
  - Global implementation examples
  - CASEL framework references
  - LLM context engineering notes

---

## The 17 Skills Reference

### Social-Emotional Learning (SEL) - 5 Skills
1. **Self-Awareness** - Identifying emotions and personal strengths
2. **Self-Management** - Managing emotions and persisting through challenges
3. **Social Awareness** - Understanding others' perspectives and emotional cues
4. **Relationship Skills** - Communicating and collaborating effectively
5. **Responsible Decision-Making** - Considering consequences and ethical implications

### Executive Functioning (EF) - 6 Skills
6. **Working Memory** - Holding and using information to complete tasks
7. **Inhibitory Control** - Resisting distractions and controlling impulses
8. **Cognitive Flexibility** - Adapting approaches and transitioning between tasks
9. **Planning & Prioritization** - Setting goals and managing time/resources
10. **Organization** - Managing materials, workspace, and information
11. **Task Initiation** - Beginning work without procrastination

### 21st Century Skills - 6 Skills
12. **Critical Thinking** - Analyzing information and solving complex problems
13. **Communication** - Expressing ideas clearly and persuasively
14. **Collaboration** - Working effectively with diverse team members
15. **Creativity & Innovation** - Generating and refining novel ideas
16. **Digital Literacy** - Using technology safely and effectively
17. **Global Awareness** - Understanding interconnected global issues

---

## Proficiency Levels

All skills are assessed on the same 4-level scale:

| Level | Code | Definition | Badge |
|---|---|---|---|
| **Emerging** | E | Needs significant, consistent support; skill application is inconsistent or absent | None |
| **Developing** | D | Applies the skill with frequent prompting or scaffolding; inconsistent success | Bronze |
| **Proficient** | P | Applies the skill independently and consistently in familiar contexts; generally successful | Silver |
| **Advanced** | A | Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others | Gold |

---

## Where Rubric Data Is Stored

### 1. Source Document
- **Location:** `/Docs/Rubric.md`
- **Format:** Markdown tables
- **Size:** ~17 KB
- **Content:** All 68 skill descriptors

### 2. Database
- **File:** `/backend/database/init.sql`
- **System:** PostgreSQL
- **Key Tables:**
  - `assessments` - Stores proficiency levels with justifications
  - `teacher_corrections` - Stores teacher feedback for refinement
  - `skill_targets` - Tracks level goals
  - `badges` - Tracks achievements

### 3. Python Validation
- **File:** `/backend/models/schemas.py`
- **Models:** Pydantic schemas for API validation
- **Key Models:** AssessmentResponse, CorrectionRequest, TargetAssignmentRequest

### 4. AI System
- **Files:**
  - `/backend/ai/rubric_loader.py` - Loads Rubric.md
  - `/backend/ai/prompts.py` - Injects rubric into system prompt
  - `/backend/ai/inference_engine.py` - Uses rubric for assessment
  - `/backend/ai/few_shot_manager.py` - Learns from corrections
  - `/backend/ai/confidence_scoring.py` - Scores assessment certainty

---

## Key API Endpoints

### Retrieve Assessments
```
GET /api/assessments/student/{student_id}
  → All assessments with skill names, levels, justifications, evidence quotes

GET /api/assessments/skill-trends/{student_id}
  → Assessments grouped by skill with level progression over time

GET /api/assessments/pending
  → Uncorrected assessments needing teacher review (sorted by lowest confidence)
```

### Submit Corrections
```
POST /api/corrections/submit
  → Teacher submits corrected_level and corrected_justification
  → Stores in teacher_corrections for future few-shot learning
```

### Award Badges
```
POST /api/badges/grant
  → Grants badge for level achieved (Bronze/D, Silver/P, Gold/A)
```

---

## Using This Documentation

### If you want to...

**Find a specific skill's descriptors**
- Use `RUBRIC_QUICK_REFERENCE.md` - organized by skill name

**Understand how assessments are stored**
- Use `RUBRIC_STORAGE_ANALYSIS.md` Section 3 (Database Schema)

**See how AI uses the rubric**
- Use `RUBRIC_STORAGE_ANALYSIS.md` Section 6 (AI Inference)

**Query assessments by level**
- Use `RUBRIC_QUICK_REFERENCE.md` Section "Quick Database Queries"

**Understand the data flow**
- Use `RUBRIC_STORAGE_ANALYSIS.md` Section 7 (Data Flow)

**Add a new skill version**
- Use `RUBRIC_STORAGE_ANALYSIS.md` Section 12 (Versioning)

**Create a new assessment endpoint**
- Use `RUBRIC_STORAGE_ANALYSIS.md` Section 8 (API Endpoints)

---

## Version History

| Version | Date | Status | Notes |
|---|---|---|---|
| 1.0 | Nov 10, 2025 | Current | Initial rubric implementation |

---

## Related Documentation

- `PROJECT_STATUS.md` - Overall project status
- `COMPLETION_SUMMARY.md` - Feature completion checklist
- `DASHBOARD_ACCESS.md` - User interface guide
- `QUICK_START.md` - Setup and deployment guide

---

## Quick Stats

- **Total Skills:** 17
- **Proficiency Levels:** 4 (E, D, P, A)
- **Skill Categories:** 3 (SEL, EF, 21st Century)
- **Total Descriptors:** 68 (17 × 4)
- **Badge Types:** 3 (Bronze, Silver, Gold)
- **Database Tables:** 4 (assessments, corrections, targets, badges)
- **API Endpoints:** 5+ (assessments, corrections, badges)

---

## Document Change Log

| File | Created | Last Updated | Reason |
|---|---|---|---|
| RUBRIC.md | Nov 10 | Nov 10 | Initial creation |
| CURRICULUM.md | Nov 10 | Nov 10 | Initial creation |
| RUBRIC_STORAGE_ANALYSIS.md | Nov 11 | Nov 11 | Comprehensive documentation |
| RUBRIC_QUICK_REFERENCE.md | Nov 11 | Nov 11 | Quick lookup guide |
| RUBRIC_DOCUMENTATION_INDEX.md | Nov 11 | Nov 11 | Navigation guide |

