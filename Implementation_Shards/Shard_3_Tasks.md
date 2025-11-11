# Shard 3 Tasks: AI Inference Pipeline

**Status:** 🔴 Not Started
**Priority:** P0 (Critical Path)
**Dependencies:** Shard 1 (Database)

---

## Overview

Build the GPT-4o powered inference engine that analyzes student data and generates skill assessments based on the rubric. Implement heuristic confidence scoring, few-shot learning integration, and modular prompt management.

---

## Prerequisites Checklist

- [ ] Shard 1 completed (Database & Infrastructure running)
- [ ] OpenAI API key configured in `.env`
- [ ] Docs/Rubric.md exists and is complete
- [ ] Docs/Curriculum.md exists and is complete
- [ ] Python environment set up with required packages
- [ ] Understanding of 17 skills and 4 proficiency levels

---

## Tasks

### 1. AI Module Structure Setup

- [ ] Create `backend/ai/` directory (if not exists)

- [ ] Create Python `__init__.py` files
  - [ ] `backend/ai/__init__.py`

---

### 2. Rubric Loader Module

- [ ] Create `backend/ai/rubric_loader.py` file

#### 2.1 Load Rubric Function
- [ ] Import `os` module
- [ ] Write `load_rubric()` function
  - [ ] Construct path to `Docs/Rubric.md` using relative path
  - [ ] Open file in read mode with UTF-8 encoding
  - [ ] Read full content
  - [ ] Return rubric string
  - [ ] Add error handling for FileNotFoundError

#### 2.2 Load Curriculum Function
- [ ] Write `load_curriculum_context()` function
  - [ ] Construct path to `Docs/Curriculum.md`
  - [ ] Open file in read mode
  - [ ] Read full content
  - [ ] Return curriculum string
  - [ ] Add error handling for FileNotFoundError

#### 2.3 Testing
- [ ] Add docstrings to both functions
- [ ] Test rubric loader returns non-empty string
- [ ] Test curriculum loader returns non-empty string
- [ ] Verify paths work from different execution contexts

---

### 3. System Prompt Builder Module

- [ ] Create `backend/ai/prompts.py` file

#### 3.1 System Prompt Template
- [ ] Define `SYSTEM_PROMPT_TEMPLATE` constant as multi-line string
  - [ ] Add "Expert Educational Assessor" role description
  - [ ] Add "YOUR ROLE" section with 5 principles
  - [ ] Add "THE 17 SKILLS YOU ASSESS" section
    - [ ] List all 5 SEL skills with numbers
    - [ ] List all 6 EF skills with numbers
    - [ ] List all 6 21st Century skills with numbers
  - [ ] Add "PROFICIENCY LEVELS" section
    - [ ] Define Emerging (E) with description
    - [ ] Define Developing (D) with description
    - [ ] Define Proficient (P) with description
    - [ ] Define Advanced (A) with description
  - [ ] Add "COMPLETE RUBRIC" section with `{rubric_content}` placeholder
  - [ ] Add "ASSESSMENT RULES" section with 7 numbered rules
    - [ ] Rule 1: Evidence-Based requirement
    - [ ] Rule 2: Specific Skill Focus
    - [ ] Rule 3: Level Justification
    - [ ] Rule 4: Quote Selection
    - [ ] Rule 5: No Assumptions
    - [ ] Rule 6: Kind Language
    - [ ] Rule 7: Confidence Threshold
  - [ ] Add "OUTPUT FORMAT" section
    - [ ] Show JSON array structure with example assessment
    - [ ] Include all required fields: skill_name, skill_category, level, justification, source_quote, data_point_count
  - [ ] Add `{few_shot_examples}` placeholder
  - [ ] Add closing instruction for analyzing data

#### 3.2 Few-Shot Section Builder
- [ ] Write `build_few_shot_section(examples: list) -> str` function
  - [ ] Check if examples list is empty, return empty string if so
  - [ ] Create section header "FEW-SHOT LEARNING EXAMPLES"
  - [ ] Add explanatory text about validated examples
  - [ ] Loop through examples with enumeration
    - [ ] Format each example with skill_name, level, justification, source_quote, teacher_notes
    - [ ] Add clear separation between examples
  - [ ] Return formatted section string
  - [ ] Add docstring explaining function purpose

#### 3.3 User Prompt Builder
- [ ] Write `build_user_prompt(data_entry: dict) -> str` function
  - [ ] Create "STUDENT DATA TO ANALYZE" header
  - [ ] Extract and display Type from metadata
  - [ ] Extract and display Date from metadata
  - [ ] Extract and display Context from metadata (with N/A fallback)
  - [ ] Display full Content from data_entry
  - [ ] Add separator line
  - [ ] Add instruction to return JSON array only
  - [ ] Return formatted prompt string
  - [ ] Add docstring with parameter explanation

---

### 4. Confidence Scoring Module

- [ ] Create `backend/ai/confidence_scoring.py` file

#### 4.1 Confidence Calculation Function
- [ ] Write `calculate_confidence_score(data_entry: dict, assessment: dict) -> float` function
  - [ ] Add comprehensive docstring explaining factors
  - [ ] Initialize base confidence at 0.5

#### 4.2 Factor 1: Quote Length
- [ ] Get source_quote from assessment (with empty string fallback)
- [ ] Count words in quote using split()
- [ ] Add 0.15 if quote length >= 20 words
- [ ] Add 0.10 if quote length >= 10 words (elif)
- [ ] Add comment explaining this factor

#### 4.3 Factor 2: Rubric Keyword Matching
- [ ] Get justification from assessment, convert to lowercase
- [ ] Define rubric_keywords list with 8 keywords:
  - [ ] 'independently'
  - [ ] 'consistently'
  - [ ] 'with prompting'
  - [ ] 'with support'
  - [ ] 'beginning to'
  - [ ] 'developing'
  - [ ] 'demonstrates'
  - [ ] 'applies'
- [ ] Count keyword matches in justification
- [ ] Add min(keyword_matches * 0.05, 0.15) to confidence
- [ ] Add comment explaining keyword matching

#### 4.4 Factor 3: Data Entry Completeness
- [ ] Get content from data_entry, count words
- [ ] Add 0.10 if content length > 200 words
- [ ] Add 0.05 if content length > 100 words (elif)
- [ ] Add comment explaining completeness factor

#### 4.5 Factor 4: Historical Data Points
- [ ] Get data_point_count from assessment (default 1)
- [ ] Add 0.10 if data_point_count >= 3
- [ ] Add comment explaining historical data factor

#### 4.6 Finalization
- [ ] Return min(confidence, 1.0) to cap at 1.0
- [ ] Test function with sample data
- [ ] Verify all confidence scores are between 0.5 and 1.0

---

### 5. Few-Shot Manager Module

- [ ] Create `backend/ai/few_shot_manager.py` file

#### 5.1 Imports and Setup
- [ ] Import `typing.List`, `typing.Dict`
- [ ] Import `sys`, `os` for path manipulation
- [ ] Add parent directory to sys.path
- [ ] Import `get_db_connection` from database.connection

#### 5.2 FewShotManager Class
- [ ] Create `FewShotManager` class
- [ ] Add class docstring

#### 5.3 Get Recent Corrections Method
- [ ] Write `get_recent_corrections(self, skill_name: str = None, limit: int = 5) -> List[Dict]` method
  - [ ] Add comprehensive docstring with Args and Returns
  - [ ] Get database connection
  - [ ] Create cursor with RealDictCursor

#### 5.4 SQL Query Construction
- [ ] Write base SQL query:
  - [ ] SELECT skill_name from assessments
  - [ ] SELECT skill_category from assessments
  - [ ] SELECT corrected_level from teacher_corrections
  - [ ] SELECT corrected_justification from teacher_corrections
  - [ ] SELECT source_quote from assessments
  - [ ] SELECT teacher_notes from teacher_corrections
  - [ ] JOIN teacher_corrections to assessments on assessment_id
  - [ ] WHERE teacher_notes IS NOT NULL

- [ ] Add conditional skill_name filter
  - [ ] If skill_name provided, add "AND a.skill_name = %s"
  - [ ] Execute with skill_name and limit parameters

- [ ] Add else clause for no skill filter
  - [ ] Execute with limit parameter only

- [ ] Add ORDER BY corrected_at DESC
- [ ] Add LIMIT clause

#### 5.5 Process Results
- [ ] Fetch all corrections from cursor
- [ ] Close cursor
- [ ] Close connection
- [ ] Create empty examples list
- [ ] Loop through corrections
  - [ ] Build dictionary with skill_name, skill_category, level, justification, source_quote, teacher_notes
  - [ ] Append to examples list
- [ ] Return examples list

#### 5.6 Testing
- [ ] Test with empty corrections table (should return empty list)
- [ ] Test with specific skill_name filter
- [ ] Test limit parameter works correctly

---

### 6. Inference Engine Module

- [ ] Create `backend/ai/inference_engine.py` file

#### 6.1 Imports
- [ ] Import `openai`
- [ ] Import `json`
- [ ] Import `os`
- [ ] Import `logging`
- [ ] Import `typing.List`, `typing.Dict`, `typing.Any`
- [ ] Import `SYSTEM_PROMPT_TEMPLATE` from .prompts
- [ ] Import `build_few_shot_section` from .prompts
- [ ] Import `build_user_prompt` from .prompts
- [ ] Import `load_rubric` from .rubric_loader
- [ ] Import `calculate_confidence_score` from .confidence_scoring

#### 6.2 Logger Setup
- [ ] Create logger with `logging.getLogger(__name__)`

#### 6.3 SkillInferenceEngine Class Definition
- [ ] Create `SkillInferenceEngine` class
- [ ] Add class docstring: "GPT-4o powered skill assessment engine"

#### 6.4 __init__ Method
- [ ] Write `__init__(self, api_key: str, rubric: str, few_shot_examples: List[Dict] = None)` method
  - [ ] Initialize `self.client` with `openai.OpenAI(api_key=api_key)`
  - [ ] Set `self.model` from environment variable (default "gpt-4o")
  - [ ] Store `self.rubric`
  - [ ] Store `self.few_shot_examples` (default to empty list if None)

#### 6.5 Assess Skills Method - Signature and Docstring
- [ ] Write `assess_skills(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]` method signature
- [ ] Add comprehensive docstring
  - [ ] Explain method purpose
  - [ ] Document Args with example structure
  - [ ] Document Returns

#### 6.6 Assess Skills Method - Prompt Building
- [ ] Call `self._build_system_prompt()` and store result
- [ ] Call `build_user_prompt(student_data)` and store result

#### 6.7 Assess Skills Method - API Call
- [ ] Wrap in try-except block
- [ ] Call `self.client.chat.completions.create()` with:
  - [ ] model=self.model
  - [ ] messages array with system and user roles
  - [ ] temperature=0.3 (with comment explaining low temperature)
  - [ ] max_tokens=4000
  - [ ] response_format={"type": "json_object"} (with comment)

#### 6.8 Assess Skills Method - Response Processing
- [ ] Extract content from response.choices[0].message.content
- [ ] Parse content as JSON with `json.loads()`
- [ ] Handle both array and object responses
  - [ ] Check if result is dict with 'assessments' key
  - [ ] If so, extract assessments array

#### 6.9 Assess Skills Method - Confidence Scoring
- [ ] Loop through assessments
  - [ ] Check if 'confidence_score' missing or None
  - [ ] If so, calculate confidence score
  - [ ] Call `calculate_confidence_score(student_data, assessment)`
  - [ ] Store result in assessment['confidence_score']

- [ ] Log info message with number of assessments generated
- [ ] Return assessments list

#### 6.10 Assess Skills Method - Error Handling
- [ ] Add `except json.JSONDecodeError as e:` block
  - [ ] Log error with exception message
  - [ ] Log response content for debugging
  - [ ] Return empty list

- [ ] Add `except Exception as e:` block
  - [ ] Log error with exception message
  - [ ] Re-raise exception

#### 6.11 Build System Prompt Method
- [ ] Write `_build_system_prompt(self) -> str` private method
  - [ ] Add docstring
  - [ ] Call `build_few_shot_section()` with last 5 few-shot examples
  - [ ] Use slice: `self.few_shot_examples[-5:]`
  - [ ] Return formatted SYSTEM_PROMPT_TEMPLATE
  - [ ] Pass rubric_content and few_shot_examples as format arguments

---

### 7. AI Module Exports

- [ ] Update `backend/ai/__init__.py`
  - [ ] Import and export `SkillInferenceEngine`
  - [ ] Import and export `load_rubric`
  - [ ] Import and export `FewShotManager`
  - [ ] Import and export `calculate_confidence_score`

---

### 8. Test Script Creation

- [ ] Create `scripts/test_inference.py` file

#### 8.1 Test Script Imports
- [ ] Import `sys`, `os` for path manipulation
- [ ] Add parent directory to path
- [ ] Import `SkillInferenceEngine` from backend.ai
- [ ] Import `load_rubric` from backend.ai
- [ ] Import `dotenv.load_dotenv`

#### 8.2 Test Script Setup
- [ ] Call `load_dotenv()` to load environment variables
- [ ] Load rubric using `load_rubric()`
- [ ] Get OpenAI API key from environment
- [ ] Create SkillInferenceEngine instance

#### 8.3 Test Data Creation
- [ ] Create test_data dictionary with:
  - [ ] "content" field with sample transcript text (Eva speaking)
  - [ ] "metadata" object with type, date, context

#### 8.4 Test Execution
- [ ] Call `engine.assess_skills(test_data)`
- [ ] Store result in assessments variable
- [ ] Print number of assessments generated
- [ ] Loop through assessments
  - [ ] Print skill_name, level, confidence_score for each
  - [ ] Format confidence as 2 decimal places

#### 8.5 Test Validation
- [ ] Add assertion: assessments list is not empty
- [ ] Add assertion: each assessment has required fields
- [ ] Add assertion: confidence scores between 0.5 and 1.0
- [ ] Print "✅ Test passed" if all assertions succeed

---

### 9. Integration Testing

#### 9.1 Unit Test: Rubric Loader
- [ ] Run test loading rubric from backend container
  ```bash
  docker-compose exec backend python -c "from backend.ai.rubric_loader import load_rubric; print(len(load_rubric()))"
  ```
- [ ] Verify output is > 1000 characters
- [ ] Verify no error messages

#### 9.2 Unit Test: Confidence Scoring
- [ ] Create test script for confidence calculation
- [ ] Test with short quote (< 10 words) - expect ~0.6-0.7
- [ ] Test with long quote (> 20 words) - expect ~0.8-0.9
- [ ] Test with rubric keywords present - expect boost
- [ ] Verify scores never exceed 1.0

#### 9.3 Unit Test: Few-Shot Manager
- [ ] Test get_recent_corrections() with empty database
- [ ] Should return empty list
- [ ] Insert test correction into database
- [ ] Re-run get_recent_corrections()
- [ ] Verify correction appears in results

#### 9.4 Integration Test: Full Inference
- [ ] Run `scripts/test_inference.py`
  ```bash
  docker-compose exec backend python scripts/test_inference.py
  ```
- [ ] Expected output: 2-4 assessments
- [ ] Expected skills: Social Awareness, Relationship Skills, Communication
- [ ] Verify each assessment has justification and source_quote
- [ ] Verify confidence scores are reasonable (0.7-0.9)

#### 9.5 OpenAI API Test
- [ ] Verify API key is valid
- [ ] Test with multiple data entry types
  - [ ] Group discussion transcript
  - [ ] Reflection journal
  - [ ] Teacher observation note
- [ ] Confirm different data types produce relevant assessments

#### 9.6 Error Handling Test
- [ ] Test with malformed data_entry (missing content)
- [ ] Verify graceful error handling
- [ ] Test with invalid API key
- [ ] Verify error logged, exception raised
- [ ] Test with very long content (> 10,000 words)
- [ ] Verify token limit handling

---

## Testing Checklist

### Module Tests

- [ ] Test rubric_loader.py
  ```bash
  docker-compose exec backend python -c "from backend.ai.rubric_loader import load_rubric, load_curriculum_context; print('Rubric:', len(load_rubric())); print('Curriculum:', len(load_curriculum_context()))"
  ```
  - [ ] Rubric length > 1000 characters
  - [ ] Curriculum length > 500 characters

- [ ] Test prompts.py
  ```bash
  docker-compose exec backend python -c "from backend.ai.prompts import SYSTEM_PROMPT_TEMPLATE, build_few_shot_section; print(len(SYSTEM_PROMPT_TEMPLATE)); print(build_few_shot_section([]))"
  ```
  - [ ] System prompt template > 2000 characters
  - [ ] Empty few-shot section returns empty string

- [ ] Test confidence_scoring.py
  ```bash
  docker-compose exec backend python scripts/test_confidence.py
  ```
  - [ ] All test cases pass
  - [ ] Scores in valid range

- [ ] Test few_shot_manager.py
  ```bash
  docker-compose exec backend python -c "from backend.ai.few_shot_manager import FewShotManager; fm = FewShotManager(); print(len(fm.get_recent_corrections()))"
  ```
  - [ ] Returns list (empty if no corrections yet)
  - [ ] No database errors

### Integration Tests

- [ ] Test full inference pipeline
  ```bash
  docker-compose exec backend python scripts/test_inference.py
  ```
  - [ ] Assessments generated successfully
  - [ ] At least 2 assessments returned
  - [ ] Each assessment has all required fields
  - [ ] Confidence scores calculated

- [ ] Test with each data entry type
  - [ ] Group discussion transcript → generates SEL + Collaboration assessments
  - [ ] Reflection journal → generates Self-Awareness + Self-Management
  - [ ] Teacher observation → generates multiple skill assessments
  - [ ] Peer feedback → generates Social Awareness + Relationship Skills
  - [ ] Project presentation → generates Communication + Critical Thinking

### Performance Tests

- [ ] Measure inference time for single entry
  - [ ] Should be < 3 seconds average

- [ ] Test with 10 entries in sequence
  - [ ] Monitor rate limiting behavior
  - [ ] Verify no timeouts

- [ ] Check token usage
  - [ ] System prompt + user prompt should be < 4000 tokens
  - [ ] Response should be < 1000 tokens

### Quality Tests

- [ ] Verify assessment quality
  - [ ] Justifications reference rubric criteria
  - [ ] Source quotes are verbatim from content
  - [ ] Levels match observable behaviors
  - [ ] Kind, growth-oriented language used

- [ ] Test few-shot learning
  - [ ] Add 5 teacher corrections to database
  - [ ] Run inference on similar data
  - [ ] Verify few-shot examples included in prompt
  - [ ] Verify assessments improve (closer to corrections)

---

## Acceptance Criteria

- [ ] All 5 AI modules created (rubric_loader, prompts, inference_engine, confidence_scoring, few_shot_manager)
- [ ] Rubric and curriculum load successfully from Docs/
- [ ] System prompt includes all 17 skills and 4 proficiency levels
- [ ] GPT-4o API integration functional
- [ ] JSON response parsing handles both array and object formats
- [ ] Confidence scores calculated for all assessments (range 0.5-1.0)
- [ ] Few-shot manager retrieves corrections from database
- [ ] Few-shot examples integrated into system prompt (last 5)
- [ ] Error handling for malformed LLM responses
- [ ] Error handling for database connection issues
- [ ] Logging captures inference metrics
- [ ] Test script runs successfully
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Assessments include: skill_name, skill_category, level, justification, source_quote, confidence_score

---

## Notes

- Temperature set to 0.3 for consistency (lower temperature = more deterministic)
- Response format enforces JSON output for reliable parsing
- Few-shot learning uses only last 5 corrections to avoid prompt bloat
- Confidence scoring is heuristic (not ML-based) for MVP speed
- Token limits: System prompt ~3000 tokens, max response 4000 tokens
- Rate limiting in ingestion script prevents OpenAI API throttling

**Next Shard:** [Shard 4: Backend API](Shard_4_Tasks.md) (requires this shard complete)
