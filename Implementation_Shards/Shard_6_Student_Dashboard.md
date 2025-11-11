# Shard 6: Student Dashboard

**Owner:** Frontend Engineer
**Estimated Time:** 2 days
**Dependencies:** Shard 4 (Backend API)
**Priority:** P1 (High Priority)

---

## Objective

Build Streamlit student dashboard with 3 pages: My Journey Map (animated skill progression), Badge Collection, and Current Goal.

---

## Dashboard Pages

### Page 1: My Journey Map
**File:** `frontend/pages/Student_01_Journey_Map.py`

**Visual Concept:**
- Horizontal progress bar for each skill: E → D → P → A
- Current position highlighted with "🎉 YOU ARE HERE!"
- Completed stages marked with checkmarks
- Future stages shown as grayed out/faded
- Celebration animation (st.balloons()) when new level reached

**Implementation:**
```python
# For each skill, show 4-column layout
cols = st.columns(4)
levels = ["Emerging", "Developing", "Proficient", "Advanced"]
current_idx = levels.index(student_skill['current_level'])

for idx, level in enumerate(levels):
    with cols[idx]:
        if idx < current_idx:
            st.success(f"✅ {level}")
        elif idx == current_idx:
            st.info(f"🎉 **YOU!**\n\n{level}")
            if skill.get('recently_advanced'):
                st.balloons()
        else:
            # Faded badge per clarification 4.1
            st.markdown(f'<div class="faded-badge">🔒 {level}</div>', unsafe_allow_html=True)
```

### Page 2: Badge Collection
**File:** `frontend/pages/Student_02_Badge_Collection.py`

**Features:**
- Display earned badges with:
  - Badge icon (bronze/silver/gold colored)
  - Skill name
  - Level achieved
  - Date earned
- Show locked badges (faded/grayscale with lock icon)
- Progress metric: "Badges Earned: 3 / 17"
- Toggle to "Show locked badges"

**Badge Display (per clarification 4.2):**
```python
# Use Heroicons SVG for medal + lock
BADGE_SVG = '''
<svg class="badge-icon" style="color: {color};">
  <path d="M..."><!-- Heroicon medal path --></path>
</svg>
'''

def render_badge(skill: str, level: str, earned: bool):
    color = get_badge_color(level)  # Bronze/Silver/Gold
    opacity = "1.0" if earned else "0.3"
    lock_overlay = render_lock_icon() if not earned else ""

    return f'''
    <div class="badge-card" style="opacity: {opacity};">
        {BADGE_SVG.format(color=color)}
        {lock_overlay}
        <p class="skill-name">{skill}</p>
        <p class="level">{level.upper()}</p>
    </div>
    '''
```

### Page 3: Current Goal
**File:** `frontend/pages/Student_03_Current_Goal.py`

**Features:**
- Display active target skill (assigned by teacher)
- **Updated format (per clarification 3.2):**
  ```
  🎯 SELF-MANAGEMENT 🎯

  Current Level: Developing (D)
  Goal: Reach Proficient (P)
  Progress: D → P
  ```
- Show rubric description for target level
- Tips to improve (3-5 actionable suggestions)
- Progress updates (recent assessments for this skill)
- Celebration if target completed recently

---

## Student Selection

### Homepage
**File:** `frontend/Home.py`

```python
import streamlit as st

st.title("🎒 Welcome to Your Skills Journey!")

# Simple student selector (no password for MVP per clarification 9)
student = st.selectbox(
    "Select your name:",
    options=[
        ("S001", "Eva"),
        ("S002", "Lucas"),
        ("S003", "Pat"),
        ("S004", "Mia")
    ],
    format_func=lambda x: x[1]  # Show name, store ID
)

if st.button("Start"):
    st.session_state.student_id = student[0]
    st.session_state.student_name = student[1]
    st.switch_page("pages/Student_01_Journey_Map.py")
```

---

## Key Implementation Notes

### Animation Triggers
- Check `recently_advanced` flag from API
- Trigger `st.balloons()` once per session per new level
- Store in session_state to prevent repeated animations

### Badge Styling (CSS)
**File:** `frontend/assets/badge_styles.css`

```css
.badge-card {
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s;
}

.badge-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.faded-badge {
    opacity: 0.3;
    filter: grayscale(100%);
    position: relative;
}

.lock-icon {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 24px;
    height: 24px;
}
```

Load CSS in Streamlit:
```python
with open('assets/badge_styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
```

---

## Acceptance Criteria

- [ ] All 3 pages functional
- [ ] Student selection on homepage (simple name dropdown)
- [ ] Journey map shows progression for all skills
- [ ] Celebration animation triggers on new level
- [ ] Badge collection displays earned + locked badges
- [ ] Badges styled with bronze/silver/gold colors
- [ ] Faded badges shown for not-yet-earned skills
- [ ] Current goal shows starting_level → target_level
- [ ] Progress updates displayed chronologically
- [ ] Navigation between pages works
- [ ] Mobile-friendly layout (Streamlit default)

---

## Testing

```bash
# Start frontend
docker-compose up frontend

# Open student dashboard
open http://localhost:8501

# Test workflow:
1. Select student (e.g., "Eva")
2. View Journey Map - check skill progression displays
3. Navigate to Badge Collection
4. Verify badges render with correct colors
5. Check locked badges are faded/grayed
6. Navigate to Current Goal
7. Verify target shows D → P format
8. Check tips and progress updates display
```

---

**Completion Checklist:**
- [ ] All 3 pages created
- [ ] Student selector implemented
- [ ] Journey map visualization complete
- [ ] Badge system styled (bronze/silver/gold)
- [ ] Faded badges for locked skills
- [ ] Current goal page functional
- [ ] Animations trigger appropriately
- [ ] CSS loaded and applied

**Sign-off:** _____________________
