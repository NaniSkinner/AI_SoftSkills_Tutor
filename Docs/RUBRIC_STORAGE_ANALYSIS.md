# Rubric Storage Architecture - Complete Analysis

## Overview
This document provides a comprehensive analysis of how rubric descriptions and skill proficiency levels are stored and utilized throughout the Flourish Skills Tracker codebase.

---

## 1. PRIMARY RUBRIC STORAGE

### Location: `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/Docs/Rubric.md`

The main rubric is stored as a **markdown file** containing detailed behavioral indicators for all 17 non-academic skills across four proficiency levels.

**File Structure:**
- Total: ~17KB markdown document
- Format: Markdown tables
- Updated: November 10, 2025
- Version: 1.0

**Proficiency Levels Defined:**
```
- Emerging (E):   Needs significant, consistent support; skill application is inconsistent or absent
- Developing (D): Applies the skill with frequent prompting or scaffolding; inconsistent success
- Proficient (P): Applies the skill independently and consistently in familiar contexts; generally successful
- Advanced (A):   Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others
```

### Content Structure (Three Main Rubric Sections):

#### I. Social-Emotional Learning (SEL) - CASEL Framework (5 Skills)
| Core Competency | Skills |
|---|---|
| 1. Self-Awareness | E/D/P/A descriptors for emotional identification, strength/weakness awareness |
| 2. Self-Management | E/D/P/A descriptors for impulse control, stress management, persistence |
| 3. Social Awareness | E/D/P/A descriptors for empathy, perspective-taking, social norm understanding |
| 4. Relationship Skills | E/D/P/A descriptors for communication, active listening, conflict resolution |
| 5. Responsible Decision-Making | E/D/P/A descriptors for consequence evaluation, ethical reasoning, safety |

**Example Entry:**
```
Self-Awareness:
- Emerging (E): Cannot identify or mislabels own emotions; unaware of personal 
                 strengths/weaknesses; blames external factors for feelings.
- Developing (D): Can name basic emotions (happy, sad, angry) when prompted; 
                   can state one or two strengths/weaknesses with guidance.
- Proficient (P): Accurately identifies and articulates a range of complex emotions 
                   (e.g., frustration, anxiety); can describe how emotions affect behavior; 
                   recognizes personal learning style.
- Advanced (A): Reflects on internal states to understand complex motivations; uses 
                 self-knowledge to adjust goals and seek appropriate challenges; 
                 demonstrates metacognition.
```

#### II. Executive Functioning (EF) Rubric (6 Skills)
| Core Skill | Skills |
|---|---|
| 1. Working Memory | E/D/P/A descriptors for multi-step instruction following, information retention |
| 2. Inhibitory Control | E/D/P/A descriptors for distraction resistance, impulse control, focus |
| 3. Cognitive Flexibility | E/D/P/A descriptors for adaptability, perspective-shifting, strategy adjustment |
| 4. Planning & Prioritization | E/D/P/A descriptors for goal-setting, time estimation, task prioritization |
| 5. Organization | E/D/P/A descriptors for material management, workspace organization, note-taking |
| 6. Task Initiation | E/D/P/A descriptors for procrastination avoidance, independent problem-solving |

#### III. 21st Century Skills Rubric (6 Skills)
| Core Skill | Skills |
|---|---|
| 1. Critical Thinking | E/D/P/A descriptors for analysis, bias detection, argument evaluation |
| 2. Communication | E/D/P/A descriptors for clarity, audience adaptation, written/oral expression |
| 3. Collaboration | E/D/P/A descriptors for teamwork, idea integration, shared responsibility |
| 4. Creativity & Innovation | E/D/P/A descriptors for idea generation, elaboration, creative risk-taking |
| 5. Digital Literacy | E/D/P/A descriptors for technology use, file management, online safety |
| 6. Global Awareness | E/D/P/A descriptors for cross-cultural competence, global issue understanding |

---

## 2. CURRICULUM CONTEXT DOCUMENT

### Location: `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/Docs/Curriculum.md`

**File Size:** ~25KB markdown document
**Updated:** November 10, 2025

**Purpose:** Provides context and rationale for why each skill is important for middle school students, developmental appropriateness research, and global implementation examples.

**Content Structure:**
- Section I: Developmental Appropriateness (adolescent brain development, sensitive periods)
- Section II: SEL Skills (definitions and rationale)
- Section III: Executive Functioning Skills (definitions and rationale)
- Section IV: 21st Century Skills (definitions and rationale)
- Section V: LLM Context Engineering Notes

---

## 3. DATABASE SCHEMA STORAGE

### Location: `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/database/init.sql`

**Database Type:** PostgreSQL

### Key Assessment-Related Tables:

#### A. ASSESSMENTS TABLE
```sql
CREATE TABLE assessments (
    id SERIAL PRIMARY KEY,
    data_entry_id VARCHAR(20) REFERENCES data_entries(id) ON DELETE CASCADE,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,           -- Exact skill name from 17 skills
    skill_category VARCHAR(50) NOT NULL,        -- 'SEL', 'EF', or '21st Century'
    level VARCHAR(20) NOT NULL,                 -- 'Emerging', 'Developing', 'Proficient', 'Advanced'
    confidence_score DECIMAL(3,2),              -- 0.50 to 1.00
    justification TEXT NOT NULL,                -- LLM-generated explanation
    source_quote TEXT NOT NULL,                 -- Verbatim quote from student data
    data_point_count INTEGER DEFAULT 1,
    rubric_version VARCHAR(10) DEFAULT '1.0',   -- Rubric version tracking
    corrected BOOLEAN DEFAULT FALSE,            -- Whether teacher has corrected this
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_assessments_student_skill ON assessments(student_id, skill_name);
CREATE INDEX idx_assessments_level ON assessments(level);
CREATE INDEX idx_assessments_pending ON assessments(student_id, created_at) 
    WHERE corrected = FALSE;
```

**Critical Fields:**
- `skill_name`: Stores the exact name from the 17-skill list (e.g., "Social Awareness", "Task Initiation")
- `skill_category`: Groups skills into SEL, EF, or 21st Century
- `level`: Stores full level names (Emerging, Developing, Proficient, Advanced)
- `justification`: LLM-generated explanation of why this level was assigned
- `rubric_version`: Allows tracking which rubric version was used (for future updates)

#### B. TEACHER_CORRECTIONS TABLE
```sql
CREATE TABLE teacher_corrections (
    id SERIAL PRIMARY KEY,
    assessment_id INTEGER REFERENCES assessments(id) ON DELETE CASCADE,
    original_level VARCHAR(20) NOT NULL,
    corrected_level VARCHAR(20) NOT NULL,       -- Corrected proficiency level
    original_justification TEXT,
    corrected_justification TEXT,               -- Teacher's corrected explanation
    teacher_notes TEXT,                         -- Additional context for few-shot learning
    corrected_by VARCHAR(10) REFERENCES teachers(id),
    corrected_at TIMESTAMP DEFAULT NOW()
);
```

**Purpose:** Stores teacher corrections for few-shot learning refinement

#### C. SKILL_TARGETS TABLE
```sql
CREATE TABLE skill_targets (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(10) REFERENCES students(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,           -- Target skill
    starting_level VARCHAR(20),                 -- Current level (E, D, P, A)
    target_level VARCHAR(20),                   -- Goal level (D, P, A)
    assigned_by VARCHAR(10) REFERENCES teachers(id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    UNIQUE (student_id, skill_name, completed)
);
```

**Purpose:** Tracks which proficiency levels students are targeting

#### D. BADGES TABLE
```sql
CREATE TABLE badges (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(10),
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(50) NOT NULL,
    level_achieved VARCHAR(20) NOT NULL,       -- D, P, or A (no Emerging badges)
    badge_type VARCHAR(20) NOT NULL,           -- 'bronze' (D), 'silver' (P), 'gold' (A)
    granted_by VARCHAR(10),
    earned_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (student_id, skill_name, level_achieved)
);
```

**Badge Mapping:**
- Bronze = Developing (D)
- Silver = Proficient (P)
- Gold = Advanced (A)

---

## 4. PYTHON MODEL SCHEMAS

### Location: `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/models/schemas.py`

**Pydantic Models for API Validation:**

#### AssessmentResponse Schema
```python
class AssessmentResponse(BaseModel):
    id: int
    data_entry_id: str
    student_id: str
    skill_name: str                    # From the 17-skill list
    skill_category: str                # 'SEL', 'EF', '21st Century'
    level: str                         # 'Emerging', 'Developing', 'Proficient', 'Advanced'
    confidence_score: float            # 0.5 to 1.0
    justification: str                 # LLM's explanation
    source_quote: str                  # Evidence from student data
    data_point_count: int
    rubric_version: str
    corrected: bool
    created_at: str
```

#### CorrectionRequest Schema
```python
class CorrectionRequest(BaseModel):
    assessment_id: int
    corrected_level: str              # Accepts 'E', 'D', 'P', 'A' or full names
    corrected_justification: Optional[str]
    teacher_notes: Optional[str]
    corrected_by: str
    
    # Validation: Normalizes to full level names
    level_map = {'E': 'Emerging', 'D': 'Developing', 'P': 'Proficient', 'A': 'Advanced'}
```

#### TargetAssignmentRequest Schema
```python
class TargetAssignmentRequest(BaseModel):
    student_id: str
    skill_name: str
    starting_level: str               # Must be one of the 4 levels
    target_level: str                 # Must be one of the 4 levels
    assigned_by: str
    
    # Validation ensures: Emerging, Developing, Proficient, or Advanced
```

---

## 5. RUBRIC LOADING & INJECTION

### Location: `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/ai/rubric_loader.py`

**Purpose:** Loads the markdown rubric into memory for AI prompt engineering

```python
def load_rubric() -> str:
    """
    Load the skill rubric from Docs/Rubric.md
    
    Returns:
        str: The complete rubric content as a string
        
    Behavior:
    - Tries Docker path first: /app/Docs/Rubric.md
    - Falls back to local dev path: Docs/Rubric.md
    """
    rubric_path = os.path.join(project_root, 'Docs', 'Rubric.md')
    with open(rubric_path, 'r', encoding='utf-8') as f:
        rubric_content = f.read()
    return rubric_content
```

**Usage:**
The rubric is loaded once during the data ingestion process and injected into the GPT-4o system prompt.

---

## 6. AI INFERENCE ENGINE & PROMPT ENGINEERING

### Location: `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/ai/`

#### A. System Prompt Template (`prompts.py`)

**Key Components:**
1. **Role Definition:** "Expert Educational Assessor specializing in middle school non-academic skills assessment"
2. **17 Skills Listed:** Complete enumeration of all 17 skills with categories
3. **Proficiency Level Definitions:** Embedded definitions for E, D, P, A
4. **Complete Rubric Injection:** `{rubric_content}` placeholder filled with full Rubric.md content
5. **Assessment Rules:** Evidence-based, specific skill focus, level justification
6. **Output Format Requirements:** Enforces JSON structure with specific fields

**Example System Prompt Section:**
```
PROFICIENCY LEVELS:
- **Emerging (E):** Needs significant, consistent support; skill application is inconsistent or absent
- **Developing (D):** Applies the skill with frequent prompting or scaffolding; inconsistent success
- **Proficient (P):** Applies the skill independently and consistently in familiar contexts; generally successful
- **Advanced (A):** Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others

COMPLETE RUBRIC:
[FULL RUBRIC.MD CONTENT INJECTED HERE]

ASSESSMENT RULES:
1. **Evidence-Based:** Only assess a skill if there is clear, observable evidence in the student data
2. **Specific Skill Focus:** Match behavior to the most specific skill
3. **Level Justification:** Explain WHY the student is at this level using rubric criteria and observable behaviors
[... more rules ...]
```

#### B. Few-Shot Learning (`few_shot_manager.py`)

**Purpose:** Use teacher-corrected assessments to improve AI accuracy

```python
class FewShotManager:
    def get_recent_corrections(self, skill_name: str = None, limit: int = 5) -> List[Dict]:
        """
        Retrieve recent teacher-corrected assessments for few-shot learning
        
        Returns:
        [
            {
                'skill_name': 'Social Awareness',
                'skill_category': 'SEL',
                'level': 'Proficient',
                'justification': 'Student accurately interpreted subtle emotional cues...',
                'source_quote': 'I could tell Marcus was feeling left out so I asked...',
                'teacher_notes': 'Good evidence but level should be Proficient'
            },
            ...
        ]
        """
```

**Few-Shot Examples Included:** Up to 5 most recent corrections are appended to system prompt

#### C. Confidence Scoring (`confidence_scoring.py`)

**Calculation Factors:**
```python
def calculate_confidence_score(data_entry, assessment) -> float:
    # Base: 0.5
    # Factor 1: Quote Length (up to +0.15)
    # Factor 2: Rubric Keyword Matching (up to +0.15)
    # Factor 3: Data Entry Completeness (up to +0.10)
    # Factor 4: Historical Data Points (up to +0.10)
    # Result: Capped at 1.0
```

**Keywords Monitored:**
- 'independently', 'consistently', 'with prompting', 'with support'
- 'beginning to', 'developing', 'demonstrates', 'applies'

---

## 7. DATA FLOW ARCHITECTURE

### Data Ingestion to Assessment Storage

```
1. Teacher/Frontend submits StudentData
   ↓
2. Data Ingestion Router (/api/data/ingest)
   ├─ Validates DataEntryRequest
   ├─ Stores in data_entries table
   ├─ Commits to database
   ↓
3. Load Rubric & Few-Shot Examples
   ├─ rubric_loader.load_rubric() → reads Rubric.md
   ├─ FewShotManager.get_recent_corrections() → queries teacher_corrections table
   ↓
4. Build System Prompt
   ├─ SYSTEM_PROMPT_TEMPLATE
   ├─ Inject rubric_content
   ├─ Append few_shot_examples
   ├─ Build user_prompt from student data
   ↓
5. GPT-4o Inference (SkillInferenceEngine)
   ├─ Send system_prompt + user_prompt
   ├─ Model: gpt-4o (temperature: 0.3 for consistency)
   ├─ Enforce JSON output
   ↓
6. Parse & Score Results
   ├─ JSON validation
   ├─ Calculate confidence_score for each assessment
   ↓
7. Store Assessments
   ├─ INSERT INTO assessments table
   ├─ Fields: skill_name, skill_category, level, confidence_score, 
              justification, source_quote, rubric_version
   ↓
8. Return Assessment IDs to Frontend
```

---

## 8. API ENDPOINTS FOR RUBRIC-RELATED DATA

### Assessment Retrieval Endpoints

#### `GET /api/assessments/student/{student_id}`
Returns all assessments with proficiency levels, justifications, and evidence

**Response Structure:**
```json
[
  {
    "id": 1,
    "skill_name": "Social Awareness",
    "skill_category": "SEL",
    "level": "Proficient",
    "confidence_score": 0.85,
    "justification": "Student accurately interpreted subtle emotional cues...",
    "source_quote": "I could tell Marcus was feeling left out...",
    "rubric_version": "1.0",
    "created_at": "2025-11-10T14:32:00"
  }
]
```

#### `GET /api/assessments/skill-trends/{student_id}`
Groups assessments by skill with level progression

**Response Structure:**
```json
[
  {
    "skill_name": "Social Awareness",
    "skill_category": "SEL",
    "assessments": [
      {
        "date": "2025-08-15",
        "level": "Developing",
        "level_numeric": 2,
        "confidence": 0.75
      },
      {
        "date": "2025-09-20",
        "level": "Proficient",
        "level_numeric": 3,
        "confidence": 0.85
      }
    ]
  }
]
```

**Level Numeric Mapping:**
- 1 = Emerging
- 2 = Developing
- 3 = Proficient
- 4 = Advanced

#### `GET /api/assessments/pending`
Returns uncorrected assessments needing teacher review (sorted by lowest confidence first)

### Correction Endpoints

#### `POST /api/corrections/submit`
Teacher submits correction with updated level and justification

**Request:**
```json
{
  "assessment_id": 1,
  "corrected_level": "Advanced",
  "corrected_justification": "Student demonstrates advanced social awareness...",
  "teacher_notes": "Excellent interpretation of group dynamics",
  "corrected_by": "T001"
}
```

**Response:**
```json
{
  "success": true,
  "correction_id": 42,
  "message": "Assessment corrected successfully"
}
```

---

## 9. SKILL ENUMERATION (17 SKILLS)

### Complete List Stored in Database

#### Social-Emotional Learning (5 Skills)
1. Self-Awareness
2. Self-Management
3. Social Awareness
4. Relationship Skills
5. Responsible Decision-Making

#### Executive Functioning (6 Skills)
6. Working Memory
7. Inhibitory Control
8. Cognitive Flexibility
9. Planning & Prioritization
10. Organization
11. Task Initiation

#### 21st Century Skills (6 Skills)
12. Critical Thinking
13. Communication
14. Collaboration
15. Creativity & Innovation
16. Digital Literacy
17. Global Awareness

---

## 10. EXAMPLE RUBRIC ENTRIES (EXACT TEXT)

### Example 1: Self-Awareness (SEL)

**Emerging (E):**
"Cannot identify or mislabels own emotions; unaware of personal strengths/weaknesses; blames external factors for feelings."

**Developing (D):**
"Can name basic emotions (happy, sad, angry) when prompted; can state one or two strengths/weaknesses with guidance."

**Proficient (P):**
"Accurately identifies and articulates a range of complex emotions (e.g., frustration, anxiety); can describe how emotions affect behavior; recognizes personal learning style."

**Advanced (A):**
"Reflects on internal states to understand complex motivations; uses self-knowledge to adjust goals and seek appropriate challenges; demonstrates metacognition."

### Example 2: Planning & Prioritization (EF)

**Emerging (E):**
"Starts tasks without a plan; estimates time inaccurately; treats all tasks as equally important; misses deadlines frequently."

**Developing (D):**
"Creates simple, linear plans when directed; can prioritize 2-3 tasks with adult guidance; needs help breaking down large projects."

**Proficient (P):**
"Independently creates detailed, multi-step plans for long-term projects; accurately estimates time needed for tasks; prioritizes tasks based on urgency and importance."

**Advanced (A):**
"Develops contingency plans; manages multiple long-term projects simultaneously; allocates resources (time, materials) strategically for maximum efficiency."

### Example 3: Critical Thinking (21st Century)

**Emerging (E):**
"Accepts information at face value; struggles to distinguish fact from opinion; cannot identify flaws in simple arguments."

**Developing (D):**
"Can identify basic facts and opinions; questions information when prompted; can identify one or two simple biases in a source."

**Proficient (P):**
"Systematically analyzes information from multiple sources; evaluates the credibility of sources; constructs well-reasoned arguments supported by evidence."

**Advanced (A):**
"Synthesizes complex, conflicting information to form original insights; develops and tests hypotheses; identifies and challenges underlying assumptions in complex problems."

---

## 11. FRONTEND INTEGRATION

### Streamlit Dashboard Pages Using Rubric Data

#### Student Overview Page
- Displays current proficiency levels for all assessed skills
- Shows badge achievement (Bronze/Silver/Gold = D/P/A)
- Displays progress toward target levels

#### Skill Trends Page
- Charts skill progression over time
- Shows level changes (1→4 numeric scale)
- Compares with class/cohort trends

#### Assessment Review Page (Teacher)
- Displays AI-generated assessments with justifications
- Shows source quotes from student data
- Allows teacher to approve or correct
- Correction feedback feeds into few-shot learning

---

## 12. VERSIONING & FUTURE UPDATES

**Current Version:** 1.0 (stored in database `rubric_version` field)

**Update Path:**
1. New Rubric.md version created in Docs/
2. Schema can support multiple rubric versions
3. New assessments generated with new version number
4. Historical assessments maintain version reference for audit trail

---

## 13. KEY SEARCH PATTERNS

**Find all references to rubric data:**
- Pattern: `skill_name` (exact skill from 17-skill list)
- Pattern: `level` (Emerging/Developing/Proficient/Advanced)
- Pattern: `skill_category` (SEL/EF/21st Century)
- Pattern: `rubric_version` (version tracking)

---

## Summary

**Rubric Storage Architecture:**
1. **Markdown Files:** Docs/Rubric.md (descriptions), Docs/Curriculum.md (context)
2. **Database:** PostgreSQL tables (assessments, corrections, targets, badges)
3. **Python Models:** Pydantic schemas with validation
4. **AI Injection:** Loaded into GPT-4o system prompts
5. **API Layer:** REST endpoints for retrieval, update, and correction
6. **Versioning:** Support for multiple rubric versions (1.0+)

**Key Files:**
- `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/Docs/Rubric.md` (MAIN SOURCE)
- `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/database/init.sql` (SCHEMA)
- `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/models/schemas.py` (VALIDATION)
- `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/ai/rubric_loader.py` (LOADER)
- `/Users/nanis/dev/Gauntlet/AI_MS_SoftSkills/backend/ai/prompts.py` (INJECTION)
