# Backend API Architecture - Shard 4

**Component:** FastAPI Backend
**Version:** 1.0
**Related Shard:** [Shard_4_Backend_API.md](../Implementation_Shards/Shard_4_Backend_API.md)

---

## Table of Contents

1. [Overview](#overview)
2. [API Architecture](#api-architecture)
3. [Endpoint Specifications](#endpoint-specifications)
4. [Request/Response Patterns](#requestresponse-patterns)
5. [Middleware & Security](#middleware--security)
6. [Error Handling](#error-handling)
7. [Data Validation](#data-validation)
8. [Performance Considerations](#performance-considerations)

---

## Overview

The FastAPI backend serves as the central API layer, coordinating between the frontend dashboards, AI inference engine, and PostgreSQL database. It provides RESTful endpoints for data ingestion, assessment retrieval, teacher corrections, and student progress tracking.

**Key Features:**
- RESTful API design
- Automatic OpenAPI documentation
- Pydantic data validation
- CORS support for Streamlit
- Async request handling
- Connection pooling

---

## API Architecture

### Layer Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        TD[Teacher Dashboard]
        SD[Student Dashboard]
        EXT[External Clients]
    end

    subgraph "Gateway Layer"
        CORS[CORS Middleware]
        VAL[Request Validator]
        AUTH[Auth Middleware]
    end

    subgraph "Router Layer"
        R1[Data Ingest Router]
        R2[Assessments Router]
        R3[Corrections Router]
        R4[Students Router]
    end

    subgraph "Service Layer"
        S1[Data Ingest Service]
        S2[Assessment Service]
        S3[Correction Service]
        S4[Student Service]
        S5[AI Service]
        S6[Analytics Service]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        CACHE[(Redis Cache)]
    end

    TD --> CORS
    SD --> CORS
    EXT --> CORS

    CORS --> VAL
    VAL --> AUTH

    AUTH --> R1
    AUTH --> R2
    AUTH --> R3
    AUTH --> R4

    R1 --> S1
    R2 --> S2
    R3 --> S3
    R4 --> S4

    S1 --> S5
    S2 --> S6
    S3 --> S5

    S1 --> DB
    S2 --> DB
    S3 --> DB
    S4 --> DB

    S2 --> CACHE
    S6 --> CACHE

    classDef client fill:#e3f2fd,stroke:#1565c0
    classDef gateway fill:#fff3e0,stroke:#ef6c00
    classDef router fill:#f3e5f5,stroke:#6a1b9a
    classDef service fill:#e8f5e9,stroke:#2e7d32
    classDef data fill:#ffebee,stroke:#c62828

    class TD,SD,EXT client
    class CORS,VAL,AUTH gateway
    class R1,R2,R3,R4 router
    class S1,S2,S3,S4,S5,S6 service
    class DB,CACHE data
```

### Application Structure

```mermaid
graph LR
    subgraph "backend/"
        Main[main.py<br/>FastAPI App]

        subgraph "routers/"
            R1[data_ingest.py]
            R2[assessments.py]
            R3[corrections.py]
            R4[students.py]
        end

        subgraph "services/"
            S1[data_service.py]
            S2[assessment_service.py]
            S3[correction_service.py]
            S4[student_service.py]
        end

        subgraph "models/"
            M1[schemas.py]
            M2[database_models.py]
        end

        subgraph "ai/"
            AI[inference_engine.py]
        end

        subgraph "database/"
            DB[connection.py]
        end

        subgraph "utils/"
            U1[validators.py]
            U2[exceptions.py]
        end
    end

    Main --> R1
    Main --> R2
    Main --> R3
    Main --> R4

    R1 --> S1
    R2 --> S2
    R3 --> S3
    R4 --> S4

    S1 --> AI
    S2 --> AI

    S1 --> DB
    S2 --> DB
    S3 --> DB
    S4 --> DB

    R1 --> M1
    R2 --> M1
    R3 --> M1
    R4 --> M1

    S1 --> U1
    S2 --> U1
```

---

## Endpoint Specifications

### API Endpoint Map

```mermaid
graph TB
    Root[API Root /]

    subgraph "Health Endpoints"
        H1[GET /health]
        H2[GET /]
    end

    subgraph "Data Endpoints"
        D1[POST /api/data/ingest]
        D2[POST /api/data/batch]
        D3[GET /api/data/types]
    end

    subgraph "Assessment Endpoints"
        A1[GET /api/assessments/student/:id]
        A2[GET /api/assessments/skill-trends/:id]
        A3[GET /api/assessments/pending]
        A4[POST /api/assessments/:id/approve]
        A5[GET /api/assessments/:id]
    end

    subgraph "Correction Endpoints"
        C1[POST /api/corrections/submit]
        C2[GET /api/corrections/history/:student_id]
        C3[GET /api/corrections/stats]
    end

    subgraph "Student Endpoints"
        S1[GET /api/students]
        S2[GET /api/students/:id]
        S3[GET /api/students/:id/progress]
        S4[GET /api/students/:id/badges]
        S5[POST /api/students/:id/target-skill]
        S6[GET /api/students/:id/targets]
    end

    Root --> H1
    Root --> H2
    Root --> D1
    Root --> D2
    Root --> D3
    Root --> A1
    Root --> A2
    Root --> A3
    Root --> A4
    Root --> A5
    Root --> C1
    Root --> C2
    Root --> C3
    Root --> S1
    Root --> S2
    Root --> S3
    Root --> S4
    Root --> S5
    Root --> S6

    classDef health fill:#4caf50,color:#fff
    classDef data fill:#2196f3,color:#fff
    classDef assessment fill:#9c27b0,color:#fff
    classDef correction fill:#ff9800,color:#fff
    classDef student fill:#f44336,color:#fff

    class H1,H2 health
    class D1,D2,D3 data
    class A1,A2,A3,A4,A5 assessment
    class C1,C2,C3 correction
    class S1,S2,S3,S4,S5,S6 student
```

### Detailed Endpoint Specifications

#### 1. Health Endpoints

##### GET /
```yaml
summary: Root endpoint
description: Returns API information and status
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            message: string
            version: string
            status: string
```

##### GET /health
```yaml
summary: Health check endpoint
description: Returns system health status
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            status: string
            database: string
            ai_service: string
            timestamp: string
```

#### 2. Data Ingest Endpoints

##### POST /api/data/ingest
```yaml
summary: Ingest single data entry
description: Ingest a data entry and trigger AI assessment
requestBody:
  content:
    application/json:
      schema:
        type: object
        required:
          - data_entry_id
          - student_id
          - type
          - date
          - content
        properties:
          data_entry_id: string
          student_id: string
          teacher_id: string
          type: string
          date: string (YYYY-MM-DD)
          content: string
          metadata: object
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            data_entry_id: string
            assessments_created: integer
            assessment_ids: array
            status: string
  400:
    description: Invalid request data
  500:
    description: Server error
```

##### POST /api/data/batch
```yaml
summary: Batch ingest multiple data entries
description: Ingest multiple data entries efficiently
requestBody:
  content:
    application/json:
      schema:
        type: object
        properties:
          entries: array of data_entry objects
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            total_entries: integer
            successful: integer
            failed: integer
            results: array
```

#### 3. Assessment Endpoints

##### GET /api/assessments/student/{student_id}
```yaml
summary: Get all assessments for a student
parameters:
  - name: student_id
    in: path
    required: true
    schema:
      type: string
  - name: skill_name
    in: query
    schema:
      type: string
  - name: date_from
    in: query
    schema:
      type: string
  - name: date_to
    in: query
    schema:
      type: string
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            student_id: string
            total_assessments: integer
            assessments: array
```

##### GET /api/assessments/skill-trends/{student_id}
```yaml
summary: Get skill progression trends
description: Returns time-series data for skill visualization
parameters:
  - name: student_id
    in: path
    required: true
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            student_id: string
            skills: array
              - skill_name: string
                skill_category: string
                trend: array
                  - date: string
                    level: string
                    level_numeric: integer
                current_level: string
                growth_direction: string
```

##### GET /api/assessments/pending
```yaml
summary: Get pending assessments for review
description: Returns assessments that need teacher validation
parameters:
  - name: confidence_threshold
    in: query
    schema:
      type: number
      default: 0.8
  - name: teacher_id
    in: query
    schema:
      type: string
responses:
  200:
    content:
      application/json:
        schema:
          type: array
          items:
            type: object
```

#### 4. Correction Endpoints

##### POST /api/corrections/submit
```yaml
summary: Submit teacher correction
description: Submit a correction for an assessment
requestBody:
  content:
    application/json:
      schema:
        type: object
        required:
          - assessment_id
          - corrected_level
          - corrected_by
        properties:
          assessment_id: integer
          corrected_level: string
          corrected_justification: string
          teacher_notes: string
          corrected_by: string
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            correction_id: integer
            status: string
            message: string
```

#### 5. Student Endpoints

##### GET /api/students/{student_id}/progress
```yaml
summary: Get student progress data
description: Returns comprehensive progress information for student dashboard
parameters:
  - name: student_id
    in: path
    required: true
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            student_id: string
            student_name: string
            skills: array
              - skill_name: string
                current_level: string
                recently_advanced: boolean
                level_history: array
```

##### GET /api/students/{student_id}/badges
```yaml
summary: Get earned badges
description: Returns badges earned by the student
parameters:
  - name: student_id
    in: path
    required: true
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            student_id: string
            total_badges: integer
            badges: array
              - badge_id: integer
                skill_name: string
                earned_date: string
                level_achieved: string
                badge_icon: string
```

---

## Request/Response Patterns

### Standard Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant MW as Middleware
    participant R as Router
    participant V as Validator
    participant S as Service
    participant DB as Database
    participant AI as AI Engine

    C->>MW: HTTP Request
    MW->>MW: CORS Check
    MW->>R: Forward Request

    R->>V: Validate Request
    V->>V: Schema Validation

    alt Invalid Request
        V-->>R: ValidationError
        R-->>C: 400 Bad Request
    else Valid Request
        V->>S: Execute Business Logic

        alt Requires AI
            S->>AI: Process with AI
            AI-->>S: AI Results
        end

        S->>DB: Database Operations
        DB-->>S: Query Results

        S-->>R: Success Response
        R-->>MW: Format Response
        MW-->>C: 200 OK
    end
```

### Error Response Flow

```mermaid
flowchart TD
    Start([Request]) --> MW[Middleware]

    MW --> E1{CORS<br/>Error?}
    E1 -->|Yes| R1[403 Forbidden]
    E1 -->|No| Router

    Router[Router] --> E2{Route<br/>Found?}
    E2 -->|No| R2[404 Not Found]
    E2 -->|Yes| Validator

    Validator[Validator] --> E3{Valid<br/>Schema?}
    E3 -->|No| R3[400 Bad Request]
    E3 -->|Yes| Service

    Service[Service] --> E4{Business<br/>Logic OK?}
    E4 -->|No| R4[422 Unprocessable]
    E4 -->|Yes| Database

    Database[Database] --> E5{DB<br/>Error?}
    E5 -->|Yes| R5[500 Server Error]
    E5 -->|No| Success[200 OK]

    R1 --> End([Error Response])
    R2 --> End
    R3 --> End
    R4 --> End
    R5 --> End
    Success --> End

    style Success fill:#4caf50,color:#fff
    style R1 fill:#f44336,color:#fff
    style R2 fill:#f44336,color:#fff
    style R3 fill:#f44336,color:#fff
    style R4 fill:#f44336,color:#fff
    style R5 fill:#f44336,color:#fff
```

---

## Middleware & Security

### Middleware Stack

```mermaid
graph TB
    Request([Incoming Request]) --> M1[CORS Middleware]

    M1 --> M2[Request Logging]
    M2 --> M3[Rate Limiting]
    M3 --> M4[Authentication]
    M4 --> M5[Request Validation]

    M5 --> Router[Router Handler]

    Router --> M6[Response Formatting]
    M6 --> M7[Response Logging]
    M7 --> M8[Error Handler]

    M8 --> Response([Outgoing Response])

    style Request fill:#4caf50,color:#fff
    style Response fill:#2196f3,color:#fff
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit default
        "http://frontend:8501",   # Docker internal
        "*"                        # Development only
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Security Checklist

```mermaid
mindmap
  root((API<br/>Security))
    Input Validation
      Schema validation
      Type checking
      SQL injection prevention
      XSS protection
    Authentication
      API key validation
      JWT tokens
      Session management
      Role-based access
    Rate Limiting
      Per endpoint limits
      Per client limits
      Burst protection
      DDoS prevention
    Data Protection
      Parameterized queries
      Input sanitization
      Output encoding
      Secrets management
    Logging
      Request logging
      Error logging
      Audit trails
      Security events
```

---

## Error Handling

### Error Response Structure

```python
from pydantic import BaseModel
from typing import Optional, List

class ErrorDetail(BaseModel):
    """Detailed error information."""
    field: Optional[str] = None
    message: str
    type: str

class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    detail: str
    status_code: int
    errors: Optional[List[ErrorDetail]] = None
    timestamp: str
```

### HTTP Status Codes

```mermaid
graph LR
    subgraph "Success 2xx"
        S1[200 OK]
        S2[201 Created]
        S3[204 No Content]
    end

    subgraph "Client Error 4xx"
        C1[400 Bad Request]
        C2[401 Unauthorized]
        C3[403 Forbidden]
        C4[404 Not Found]
        C5[422 Unprocessable]
        C6[429 Too Many Requests]
    end

    subgraph "Server Error 5xx"
        E1[500 Internal Server]
        E2[503 Service Unavailable]
    end

    style S1 fill:#4caf50,color:#fff
    style S2 fill:#4caf50,color:#fff
    style S3 fill:#4caf50,color:#fff
    style C1 fill:#ff9800,color:#fff
    style C2 fill:#ff9800,color:#fff
    style C3 fill:#ff9800,color:#fff
    style C4 fill:#ff9800,color:#fff
    style C5 fill:#ff9800,color:#fff
    style C6 fill:#ff9800,color:#fff
    style E1 fill:#f44336,color:#fff
    style E2 fill:#f44336,color:#fff
```

### Custom Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for all uncaught exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handler for Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Request validation failed",
            "status_code": 422,
            "errors": exc.errors(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

---

## Data Validation

### Pydantic Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, Literal
from datetime import date

class DataEntryRequest(BaseModel):
    """Request model for data ingestion."""

    data_entry_id: str = Field(..., regex=r'^DE[0-9]{3,}$')
    student_id: str = Field(..., regex=r'^S[0-9]{3}$')
    teacher_id: Optional[str] = Field(None, regex=r'^T[0-9]{3}$')
    type: Literal[
        'group_discussion_transcript',
        'peer_tutoring_transcript',
        'project_presentation_transcript',
        'reflection_journal',
        'peer_feedback',
        'teacher_observation_note',
        'parent_note'
    ]
    date: date
    content: str = Field(..., min_length=10)
    metadata: Optional[Dict[str, Any]] = {}

    @validator('content')
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty')
        return v

class AssessmentResponse(BaseModel):
    """Response model for assessments."""

    id: int
    data_entry_id: str
    student_id: str
    skill_name: str
    skill_category: Literal['SEL', 'EF', '21st_Century']
    level: Literal['Emerging', 'Developing', 'Proficient', 'Advanced']
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    justification: str
    source_quote: str
    created_at: str
    corrected: bool = False

class CorrectionRequest(BaseModel):
    """Request model for teacher corrections."""

    assessment_id: int
    corrected_level: Literal['Emerging', 'Developing', 'Proficient', 'Advanced']
    corrected_justification: Optional[str] = None
    teacher_notes: Optional[str] = None
    corrected_by: str = Field(..., regex=r'^T[0-9]{3}$')

    @validator('teacher_notes')
    def notes_required_for_changes(cls, v, values):
        if v is None or not v.strip():
            raise ValueError('Teacher notes required for corrections')
        return v
```

### Validation Flow

```mermaid
flowchart TD
    Start([Request Data]) --> Pydantic[Pydantic Model]

    Pydantic --> V1{Type<br/>Validation}
    V1 -->|Fail| E1[Type Error]
    V1 -->|Pass| V2{Field<br/>Validation}

    V2 -->|Fail| E2[Field Error]
    V2 -->|Pass| V3{Custom<br/>Validators}

    V3 -->|Fail| E3[Validation Error]
    V3 -->|Pass| V4{Business<br/>Rules}

    V4 -->|Fail| E4[Business Logic Error]
    V4 -->|Pass| Valid[Valid Data]

    E1 --> ErrorResponse[422 Response]
    E2 --> ErrorResponse
    E3 --> ErrorResponse
    E4 --> ErrorResponse

    Valid --> Process[Process Request]

    style Valid fill:#4caf50,color:#fff
    style ErrorResponse fill:#f44336,color:#fff
```

---

## Performance Considerations

### Performance Optimization Strategy

```mermaid
mindmap
  root((API<br/>Performance))
    Async Operations
      Async endpoints
      Async database calls
      Concurrent requests
      Background tasks
    Caching
      Response caching
      Query result caching
      Static data caching
      CDN integration
    Database
      Connection pooling
      Query optimization
      Indexing strategy
      Read replicas
    Request Optimization
      Pagination
      Field filtering
      Compression
      Batching
```

### Performance Metrics

| Endpoint Type | Target Latency | Current | Optimization |
|--------------|----------------|---------|--------------|
| Health Check | < 50ms | ~30ms | ✓ Target met |
| Data Ingest | < 5s | ~6s | Async AI calls |
| Assessment Query | < 200ms | ~150ms | ✓ Target met |
| Skill Trends | < 500ms | ~400ms | ✓ Target met |
| Batch Operations | < 10s | ~12s | Parallel processing |

### Caching Strategy

```mermaid
graph TB
    subgraph "Cache Layers"
        L1[Response Cache<br/>Redis]
        L2[Query Cache<br/>PostgreSQL]
        L3[Application Cache<br/>In-Memory]
    end

    subgraph "Cache Policies"
        P1[TTL: 5 minutes]
        P2[LRU Eviction]
        P3[Cache Invalidation]
    end

    Request[API Request] --> Check{Cache<br/>Hit?}

    Check -->|Yes| L1
    Check -->|No| DB[(Database)]

    L1 --> P1
    DB --> P2
    DB --> Update[Update Cache]
    Update --> L1

    Write[Write Operation] --> P3
    P3 --> Invalidate[Clear Cache]

    style L1 fill:#4caf50,color:#fff
    style Check fill:#2196f3,color:#fff
```

---

## Integration Examples

### FastAPI Application Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Initialize FastAPI app
app = FastAPI(
    title="Flourish Skills Tracker API",
    version="1.0.0",
    description="API for AI-powered non-academic skills assessment"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include routers
from routers import data_ingest, assessments, corrections, students

app.include_router(data_ingest.router, prefix="/api/data", tags=["Data"])
app.include_router(assessments.router, prefix="/api/assessments", tags=["Assessments"])
app.include_router(corrections.router, prefix="/api/corrections", tags=["Corrections"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Flourish Skills Tracker API")
    # Initialize database pool
    from database.connection import db_pool
    db_pool.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Flourish Skills Tracker API")
    from database.connection import db_pool
    db_pool.close_all()

@app.get("/")
async def root():
    return {
        "message": "Flourish Skills Tracker API v1.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

**Related Documents:**
- [Main Architecture Overview](./ARCHITECTURE_OVERVIEW.md)
- [Shard 4 Implementation Tasks](../Implementation_Shards/Shard_4_Tasks.md)
- [PRD API Section](../Docs/PRD.md#5-api-endpoints)
