# Flourish Skills Tracker - Architecture Overview

**Project:** Middle School Non-Academic Skills Measurement Engine
**Version:** 1.0 (MVP)
**Date:** November 10, 2025
**Organization:** Flourish Schools

---

## Table of Contents

1. [System Architecture Overview](#system-architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Component Architecture](#component-architecture)
4. [Data Flow Architecture](#data-flow-architecture)
5. [Database Architecture](#database-architecture)
6. [AI Pipeline Architecture](#ai-pipeline-architecture)
7. [API Architecture](#api-architecture)
8. [Frontend Architecture](#frontend-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Security Architecture](#security-architecture)

---

## System Architecture Overview

The Flourish Skills Tracker is a microservices-based application that uses AI to assess student non-academic skills through analysis of various data sources (transcripts, reflections, feedback). The system implements a human-in-the-loop approach with teacher validation.

```mermaid
graph TB
    subgraph "Client Layer"
        TD[Teacher Dashboard<br/>Streamlit]
        SD[Student Dashboard<br/>Streamlit]
    end

    subgraph "API Layer"
        API[FastAPI Backend<br/>Port 8000]
    end

    subgraph "Processing Layer"
        AI[AI Inference Engine<br/>OpenAI GPT-4]
        FSM[Few-Shot Manager]
        DI[Data Ingestion Service]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL 15+<br/>Port 5432)]
        MD[Mock Data<br/>JSON/Markdown]
    end

    TD -->|HTTP/REST| API
    SD -->|HTTP/REST| API
    API --> DI
    API --> AI
    API --> FSM
    DI --> DB
    AI --> DB
    FSM --> DB
    MD -.->|Seed Data| DB
    AI -.->|LLM Calls| OpenAI[OpenAI API]

    classDef frontend fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef backend fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef data fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef ai fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px

    class TD,SD frontend
    class API,DI backend
    class DB,MD data
    class AI,FSM,OpenAI ai
```

---

## Technology Stack

### Core Technologies

```mermaid
graph LR
    subgraph "Backend"
        B1[Python 3.11+]
        B2[FastAPI 0.104+]
        B3[Uvicorn ASGI Server]
        B4[Pydantic 2.5+]
    end

    subgraph "Database"
        D1[PostgreSQL 15+]
        D2[psycopg2-binary]
    end

    subgraph "AI/ML"
        A1[OpenAI API]
        A2[GPT-4 Model]
        A3[Context Engineering]
    end

    subgraph "Frontend"
        F1[Streamlit 1.28+]
        F2[Plotly 5.17+]
        F3[Pandas 2.1+]
    end

    subgraph "DevOps"
        O1[Docker]
        O2[Docker Compose]
        O3[Python venv]
    end

    style B1 fill:#3776ab,color:#fff
    style D1 fill:#336791,color:#fff
    style A1 fill:#412991,color:#fff
    style F1 fill:#ff4b4b,color:#fff
    style O1 fill:#2496ed,color:#fff
```

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend API** | FastAPI | 0.104.1+ | RESTful API framework |
| **Database** | PostgreSQL | 15+ | Relational data storage |
| **AI Engine** | OpenAI GPT-4 | Latest | LLM-based skill inference |
| **Frontend** | Streamlit | 1.28+ | Rapid UI prototyping |
| **Containerization** | Docker | Latest | Development environment |
| **Language** | Python | 3.11+ | Primary programming language |

---

## Component Architecture

### High-Level Component Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        TC[Teacher Components]
        SC[Student Components]

        TC --> TO[Overview Page]
        TC --> TT[Skill Trends]
        TC --> TR[Assessment Review]
        TC --> TA[Target Assignment]

        SC --> SJ[Journey Map]
        SC --> SB[Badge Collection]
        SC --> SG[Current Goal]
    end

    subgraph "API Gateway Layer"
        AG[FastAPI Application]
        MW[CORS Middleware]

        AG --> MW
    end

    subgraph "Business Logic Layer"
        DIG[Data Ingest Router]
        ASR[Assessments Router]
        COR[Corrections Router]
        STR[Students Router]
    end

    subgraph "AI Processing Layer"
        IE[Inference Engine]
        FSL[Few-Shot Learner]
        RL[Rubric Loader]
        CS[Confidence Scorer]
    end

    subgraph "Data Access Layer"
        DBC[DB Connection Pool]
        QE[Query Executor]
        TM[Transaction Manager]
    end

    subgraph "Data Storage Layer"
        PG[(PostgreSQL)]

        PG --> ST[students]
        PG --> TCH[teachers]
        PG --> DE[data_entries]
        PG --> AS[assessments]
        PG --> TC[teacher_corrections]
        PG --> SKT[skill_targets]
    end

    TC --> AG
    SC --> AG
    AG --> DIG
    AG --> ASR
    AG --> COR
    AG --> STR

    DIG --> IE
    ASR --> FSL
    COR --> FSL

    IE --> RL
    IE --> CS
    FSL --> RL

    DIG --> DBC
    ASR --> DBC
    COR --> DBC
    STR --> DBC

    DBC --> QE
    QE --> TM
    TM --> PG

    classDef presentation fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef api fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef business fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef ai fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef data fill:#fce4ec,stroke:#c2185b,stroke-width:2px

    class TC,SC,TO,TT,TR,TA,SJ,SB,SG presentation
    class AG,MW api
    class DIG,ASR,COR,STR business
    class IE,FSL,RL,CS ai
    class DBC,QE,TM,PG,ST,TCH,DE,AS,TC,SKT data
```

---

## Data Flow Architecture

### End-to-End Data Flow

```mermaid
sequenceDiagram
    participant MD as Mock Data
    participant DI as Data Ingestion
    participant DB as PostgreSQL
    participant AI as AI Engine
    participant API as FastAPI
    participant TD as Teacher Dashboard
    participant SD as Student Dashboard

    Note over MD,SD: Initial Data Ingestion Flow
    MD->>DI: Load mock data entries
    DI->>DB: Insert data_entries
    DI->>AI: Trigger skill assessment
    AI->>AI: Process with GPT-4 + Rubric
    AI->>DB: Store assessments

    Note over MD,SD: Teacher Review Flow
    TD->>API: Request pending assessments
    API->>DB: Query assessments (corrected=false)
    DB-->>API: Return assessments
    API-->>TD: Display assessments
    TD->>API: Submit correction
    API->>DB: Store teacher_corrections
    API->>AI: Update few-shot examples

    Note over MD,SD: Student View Flow
    SD->>API: Request student progress
    API->>DB: Query assessments + targets
    DB-->>API: Aggregate skill levels
    API-->>SD: Display journey map

    Note over MD,SD: Continuous Improvement Loop
    AI->>DB: Fetch recent corrections
    DB-->>AI: Return few-shot examples
    AI->>AI: Update prompt context
    AI->>DB: Generate improved assessments
```

### Assessment Generation Pipeline

```mermaid
flowchart TD
    Start([Data Entry]) --> Parse[Parse Content]
    Parse --> Validate{Valid<br/>Format?}
    Validate -->|No| Error[Return Error]
    Validate -->|Yes| LoadRubric[Load Rubric]
    LoadRubric --> LoadFewShot[Load Few-Shot Examples]
    LoadFewShot --> BuildPrompt[Build System Prompt]
    BuildPrompt --> CallGPT[Call GPT-4 API]
    CallGPT --> ParseResponse[Parse JSON Response]
    ParseResponse --> ValidateSkills{All Skills<br/>Valid?}
    ValidateSkills -->|No| FilterInvalid[Filter Invalid Skills]
    ValidateSkills -->|Yes| CalcConfidence[Calculate Confidence Scores]
    FilterInvalid --> CalcConfidence
    CalcConfidence --> StoreDB[Store in Database]
    StoreDB --> End([Return Assessment IDs])

    Error --> End

    style Start fill:#4caf50,color:#fff
    style End fill:#2196f3,color:#fff
    style Error fill:#f44336,color:#fff
    style CallGPT fill:#9c27b0,color:#fff
```

---

## Database Architecture

### Entity Relationship Diagram

```mermaid
erDiagram
    teachers ||--o{ students : teaches
    teachers ||--o{ data_entries : creates
    teachers ||--o{ teacher_corrections : makes
    teachers ||--o{ skill_targets : assigns

    students ||--o{ data_entries : has
    students ||--o{ assessments : receives
    students ||--o{ skill_targets : assigned

    data_entries ||--o{ assessments : generates

    assessments ||--o| teacher_corrections : corrected_by

    teachers {
        varchar id PK
        varchar name
        varchar email
        timestamp created_at
    }

    students {
        varchar id PK
        varchar name
        integer grade
        varchar teacher_id FK
        timestamp created_at
    }

    data_entries {
        varchar id PK
        varchar student_id FK
        varchar teacher_id FK
        varchar type
        date date
        text content
        jsonb metadata
        timestamp created_at
    }

    assessments {
        serial id PK
        varchar data_entry_id FK
        varchar student_id FK
        varchar skill_name
        varchar skill_category
        varchar level
        decimal confidence_score
        text justification
        text source_quote
        integer data_point_count
        varchar rubric_version
        timestamp created_at
        timestamp updated_at
    }

    teacher_corrections {
        serial id PK
        integer assessment_id FK
        varchar original_level
        varchar corrected_level
        text original_justification
        text corrected_justification
        text teacher_notes
        varchar corrected_by FK
        timestamp corrected_at
    }

    skill_targets {
        serial id PK
        varchar student_id FK
        varchar skill_name
        varchar assigned_by FK
        timestamp assigned_at
        boolean completed
        timestamp completed_at
    }
```

### Database Schema Details

For detailed database schema including indexes, constraints, and optimization strategies, see [ARCHITECTURE_DATABASE.md](./ARCHITECTURE_DATABASE.md)

---

## AI Pipeline Architecture

### AI Inference Engine Components

```mermaid
graph TB
    subgraph "Input Processing"
        I1[Data Entry Content]
        I2[Metadata Context]
        I3[Historical Data]
    end

    subgraph "Context Assembly"
        C1[System Prompt Builder]
        C2[Rubric Injector]
        C3[Few-Shot Example Selector]
        C4[User Prompt Constructor]
    end

    subgraph "LLM Processing"
        L1[OpenAI API Client]
        L2[GPT-4 Model]
        L3[Temperature: 0.3]
        L4[Max Tokens: 3000]
    end

    subgraph "Response Processing"
        R1[JSON Parser]
        R2[Schema Validator]
        R3[Confidence Calculator]
        R4[Quality Filter]
    end

    subgraph "Output Storage"
        O1[Assessment Records]
        O2[Confidence Scores]
        O3[Source Quotes]
        O4[Justifications]
    end

    I1 --> C4
    I2 --> C4
    I3 --> C3

    C1 --> L1
    C2 --> C1
    C3 --> C1
    C4 --> L1

    L1 --> L2
    L2 --> L3
    L3 --> L4

    L4 --> R1
    R1 --> R2
    R2 --> R3
    R3 --> R4

    R4 --> O1
    R4 --> O2
    R4 --> O3
    R4 --> O4

    style L2 fill:#9c27b0,color:#fff
    style R4 fill:#4caf50,color:#fff
```

### Few-Shot Learning Loop

```mermaid
flowchart LR
    A[Initial AI Assessment] --> B[Teacher Reviews]
    B --> C{Agrees?}
    C -->|Yes| D[Approve]
    C -->|No| E[Submit Correction]
    E --> F[Store Correction]
    F --> G[Add to Few-Shot Pool]
    G --> H[Select Top 5 Recent]
    H --> I[Update System Prompt]
    I --> A
    D --> J[Mark as Validated]

    style E fill:#ff9800,color:#fff
    style G fill:#4caf50,color:#fff
    style I fill:#2196f3,color:#fff
```

For detailed AI architecture including prompt engineering and model optimization, see [ARCHITECTURE_AI.md](./ARCHITECTURE_AI.md)

---

## API Architecture

### API Endpoint Structure

```mermaid
graph TB
    subgraph "API Gateway"
        Root[/ Root Endpoint]
        Health[/health Health Check]
    end

    subgraph "Data Management"
        DI[/api/data/ingest<br/>POST]
        DB[/api/data/batch<br/>POST]
    end

    subgraph "Assessment Endpoints"
        AS[/api/assessments/student/:id<br/>GET]
        AT[/api/assessments/skill-trends/:id<br/>GET]
        AP[/api/assessments/pending<br/>GET]
        AA[/api/assessments/:id/approve<br/>POST]
    end

    subgraph "Correction Endpoints"
        CS[/api/corrections/submit<br/>POST]
        CG[/api/corrections/history/:id<br/>GET]
    end

    subgraph "Student Endpoints"
        SL[/api/students<br/>GET]
        SG[/api/students/:id<br/>GET]
        SP[/api/students/:id/progress<br/>GET]
        SB[/api/students/:id/badges<br/>GET]
        ST[/api/students/:id/target-skill<br/>POST]
    end

    Root --> Health

    DI --> Ingest[Data Ingest Service]
    DB --> Ingest

    AS --> Query[Query Service]
    AT --> Trend[Trend Analysis]
    AP --> Review[Review Service]
    AA --> Approve[Approval Service]

    CS --> Correction[Correction Service]
    CG --> History[History Service]

    SL --> Student[Student Service]
    SG --> Student
    SP --> Progress[Progress Service]
    SB --> Badge[Badge Service]
    ST --> Target[Target Service]

    classDef gateway fill:#e1f5ff,stroke:#01579b
    classDef data fill:#fff3e0,stroke:#e65100
    classDef assessment fill:#f3e5f5,stroke:#4a148c
    classDef correction fill:#e8f5e9,stroke:#1b5e20
    classDef student fill:#fce4ec,stroke:#c2185b

    class Root,Health gateway
    class DI,DB data
    class AS,AT,AP,AA assessment
    class CS,CG correction
    class SL,SG,SP,SB,ST student
```

### Request/Response Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant M as CORS Middleware
    participant R as Router
    participant S as Service Layer
    participant D as Database
    participant A as AI Engine

    C->>M: HTTP Request
    M->>M: Validate CORS
    M->>R: Forward Request
    R->>R: Validate Route
    R->>S: Execute Business Logic

    alt Data Ingestion
        S->>D: Store Data Entry
        S->>A: Trigger Assessment
        A->>D: Store Assessments
        D-->>S: Return IDs
    else Query Operation
        S->>D: Execute Query
        D-->>S: Return Results
    end

    S-->>R: Return Response
    R-->>M: Format Response
    M-->>C: HTTP Response
```

For detailed API specifications including all endpoints and schemas, see [ARCHITECTURE_API.md](./ARCHITECTURE_API.md)

---

## Frontend Architecture

### Dashboard Component Structure

```mermaid
graph TB
    subgraph "Teacher Dashboard"
        TH[Home.py<br/>Main Entry]

        TH --> T1[01_Student_Overview.py]
        TH --> T2[02_Skill_Trends.py]
        TH --> T3[03_Assessment_Review.py]
        TH --> T4[04_Target_Assignment.py]

        T1 --> TU1[Student Cards]
        T1 --> TU2[Growth Indicators]

        T2 --> TU3[Trend Charts]
        T2 --> TU4[Timeline Views]

        T3 --> TU5[Assessment List]
        T3 --> TU6[Correction Form]
        T3 --> TU7[Rubric Reference]

        T4 --> TU8[Target Selector]
        T4 --> TU9[Suggestion Engine]
    end

    subgraph "Student Dashboard"
        SH[Student_Home.py]

        SH --> S1[Student_01_Journey_Map.py]
        SH --> S2[Student_02_Badge_Collection.py]
        SH --> S3[Student_03_Current_Goal.py]

        S1 --> SU1[Progress Bars]
        S1 --> SU2[Level Indicators]

        S2 --> SU3[Badge Grid]
        S2 --> SU4[Achievement Display]

        S3 --> SU5[Goal Card]
        S3 --> SU6[Tips Display]
    end

    subgraph "Shared Utilities"
        U1[api_client.py<br/>Backend API Wrapper]
        U2[chart_helpers.py<br/>Visualization Utils]
        U3[session_manager.py<br/>State Management]
    end

    TU1 --> U1
    TU3 --> U2
    SU1 --> U2
    T3 --> U3
    S1 --> U3

    classDef teacher fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef student fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef shared fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px

    class TH,T1,T2,T3,T4,TU1,TU2,TU3,TU4,TU5,TU6,TU7,TU8,TU9 teacher
    class SH,S1,S2,S3,SU1,SU2,SU3,SU4,SU5,SU6 student
    class U1,U2,U3 shared
```

### UI State Management

```mermaid
stateDiagram-v2
    [*] --> Login
    Login --> TeacherDashboard: Teacher Login
    Login --> StudentDashboard: Student Login

    state TeacherDashboard {
        [*] --> Overview
        Overview --> SkillTrends: Select Student
        SkillTrends --> AssessmentReview: Review Needed
        AssessmentReview --> TargetAssignment: After Correction
        TargetAssignment --> Overview: Assign Complete

        SkillTrends --> Overview: Back
        AssessmentReview --> Overview: Back
    }

    state StudentDashboard {
        [*] --> JourneyMap
        JourneyMap --> BadgeCollection: View Badges
        BadgeCollection --> CurrentGoal: Check Goal
        CurrentGoal --> JourneyMap: Back to Journey
    }

    TeacherDashboard --> [*]: Logout
    StudentDashboard --> [*]: Logout
```

For detailed frontend architecture including component specifications, see [ARCHITECTURE_FRONTEND.md](./ARCHITECTURE_FRONTEND.md)

---

## Deployment Architecture

### Docker Compose Architecture

```mermaid
graph TB
    subgraph "Docker Host"
        subgraph "Frontend Container"
            F[Streamlit App<br/>Port 8501]
            FV[/app Volume Mount]
        end

        subgraph "Backend Container"
            B[FastAPI App<br/>Port 8000]
            BV1[/app Volume Mount]
            BV2[/mock_data Volume Mount]
        end

        subgraph "Database Container"
            D[(PostgreSQL 15<br/>Port 5432)]
            DV[postgres_data Volume]
        end

        subgraph "External Services"
            O[OpenAI API<br/>HTTPS]
        end
    end

    F -->|HTTP| B
    B -->|TCP| D
    B -.->|HTTPS| O

    FV -.->|Source Code| F
    BV1 -.->|Source Code| B
    BV2 -.->|Mock Data| B
    DV -.->|Persistent Data| D

    style F fill:#ff4b4b,color:#fff
    style B fill:#009688,color:#fff
    style D fill:#336791,color:#fff
    style O fill:#412991,color:#fff
```

### Environment Configuration

```mermaid
flowchart LR
    ENV[.env File] --> E1[OPENAI_API_KEY]
    ENV --> E2[DATABASE_URL]
    ENV --> E3[POSTGRES_USER]
    ENV --> E4[POSTGRES_PASSWORD]
    ENV --> E5[POSTGRES_DB]

    E1 --> BC[Backend Container]
    E2 --> BC
    E3 --> DC[Database Container]
    E4 --> DC
    E5 --> DC

    BC --> BA[Backend Application]
    DC --> DB[(PostgreSQL)]

    style ENV fill:#ffeb3b,color:#000
    style BC fill:#4caf50,color:#fff
    style DC fill:#2196f3,color:#fff
```

### Network Architecture

```mermaid
graph LR
    subgraph "Host Network"
        H[Host Machine<br/>localhost]
    end

    subgraph "Docker Network (default)"
        F[frontend<br/>container]
        B[backend<br/>container]
        D[db<br/>container]
    end

    H -->|Port 8501| F
    H -->|Port 8000| B
    H -->|Port 5432| D

    F -->|backend:8000| B
    B -->|db:5432| D

    style H fill:#9e9e9e,color:#fff
    style F fill:#ff4b4b,color:#fff
    style B fill:#009688,color:#fff
    style D fill:#336791,color:#fff
```

For detailed deployment configurations and scaling strategies, see [ARCHITECTURE_DEPLOYMENT.md](./ARCHITECTURE_DEPLOYMENT.md)

---

## Security Architecture

### Security Layers

```mermaid
graph TB
    subgraph "Application Security"
        A1[Input Validation]
        A2[SQL Injection Prevention]
        A3[XSS Protection]
        A4[CORS Configuration]
    end

    subgraph "API Security"
        AP1[Rate Limiting]
        AP2[Request Validation]
        AP3[Response Sanitization]
    end

    subgraph "Data Security"
        D1[Database Connection Pooling]
        D2[Prepared Statements]
        D3[Encrypted Connections]
    end

    subgraph "Secrets Management"
        S1[Environment Variables]
        S2[API Key Protection]
        S3[No Hardcoded Secrets]
    end

    subgraph "External API Security"
        E1[OpenAI API Key]
        E2[HTTPS Only]
        E3[Error Handling]
    end

    A1 --> AP2
    A2 --> D2
    A3 --> AP3
    A4 --> AP1

    S1 --> E1
    S2 --> E1
    E1 --> E2

    D1 --> D3
    D2 --> D3

    classDef app fill:#e3f2fd,stroke:#1565c0
    classDef api fill:#fff3e0,stroke:#ef6c00
    classDef data fill:#f3e5f5,stroke:#6a1b9a
    classDef secrets fill:#ffebee,stroke:#c62828
    classDef external fill:#e8f5e9,stroke:#2e7d32

    class A1,A2,A3,A4 app
    class AP1,AP2,AP3 api
    class D1,D2,D3 data
    class S1,S2,S3 secrets
    class E1,E2,E3 external
```

### Data Flow Security

```mermaid
sequenceDiagram
    participant U as User/Client
    participant F as Frontend
    participant M as CORS Middleware
    participant B as Backend API
    participant V as Validator
    participant D as Database
    participant A as OpenAI API

    U->>F: User Input
    F->>F: Client-side Validation
    F->>M: HTTPS Request
    M->>M: Validate Origin
    M->>B: Forward Request
    B->>V: Validate Schema
    V->>V: Sanitize Input
    V->>D: Prepared Statement
    D-->>V: Query Result
    V->>V: Sanitize Output
    V-->>B: Safe Response

    opt AI Processing
        B->>A: API Call (Encrypted)
        A-->>B: AI Response
        B->>B: Validate Response
    end

    B-->>M: JSON Response
    M-->>F: HTTPS Response
    F->>F: Sanitize Display
    F-->>U: Rendered UI

    Note over U,A: All communication over HTTPS/TLS
```

---

## Implementation Shard Mapping

This architecture is implemented through the following shards:

| Shard | Component Coverage | Architecture Document |
|-------|-------------------|----------------------|
| **Shard 1** | Database Infrastructure | [ARCHITECTURE_DATABASE.md](./ARCHITECTURE_DATABASE.md) |
| **Shard 2** | Mock Data Generation | [ARCHITECTURE_DATA_GENERATION.md](./ARCHITECTURE_DATA_GENERATION.md) |
| **Shard 3** | AI Inference Pipeline | [ARCHITECTURE_AI.md](./ARCHITECTURE_AI.md) |
| **Shard 4** | Backend API | [ARCHITECTURE_API.md](./ARCHITECTURE_API.md) |
| **Shard 5** | Teacher Dashboard | [ARCHITECTURE_FRONTEND_TEACHER.md](./ARCHITECTURE_FRONTEND_TEACHER.md) |
| **Shard 6** | Student Dashboard | [ARCHITECTURE_FRONTEND_STUDENT.md](./ARCHITECTURE_FRONTEND_STUDENT.md) |
| **Shard 7** | Data Ingestion & Testing | [ARCHITECTURE_TESTING.md](./ARCHITECTURE_TESTING.md) |
| **Shard 8** | Integration & Validation | [ARCHITECTURE_INTEGRATION.md](./ARCHITECTURE_INTEGRATION.md) |

---

## Key Architectural Decisions

### 1. Microservices vs Monolithic
**Decision:** Modular monolith with clear separation of concerns
**Rationale:**
- MVP scope allows for single deployment
- Clear module boundaries enable future microservices split
- Simplified development and debugging

### 2. Streamlit vs React
**Decision:** Streamlit for MVP frontend
**Rationale:**
- 80% faster development time
- Python-native integration with backend
- Sufficient for demo and validation
- Can be replaced with React for production

### 3. Context Engineering vs Fine-Tuning
**Decision:** Context engineering with few-shot learning
**Rationale:**
- No labeled training data available initially
- More flexible and faster to iterate
- Teacher corrections build training dataset over time
- Can transition to fine-tuning with sufficient data

### 4. PostgreSQL vs NoSQL
**Decision:** PostgreSQL relational database
**Rationale:**
- Structured data with clear relationships
- Complex queries for trend analysis
- ACID compliance for corrections
- Mature ecosystem and tooling

### 5. Docker vs Cloud Deployment
**Decision:** Docker Compose for MVP
**Rationale:**
- Faster local development setup
- Lower costs for initial development
- Easier debugging and iteration
- Clear path to Kubernetes/cloud deployment

---

## Performance Considerations

### Target Metrics

| Metric | Target | Monitoring |
|--------|--------|-----------|
| API Response Time | < 2s | FastAPI logging |
| Assessment Generation | < 5s per entry | OpenAI API timing |
| Database Query | < 500ms | PostgreSQL EXPLAIN |
| Dashboard Load | < 3s | Streamlit profiling |
| Teacher Agreement Rate | ≥ 85% | Manual validation |

### Optimization Strategies

```mermaid
mindmap
  root((Performance<br/>Optimization))
    Database
      Connection Pooling
      Query Indexing
      Materialized Views
      Caching Layer
    API
      Response Compression
      Async Processing
      Rate Limiting
      Batch Endpoints
    AI Pipeline
      Prompt Optimization
      Batch Inference
      Response Caching
      Temperature Tuning
    Frontend
      Lazy Loading
      Data Pagination
      Chart Optimization
      Session Caching
```

---

## Scalability Roadmap

### MVP → Production Evolution

```mermaid
graph LR
    MVP[MVP<br/>Docker Compose] --> V2[Version 2<br/>Cloud Deploy]
    V2 --> V3[Version 3<br/>Microservices]

    MVP -.->|Features| M1[4 Students<br/>Mock Data]
    V2 -.->|Features| M2[100+ Students<br/>Real Data]
    V3 -.->|Features| M3[1000+ Students<br/>Multi-School]

    MVP -.->|Tech| T1[Streamlit<br/>Local DB]
    V2 -.->|Tech| T2[React<br/>Cloud DB]
    V3 -.->|Tech| T3[React<br/>Distributed]

    style MVP fill:#ffeb3b,color:#000
    style V2 fill:#ff9800,color:#fff
    style V3 fill:#f44336,color:#fff
```

---

## Appendix: System Diagrams

### Project Structure

```
flourish-skills-tracker/
├── backend/                    # FastAPI backend application
│   ├── ai/                    # AI inference components
│   ├── database/              # Database schemas & connections
│   ├── routers/               # API endpoint routers
│   └── models/                # Pydantic data models
├── frontend/                  # Streamlit dashboard applications
│   ├── pages/                 # Dashboard page components
│   └── utils/                 # Shared utilities
├── mock_data/                 # Mock data for MVP
├── scripts/                   # Utility scripts
├── Architecture/              # Architecture documentation (this folder)
└── Implementation_Shards/     # Implementation task breakdown
```

---

## Contact & Documentation

**Project Documentation:**
- Architecture Overview (this document)
- [Implementation Roadmap](../Implementation_Shards/IMPLEMENTATION_ROADMAP.md)
- [Master Task Tracker](../Implementation_Shards/MASTER_TASK_TRACKER.md)
- [Product Requirements Document](../Docs/PRD.md)

**For detailed component architecture, refer to the specific architecture documents listed in the Implementation Shard Mapping section above.**

---

**Document Version:** 1.0
**Last Updated:** November 10, 2025
**Maintained By:** Flourish Schools Engineering Team
