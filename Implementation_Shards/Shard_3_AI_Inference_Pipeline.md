# Shard 3: AI Inference Pipeline

**Owner:** ML/AI Engineer
**Estimated Time:** 2 days
**Dependencies:** Shard 1 (Database)
**Priority:** P0 (Critical Path)

---

## Objective

Build the GPT-4o powered inference engine that analyzes student data and generates skill assessments based on the rubric. Implement heuristic confidence scoring and few-shot learning integration.

---

## Key Components

### 1. Rubric Loader

**File:** `backend/ai/rubric_loader.py`

```python
"""Load and format rubric for LLM context."""
import os

def load_rubric() -> str:
    """Load full rubric from Docs/Rubric.md"""
    rubric_path = os.path.join(os.path.dirname(__file__), '../../Docs/Rubric.md')
    with open(rubric_path, 'r') as f:
        return f.read()

def load_curriculum_context() -> str:
    """Load curriculum for additional context."""
    curr_path = os.path.join(os.path.dirname(__file__), '../../Docs/Curriculum.md')
    with open(curr_path, 'r') as f:
        return f.read()
```

### 2. System Prompt Builder

**File:** `backend/ai/prompts.py`

```python
"""System prompts for skill assessment."""

SYSTEM_PROMPT_TEMPLATE = """You are an Expert Educational Assessor specializing in middle school non-academic skill development. Your task is to analyze student data (transcripts, notes, reflections, feedback) and assess proficiency levels for specific skills based on a comprehensive behavioral rubric.

# YOUR ROLE
- Objective and unbiased
- Focus on observable behaviors, not assumptions
- Provide specific evidence for every assessment
- Use the EXACT proficiency levels defined in the rubric
- Use kind, growth-oriented language

# THE 17 SKILLS YOU ASSESS

**SEL (Social-Emotional Learning):**
1. Self-Awareness
2. Self-Management
3. Social Awareness
4. Relationship Skills
5. Responsible Decision-Making

**EF (Executive Functioning):**
6. Working Memory
7. Inhibitory Control
8. Cognitive Flexibility
9. Planning & Prioritization
10. Organization
11. Task Initiation

**21st Century Skills:**
12. Critical Thinking
13. Communication
14. Collaboration
15. Creativity & Innovation
16. Digital Literacy
17. Global Awareness

# PROFICIENCY LEVELS
- **Emerging (E):** Needs significant, consistent support; skill application is inconsistent or absent.
- **Developing (D):** Applies the skill with frequent prompting or scaffolding; inconsistent success.
- **Proficient (P):** Applies the skill independently and consistently in familiar contexts; generally successful.
- **Advanced (A):** Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others.

# COMPLETE RUBRIC
{rubric_content}

# ASSESSMENT RULES
1. **Evidence-Based:** Every assessment MUST include a direct quote from the source material
2. **Specific Skill Focus:** Assess ONLY the skills that have observable evidence in the data
3. **Level Justification:** Explain WHY the student is at that level using rubric criteria
4. **Quote Selection:** Choose the MOST representative quote (1-3 sentences) that demonstrates the behavior
5. **No Assumptions:** Do not infer beyond what is observable in the text
6. **Kind Language:** Use growth-oriented descriptors (e.g., "beginning to develop", "showing progress in")
7. **Confidence Threshold:** If there is insufficient evidence to assess a skill, do not include it in the output

# OUTPUT FORMAT
Return your assessment as a JSON array with the following structure (return ONLY valid JSON, no markdown formatting):

[
  {{
    "skill_name": "Self-Awareness",
    "skill_category": "SEL",
    "level": "Developing",
    "justification": "The student can name basic emotions when prompted and is beginning to connect feelings to behavior. In the transcript, the student says 'I was feeling frustrated because...' after being asked by the teacher to reflect. This demonstrates Developing-level self-awareness: naming emotions with prompting.",
    "source_quote": "I was feeling frustrated because the group wasn't listening to my ideas, and that made me want to just stop participating.",
    "data_point_count": 1
  }}
]

{few_shot_examples}

Now, analyze the following student data and provide assessments for ALL observable skills."""


def build_few_shot_section(examples: list) -> str:
    """Format few-shot examples from teacher corrections."""
    if not examples:
        return ""

    section = "\n\n# FEW-SHOT LEARNING EXAMPLES\n"
    section += "Here are examples of high-quality assessments validated by teachers:\n\n"

    for i, ex in enumerate(examples, 1):
        section += f"""**Example {i}:**
Skill: {ex['skill_name']}
Level: {ex['level']}
Justification: {ex['justification']}
Source Quote: "{ex['source_quote']}"
Teacher Notes: {ex.get('teacher_notes', 'N/A')}

"""
    return section


def build_user_prompt(data_entry: dict) -> str:
    """Build user prompt with student data."""
    return f"""# STUDENT DATA TO ANALYZE

**Type:** {data_entry['metadata']['type']}
**Date:** {data_entry['metadata']['date']}
**Context:** {data_entry['metadata'].get('context', 'N/A')}

**Content:**
{data_entry['content']}

---

Please assess all observable skills based on this data. Return ONLY the JSON array, no additional text."""
```

### 3. Inference Engine

**File:** `backend/ai/inference_engine.py`

```python
"""Core AI inference engine for skill assessment."""
import openai
import json
import os
import logging
from typing import List, Dict, Any
from .prompts import SYSTEM_PROMPT_TEMPLATE, build_few_shot_section, build_user_prompt
from .rubric_loader import load_rubric
from .confidence_scoring import calculate_confidence_score

logger = logging.getLogger(__name__)


class SkillInferenceEngine:
    """GPT-4o powered skill assessment engine."""

    def __init__(self, api_key: str, rubric: str, few_shot_examples: List[Dict] = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
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
        user_prompt = build_user_prompt(student_data)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Low temperature for consistency
                max_tokens=4000,
                response_format={"type": "json_object"}  # Enforce JSON output
            )

            content = response.choices[0].message.content
            assessments = json.loads(content)

            # Handle both array and object responses
            if isinstance(assessments, dict) and 'assessments' in assessments:
                assessments = assessments['assessments']

            # Calculate confidence scores
            for assessment in assessments:
                if 'confidence_score' not in assessment or assessment['confidence_score'] is None:
                    assessment['confidence_score'] = calculate_confidence_score(
                        student_data, assessment
                    )

            logger.info(f"Generated {len(assessments)} assessments for data entry")
            return assessments

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response content: {content}")
            return []
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise

    def _build_system_prompt(self) -> str:
        """Build complete system prompt with rubric and few-shot examples."""
        few_shot_section = build_few_shot_section(self.few_shot_examples[-5:])  # Last 5 corrections

        return SYSTEM_PROMPT_TEMPLATE.format(
            rubric_content=self.rubric,
            few_shot_examples=few_shot_section
        )
```

### 4. Confidence Scoring

**File:** `backend/ai/confidence_scoring.py`

```python
"""Heuristic confidence scoring for assessments."""

def calculate_confidence_score(data_entry: dict, assessment: dict) -> float:
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
    quote_length = len(assessment.get('source_quote', '').split())
    if quote_length >= 20:
        confidence += 0.15
    elif quote_length >= 10:
        confidence += 0.10

    # Factor 2: Rubric keyword matching
    justification = assessment.get('justification', '').lower()
    rubric_keywords = [
        'independently', 'consistently', 'with prompting', 'with support',
        'beginning to', 'developing', 'demonstrates', 'applies'
    ]
    keyword_matches = sum(1 for kw in rubric_keywords if kw in justification)
    confidence += min(keyword_matches * 0.05, 0.15)

    # Factor 3: Data entry completeness
    content_length = len(data_entry.get('content', '').split())
    if content_length > 200:
        confidence += 0.10
    elif content_length > 100:
        confidence += 0.05

    # Factor 4: Historical data point count
    if assessment.get('data_point_count', 1) >= 3:
        confidence += 0.10

    return min(confidence, 1.0)  # Cap at 1.0
```

### 5. Few-Shot Manager

**File:** `backend/ai/few_shot_manager.py`

```python
"""Manages teacher corrections for few-shot learning."""
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.connection import get_db_connection


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
        cursor.close()
        conn.close()

        examples = []
        for correction in corrections:
            examples.append({
                "skill_name": correction['skill_name'],
                "skill_category": correction['skill_category'],
                "level": correction['corrected_level'],
                "justification": correction['corrected_justification'],
                "source_quote": correction['source_quote'],
                "teacher_notes": correction['teacher_notes']
            })

        return examples
```

---

## Acceptance Criteria

- [ ] Inference engine successfully loads rubric from Docs/
- [ ] System prompt includes all 17 skills and proficiency levels
- [ ] GPT-4o returns valid JSON array of assessments
- [ ] Each assessment includes: skill_name, level, justification, source_quote
- [ ] Confidence scores calculated for all assessments
- [ ] Few-shot manager retrieves corrections from database
- [ ] Few-shot examples integrated into system prompt
- [ ] Error handling for malformed LLM responses
- [ ] Logging captures inference metrics

---

## Testing

```python
# Test script: scripts/test_inference.py
from backend.ai.inference_engine import SkillInferenceEngine
from backend.ai.rubric_loader import load_rubric
import os

rubric = load_rubric()
engine = SkillInferenceEngine(
    api_key=os.getenv("OPENAI_API_KEY"),
    rubric=rubric
)

# Test with sample data
test_data = {
    "content": """Eva: "I hear you, Lucas. Food waste is definitely important. Maybe we could look at both? They're kind of connected—like, food production uses a lot of energy." """,
    "metadata": {
        "type": "group_discussion_transcript",
        "date": "2025-08-15",
        "context": "Science class"
    }
}

assessments = engine.assess_skills(test_data)
print(f"Generated {len(assessments)} assessments:")
for a in assessments:
    print(f"  - {a['skill_name']}: {a['level']} (confidence: {a['confidence_score']})")
```

**Expected Output:**
```
Generated 2-3 assessments:
  - Social Awareness: Proficient (confidence: 0.85)
  - Relationship Skills: Proficient (confidence: 0.80)
```

---

**Completion Checklist:**
- [ ] All modules created and tested
- [ ] Rubric loader functional
- [ ] System prompt validated
- [ ] Test inferences successful
- [ ] Confidence scoring working
- [ ] Few-shot integration tested

**Sign-off:** _____________________
