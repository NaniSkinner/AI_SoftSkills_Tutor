# Shard 5: Teacher Dashboard

**Owner:** Frontend Engineer
**Estimated Time:** 2 days
**Dependencies:** Shard 4 (Backend API)
**Priority:** P1 (High Priority)

---

## Objective

Build Streamlit teacher dashboard with 4 pages: Student Overview, Skill Trends, Assessment Review (correction workflow), and Target Assignment.

---

## Dashboard Pages

### Page 1: Student Overview
**File:** `frontend/pages/01_Student_Overview.py`

**Features:**
- Grid view of all students (filter by teacher)
- Student cards showing: name, total assessments, growth trend indicator
- "View Details" button navigates to Skill Trends page

### Page 2: Skill Trends
**File:** `frontend/pages/02_Skill_Trends.py`

**Features:**
- Select student from dropdown
- Display skills grouped by category (SEL, EF, 21st Century)
- Mini timeline per skill: E → D → P → A
- Expandable detailed chart (Plotly line graph)
- Recent data points table (5 most recent assessments)

### Page 3: Assessment Review (Correction Workflow)
**File:** `frontend/pages/03_Assessment_Review.py`

**Features:**
- **Filters:** Student dropdown, Skill dropdown, "Low Confidence Only" checkbox
- **Review UI:** One assessment at a time with:
  - AI assessment (level, justification, source quote)
  - Confidence score display
  - Rubric reference expander (show relevant rubric text)
  - Correction form: Level dropdown, Justification text area, Teacher notes
  - Actions: "Approve as-is", "Submit Correction", "Skip"
- **Navigation:** Auto-advance to next assessment after action

### Page 4: Target Assignment
**File:** `frontend/pages/04_Target_Assignment.py`

**Features:**
- Select student
- Show current active target (with starting_level → target_level)
- **Updated display:** "Self-Management: **D** → **P**" (per clarification 3.2)
- Suggested next skills (based on current levels)
- Manual skill assignment dropdown
- Assign button

---

## Badge System Integration

### Badge Display (All Pages)
- **CSS Badge Styles:** Bronze (#CD7F32), Silver (#C0C0C0), Gold (#FFD700)
- **Faded Badge:** Grayscale with lock icon overlay (per clarification 4.1)
- **Icons:** Heroicons SVG (medal, lock) (per clarification 4.2)

**File:** `frontend/utils/badge_utils.py`

```python
def get_badge_color(level: str) -> str:
    """Return badge color based on level."""
    colors = {
        "Developing": "#CD7F32",  # Bronze
        "Proficient": "#C0C0C0",  # Silver
        "Advanced": "#FFD700"     # Gold
    }
    return colors.get(level, "#E0E0E0")  # Gray for Emerging

def render_badge_html(skill_name: str, level: str, earned: bool) -> str:
    """Generate HTML for badge display."""
    color = get_badge_color(level)
    opacity = "1.0" if earned else "0.3"
    lock_icon = "" if earned else '<svg class="lock-icon">...</svg>'

    return f'''
    <div class="badge" style="background-color: {color}; opacity: {opacity};">
        {lock_icon}
        <span class="badge-skill">{skill_name}</span>
        <span class="badge-level">{level.upper()}</span>
    </div>
    '''
```

---

## Key Implementation Notes

### API Integration
**File:** `frontend/utils/api_client.py`

```python
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

class APIClient:
    @staticmethod
    def get_students(teacher_id: str):
        response = requests.get(f"{BACKEND_URL}/api/students?teacher_id={teacher_id}")
        return response.json()

    @staticmethod
    def get_skill_trends(student_id: str):
        response = requests.get(f"{BACKEND_URL}/api/assessments/skill-trends/{student_id}")
        return response.json()

    @staticmethod
    def submit_correction(correction_data: dict):
        response = requests.post(f"{BACKEND_URL}/api/corrections/submit", json=correction_data)
        return response.json()

    # ... other methods
```

### Session State Management
```python
# Store teacher selection
if 'teacher_id' not in st.session_state:
    st.session_state.teacher_id = 'T001'  # Default for demo

# Store selected student for navigation
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None

# Store review progress
if 'review_index' not in st.session_state:
    st.session_state.review_index = 0
```

---

## Acceptance Criteria

- [ ] All 4 pages functional
- [ ] Teacher can select role (T001 or T002) on homepage
- [ ] Student overview shows all students for selected teacher
- [ ] Skill trends display progression charts correctly
- [ ] Assessment review workflow allows approve/correct/skip
- [ ] Corrections save to database and trigger few-shot update
- [ ] Target assignment shows starting_level → target_level format
- [ ] Badge system displays bronze/silver/gold colored badges
- [ ] Faded badges shown for Emerging (locked) skills
- [ ] Navigation between pages preserves state
- [ ] Error handling shows user-friendly messages

---

## Testing

```bash
# Start frontend
docker-compose up frontend

# Open dashboard
open http://localhost:8501

# Test workflow:
1. Select Teacher (T001 - Ms. Rodriguez)
2. View Student Overview
3. Click "View" on Eva
4. Check Skill Trends page loads
5. Navigate to Assessment Review
6. Filter for Low Confidence assessments
7. Submit a correction
8. Verify correction saved in DB
```

---

**Completion Checklist:**
- [ ] All 4 pages created
- [ ] API client implemented
- [ ] Charts render correctly (Plotly)
- [ ] Correction workflow functional
- [ ] Badge system styled
- [ ] Session state managed
- [ ] Error handling robust

**Sign-off:** _____________________
