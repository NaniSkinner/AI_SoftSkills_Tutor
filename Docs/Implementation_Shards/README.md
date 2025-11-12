# Flourish Skills Tracker - Implementation Shards

## Overview

This directory contains 8 implementation shards that break down the complete MVP into manageable, parallel-executable components. Each shard is a self-contained specification document with clear inputs, outputs, and acceptance criteria.

---

## Shard Dependency Map

```
┌─────────────────────────────────────────────────────────────┐
│                     SHARD DEPENDENCIES                       │
└─────────────────────────────────────────────────────────────┘

DAY 1:
┌──────────────────────────────┐
│ Shard 1: Database &          │  ← START HERE (No dependencies)
│          Infrastructure      │
└──────────────────────────────┘
                │
                ├──────────────────────────────┐
                │                              │
DAY 2-3:        ▼                              ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│ Shard 2: Mock Data       │   │ Shard 3: AI Inference    │
│          Generation      │   │          Pipeline        │
└──────────────────────────┘   └──────────────────────────┘
                │                              │
                └──────────┬───────────────────┘
                           │
DAY 4-5:                   ▼
                ┌──────────────────────────┐
                │ Shard 4: Backend API     │
                └──────────────────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
DAY 6-8:        ▼                     ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│ Shard 5: Teacher         │   │ Shard 6: Student         │
│          Dashboard       │   │          Dashboard       │
└──────────────────────────┘   └──────────────────────────┘
                │                     │
                └──────────┬──────────┘
                           │
DAY 8-9:                   ▼
                ┌──────────────────────────┐
                │ Shard 7: Data Ingestion  │
                │          & Testing       │
                └──────────────────────────┘
                           │
DAY 9-10:                  ▼
                ┌──────────────────────────┐
                │ Shard 8: Integration     │
                │          Testing &       │
                │          Validation      │
                └──────────────────────────┘
```

---

## Shard Summary

| # | Shard Name | Owner | Time | Priority | Files | Key Deliverables |
|---|------------|-------|------|----------|-------|------------------|
| **1** | [Database & Infrastructure](Shard_1_Database_Infrastructure.md) | Backend Engineer | 1 day | P0 | docker-compose.yml, init.sql | PostgreSQL DB, Docker env, 6 tables |
| **2** | [Mock Data Generation](Shard_2_Mock_Data_Generation.md) | Content/Data Engineer | 2 days | P0 | 76 data files, config.json | Realistic transcripts, reflections, notes |
| **3** | [AI Inference Pipeline](Shard_3_AI_Inference_Pipeline.md) | ML/AI Engineer | 2 days | P0 | inference_engine.py, prompts.py | GPT-4o assessment engine, rubric loader |
| **4** | [Backend API Layer](Shard_4_Backend_API.md) | Backend Engineer | 2 days | P0 | main.py, 5 routers | FastAPI with 15+ endpoints |
| **5** | [Teacher Dashboard](Shard_5_Teacher_Dashboard.md) | Frontend Engineer | 2 days | P1 | 4 Streamlit pages | Correction workflow, skill trends, targets |
| **6** | [Student Dashboard](Shard_6_Student_Dashboard.md) | Frontend Engineer | 2 days | P1 | 3 Streamlit pages | Journey map, badges, current goal |
| **7** | [Data Ingestion & Testing](Shard_7_Data_Ingestion_Testing.md) | QA/Integration Engineer | 2 days | P1 | ingestion scripts | Bulk ingest 76 entries, validation |
| **8** | [Integration Testing](Shard_8_Integration_Testing_Validation.md) | QA Lead | 2 days | P1 | test scripts | TAR validation, E2E testing, demo prep |

---

## Implementation Strategy

### Parallel Execution Tracks

**Track A: Data Foundation** (Critical Path)
- Day 1: Shard 1 (Database setup)
- Day 2-3: Shard 2 (Mock data generation)
- Day 8-9: Shard 7 (Data ingestion)

**Track B: AI & Backend** (Critical Path)
- Day 1: (Wait for Shard 1)
- Day 2-4: Shard 3 (AI inference)
- Day 4-5: Shard 4 (Backend API)

**Track C: Teacher Frontend**
- Day 1-5: (Wait for Shard 4)
- Day 6-7: Shard 5 (Teacher dashboard)

**Track D: Student Frontend**
- Day 1-5: (Wait for Shard 4)
- Day 6-8: Shard 6 (Student dashboard)

**Track E: Final Integration**
- Day 9-10: Shard 8 (Integration testing)

### Recommended Team Assignment

**Scenario 1: Solo Developer**
- Follow shards 1→2→3→4→5→6→7→8 sequentially
- Estimated: 14 working days

**Scenario 2: Team of 3**
- **Developer A:** Shards 1, 3, 4 (Backend + AI)
- **Developer B:** Shards 2, 7 (Data + QA)
- **Developer C:** Shards 5, 6 (Frontend)
- **All:** Shard 8 (Integration testing)
- Estimated: 10 working days with parallelization

**Scenario 3: Team of 5+**
- **Backend Engineer:** Shard 1, 4
- **ML Engineer:** Shard 3
- **Content Engineer:** Shard 2
- **Frontend Engineer 1:** Shard 5
- **Frontend Engineer 2:** Shard 6
- **QA Engineer:** Shards 7, 8
- Estimated: 8 working days

---

## Key Decisions Captured in Shards

### From User Clarifications

1. **Database Schema** (Shard 1)
   - ✅ REMOVED unique constraint on `(data_entry_id, skill_name)` - allows multiple assessments per entry
   - ✅ ADDED `starting_level` and `target_level` to `skill_targets` table
   - ✅ ADDED `badges` table with bronze/silver/gold types

2. **Mock Data** (Shard 2)
   - ✅ Use kind, growth-oriented language (no deficit language)
   - ✅ Students can regress/plateau (realistic trajectories)
   - ✅ Skill-specific growth (Eva strong in Communication, weak in Organization)

3. **AI Inference** (Shard 3)
   - ✅ GPT-4o model (not GPT-4-mini) for better quality
   - ✅ Heuristic confidence scoring (not LLM-based for MVP)
   - ✅ Few-shot learning from teacher corrections
   - ✅ Complete rubric from Docs/Rubric.md embedded in system prompt

4. **Badge System** (Shards 4, 5, 6)
   - ✅ Bronze (Developing), Silver (Proficient), Gold (Advanced)
   - ✅ Faded/grayscale badges for Emerging (locked state)
   - ✅ Heroicons open-source SVG icons
   - ✅ Teachers grant badges (not automatic)

5. **Student Dashboard** (Shard 6)
   - ✅ Simple name dropdown (no password for MVP)
   - ✅ Journey map with E → D → P → A progression bars
   - ✅ Celebration animations (st.balloons()) on level advancement

6. **Target Assignment** (Shards 4, 5, 6)
   - ✅ Display format: "Self-Management: **D** → **P**"
   - ✅ Shows starting level and target level explicitly

---

## Quick Start Guide

### Prerequisites
```bash
# Install Docker Desktop
# Get OpenAI API key
# Clone repository
```

### Setup (Following Shard 1)
```bash
# 1. Create project structure
bash scripts/setup_project_structure.sh

# 2. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Start services
docker-compose up -d

# 4. Verify database
docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "SELECT COUNT(*) FROM students;"
# Expected output: 4
```

### Development Workflow

```bash
# Generate mock data (Shard 2)
docker-compose exec backend python scripts/generate_mock_data.py

# Test AI inference (Shard 3)
docker-compose exec backend python scripts/test_inference.py

# Ingest all data (Shard 7)
docker-compose exec backend python scripts/ingest_all_data.py

# Run validation (Shard 8)
docker-compose exec backend python scripts/validate_ingestion.py
docker-compose exec backend python scripts/test_ai_accuracy.py

# Access dashboards
open http://localhost:8501  # Teacher Dashboard
open http://localhost:8000/docs  # API Documentation
```

---

## Testing Checklist

Use this checklist to verify shard completion:

### Shard 1: Database & Infrastructure
- [ ] Docker services start successfully
- [ ] PostgreSQL accessible on port 5432
- [ ] All 6 tables + badges table created
- [ ] Seed data loaded (2 teachers, 4 students)
- [ ] Backend health check passes

### Shard 2: Mock Data Generation
- [ ] 76 data entry files created
- [ ] config.json validates as valid JSON
- [ ] Kind, growth-oriented language used throughout
- [ ] All 4 student archetypes represented
- [ ] All 17 skills have observable markers

### Shard 3: AI Inference Pipeline
- [ ] Rubric loads from Docs/Rubric.md
- [ ] GPT-4o generates valid JSON assessments
- [ ] Confidence scores calculated (0.5-1.0 range)
- [ ] Few-shot manager retrieves corrections
- [ ] Test inference successful

### Shard 4: Backend API
- [ ] All 15+ endpoints functional
- [ ] API docs at /docs
- [ ] Data ingestion triggers AI assessment
- [ ] Badge granting endpoint works
- [ ] Target assignment includes starting_level → target_level

### Shard 5: Teacher Dashboard
- [ ] All 4 pages render without errors
- [ ] Skill trends display progression charts
- [ ] Correction workflow saves to database
- [ ] Badge system displays bronze/silver/gold colors
- [ ] Target assignment shows D → P format

### Shard 6: Student Dashboard
- [ ] Student selection works (name dropdown)
- [ ] Journey map shows progression accurately
- [ ] Badges display with correct colors
- [ ] Faded badges for locked skills
- [ ] Current goal shows starting → target format

### Shard 7: Data Ingestion
- [ ] All 76 entries ingested successfully
- [ ] 300+ assessments generated
- [ ] Validation script passes
- [ ] Performance acceptable (< 3s per entry)

### Shard 8: Integration Testing
- [ ] TAR ≥ 85%
- [ ] All workflows tested end-to-end
- [ ] Performance benchmarks met
- [ ] Data quality checks pass
- [ ] Demo rehearsal successful

---

## Troubleshooting

### Common Issues

**Issue:** Docker services won't start
**Solution:** Check port conflicts (5432, 8000, 8501)
```bash
lsof -i :5432
lsof -i :8000
lsof -i :8501
```

**Issue:** Database connection refused
**Solution:** Wait for PostgreSQL health check
```bash
docker-compose logs db
# Look for "database system is ready to accept connections"
```

**Issue:** OpenAI API rate limits
**Solution:** Increase sleep intervals in ingestion script (Shard 7)

**Issue:** Frontend can't reach backend
**Solution:** Verify BACKEND_URL environment variable
```bash
docker-compose exec frontend env | grep BACKEND_URL
```

---

## Success Metrics

### Technical Metrics
- [ ] TAR (Teacher Agreement Rate) ≥ 85%
- [ ] API response time < 3s
- [ ] Dashboard load time < 3s
- [ ] Zero critical bugs in production
- [ ] All 300+ assessments generated successfully

### Demo Readiness Metrics
- [ ] All 4 student archetypes show realistic growth
- [ ] Teacher correction workflow demonstrates AI improvement
- [ ] Badge system visually appealing and functional
- [ ] Student dashboard engaging (animations, colors)
- [ ] No console errors during demo

---

## Contact & Support

**Project Documentation:**
- PRD: [Docs/PRD.md](../Docs/PRD.md)
- Rubric: [Docs/Rubric.md](../Docs/Rubric.md)
- Curriculum: [Docs/Curriculum.md](../Docs/Curriculum.md)

**Implementation Questions:**
- Refer to specific shard document for technical details
- Check troubleshooting section in each shard
- Review acceptance criteria for completion validation

---

**Last Updated:** November 10, 2025
**Version:** 1.0
**Status:** Ready for Implementation

---

## Next Steps

1. ✅ Review all 8 shard documents
2. ✅ Assign shards to team members (if applicable)
3. → **Start with Shard 1** (Database & Infrastructure)
4. → Follow dependency map for parallel execution
5. → Use acceptance criteria to validate each shard
6. → Complete Shard 8 for final integration testing
7. → Prepare demo presentation

**Ready to build? Start here:** [Shard 1: Database & Infrastructure](Shard_1_Database_Infrastructure.md)
