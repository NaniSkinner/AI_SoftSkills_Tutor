# Flourish Skills Tracker - Implementation Roadmap

**Project:** Middle School Non-Academic Skills Measurement Engine (MVP)
**Timeline:** 10 working days
**Team:** 1-5 engineers
**Budget:** ~$25 (OpenAI GPT-4o API costs)

---

## Executive Summary

The PRD has been sharded into **8 independent implementation documents**, each representing 1-2 days of focused work. The shards are designed for parallel execution where dependencies allow, with a critical path of 10 days for a solo developer or 8 days for a team of 3+.

**Key Decisions Finalized:**
- ✅ **AI Model:** GPT-4o (best quality/cost balance)
- ✅ **Confidence Scoring:** Heuristic approach (fast, transparent)
- ✅ **Badge System:** Bronze/Silver/Gold with faded locked badges
- ✅ **Target Display:** Shows starting_level → target_level (e.g., "D → P")
- ✅ **Mock Data:** 76 entries with kind, growth-oriented language
- ✅ **Database:** Allows multiple assessments per skill per entry (realistic)

---

## Shard Breakdown

### 🔧 **Shard 1: Database & Infrastructure** (Day 1)
**Critical Path Component**

**What It Delivers:**
- Docker Compose environment (PostgreSQL + FastAPI + Streamlit)
- Complete database schema with 7 tables
- Seed data (2 teachers, 4 students)
- Database connection module

**Why It Matters:**
Every other shard depends on this foundation. Sets up the entire development environment.

**Success Criteria:**
```bash
docker-compose up -d
curl http://localhost:8000/health
# Response: {"status": "healthy", "database": "connected"}
```

---

### 📝 **Shard 2: Mock Data Generation** (Days 2-3)
**Critical Path Component**

**What It Delivers:**
- 76 realistic data entries (transcripts, reflections, notes)
- config.json master manifest
- 4 student growth arcs (Eva, Lucas, Pat, Mia)
- Kind, growth-oriented language throughout

**Why It Matters:**
Without authentic data, the AI can't demonstrate its assessment capabilities. This shard creates the "evidence" the system analyzes.

**Success Criteria:**
```bash
find mock_data -name "*.md" -o -name "*.json" | wc -l
# Output: 77 (76 data files + config.json)
```

**Sample Output:**
```
mock_data/transcripts/S001_group_disc_2025-08-15.md
mock_data/reflections/S001_reflection_2025-08-18.md
mock_data/teacher_notes/S001_teacher_obs_2025-08-20.md
...
```

---

### 🤖 **Shard 3: AI Inference Pipeline** (Days 3-4)
**Critical Path Component**

**What It Delivers:**
- GPT-4o powered inference engine
- System prompt with full rubric embedded
- Heuristic confidence scoring
- Few-shot learning manager

**Why It Matters:**
This is the "brain" of the system - the AI that reads student data and generates skill assessments.

**Success Criteria:**
```python
# Test inference
engine.assess_skills(sample_data)
# Returns: [
#   {"skill_name": "Self-Awareness", "level": "Developing", "confidence": 0.85},
#   {"skill_name": "Collaboration", "level": "Proficient", "confidence": 0.90}
# ]
```

---

### 🔌 **Shard 4: Backend API Layer** (Days 4-5)
**Critical Path Component**

**What It Delivers:**
- FastAPI application with 15+ RESTful endpoints
- Data ingestion endpoint (triggers AI)
- Assessment retrieval & correction endpoints
- Badge granting & target assignment endpoints

**Why It Matters:**
Connects the AI engine to the dashboards. The "nervous system" that routes data through the application.

**Success Criteria:**
```bash
open http://localhost:8000/docs
# View interactive API documentation with all endpoints
```

**Key Endpoints:**
- `POST /api/data/ingest` → Analyze student data
- `GET /api/assessments/skill-trends/{student_id}` → Get progression
- `POST /api/corrections/submit` → Teacher feedback loop
- `POST /api/badges/grant` → Award badges

---

### 👩‍🏫 **Shard 5: Teacher Dashboard** (Days 6-7)

**What It Delivers:**
- 4-page Streamlit dashboard
  1. Student Overview (grid view)
  2. Skill Trends (progression charts)
  3. Assessment Review (correction workflow)
  4. Target Assignment (set student goals)

**Why It Matters:**
Demonstrates the human-in-the-loop correction system - teachers validate and improve AI assessments.

**Success Criteria:**
- Teacher can review 20 assessments in < 10 minutes
- Corrections save to database and appear in few-shot examples
- Charts render skill progression (E → D → P → A)

**Visual Highlight:**
![Correction Workflow Mockup]
```
┌─────────────────────────────────────────┐
│ Assessment #47 - Eva - Self-Management  │
│ AI: Developing (78% confidence)         │
│ ┌─────────────────────────────────────┐ │
│ │ Change to: [Proficient ▼]           │ │
│ │ Teacher Notes: [text area]          │ │
│ │ [✓ Approve] [📝 Submit] [⏭️ Skip]   │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

### 🎒 **Shard 6: Student Dashboard** (Days 7-8)

**What It Delivers:**
- 3-page Streamlit dashboard
  1. My Journey Map (animated progression)
  2. Badge Collection (bronze/silver/gold badges)
  3. Current Goal (teacher-assigned target)

**Why It Matters:**
Makes skill development visible and engaging for students. Gamifies non-academic growth.

**Success Criteria:**
- Students see clear visual progression (E → D → P → A)
- Badges display with correct colors (bronze=#CD7F32, silver=#C0C0C0, gold=#FFD700)
- Faded badges shown for locked (Emerging) skills
- Celebration animations trigger on level advancement

**Visual Highlight:**
```
┌──────────────────────────────────────┐
│ 🎒 Eva's Skill Journey               │
├──────────────────────────────────────┤
│ Self-Awareness:                      │
│ E ──→ D ──→ [P] ──→ A               │
│ Aug   Sep   🎉 YOU!  Goal            │
├──────────────────────────────────────┤
│ 🏆 Badge Collection: 3 / 17          │
│ [🥉 Bronze] [🥈 Silver] [🥇 Gold]   │
└──────────────────────────────────────┘
```

---

### 🚀 **Shard 7: Data Ingestion & Testing** (Days 8-9)

**What It Delivers:**
- Bulk ingestion script (processes all 76 entries)
- Validation scripts (check data quality)
- Performance testing
- Database integrity checks

**Why It Matters:**
Populates the system with real data so dashboards come alive. Validates the entire pipeline works end-to-end.

**Success Criteria:**
```bash
python scripts/ingest_all_data.py
# Output:
# ✅ Ingested 76 entries
# ✅ Created 324 assessments
# ✅ All students have data
# ✅ Average time: 2.4s per entry
```

**Expected Results:**
- 76 data entries in `data_entries` table
- 300+ assessments in `assessments` table
- All 17 skills represented
- Mix of Emerging/Developing/Proficient/Advanced levels

---

### ✅ **Shard 8: Integration Testing & Validation** (Days 9-10)

**What It Delivers:**
- TAR (Teacher Agreement Rate) calculation ≥85%
- End-to-end workflow testing
- Performance benchmarks
- Demo preparation checklist

**Why It Matters:**
Proves the system works as intended. Validates AI accuracy and ensures demo-readiness.

**Success Criteria:**
- TAR ≥ 85% (AI matches expected assessments)
- All user workflows functional (teacher correction, badge granting, target assignment)
- Performance targets met (API < 3s, Dashboard < 3s)
- No errors during demo rehearsal

**Test Cases:**
1. Teacher correction workflow (approve/edit/skip)
2. Target assignment & student view
3. Badge granting (bronze/silver/gold)
4. Skill progression tracking (E → D → P → A)

---

## Implementation Timeline

### Solo Developer (14 days)

```
Week 1:
Mon:    Shard 1 (Database setup)
Tue:    Shard 2 (Mock data - Day 1)
Wed:    Shard 2 (Mock data - Day 2)
Thu:    Shard 3 (AI Pipeline - Day 1)
Fri:    Shard 3 (AI Pipeline - Day 2)

Week 2:
Mon:    Shard 4 (Backend API - Day 1)
Tue:    Shard 4 (Backend API - Day 2)
Wed:    Shard 5 (Teacher Dashboard - Day 1)
Thu:    Shard 5 (Teacher Dashboard - Day 2)
Fri:    Shard 6 (Student Dashboard - Day 1)

Week 3:
Mon:    Shard 6 (Student Dashboard - Day 2)
Tue:    Shard 7 (Data Ingestion - Day 1)
Wed:    Shard 7 (Validation - Day 2)
Thu:    Shard 8 (Integration Testing - Day 1)
Fri:    Shard 8 (Demo Prep - Day 2)
```

### Team of 3 (10 days)

```
Developer A (Backend + AI):
Days 1-5:   Shards 1, 3, 4
Days 6-10:  Support integration testing

Developer B (Data + QA):
Days 1-3:   Shard 2 (Mock data)
Days 4-5:   Wait / Documentation
Days 6-8:   Shard 7 (Ingestion)
Days 9-10:  Shard 8 (Testing)

Developer C (Frontend):
Days 1-5:   Wait for API (or start UI mockups)
Days 6-8:   Shards 5 & 6 (Dashboards)
Days 9-10:  Shard 8 (Testing)
```

---

## Resource Requirements

### Software/Tools
- **Docker Desktop** (required)
- **OpenAI API Key** (required, ~$25 budget)
- **Code Editor** (VS Code recommended)
- **PostgreSQL Client** (optional, for debugging)
- **Postman/Insomnia** (optional, for API testing)

### Skills Needed
- **Python 3.11+** (FastAPI, Streamlit)
- **PostgreSQL** (SQL queries, schema design)
- **Docker** (container orchestration)
- **LLM Prompt Engineering** (for AI accuracy)
- **Frontend basics** (Streamlit, Plotly)

### Team Composition (Ideal)
- 1x Backend Engineer (Shards 1, 4)
- 1x ML Engineer (Shard 3)
- 1x Content Engineer (Shard 2)
- 1x Frontend Engineer (Shards 5, 6)
- 1x QA Engineer (Shards 7, 8)

---

## Risk Mitigation

### High Risk: AI Accuracy (TAR < 85%)
**Mitigation:**
- Use GPT-4o (not mini) for better quality
- Embed complete rubric in system prompt
- Implement few-shot learning from teacher corrections
- Allow multiple rounds of prompt tuning

### Medium Risk: OpenAI Rate Limits
**Mitigation:**
- Add sleep intervals in ingestion script (5-10s per request)
- Process data in batches
- Monitor API usage dashboard

### Medium Risk: Mock Data Quality
**Mitigation:**
- Use rubric behavioral indicators as guide
- Have content reviewed by educator
- Include validation script for language check

### Low Risk: Docker Environment Issues
**Mitigation:**
- Provide clear setup instructions
- Include health checks in docker-compose
- Document common troubleshooting steps

---

## Success Metrics

### Technical Metrics
| Metric | Target | Shard |
|--------|--------|-------|
| TAR (Teacher Agreement Rate) | ≥85% | Shard 8 |
| API Response Time | <3s | Shard 4, 7 |
| Dashboard Load Time | <3s | Shard 5, 6 |
| Total Assessments Generated | ≥300 | Shard 7 |
| Data Quality (No Nulls) | 100% | Shard 7 |

### Demo Metrics
| Criterion | Status | Verified By |
|-----------|--------|-------------|
| All 4 students show growth | ✅ | Shard 8 |
| Teacher correction workflow works | ✅ | Shard 5, 8 |
| Badge system visually appealing | ✅ | Shard 6, 8 |
| Student dashboard engaging | ✅ | Shard 6, 8 |
| No console errors | ✅ | Shard 8 |

---

## Quick Reference Card

### Start Here
```bash
# 1. Setup environment
cd Gauntlet/AI_MS_SoftSkills
cp .env.example .env
# Add OPENAI_API_KEY to .env

# 2. Start services
docker-compose up -d

# 3. Verify setup
curl http://localhost:8000/health
```

### Development Commands
```bash
# Generate mock data
docker-compose exec backend python scripts/generate_mock_data.py

# Ingest data
docker-compose exec backend python scripts/ingest_all_data.py

# Run tests
docker-compose exec backend python scripts/test_ai_accuracy.py

# View dashboards
open http://localhost:8501
open http://localhost:8000/docs
```

### Troubleshooting
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Restart services
docker-compose restart

# Full reset
docker-compose down -v
docker-compose up -d
```

---

## Next Steps

1. **Read:** [Implementation_Shards/README.md](README.md) - Detailed shard overview
2. **Start:** [Shard_1_Database_Infrastructure.md](Shard_1_Database_Infrastructure.md) - Begin implementation
3. **Follow:** Dependency map for parallel execution
4. **Validate:** Use acceptance criteria at end of each shard
5. **Test:** Complete Shard 8 for final integration testing
6. **Demo:** Prepare presentation showcasing all workflows

---

**Document Version:** 1.0
**Last Updated:** November 10, 2025
**Status:** ✅ Ready for Implementation

**Let's build something amazing!** 🚀
