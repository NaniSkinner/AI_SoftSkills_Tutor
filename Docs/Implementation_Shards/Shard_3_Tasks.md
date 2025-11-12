# Shard 3 Tasks: AI Inference Pipeline

**Status:** ✅ Completed
**Priority:** P0 (Critical Path)
**Dependencies:** Shard 1 (Database)

---

## Overview

Build the GPT-4o powered inference engine that analyzes student data and generates skill assessments based on the rubric. Implement heuristic confidence scoring, few-shot learning integration, and modular prompt management.

---

## Prerequisites Checklist

- [x] Shard 1 completed (Database & Infrastructure running)
- [x] OpenAI API key configured in `.env`
- [x] Docs/Rubric.md exists and is complete
- [x] Docs/Curriculum.md exists and is complete
- [x] Python environment set up with required packages
- [x] Understanding of 17 skills and 4 proficiency levels

---

## Tasks

### 1. AI Module Structure Setup

- [x] Create `backend/ai/` directory (if not exists)

- [x] Create Python `__init__.py` files
  - [x] `backend/ai/__init__.py`

---

### 2. Rubric Loader Module

- [x] Create `backend/ai/rubric_loader.py` file

#### 2.1 Load Rubric Function
- [x] Import `os` module
- [x] Write `load_rubric()` function
  - [x] Construct path to `Docs/Rubric.md` using relative path
  - [x] Open file in read mode with UTF-8 encoding
  - [x] Read full content
  - [x] Return rubric string
  - [x] Add error handling for FileNotFoundError

#### 2.2 Load Curriculum Function
- [x] Write `load_curriculum_context()` function
  - [x] Construct path to `Docs/Curriculum.md`
  - [x] Open file in read mode
  - [x] Read full content
  - [x] Return curriculum string
  - [x] Add error handling for FileNotFoundError

#### 2.3 Testing
- [x] Add docstrings to both functions
- [x] Test rubric loader returns non-empty string
- [x] Test curriculum loader returns non-empty string
- [x] Verify paths work from different execution contexts

---

### 3. System Prompt Builder Module

- [x] Create `backend/ai/prompts.py` file

#### 3.1 System Prompt Template
- [x] Define `SYSTEM_PROMPT_TEMPLATE` constant as multi-line string
  - [x] Add "Expert Educational Assessor" role description
  - [x] Add "YOUR ROLE" section with 5 principles
  - [x] Add "THE 17 SKILLS YOU ASSESS" section
    - [x] List all 5 SEL skills with numbers
    - [x] List all 6 EF skills with numbers
    - [x] List all 6 21st Century skills with numbers
  - [x] Add "PROFICIENCY LEVELS" section
    - [x] Define Emerging (E) with description
    - [x] Define Developing (D) with description
    - [x] Define Proficient (P) with description
    - [x] Define Advanced (A) with description
  - [x] Add "COMPLETE RUBRIC" section with `{rubric_content}` placeholder
  - [x] Add "ASSESSMENT RULES" section with 7 numbered rules
    - [x] Rule 1: Evidence-Based requirement
    - [x] Rule 2: Specific Skill Focus
    - [x] Rule 3: Level Justification
    - [x] Rule 4: Quote Selection
    - [x] Rule 5: No Assumptions
    - [x] Rule 6: Kind Language
    - [x] Rule 7: Confidence Threshold
  - [x] Add "OUTPUT FORMAT" section
    - [x] Show JSON array structure with example assessment
    - [x] Include all required fields: skill_name, skill_category, level, justification, source_quote, data_point_count
  - [x] Add `{few_shot_examples}` placeholder
  - [x] Add closing instruction for analyzing data

#### 3.2 Few-Shot Section Builder
- [x] Write `build_few_shot_section(examples: list) -> str` function
  - [x] Check if examples list is empty, return empty string if so
  - [x] Create section header "FEW-SHOT LEARNING EXAMPLES"
  - [x] Add explanatory text about validated examples
  - [x] Loop through examples with enumeration
    - [x] Format each example with skill_name, level, justification, source_quote, teacher_notes
    - [x] Add clear separation between examples
  - [x] Return formatted section string
  - [x] Add docstring explaining function purpose

#### 3.3 User Prompt Builder
- [x] Write `build_user_prompt(data_entry: dict) -> str` function
  - [x] Create "STUDENT DATA TO ANALYZE" header
  - [x] Extract and display Type from metadata
  - [x] Extract and display Date from metadata
  - [x] Extract and display Context from metadata (with N/A fallback)
  - [x] Display full Content from data_entry
  - [x] Add separator line
  - [x] Add instruction to return JSON array only
  - [x] Return formatted prompt string
  - [x] Add docstring with parameter explanation

---

### 4. Confidence Scoring Module

- [x] Create `backend/ai/confidence_scoring.py` file

#### 4.1 Confidence Calculation Function
- [x] Write `calculate_confidence_score(data_entry: dict, assessment: dict) -> float` function
  - [x] Add comprehensive docstring explaining factors
  - [x] Initialize base confidence at 0.5

#### 4.2 Factor 1: Quote Length
- [x] Get source_quote from assessment (with empty string fallback)
- [x] Count words in quote using split()
- [x] Add 0.15 if quote length >= 20 words
- [x] Add 0.10 if quote length >= 10 words (elif)
- [x] Add comment explaining this factor

#### 4.3 Factor 2: Rubric Keyword Matching
- [x] Get justification from assessment, convert to lowercase
- [x] Define rubric_keywords list with 8 keywords:
  - [x] 'independently'
  - [x] 'consistently'
  - [x] 'with prompting'
  - [x] 'with support'
  - [x] 'beginning to'
  - [x] 'developing'
  - [x] 'demonstrates'
  - [x] 'applies'
- [x] Count keyword matches in justification
- [x] Add min(keyword_matches * 0.05, 0.15) to confidence
- [x] Add comment explaining keyword matching

#### 4.4 Factor 3: Data Entry Completeness
- [x] Get content from data_entry, count words
- [x] Add 0.10 if content length > 200 words
- [x] Add 0.05 if content length > 100 words (elif)
- [x] Add comment explaining completeness factor

#### 4.5 Factor 4: Historical Data Points
- [x] Get data_point_count from assessment (default 1)
- [x] Add 0.10 if data_point_count >= 3
- [x] Add comment explaining historical data factor

#### 4.6 Finalization
- [x] Return min(confidence, 1.0) to cap at 1.0
- [x] Test function with sample data
- [x] Verify all confidence scores are between 0.5 and 1.0

---

### 5. Few-Shot Manager Module

- [x] Create `backend/ai/few_shot_manager.py` file

#### 5.1 Imports and Setup
- [x] Import `typing.List`, `typing.Dict`
- [x] Import `sys`, `os` for path manipulation
- [x] Add parent directory to sys.path
- [x] Import `get_db_connection` from database.connection

#### 5.2 FewShotManager Class
- [x] Create `FewShotManager` class
- [x] Add class docstring

#### 5.3 Get Recent Corrections Method
- [x] Write `get_recent_corrections(self, skill_name: str = None, limit: int = 5) -> List[Dict]` method
  - [x] Add comprehensive docstring with Args and Returns
  - [x] Get database connection
  - [x] Create cursor with RealDictCursor

#### 5.4 SQL Query Construction
- [x] Write base SQL query:
  - [x] SELECT skill_name from assessments
  - [x] SELECT skill_category from assessments
  - [x] SELECT corrected_level from teacher_corrections
  - [x] SELECT corrected_justification from teacher_corrections
  - [x] SELECT source_quote from assessments
  - [x] SELECT teacher_notes from teacher_corrections
  - [x] JOIN teacher_corrections to assessments on assessment_id
  - [x] WHERE teacher_notes IS NOT NULL

- [x] Add conditional skill_name filter
  - [x] If skill_name provided, add "AND a.skill_name = %s"
  - [x] Execute with skill_name and limit parameters

- [x] Add else clause for no skill filter
  - [x] Execute with limit parameter only

- [x] Add ORDER BY corrected_at DESC
- [x] Add LIMIT clause

#### 5.5 Process Results
- [x] Fetch all corrections from cursor
- [x] Close cursor
- [x] Close connection
- [x] Create empty examples list
- [x] Loop through corrections
  - [x] Build dictionary with skill_name, skill_category, level, justification, source_quote, teacher_notes
  - [x] Append to examples list
- [x] Return examples list

#### 5.6 Testing
- [x] Test with empty corrections table (should return empty list)
- [x] Test with specific skill_name filter
- [x] Test limit parameter works correctly

---

### 6. Inference Engine Module

- [x] Create `backend/ai/inference_engine.py` file

#### 6.1 Imports
- [x] Import `openai`
- [x] Import `json`
- [x] Import `os`
- [x] Import `logging`
- [x] Import `typing.List`, `typing.Dict`, `typing.Any`
- [x] Import `SYSTEM_PROMPT_TEMPLATE` from .prompts
- [x] Import `build_few_shot_section` from .prompts
- [x] Import `build_user_prompt` from .prompts
- [x] Import `load_rubric` from .rubric_loader
- [x] Import `calculate_confidence_score` from .confidence_scoring

#### 6.2 Logger Setup
- [x] Create logger with `logging.getLogger(__name__)`

#### 6.3 SkillInferenceEngine Class Definition
- [x] Create `SkillInferenceEngine` class
- [x] Add class docstring: "GPT-4o powered skill assessment engine"

#### 6.4 __init__ Method
- [x] Write `__init__(self, api_key: str, rubric: str, few_shot_examples: List[Dict] = None)` method
  - [x] Initialize `self.client` with `openai.OpenAI(api_key=api_key)`
  - [x] Set `self.model` from environment variable (default "gpt-4o")
  - [x] Store `self.rubric`
  - [x] Store `self.few_shot_examples` (default to empty list if None)

#### 6.5 Assess Skills Method - Signature and Docstring
- [x] Write `assess_skills(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]` method signature
- [x] Add comprehensive docstring
  - [x] Explain method purpose
  - [x] Document Args with example structure
  - [x] Document Returns

#### 6.6 Assess Skills Method - Prompt Building
- [x] Call `self._build_system_prompt()` and store result
- [x] Call `build_user_prompt(student_data)` and store result

#### 6.7 Assess Skills Method - API Call
- [x] Wrap in try-except block
- [x] Call `self.client.chat.completions.create()` with:
  - [x] model=self.model
  - [x] messages array with system and user roles
  - [x] temperature=0.3 (with comment explaining low temperature)
  - [x] max_tokens=4000
  - [x] response_format={"type": "json_object"} (with comment)

#### 6.8 Assess Skills Method - Response Processing
- [x] Extract content from response.choices[0].message.content
- [x] Parse content as JSON with `json.loads()`
- [x] Handle both array and object responses
  - [x] Check if result is dict with 'assessments' key
  - [x] If so, extract assessments array

#### 6.9 Assess Skills Method - Confidence Scoring
- [x] Loop through assessments
  - [x] Check if 'confidence_score' missing or None
  - [x] If so, calculate confidence score
  - [x] Call `calculate_confidence_score(student_data, assessment)`
  - [x] Store result in assessment['confidence_score']

- [x] Log info message with number of assessments generated
- [x] Return assessments list

#### 6.10 Assess Skills Method - Error Handling
- [x] Add `except json.JSONDecodeError as e:` block
  - [x] Log error with exception message
  - [x] Log response content for debugging
  - [x] Return empty list

- [x] Add `except Exception as e:` block
  - [x] Log error with exception message
  - [x] Re-raise exception

#### 6.11 Build System Prompt Method
- [x] Write `_build_system_prompt(self) -> str` private method
  - [x] Add docstring
  - [x] Call `build_few_shot_section()` with last 5 few-shot examples
  - [x] Use slice: `self.few_shot_examples[-5:]`
  - [x] Return formatted SYSTEM_PROMPT_TEMPLATE
  - [x] Pass rubric_content and few_shot_examples as format arguments

---

### 7. AI Module Exports

- [x] Update `backend/ai/__init__.py`
  - [x] Import and export `SkillInferenceEngine`
  - [x] Import and export `load_rubric`
  - [x] Import and export `FewShotManager`
  - [x] Import and export `calculate_confidence_score`

---

### 8. Test Script Creation

- [x] Create `scripts/test_inference.py` file

#### 8.1 Test Script Imports
- [x] Import `sys`, `os` for path manipulation
- [x] Add parent directory to path
- [x] Import `SkillInferenceEngine` from backend.ai
- [x] Import `load_rubric` from backend.ai
- [x] Import `dotenv.load_dotenv`

#### 8.2 Test Script Setup
- [x] Call `load_dotenv()` to load environment variables
- [x] Load rubric using `load_rubric()`
- [x] Get OpenAI API key from environment
- [x] Create SkillInferenceEngine instance

#### 8.3 Test Data Creation
- [x] Create test_data dictionary with:
  - [x] "content" field with sample transcript text (Eva speaking)
  - [x] "metadata" object with type, date, context

#### 8.4 Test Execution
- [x] Call `engine.assess_skills(test_data)`
- [x] Store result in assessments variable
- [x] Print number of assessments generated
- [x] Loop through assessments
  - [x] Print skill_name, level, confidence_score for each
  - [x] Format confidence as 2 decimal places

#### 8.5 Test Validation
- [x] Add assertion: assessments list is not empty
- [x] Add assertion: each assessment has required fields
- [x] Add assertion: confidence scores between 0.5 and 1.0
- [x] Print "✅ Test passed" if all assertions succeed

---

### 9. Integration Testing

#### 9.1 Unit Test: Rubric Loader
- [x] Run test loading rubric from backend container
  ```bash
  docker-compose exec backend python -c "from backend.ai.rubric_loader import load_rubric; print(len(load_rubric()))"
  ```
- [x] Verify output is > 1000 characters
- [x] Verify no error messages

#### 9.2 Unit Test: Confidence Scoring
- [x] Create test script for confidence calculation
- [x] Test with short quote (< 10 words) - expect ~0.6-0.7
- [x] Test with long quote (> 20 words) - expect ~0.8-0.9
- [x] Test with rubric keywords present - expect boost
- [x] Verify scores never exceed 1.0

#### 9.3 Unit Test: Few-Shot Manager
- [x] Test get_recent_corrections() with empty database
- [x] Should return empty list
- [x] Insert test correction into database
- [x] Re-run get_recent_corrections()
- [x] Verify correction appears in results

#### 9.4 Integration Test: Full Inference
- [x] Run `scripts/test_inference.py`
  ```bash
  docker-compose exec backend python scripts/test_inference.py
  ```
- [x] Expected output: 2-4 assessments
- [x] Expected skills: Social Awareness, Relationship Skills, Communication
- [x] Verify each assessment has justification and source_quote
- [x] Verify confidence scores are reasonable (0.7-0.9)

#### 9.5 OpenAI API Test
- [x] Verify API key is valid
- [x] Test with multiple data entry types
  - [x] Group discussion transcript
  - [x] Reflection journal
  - [x] Teacher observation note
- [x] Confirm different data types produce relevant assessments

#### 9.6 Error Handling Test
- [x] Test with malformed data_entry (missing content)
- [x] Verify graceful error handling
- [x] Test with invalid API key
- [x] Verify error logged, exception raised
- [x] Test with very long content (> 10,000 words)
- [x] Verify token limit handling

---

## Testing Checklist

### Module Tests

- [x] Test rubric_loader.py
  ```bash
  docker-compose exec backend python -c "from backend.ai.rubric_loader import load_rubric, load_curriculum_context; print('Rubric:', len(load_rubric())); print('Curriculum:', len(load_curriculum_context()))"
  ```
  - [x] Rubric length > 1000 characters
  - [x] Curriculum length > 500 characters

- [x] Test prompts.py
  ```bash
  docker-compose exec backend python -c "from backend.ai.prompts import SYSTEM_PROMPT_TEMPLATE, build_few_shot_section; print(len(SYSTEM_PROMPT_TEMPLATE)); print(build_few_shot_section([]))"
  ```
  - [x] System prompt template > 2000 characters
  - [x] Empty few-shot section returns empty string

- [x] Test confidence_scoring.py
  ```bash
  docker-compose exec backend python scripts/test_confidence.py
  ```
  - [x] All test cases pass
  - [x] Scores in valid range

- [x] Test few_shot_manager.py
  ```bash
  docker-compose exec backend python -c "from backend.ai.few_shot_manager import FewShotManager; fm = FewShotManager(); print(len(fm.get_recent_corrections()))"
  ```
  - [x] Returns list (empty if no corrections yet)
  - [x] No database errors

### Integration Tests

- [x] Test full inference pipeline
  ```bash
  docker-compose exec backend python scripts/test_inference.py
  ```
  - [x] Assessments generated successfully
  - [x] At least 2 assessments returned
  - [x] Each assessment has all required fields
  - [x] Confidence scores calculated

- [x] Test with each data entry type
  - [x] Group discussion transcript → generates SEL + Collaboration assessments
  - [x] Reflection journal → generates Self-Awareness + Self-Management
  - [x] Teacher observation → generates multiple skill assessments
  - [x] Peer feedback → generates Social Awareness + Relationship Skills
  - [x] Project presentation → generates Communication + Critical Thinking

### Performance Tests

- [x] Measure inference time for single entry
  - [x] Should be < 3 seconds average

- [x] Test with 10 entries in sequence
  - [x] Monitor rate limiting behavior
  - [x] Verify no timeouts

- [x] Check token usage
  - [x] System prompt + user prompt should be < 4000 tokens
  - [x] Response should be < 1000 tokens

### Quality Tests

- [x] Verify assessment quality
  - [x] Justifications reference rubric criteria
  - [x] Source quotes are verbatim from content
  - [x] Levels match observable behaviors
  - [x] Kind, growth-oriented language used

- [x] Test few-shot learning
  - [x] Add 5 teacher corrections to database
  - [x] Run inference on similar data
  - [x] Verify few-shot examples included in prompt
  - [x] Verify assessments improve (closer to corrections)

---

## Acceptance Criteria

- [x] All 5 AI modules created (rubric_loader, prompts, inference_engine, confidence_scoring, few_shot_manager)
- [x] Rubric and curriculum load successfully from Docs/
- [x] System prompt includes all 17 skills and 4 proficiency levels
- [x] GPT-4o API integration functional
- [x] JSON response parsing handles both array and object formats
- [x] Confidence scores calculated for all assessments (range 0.5-1.0)
- [x] Few-shot manager retrieves corrections from database
- [x] Few-shot examples integrated into system prompt (last 5)
- [x] Error handling for malformed LLM responses
- [x] Error handling for database connection issues
- [x] Logging captures inference metrics
- [x] Test script runs successfully
- [x] All unit tests pass
- [x] Integration tests pass
- [x] Assessments include: skill_name, skill_category, level, justification, source_quote, confidence_score

---

## Notes

- Temperature set to 0.3 for consistency (lower temperature = more deterministic)
- Response format enforces JSON output for reliable parsing
- Few-shot learning uses only last 5 corrections to avoid prompt bloat
- Confidence scoring is heuristic (not ML-based) for MVP speed
- Token limits: System prompt ~3000 tokens, max response 4000 tokens
- Rate limiting in ingestion script prevents OpenAI API throttling

**Next Shard:** [Shard 4: Backend API](Shard_4_Tasks.md) (requires this shard complete)
