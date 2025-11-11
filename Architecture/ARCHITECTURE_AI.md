# AI Inference Pipeline Architecture - Shard 3

**Component:** AI Inference Engine
**Version:** 1.0
**Related Shard:** [Shard_3_AI_Inference_Pipeline.md](../Implementation_Shards/Shard_3_AI_Inference_Pipeline.md)

---

## Table of Contents

1. [Overview](#overview)
2. [AI Pipeline Architecture](#ai-pipeline-architecture)
3. [Context Engineering Strategy](#context-engineering-strategy)
4. [Prompt Design](#prompt-design)
5. [Few-Shot Learning System](#few-shot-learning-system)
6. [Confidence Scoring](#confidence-scoring)
7. [Response Processing](#response-processing)
8. [Error Handling](#error-handling)
9. [Performance Optimization](#performance-optimization)

---

## Overview

The AI Inference Pipeline is the core intelligence layer that analyzes student data and generates skill assessments using OpenAI's GPT-4 model. The system employs context engineering with few-shot learning rather than fine-tuning, enabling rapid iteration and continuous improvement through teacher corrections.

**Key Capabilities:**
- Multi-skill assessment from single data entries
- Evidence-based justifications with source quotes
- Confidence scoring for quality assurance
- Adaptive learning from teacher corrections
- Support for 7 data types across 17 skills

---

## AI Pipeline Architecture

### High-Level Pipeline Flow

```mermaid
graph TB
    Start([Data Entry]) --> Load[Load Components]

    subgraph "Context Assembly"
        Load --> R[Load Rubric]
        Load --> FS[Fetch Few-Shot Examples]
        Load --> H[Get Historical Context]

        R --> SP[Build System Prompt]
        FS --> SP
        H --> UP[Build User Prompt]
    end

    subgraph "LLM Processing"
        SP --> API[OpenAI API Call]
        UP --> API
        API --> GPT[GPT-4 Processing]
        GPT --> JSON[JSON Response]
    end

    subgraph "Response Processing"
        JSON --> Parse[Parse Response]
        Parse --> Validate[Validate Schema]
        Validate --> Score[Calculate Confidence]
        Score --> Filter[Quality Filter]
    end

    subgraph "Storage"
        Filter --> Store[Store Assessments]
        Store --> Index[Index for Retrieval]
    end

    Index --> End([Assessment IDs])

    style Start fill:#4caf50,color:#fff
    style GPT fill:#9c27b0,color:#fff
    style End fill:#2196f3,color:#fff
```

### Component Architecture

```mermaid
graph TB
    subgraph "Inference Engine Core"
        IE[SkillInferenceEngine]

        IE --> PC[PromptConstructor]
        IE --> RC[RubricLoader]
        IE --> AC[APIClient]
        IE --> RP[ResponseProcessor]
    end

    subgraph "Few-Shot Manager"
        FSM[FewShotManager]

        FSM --> DB[(Database)]
        FSM --> ES[ExampleSelector]
        FSM --> EF[ExampleFormatter]
    end

    subgraph "Confidence Scorer"
        CS[ConfidenceScorer]

        CS --> QL[QuoteLengthAnalyzer]
        CS --> KM[KeywordMatcher]
        CS --> CC[ContextChecker]
    end

    subgraph "External Services"
        OAI[OpenAI API]
    end

    IE --> FSM
    IE --> CS
    AC --> OAI

    classDef core fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef fewshot fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef confidence fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#ef6c00,stroke-width:2px

    class IE,PC,RC,AC,RP core
    class FSM,ES,EF fewshot
    class CS,QL,KM,CC confidence
    class OAI external
```

---

## Context Engineering Strategy

### Why Context Engineering Over Fine-Tuning

```mermaid
mindmap
  root((Context<br/>Engineering))
    Advantages
      No labeled data needed
      Faster iteration cycles
      Flexible updates
      Lower initial cost
      Immediate deployment
    Implementation
      Zero-shot baseline
      Few-shot enhancement
      Dynamic examples
      Rubric injection
      Structured output
    Evolution Path
      Start: Context eng
      Collect: Teacher corrections
      Analyze: Performance metrics
      Decide: Fine-tune threshold
      Transition: Gradual migration
```

### Context Components

```mermaid
graph LR
    subgraph "Static Context"
        SC1[System Role Definition]
        SC2[Complete Rubric]
        SC3[Assessment Rules]
        SC4[Output Format Spec]
    end

    subgraph "Dynamic Context"
        DC1[Few-Shot Examples]
        DC2[Student History]
        DC3[Data Type Context]
    end

    subgraph "Input Context"
        IC1[Data Entry Content]
        IC2[Metadata]
        IC3[Date/Timing]
    end

    SC1 --> Prompt[Complete Prompt]
    SC2 --> Prompt
    SC3 --> Prompt
    SC4 --> Prompt
    DC1 --> Prompt
    DC2 --> Prompt
    DC3 --> Prompt
    IC1 --> Prompt
    IC2 --> Prompt
    IC3 --> Prompt

    Prompt --> GPT[GPT-4]

    style Prompt fill:#9c27b0,color:#fff
    style GPT fill:#412991,color:#fff
```

---

## Prompt Design

### System Prompt Structure

```mermaid
graph TB
    Start([System Prompt]) --> Role[Role Definition]

    Role --> Skills[17 Skills List]
    Skills --> Levels[Proficiency Levels]
    Levels --> Rubric[Complete Rubric]

    Rubric --> Rules[Assessment Rules]
    Rules --> R1[Evidence-Based]
    Rules --> R2[Specific Skill Focus]
    Rules --> R3[Level Justification]
    Rules --> R4[Quote Selection]
    Rules --> R5[No Assumptions]
    Rules --> R6[Confidence Threshold]

    R1 --> Format[Output Format]
    R2 --> Format
    R3 --> Format
    R4 --> Format
    R5 --> Format
    R6 --> Format

    Format --> Examples{Few-Shot<br/>Available?}
    Examples -->|Yes| FSE[Add Examples]
    Examples -->|No| Complete

    FSE --> Complete([Complete Prompt])

    style Start fill:#4caf50,color:#fff
    style Complete fill:#2196f3,color:#fff
    style Rubric fill:#ff9800,color:#fff
```

### System Prompt Template

```python
SYSTEM_PROMPT_TEMPLATE = """You are an Expert Educational Assessor specializing in middle school non-academic skill development. Your task is to analyze student data (transcripts, notes, reflections, feedback) and assess proficiency levels for specific skills based on a comprehensive behavioral rubric.

# YOUR ROLE
- Objective and unbiased
- Focus on observable behaviors, not assumptions
- Provide specific evidence for every assessment
- Use the EXACT proficiency levels defined in the rubric

# THE 17 SKILLS YOU ASSESS

## SEL (Social-Emotional Learning) - 5 Skills
1. Self-Awareness
2. Self-Management
3. Social Awareness
4. Relationship Skills
5. Responsible Decision-Making

## EF (Executive Function) - 6 Skills
6. Working Memory
7. Flexible Thinking
8. Self-Control
9. Task Initiation
10. Planning & Prioritization
11. Organization

## 21st Century Skills - 6 Skills
12. Communication
13. Collaboration
14. Critical Thinking
15. Creativity
16. Digital Literacy
17. Metacognition

# PROFICIENCY LEVELS
- **Emerging (E):** Needs significant, consistent support; skill application is inconsistent or absent.
- **Developing (D):** Applies the skill with frequent prompting or scaffolding; inconsistent success.
- **Proficient (P):** Applies the skill independently and consistently in familiar contexts; generally successful.
- **Advanced (A):** Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others.

# COMPLETE RUBRIC
{rubric_content}

# ASSESSMENT RULES
1. **Evidence-Based:** Every assessment MUST include a direct quote from the source material.
2. **Specific Skill Focus:** Assess ONLY the skills that have observable evidence in the data.
3. **Level Justification:** Explain WHY the student is at that level using rubric criteria.
4. **Quote Selection:** Choose the MOST representative quote (1-3 sentences) that demonstrates the behavior.
5. **No Assumptions:** Do not infer beyond what is observable in the text.
6. **Confidence Threshold:** If there is insufficient evidence to assess a skill, do not include it in your response.

# OUTPUT FORMAT
Return your assessment as a JSON array with the following structure:

```json
[
  {{
    "skill_name": "Self-Awareness",
    "skill_category": "SEL",
    "level": "Developing",
    "confidence_score": 0.85,
    "justification": "The student can name basic emotions when prompted and is beginning to connect feelings to behavior. In the transcript, the student says 'I was feeling frustrated because...' after being asked by the teacher to reflect. This demonstrates D-level self-awareness: naming emotions with prompting.",
    "source_quote": "I was feeling frustrated because the group wasn't listening to my ideas, and that made me want to just stop participating.",
    "data_point_count": 1
  }}
]
```

# FEW-SHOT EXAMPLES
{few_shot_examples}

Now, analyze the following student data and provide assessments for ALL observable skills.
"""
```

### User Prompt Template

```python
USER_PROMPT_TEMPLATE = """
# STUDENT DATA TO ANALYZE

**Student ID:** {student_id}
**Type:** {data_type}
**Date:** {date}
**Context:** {context}

**Content:**
{content}

---

Please assess all observable skills based on this data. Return ONLY the JSON array, no additional text.
"""
```

### Prompt Engineering Best Practices

```mermaid
mindmap
  root((Prompt<br/>Engineering))
    Clarity
      Explicit instructions
      Structured format
      Examples provided
      Clear boundaries
    Consistency
      Fixed temperature
      Deterministic output
      Rubric alignment
      Level definitions
    Quality
      Evidence requirement
      Quote extraction
      Confidence scoring
      No hallucinations
    Optimization
      Token efficiency
      Relevant context only
      Selective examples
      Output constraints
```

---

## Few-Shot Learning System

### Learning Loop Architecture

```mermaid
sequenceDiagram
    participant AI as AI Engine
    participant DB as Database
    participant T as Teacher
    participant FSM as Few-Shot Manager

    Note over AI,FSM: Initial Assessment
    AI->>DB: Generate assessments
    DB-->>T: Display for review

    Note over AI,FSM: Teacher Correction
    T->>DB: Submit correction
    DB->>FSM: Trigger update

    Note over AI,FSM: Few-Shot Update
    FSM->>DB: Fetch recent corrections
    DB-->>FSM: Return top 5
    FSM->>FSM: Format examples
    FSM->>AI: Update prompt context

    Note over AI,FSM: Improved Assessment
    AI->>AI: Use updated examples
    AI->>DB: Generate better assessments
```

### Example Selection Strategy

```mermaid
flowchart TD
    Start([New Assessment<br/>Request]) --> CheckSkill{Specific<br/>Skill?}

    CheckSkill -->|Yes| SkillFilter[Filter by Skill Name]
    CheckSkill -->|No| AllCorrections[Get All Corrections]

    SkillFilter --> HasNotes{Teacher<br/>Notes?}
    AllCorrections --> HasNotes

    HasNotes -->|Yes| Priority[High Priority]
    HasNotes -->|No| LowPriority[Low Priority]

    Priority --> Recent[Sort by Date DESC]
    LowPriority --> Recent

    Recent --> Limit[Take Top 5]
    Limit --> Format[Format as Examples]
    Format --> End([Return Examples])

    style Priority fill:#4caf50,color:#fff
    style LowPriority fill:#ff9800,color:#fff
```

### Few-Shot Example Format

```python
class FewShotExample:
    """Structure for few-shot learning examples."""

    def __init__(
        self,
        skill_name: str,
        skill_category: str,
        level: str,
        justification: str,
        source_quote: str,
        teacher_notes: str = None,
        original_content: str = None
    ):
        self.skill_name = skill_name
        self.skill_category = skill_category
        self.level = level
        self.justification = justification
        self.source_quote = source_quote
        self.teacher_notes = teacher_notes
        self.original_content = original_content

    def to_prompt_format(self) -> str:
        """Convert to few-shot prompt format."""
        example = f"""
**Example - {self.skill_name} ({self.level})**

Original Data Excerpt:
"{self.source_quote}"

Assessment:
- Skill: {self.skill_name} ({self.skill_category})
- Level: {self.level}
- Justification: {self.justification}
"""
        if self.teacher_notes:
            example += f"\nTeacher Note: {self.teacher_notes}\n"

        return example
```

### Few-Shot Performance Metrics

```mermaid
graph LR
    subgraph "Metrics"
        M1[Teacher Agreement Rate]
        M2[Confidence Score Avg]
        M3[Correction Frequency]
        M4[Assessment Accuracy]
    end

    subgraph "Targets"
        T1[>= 85%]
        T2[>= 0.80]
        T3[< 20%]
        T4[>= 90%]
    end

    M1 -->|Target| T1
    M2 -->|Target| T2
    M3 -->|Target| T3
    M4 -->|Target| T4

    style T1 fill:#4caf50,color:#fff
    style T2 fill:#4caf50,color:#fff
    style T3 fill:#4caf50,color:#fff
    style T4 fill:#4caf50,color:#fff
```

---

## Confidence Scoring

### Confidence Calculation Algorithm

```mermaid
flowchart TD
    Start([Assessment]) --> Base[Base Score: 0.5]

    Base --> F1{Quote Length<br/>>= 20 words?}
    F1 -->|Yes| A1[+0.15]
    F1 -->|No| F2{Quote Length<br/>>= 10 words?}
    F2 -->|Yes| A2[+0.10]
    F2 -->|No| A3[+0.05]

    A1 --> RubricCheck
    A2 --> RubricCheck
    A3 --> RubricCheck

    RubricCheck{Rubric<br/>Keywords?} -->|Yes| B1[+0.15]
    RubricCheck -->|No| B2[+0.00]

    B1 --> ContentCheck
    B2 --> ContentCheck

    ContentCheck{Content Length<br/>> 200 words?} -->|Yes| C1[+0.10]
    ContentCheck -->|No| C2[+0.00]

    C1 --> DataCheck
    C2 --> DataCheck

    DataCheck{Data Points<br/>>= 3?} -->|Yes| D1[+0.10]
    DataCheck -->|No| D2[+0.00]

    D1 --> Cap[Cap at 1.0]
    D2 --> Cap

    Cap --> End([Final Score])

    style Start fill:#4caf50,color:#fff
    style End fill:#2196f3,color:#fff
```

### Confidence Score Implementation

```python
def calculate_confidence_score(
    data_entry: Dict[str, Any],
    assessment: Dict[str, Any]
) -> float:
    """
    Calculate confidence score based on data quality indicators.

    Factors:
    - Quote length and specificity
    - Data entry length
    - Alignment with rubric language
    - Historical data availability

    Returns:
        float: Confidence score between 0.0 and 1.0
    """
    confidence = 0.5  # Base confidence

    # Factor 1: Source quote length (longer quotes = clearer evidence)
    quote_words = len(assessment['source_quote'].split())
    if quote_words >= 20:
        confidence += 0.15
    elif quote_words >= 10:
        confidence += 0.10
    else:
        confidence += 0.05

    # Factor 2: Rubric keyword matching
    rubric_keywords = [
        'independently', 'consistently', 'with prompting',
        'struggles to', 'demonstrates', 'applies', 'shows'
    ]
    justification_lower = assessment['justification'].lower()
    if any(keyword in justification_lower for keyword in rubric_keywords):
        confidence += 0.15

    # Factor 3: Data entry completeness
    content_words = len(data_entry['content'].split())
    if content_words > 200:
        confidence += 0.10

    # Factor 4: Historical data point count
    if assessment.get('data_point_count', 1) >= 3:
        confidence += 0.10

    # Cap at 1.0
    return min(confidence, 1.0)
```

### Confidence Interpretation

| Score Range | Interpretation | Action |
|-------------|---------------|--------|
| 0.90 - 1.00 | Very High | Auto-approve possible |
| 0.80 - 0.89 | High | Minimal review needed |
| 0.65 - 0.79 | Medium | Teacher review recommended |
| 0.50 - 0.64 | Low | Teacher review required |
| < 0.50 | Very Low | Flag for manual assessment |

---

## Response Processing

### Response Validation Pipeline

```mermaid
flowchart TD
    Start([GPT Response]) --> Parse[Parse JSON]

    Parse --> Valid{Valid<br/>JSON?}
    Valid -->|No| Error1[Return Error]
    Valid -->|Yes| Array{Is<br/>Array?}

    Array -->|No| Error2[Return Error]
    Array -->|Yes| Loop[For Each Assessment]

    Loop --> CheckFields{Required<br/>Fields?}
    CheckFields -->|No| Skip[Skip Assessment]
    CheckFields -->|Yes| ValidateSkill{Valid<br/>Skill?}

    ValidateSkill -->|No| Skip
    ValidateSkill -->|Yes| ValidateLevel{Valid<br/>Level?}

    ValidateLevel -->|No| Skip
    ValidateLevel -->|Yes| ValidateQuote{Has<br/>Quote?}

    ValidateQuote -->|No| Skip
    ValidateQuote -->|Yes| CalcConf[Calculate Confidence]

    CalcConf --> AddToValid[Add to Valid List]

    AddToValid --> More{More<br/>Assessments?}
    More -->|Yes| Loop
    More -->|No| Return[Return Valid Assessments]

    Skip --> More
    Error1 --> End([Empty Array])
    Error2 --> End
    Return --> End

    style Start fill:#4caf50,color:#fff
    style End fill:#2196f3,color:#fff
    style Error1 fill:#f44336,color:#fff
    style Error2 fill:#f44336,color:#fff
```

### Schema Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Literal

class AssessmentResponse(BaseModel):
    """Schema for AI-generated assessment response."""

    skill_name: str = Field(..., min_length=1)
    skill_category: Literal["SEL", "EF", "21st_Century"]
    level: Literal["Emerging", "Developing", "Proficient", "Advanced"]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    justification: str = Field(..., min_length=10)
    source_quote: str = Field(..., min_length=5)
    data_point_count: int = Field(default=1, ge=1)

    @validator('skill_name')
    def validate_skill_name(cls, v):
        """Validate skill name against known skills."""
        valid_skills = [
            'Self-Awareness', 'Self-Management', 'Social Awareness',
            'Relationship Skills', 'Responsible Decision-Making',
            'Working Memory', 'Flexible Thinking', 'Self-Control',
            'Task Initiation', 'Planning & Prioritization', 'Organization',
            'Communication', 'Collaboration', 'Critical Thinking',
            'Creativity', 'Digital Literacy', 'Metacognition'
        ]
        if v not in valid_skills:
            raise ValueError(f"Invalid skill name: {v}")
        return v

    @validator('justification')
    def validate_justification(cls, v):
        """Ensure justification references the rubric."""
        if len(v.split()) < 10:
            raise ValueError("Justification too short")
        return v
```

---

## Error Handling

### Error Classification

```mermaid
graph TB
    subgraph "API Errors"
        E1[Rate Limit]
        E2[API Key Invalid]
        E3[Timeout]
        E4[Server Error]
    end

    subgraph "Response Errors"
        E5[Invalid JSON]
        E6[Schema Mismatch]
        E7[Empty Response]
        E8[Hallucination]
    end

    subgraph "Data Errors"
        E9[Missing Content]
        E10[Invalid Format]
        E11[Encoding Issues]
    end

    E1 --> R1[Retry with Backoff]
    E2 --> R2[Log & Alert]
    E3 --> R1
    E4 --> R1

    E5 --> R3[Parse Error Handler]
    E6 --> R4[Schema Validator]
    E7 --> R5[Return Empty Array]
    E8 --> R6[Confidence Filter]

    E9 --> R7[Skip Entry]
    E10 --> R8[Data Validator]
    E11 --> R9[Encoding Handler]

    style E2 fill:#f44336,color:#fff
    style E8 fill:#ff9800,color:#fff
```

### Retry Strategy

```python
import time
from functools import wraps

def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0
):
    """Decorator for retrying API calls with exponential backoff."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except openai.error.RateLimitError:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)
                except openai.error.APIError as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)

        return wrapper
    return decorator
```

---

## Performance Optimization

### Optimization Strategies

```mermaid
mindmap
  root((Performance<br/>Optimization))
    API Calls
      Batch processing
      Async requests
      Response caching
      Token optimization
    Prompt Design
      Minimal rubric
      Selective examples
      Structured output
      Clear constraints
    Response Processing
      Stream parsing
      Parallel validation
      Early filtering
      Lazy evaluation
    Caching
      Rubric cache
      Example cache
      Result cache
      Prompt cache
```

### Performance Metrics

| Metric | Target | Current | Strategy |
|--------|--------|---------|----------|
| API Call Duration | < 3s | ~4s | Optimize prompt length |
| Token Usage | < 2000 | ~2500 | Reduce rubric size |
| Response Parsing | < 100ms | ~80ms | ✓ Target met |
| End-to-End Time | < 5s | ~6s | Async processing |
| Cost per Assessment | < $0.02 | $0.025 | Batch requests |

---

## Integration Points

### AI Engine Integration Map

```mermaid
graph TB
    subgraph "Input Sources"
        DI[Data Ingestion API]
        BA[Batch Assessment]
        RT[Real-time Assessment]
    end

    subgraph "AI Engine"
        IE[Inference Engine]
    end

    subgraph "Output Targets"
        DB[(Database)]
        API[REST API]
        WS[WebSocket]
    end

    subgraph "Support Services"
        FSM[Few-Shot Manager]
        CS[Confidence Scorer]
        RL[Rubric Loader]
    end

    DI --> IE
    BA --> IE
    RT --> IE

    IE --> FSM
    IE --> CS
    IE --> RL

    IE --> DB
    IE --> API
    IE --> WS

    style IE fill:#9c27b0,color:#fff
```

---

**Related Documents:**
- [Main Architecture Overview](./ARCHITECTURE_OVERVIEW.md)
- [Shard 3 Implementation Tasks](../Implementation_Shards/Shard_3_Tasks.md)
- [PRD AI Section](../Docs/PRD.md#4-ai-inference-pipeline)
