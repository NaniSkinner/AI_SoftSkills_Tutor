# Shard 4: Backend API Layer

**Owner:** Backend Engineer
**Estimated Time:** 2 days
**Dependencies:** Shards 1, 3 (Database + AI Pipeline)
**Priority:** P0 (Critical Path)

---

## Objective

Build FastAPI REST API with endpoints for data ingestion, assessment retrieval, teacher corrections, student progress, and badge management.

---

## Key Endpoints

### 1. Data Ingestion
- `POST /api/data/ingest` - Ingest data entry + trigger AI assessment

### 2. Assessment Retrieval
- `GET /api/assessments/student/{student_id}` - Get all assessments for student
- `GET /api/assessments/skill-trends/{student_id}` - Get progression over time
- `GET /api/assessments/pending` - Get assessments needing teacher review

### 3. Teacher Corrections
- `POST /api/corrections/submit` - Submit teacher correction
- `POST /api/assessments/{id}/approve` - Approve assessment as-is

### 4. Student & Target Management
- `GET /api/students` - List students (filter by teacher)
- `GET /api/students/{student_id}/progress` - Student progress summary
- `POST /api/students/{student_id}/target-skill` - Assign target skill
- `GET /api/students/{student_id}/targets` - Get active/completed targets

### 5. Badge System
- `GET /api/students/{student_id}/badges` - Get earned + locked badges
- `POST /api/badges/grant` - Teacher grants badge for skill level

### 6. Health & Utility
- `GET /health` - Health check
- `GET /` - API info

---

## File Structure

```
backend/
├── main.py                    # FastAPI app + CORS setup
├── models/
│   └── schemas.py             # Pydantic models
└── routers/
    ├── data_ingest.py         # Data ingestion router
    ├── assessments.py         # Assessment endpoints
    ├── corrections.py         # Teacher correction endpoints
    ├── students.py            # Student & target endpoints
    └── badges.py              # Badge management endpoints
```

---

## Key Implementation Notes

### Data Ingestion Flow
```python
1. Receive data_entry JSON
2. Insert into data_entries table
3. Call SkillInferenceEngine.assess_skills()
4. Insert assessments into assessments table
5. Return {assessments_created, assessment_ids}
```

### Skill Trends Calculation
```sql
-- Get assessments ordered by date, grouped by skill
SELECT skill_name, level, date
FROM assessments
WHERE student_id = ?
ORDER BY skill_name, date ASC
```

Convert levels to numeric: E=1, D=2, P=3, A=4 for charting

### Badge Granting Logic
- Teacher explicitly grants badge via `/api/badges/grant`
- Badge type determined by level: D→Bronze, P→Silver, A→Gold
- Unique constraint prevents duplicate badges for same skill+level

### Target Assignment (Updated per clarification 3.2)
```json
{
  "student_id": "S001",
  "skill_name": "Self-Management",
  "starting_level": "D",
  "target_level": "P",
  "assigned_by": "T001"
}
```

---

## Acceptance Criteria

- [ ] All 15+ endpoints functional
- [ ] FastAPI auto-docs available at `/docs`
- [ ] CORS enabled for Streamlit frontend
- [ ] Pydantic models validate all request/response bodies
- [ ] Error handling returns proper HTTP status codes
- [ ] Database transactions committed properly
- [ ] AI inference integrated into ingestion endpoint
- [ ] Badge system enforces teacher-only granting
- [ ] Target assignment includes starting_level + target_level

---

## Testing

```bash
# Start backend
docker-compose up backend

# Test health endpoint
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Test data ingestion (with sample file)
curl -X POST http://localhost:8000/api/data/ingest \
  -H "Content-Type: application/json" \
  -d @mock_data/test_entry.json
```

---

**Completion Checklist:**
- [ ] FastAPI app structure created
- [ ] All routers implemented
- [ ] Pydantic schemas defined
- [ ] Database queries optimized
- [ ] Error handling comprehensive
- [ ] API documentation complete

**Sign-off:** _____________________
