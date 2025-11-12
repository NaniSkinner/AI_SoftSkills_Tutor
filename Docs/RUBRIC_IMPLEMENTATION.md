# Rubric Implementation Reference

**Status**: ✅ Complete and Production-Ready
**Critical Files** (Required by Code):
- [Docs/Rubric.md](Rubric.md) - **REQUIRED** by [backend/ai/rubric_loader.py:26](backend/ai/rubric_loader.py#L26)
- [Docs/Curriculum.md](Curriculum.md) - **REQUIRED** by [backend/ai/rubric_loader.py:57](backend/ai/rubric_loader.py#L57)

---

## Overview

The rubric system provides the foundation for AI skill assessment. It defines 17 non-academic skills across 4 proficiency levels (Emerging, Developing, Proficient, Advanced).

---

## Rubric Structure

### 17 Skills Across 3 Categories

**Social-Emotional Learning (SEL) - 5 Skills:**
1. Self-Awareness
2. Self-Management
3. Social Awareness
4. Relationship Skills
5. Responsible Decision-Making

**Executive Functioning (EF) - 8 Skills:**
6. Working Memory
7. Inhibitory Control
8. Cognitive Flexibility
9. Planning & Prioritization
10. Organization
11. Task Initiation
12. Time Management
13. Metacognition

**21st Century Skills - 4 Skills:**
14. Critical Thinking
15. Communication
16. Collaboration
17. Creativity & Innovation

---

## Proficiency Levels

| Level | Icon | Badge | Numeric | Description |
|-------|------|-------|---------|-------------|
| **Emerging (E)** | 🌱 | None | 1 | Beginning awareness; needs significant support |
| **Developing (D)** | 🥉 | Bronze | 2 | Shows capability with guidance; developing consistency |
| **Proficient (P)** | 🥈 | Silver | 3 | Demonstrates skill independently; consistent application |
| **Advanced (A)** | 🥇 | Gold | 4 | Excels in skill; can teach others; innovates |

---

## Code Integration

### Backend Rubric Loader

File: [backend/ai/rubric_loader.py](backend/ai/rubric_loader.py)

```python
def load_rubric() -> str:
    """Load the skill rubric from Docs/Rubric.md"""
    rubric_path = os.path.join(project_root, 'Docs', 'Rubric.md')
    with open(rubric_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_curriculum_context() -> str:
    """Load the curriculum context from Docs/Curriculum.md"""
    curriculum_path = os.path.join(project_root, 'Docs', 'Curriculum.md')
    with open(curriculum_path, 'r', encoding='utf-8') as f:
        return f.read()
```

**Critical**: These functions are called by the AI inference engine to provide context for skill assessments. Deleting or moving these files will break the system.

### Frontend Rubric Utilities

File: [frontend/utils/rubric_utils.py](frontend/utils/rubric_utils.py) (280 lines)

Functions:
- `get_skill_rubric(skill_name)` - Get rubric for a specific skill
- `render_rubric_html(skill_name, current_level)` - Render rubric with highlighting
- `get_all_skill_names()` - List all 17 skills
- `get_skills_by_category()` - Skills organized by category

---

## Teacher Dashboard Integration

### Assessment Review Page

File: [frontend/pages/03_Assessment_Review.py](frontend/pages/03_Assessment_Review.py)

The rubric reference feature allows teachers to view the full rubric for any skill being assessed:

```python
with st.expander("📋 View Rubric for This Skill"):
    st.markdown("Use this rubric to verify the AI's assessment. The current level is highlighted.")

    rubric_html = render_rubric_html(
        skill_name=current_assessment['skill_name'],
        current_level=full_level_name
    )
    st.markdown(rubric_html, unsafe_allow_html=True)
```

**Features**:
- In-context reference (no external documents needed)
- Current level highlighted with orange border
- Level-specific colors (Flourish theme)
- Clean text format for readability

---

## Student Dashboard Integration

### Skill Tips

File: [frontend/data/skill_tips.json](frontend/data/skill_tips.json)

**68 unique tip sets** (17 skills × 4 levels):
- Each tip set contains 3-5 actionable suggestions
- Language tailored for ages 9-14
- Derived from professional rubric but simplified
- No external links

**Example Tips for Self-Awareness - Developing:**
- "Keep a feelings journal - write down how you feel each day and why"
- "Name specific emotions like frustrated, anxious, or excited (not just happy/sad)"
- "Think about one thing you're good at and one thing you want to improve"

---

## Database Queries

### Find Assessments by Level

```sql
-- All Emerging assessments
SELECT * FROM assessments WHERE level = 'Emerging';

-- Student skill progression
SELECT skill_name, level, created_at FROM assessments
WHERE student_id = 'S001'
ORDER BY skill_name, created_at;

-- Latest assessment per skill per student
SELECT DISTINCT ON (student_id, skill_name)
  skill_name, level, confidence_score
FROM assessments
ORDER BY student_id, skill_name, created_at DESC;
```

---

## Visual Design

### Flourish Theme Colors

**Teacher Dashboard**:
- Emerging: Light beige (#e8e5df)
- Developing: Nature green (#6b8456)
- Proficient: Forest green (#3a5a44)
- Advanced: Warm orange (#d67e3a)
- Highlight: Orange accent (#d67e3a)

**Student Dashboard**:
- Emerging: Green (#81C784)
- Developing: Bronze (#CD7F32)
- Proficient: Silver (#C0C0C0)
- Advanced: Gold (#FFD700)

---

## Quick Reference: Skill Descriptors

See [RUBRIC_QUICK_REFERENCE.md](RUBRIC_QUICK_REFERENCE.md) for a scannable list of all skill descriptors at all levels (kept as separate reference doc).

---

## Technical Notes

- **Rubric Version**: 1.0
- **Total Descriptors**: 68 (17 skills × 4 levels)
- **Data Format**: Markdown (Docs/Rubric.md) + JSON (frontend/data/skill_tips.json)
- **No API Calls**: Rubric data embedded for fast loading
- **Last Updated**: November 12, 2024

---

## File Dependencies

**DO NOT DELETE OR MOVE**:
- `/Docs/Rubric.md` - Required by backend AI engine
- `/Docs/Curriculum.md` - Required by backend AI engine

**Frontend Files** (can be edited):
- `/frontend/utils/rubric_utils.py` - Rubric display utilities
- `/frontend/data/skill_tips.json` - Student tips database
- `/Docs/RUBRIC_QUICK_REFERENCE.md` - Teacher reference guide
