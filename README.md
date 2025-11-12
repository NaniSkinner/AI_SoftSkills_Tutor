# Flourish Skills Tracker

**AI-Powered Soft Skills Assessment for Middle School Students**

A Gauntlet project made with 🍵 by **Nani Skinner**

---

## Overview

Flourish Skills Tracker is an intelligent educational assessment system that helps teachers track and develop students' non-academic skills using AI-powered analysis. The system evaluates 17 key competencies across Social-Emotional Learning (SEL), Executive Function (EF), and 21st Century Skills.

### Key Features

- **AI-Powered Assessment**: GPT-4o analyzes student observations and generates skill assessments
- **Teacher Dashboard**: Review AI assessments, make corrections, assign learning targets
- **Student Dashboard**: Interactive journey map with custom avatars, badges, and progress tracking
- **Human-in-the-Loop Learning**: Teacher corrections improve AI accuracy over time
- **17 Skill Competencies**: Comprehensive coverage of soft skills development
- **4 Proficiency Levels**: Emerging, Developing, Proficient, Advanced

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API key (or OpenRouter key)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI_MS_SoftSkills
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Start services**
   ```bash
   docker-compose up --build
   ```

4. **Access dashboards**
   - Teacher Dashboard: http://localhost:8501
   - Student Dashboard: http://localhost:8501/Student_00_Home
   - API Documentation: http://localhost:8000/docs

For detailed setup instructions, see [QUICK_START.md](Docs/QUICK_START.md)

---

## Documentation

### Core Documentation
- [PRD.md](Docs/PRD.md) - Product Requirements Document
- [QUICK_START.md](Docs/QUICK_START.md) - Setup Guide
- [PROJECT_PROGRESS.md](Docs/PROJECT_PROGRESS.md) - Current Status (75% complete)

### Feature Documentation
- [FEATURE_JOURNEY_MAP.md](Docs/FEATURE_JOURNEY_MAP.md) - Interactive student journey map
- [FEATURE_INTERACTIVE_CONTROLS.md](Docs/FEATURE_INTERACTIVE_CONTROLS.md) - Pan/drag/zoom controls
- [FEATURE_AVATARS.md](Docs/FEATURE_AVATARS.md) - Student avatar system
- [RUBRIC_IMPLEMENTATION.md](Docs/RUBRIC_IMPLEMENTATION.md) - Skill rubric system

### Architecture Documentation
- [ARCHITECTURE_OVERVIEW.md](Architecture/ARCHITECTURE_OVERVIEW.md) - System architecture
- [ARCHITECTURE_DATABASE.md](Architecture/ARCHITECTURE_DATABASE.md) - Database schema
- [ARCHITECTURE_AI.md](Architecture/ARCHITECTURE_AI.md) - AI inference pipeline
- [ARCHITECTURE_API.md](Architecture/ARCHITECTURE_API.md) - Backend API design

---

## Technology Stack

**Frontend**:
- Streamlit 1.31.0 (Python web framework)
- Plotly 5.17.0 (data visualization)
- Custom React components (journey map)

**Backend**:
- FastAPI 0.104.1 (REST API)
- PostgreSQL 15+ (database)
- OpenAI GPT-4o (AI assessment)

**DevOps**:
- Docker & Docker Compose
- Multi-service orchestration

---

## Project Structure

```
AI_MS_SoftSkills/
├── Architecture/          # System architecture documentation (5 files)
├── Docs/                  # Project documentation (13 files)
├── backend/               # Python FastAPI backend
│   ├── ai/               # AI inference engine
│   ├── database/         # Database connection and schema
│   ├── models/           # Pydantic schemas
│   └── routers/          # API endpoints (5 routers)
├── frontend/              # Streamlit dashboards
│   ├── assets/           # Avatars, backgrounds
│   ├── components/       # React components
│   ├── data/             # Skill tips and configuration
│   ├── pages/            # Dashboard pages (8 total)
│   └── utils/            # Helper utilities
├── mock_data/            # Sample student data (32 entries)
├── scripts/              # Data ingestion and testing
├── secrets/              # API keys (not in git)
└── docker-compose.yml    # Service orchestration
```

---

## The 17 Skills

### Social-Emotional Learning (SEL) - 5 Skills
1. Self-Awareness
2. Self-Management
3. Social Awareness
4. Relationship Skills
5. Responsible Decision-Making

### Executive Function (EF) - 8 Skills
6. Working Memory
7. Inhibitory Control
8. Cognitive Flexibility
9. Planning & Prioritization
10. Organization
11. Task Initiation
12. Time Management
13. Metacognition

### 21st Century Skills - 4 Skills
14. Critical Thinking
15. Communication
16. Collaboration
17. Creativity & Innovation

See [RUBRIC_QUICK_REFERENCE.md](Docs/RUBRIC_QUICK_REFERENCE.md) for detailed proficiency descriptors.

---

## Teacher Dashboard

**4 Pages**:
1. **Home** - Overview and navigation
2. **Student Overview** - Grid view of all students with metrics
3. **Skill Trends** - Interactive charts showing skill progression
4. **Assessment Review** - Review and correct AI assessments
5. **Target Assignment** - Set learning goals for students

**Features**:
- Professional earth-tone design
- Inline rubric reference
- Correction workflow with few-shot learning
- Target tracking and completion

---

## Student Dashboard

**4 Pages**:
1. **Home** - Avatar selection (Boy, Girl, Robot, Axolotl)
2. **Journey Map** - Interactive road to skills with pan/zoom controls
3. **Badge Collection** - Bronze, silver, and gold badges
4. **Current Goal** - Active learning target with age-appropriate tips

**Features**:
- Hand-drawn/sketch theme
- Whimsical illustrated background
- Custom avatars with sway animation
- 68 skill tip sets (ages 9-14)
- Google Maps-style navigation

---

## API Endpoints

**15+ REST Endpoints** across 5 routers:

- **Data Ingestion**: `/api/data/ingest`
- **Assessments**: `/api/assessments/*`
- **Corrections**: `/api/corrections/*`
- **Students**: `/api/students/*`
- **Badges**: `/api/badges/*`

View interactive API docs at http://localhost:8000/docs

---

## Database Schema

**8 Tables**:
- `students` - Student profiles
- `teachers` - Teacher accounts
- `data_entries` - Raw observation data
- `assessments` - AI-generated skill assessments
- `teacher_corrections` - Correction feedback
- `skill_targets` - Learning goals
- `badges` - Gamification data
- `few_shot_examples` - AI learning examples

See [ARCHITECTURE_DATABASE.md](Architecture/ARCHITECTURE_DATABASE.md) for complete schema.

---

## Development Status

**Overall Completion**: 75% (6 of 8 shards complete)

**Completed**:
- ✅ Database infrastructure
- ✅ Mock data generation
- ✅ AI inference pipeline
- ✅ Backend API (15+ endpoints)
- ✅ Teacher Dashboard (5 pages)
- ✅ Student Dashboard (4 pages)

**In Progress**:
- ⚠️ Data ingestion (40% - need more skill coverage)
- 🔴 Integration testing (blocked)

See [PROJECT_PROGRESS.md](Docs/PROJECT_PROGRESS.md) for detailed status.

---

## Testing

### Run Data Ingestion
```bash
docker exec -it ai_ms_softskills-backend-1 python scripts/ingest_all_data.py
```

### Validate Data
```bash
docker exec -it ai_ms_softskills-backend-1 python scripts/validate_ingestion.py
```

### Test Workflows
```bash
docker exec -it ai_ms_softskills-backend-1 python scripts/test_correction_workflow.py
docker exec -it ai_ms_softskills-backend-1 python scripts/test_target_workflow.py
```

See [QUICK_TEST_GUIDE.md](Docs/QUICK_TEST_GUIDE.md) for detailed testing procedures.

---

## Configuration

### Environment Variables (.env)
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o
USE_LLM_CONFIDENCE=true

# Database Configuration
POSTGRES_USER=flourish_user
POSTGRES_PASSWORD=flourish_password
POSTGRES_DB=flourish_skills
DATABASE_URL=postgresql://flourish_user:flourish_password@db:5432/flourish_skills
```

### Docker Services
```yaml
services:
  db:        # PostgreSQL on port 5433
  backend:   # FastAPI on port 8000
  frontend:  # Streamlit on port 8501
```

---

## Contributing

This is a Gauntlet project. For questions or contributions, please contact the project owner.

### Development Workflow

1. Make changes in a feature branch
2. Test locally with `docker-compose up`
3. Verify both dashboards work
4. Update documentation if needed
5. Submit pull request

---

## License

All rights reserved. This is a proprietary Gauntlet project.

---

## Credits

**Project**: Gauntlet - Flourish Skills Tracker
**Author**: Nani Skinner
**AI Framework**: OpenAI GPT-4o
**UI Framework**: Streamlit
**Backend**: FastAPI + PostgreSQL

---

## Support

For setup help, see [QUICK_START.md](Docs/QUICK_START.md)

For feature documentation, see [Docs/](Docs/) directory

For technical architecture, see [Architecture/](Architecture/) directory

---

<div align="center">
  <p>A Gauntlet project made with 🍵 by <strong>Nani Skinner</strong></p>
</div>
