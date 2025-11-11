# Quick Start Guide - Flourish Skills Tracker MVP

**Ready to build?** Follow these steps to get started immediately.

---

## ⚡ 5-Minute Setup

### Prerequisites
- [ ] Docker Desktop installed
- [ ] OpenAI API key ready
- [ ] Terminal open

### Setup Commands
```bash
# 1. Navigate to project
cd /Users/nanis/dev/Gauntlet/AI_MS_SoftSkills

# 2. Create environment file
cp .env.example .env

# 3. Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# 4. Start all services
docker-compose up -d

# 5. Verify setup
curl http://localhost:8000/health
# Expected: {"status": "healthy", "database": "connected"}

# 6. Open dashboards
open http://localhost:8501  # Teacher Dashboard
open http://localhost:8000/docs  # API Documentation
```

---

## 📋 Your Implementation Path

### **Current Task:** Shard 1 - Database & Infrastructure

**Open your task file:**
```bash
open Implementation_Shards/Shard_1_Tasks.md
```

**Start with:**
1. ✅ Project structure setup
2. ✅ Create docker-compose.yml
3. ✅ Create database schema (init.sql)
4. ✅ Start Docker services

**Track progress in:**
[Implementation_Shards/MASTER_TASK_TRACKER.md](Implementation_Shards/MASTER_TASK_TRACKER.md)

---

## 🗂️ Your Task Files

Each shard has a detailed task breakdown:

| Day | Shard | Task File | Checkboxes |
|-----|-------|-----------|------------|
| 1 | Database & Infrastructure | [Shard_1_Tasks.md](Implementation_Shards/Shard_1_Tasks.md) | 127 |
| 2-3 | Mock Data Generation | [Shard_2_Tasks.md](Implementation_Shards/Shard_2_Tasks.md) | 180+ |
| 3-4 | AI Inference Pipeline | [Shard_3_Tasks.md](Implementation_Shards/Shard_3_Tasks.md) | 146 |
| 4-5 | Backend API Layer | [Shard_4_Tasks.md](Implementation_Shards/Shard_4_Tasks.md) | 180+ |
| 6-7 | Teacher Dashboard | [Shard_5_Tasks.md](Implementation_Shards/Shard_5_Tasks.md) | 165+ |
| 7-8 | Student Dashboard | [Shard_6_Tasks.md](Implementation_Shards/Shard_6_Tasks.md) | 155+ |
| 8-9 | Data Ingestion & Testing | [Shard_7_Tasks.md](Implementation_Shards/Shard_7_Tasks.md) | 140+ |
| 9-10 | Integration Testing | [Shard_8_Tasks.md](Implementation_Shards/Shard_8_Tasks.md) | 130+ |

**Total:** ~1,223 tasks

---

## 📚 Documentation Structure

```
AI_MS_SoftSkills/
├── QUICK_START.md ← YOU ARE HERE
├── Docs/
│   ├── PRD.md ← Original PRD (1,948 lines)
│   ├── Rubric.md ← 17 skills with behavioral indicators
│   └── Curriculum.md ← Educational context
└── Implementation_Shards/
    ├── README.md ← Overview of all shards
    ├── IMPLEMENTATION_ROADMAP.md ← Visual roadmap & timeline
    ├── MASTER_TASK_TRACKER.md ← Progress tracking
    ├── Shard_1_Database_Infrastructure.md ← Implementation spec
    ├── Shard_1_Tasks.md ← ✅ Detailed task list
    ├── Shard_2_Mock_Data_Generation.md
    ├── Shard_2_Tasks.md ← ✅ Detailed task list
    └── ... (Shards 3-8)
```

---

## 🎯 Work Flow

### Daily Routine

**Morning:**
1. Open [MASTER_TASK_TRACKER.md](Implementation_Shards/MASTER_TASK_TRACKER.md)
2. Check which shard you're working on
3. Open the corresponding `Shard_X_Tasks.md` file
4. Start Docker services: `docker-compose up -d`

**During Work:**
- Mark tasks complete: `- [ ]` → `- [x]`
- Track blockers in MASTER_TASK_TRACKER.md
- Run tests as you complete sections
- Commit code frequently with descriptive messages

**End of Day:**
- Update progress in MASTER_TASK_TRACKER.md
- Run `docker-compose logs` to check for errors
- Commit remaining work
- Note next day's starting point

---

## 🔍 Finding Information

### "Where do I find...?"

**Detailed technical specs:**
→ `Implementation_Shards/Shard_X_<Name>.md`

**Granular task breakdown:**
→ `Implementation_Shards/Shard_X_Tasks.md`

**Database schema:**
→ `Implementation_Shards/Shard_1_Database_Infrastructure.md` (Section 6)

**API endpoints:**
→ `Implementation_Shards/Shard_4_Backend_API.md`

**Rubric & skills:**
→ `Docs/Rubric.md` (17 skills, 4 levels each)

**Student archetypes:**
→ `Docs/PRD.md` (Section 3.1) or `Implementation_Shards/Shard_2_Tasks.md`

**Badge system:**
→ `Implementation_Shards/Shard_5_Tasks.md` or `Shard_6_Tasks.md`

---

## 🚀 Common Commands

### Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Full reset (including database)
docker-compose down -v && docker-compose up -d
```

### Testing

```bash
# Test database connection
docker-compose exec backend python scripts/test_db_connection.py

# Validate ingested data
docker-compose exec backend python scripts/validate_ingestion.py

# Calculate TAR (Teacher Agreement Rate)
docker-compose exec backend python scripts/test_ai_accuracy.py
```

### Database

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U flourish_admin -d skills_tracker_db

# Check table count
docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "\dt"

# Check student count
docker-compose exec db psql -U flourish_admin -d skills_tracker_db -c "SELECT COUNT(*) FROM students;"
```

---

## ✅ Completion Milestones

Track your progress through these major milestones:

- [ ] **Day 1:** Database up and seeded ✅ Verify: 4 students in DB
- [ ] **Day 3:** AI can assess 1 transcript ✅ Verify: Run test_inference.py
- [ ] **Day 5:** Backend API serving data ✅ Verify: API docs at /docs
- [ ] **Day 8:** Dashboards navigable ✅ Verify: Open both dashboards
- [ ] **Day 9:** Full dataset loaded ✅ Verify: 76 entries, 300+ assessments
- [ ] **Day 10:** Demo-ready ✅ Verify: TAR ≥ 85%, all workflows tested

---

## 🆘 Troubleshooting

### "Docker won't start"
```bash
# Check Docker Desktop is running
# Check ports not in use
lsof -i :5432 :8000 :8501

# Check docker-compose syntax
docker-compose config
```

### "Database connection failed"
```bash
# Wait for PostgreSQL to be ready
docker-compose logs db | grep "ready to accept connections"

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### "API returns errors"
```bash
# Check backend logs
docker-compose logs backend | grep ERROR

# Verify OpenAI API key
docker-compose exec backend env | grep OPENAI_API_KEY
```

### "Tests are failing"
```bash
# Check all services running
docker-compose ps

# Restart services
docker-compose restart

# Check test script syntax
python scripts/test_name.py --help
```

---

## 📞 Getting Help

**Stuck on a task?**
1. Check the corresponding `Shard_X_<Name>.md` implementation doc
2. Check the `Shard_X_Tasks.md` testing section
3. Review the PRD for context: `Docs/PRD.md`
4. Check the troubleshooting section above

**Found a bug or issue?**
- Document it in `MASTER_TASK_TRACKER.md` under "Blockers & Issues"
- Note the shard, task, and error message
- Include steps to reproduce

**Need to understand a concept?**
- **Skills & Rubric:** `Docs/Rubric.md`
- **Educational Context:** `Docs/Curriculum.md`
- **Architecture:** `Docs/PRD.md` Section 1
- **Database Design:** `Implementation_Shards/Shard_1_Database_Infrastructure.md`

---

## 🎬 Ready to Start?

### Your Next Steps:

1. **Open your first task file:**
   ```bash
   open Implementation_Shards/Shard_1_Tasks.md
   ```

2. **Review the prerequisites section**

3. **Start checking off boxes!**

4. **Track progress in MASTER_TASK_TRACKER.md**

---

**You've got this!** 🚀

With 1,223 granular tasks broken down for you, just follow the checklist and you'll have a fully functional MVP in 8-14 days.

**Questions?** Re-read the relevant shard documentation or check the original PRD.

**Ready?** → [START HERE: Shard 1 Tasks](Implementation_Shards/Shard_1_Tasks.md)
