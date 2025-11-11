# Shard 5 Tasks: Teacher Dashboard

**Status:** 🔴 Not Started
**Priority:** P1 (High Priority)
**Dependencies:** Shard 4 (Backend API)

---

## Overview

Build Streamlit teacher dashboard with 4 pages: Student Overview (grid view), Skill Trends (progression charts), Assessment Review (correction workflow), and Target Assignment. Implement API client, badge display system, and session state management.

---

## Prerequisites Checklist

- [ ] Shard 4 completed (Backend API functional)
- [ ] Streamlit package installed
- [ ] Plotly package installed
- [ ] Understanding of Streamlit session state
- [ ] Backend API accessible at http://backend:8000
- [ ] Sample data ingested for testing

---

## Tasks

### 1. Frontend Structure Setup

- [ ] Verify `frontend/pages/` directory exists
- [ ] Verify `frontend/utils/` directory exists
- [ ] Verify `frontend/assets/` directory exists

---

### 2. API Client Utility

- [ ] Create `frontend/utils/api_client.py` file

#### 2.1 Imports and Configuration
- [ ] Import `requests`
- [ ] Import `os`
- [ ] Import `logging`
- [ ] Define `BACKEND_URL` constant from environment (default "http://backend:8000")
- [ ] Create logger instance

#### 2.2 APIClient Class Definition
- [ ] Create `APIClient` class
- [ ] Add class docstring

#### 2.3 Students Methods
- [ ] Write `@staticmethod get_students(teacher_id: str = None) -> list` method
  - [ ] Build URL: /api/students with optional teacher_id param
  - [ ] Make GET request
  - [ ] Handle request exceptions
  - [ ] Return response.json()
  - [ ] Add error logging

- [ ] Write `@staticmethod get_student_progress(student_id: str) -> dict` method
  - [ ] Build URL: /api/students/{student_id}/progress
  - [ ] Make GET request
  - [ ] Handle 404 errors
  - [ ] Return response.json()
  - [ ] Add error logging

#### 2.4 Assessments Methods
- [ ] Write `@staticmethod get_student_assessments(student_id: str) -> list` method
  - [ ] Build URL: /api/assessments/student/{student_id}
  - [ ] Make GET request
  - [ ] Return response.json()
  - [ ] Add error handling

- [ ] Write `@staticmethod get_skill_trends(student_id: str) -> list` method
  - [ ] Build URL: /api/assessments/skill-trends/{student_id}
  - [ ] Make GET request
  - [ ] Return response.json()
  - [ ] Add error handling

- [ ] Write `@staticmethod get_pending_assessments(limit: int = 50, min_confidence: float = None) -> list` method
  - [ ] Build URL: /api/assessments/pending with query params
  - [ ] Make GET request
  - [ ] Return response.json()
  - [ ] Add error handling

#### 2.5 Corrections Methods
- [ ] Write `@staticmethod submit_correction(correction_data: dict) -> dict` method
  - [ ] Build URL: /api/corrections/submit
  - [ ] Make POST request with JSON body
  - [ ] Return response.json()
  - [ ] Add error handling

- [ ] Write `@staticmethod approve_assessment(assessment_id: int, approved_by: str) -> dict` method
  - [ ] Build URL: /api/assessments/{assessment_id}/approve
  - [ ] Make POST request
  - [ ] Return response.json()
  - [ ] Add error handling

#### 2.6 Targets Methods
- [ ] Write `@staticmethod assign_target(student_id: str, target_data: dict) -> dict` method
  - [ ] Build URL: /api/students/{student_id}/target-skill
  - [ ] Make POST request with JSON body
  - [ ] Return response.json()
  - [ ] Add error handling

- [ ] Write `@staticmethod get_student_targets(student_id: str, completed: bool = None) -> list` method
  - [ ] Build URL: /api/students/{student_id}/targets with optional param
  - [ ] Make GET request
  - [ ] Return response.json()
  - [ ] Add error handling

#### 2.7 Badges Methods
- [ ] Write `@staticmethod get_student_badges(student_id: str) -> dict` method
  - [ ] Build URL: /api/badges/students/{student_id}/badges
  - [ ] Make GET request
  - [ ] Return response.json()
  - [ ] Add error handling

- [ ] Write `@staticmethod grant_badge(badge_data: dict) -> dict` method
  - [ ] Build URL: /api/badges/grant
  - [ ] Make POST request with JSON body
  - [ ] Return response.json()
  - [ ] Add error handling

---

### 3. Badge Utilities Module

- [ ] Create `frontend/utils/badge_utils.py` file

#### 3.1 Badge Color Function
- [ ] Write `get_badge_color(level: str) -> str` function
  - [ ] Create colors dictionary:
    - [ ] "Emerging": "#E0E0E0" (gray)
    - [ ] "Developing": "#CD7F32" (bronze)
    - [ ] "Proficient": "#C0C0C0" (silver)
    - [ ] "Advanced": "#FFD700" (gold)
  - [ ] Return color from dictionary with gray default
  - [ ] Add docstring

#### 3.2 Badge Type Function
- [ ] Write `get_badge_type(level: str) -> str` function
  - [ ] Return "bronze" for Developing
  - [ ] Return "silver" for Proficient
  - [ ] Return "gold" for Advanced
  - [ ] Return None for Emerging
  - [ ] Add docstring

#### 3.3 Badge HTML Renderer
- [ ] Write `render_badge_html(skill_name: str, level: str, earned: bool) -> str` function
  - [ ] Get badge color
  - [ ] Set opacity: "1.0" if earned else "0.3"
  - [ ] Add lock icon SVG if not earned
  - [ ] Build HTML div with inline styles
  - [ ] Include skill name and level text
  - [ ] Return HTML string
  - [ ] Add docstring

#### 3.4 Badge Icon SVG
- [ ] Write `get_badge_icon_svg(badge_type: str) -> str` function
  - [ ] Return Heroicons medal SVG for bronze/silver/gold
  - [ ] Use different colors based on badge_type
  - [ ] Add docstring

- [ ] Write `get_lock_icon_svg() -> str` function
  - [ ] Return Heroicons lock SVG
  - [ ] Add docstring

---

### 4. Page 1: Student Overview

- [ ] Create `frontend/pages/01_Student_Overview.py` file

#### 4.1 Page Setup
- [ ] Import `streamlit as st`
- [ ] Import `APIClient` from utils.api_client
- [ ] Import `pandas as pd`
- [ ] Set page config with title, icon, layout="wide"

#### 4.2 Header Section
- [ ] Add page title: "Student Overview"
- [ ] Add teacher selection dropdown
  - [ ] Options: T001 (Ms. Rodriguez), T002 (Mr. Thompson)
  - [ ] Store selected teacher_id in session_state
  - [ ] Default to T001

#### 4.3 Fetch Students Data
- [ ] Get students using APIClient.get_students(teacher_id)
- [ ] Handle API errors with st.error()
- [ ] Display loading spinner while fetching

#### 4.4 Student Grid Display
- [ ] Calculate grid columns (3 columns)
- [ ] Loop through students
  - [ ] For each student, create column
  - [ ] Display student card with:
    - [ ] Student name (header)
    - [ ] Grade level
    - [ ] Total assessments count
    - [ ] Growth trend indicator (↑ or →)
    - [ ] "View Details" button
  - [ ] On button click, set session_state.selected_student
  - [ ] Navigate to Skill Trends page

#### 4.5 Summary Statistics
- [ ] Display metrics row:
  - [ ] Total students
  - [ ] Average assessments per student
  - [ ] Students with active targets

#### 4.6 Filters
- [ ] Add sidebar filters:
  - [ ] Search by student name
  - [ ] Filter by grade
  - [ ] Sort by: name, total assessments, recent activity

#### 4.7 Error Handling
- [ ] Add try-except around API calls
- [ ] Display user-friendly error messages
- [ ] Add retry button on error

---

### 5. Page 2: Skill Trends

- [ ] Create `frontend/pages/02_Skill_Trends.py` file

#### 5.1 Page Setup
- [ ] Import streamlit, plotly.express, plotly.graph_objects
- [ ] Import APIClient
- [ ] Set page config

#### 5.2 Student Selection
- [ ] Add student dropdown
  - [ ] Fetch all students for current teacher
  - [ ] Display student names
  - [ ] Store student_id in session_state
  - [ ] Pre-select if coming from Student Overview

#### 5.3 Fetch Skill Trends Data
- [ ] Get skill trends using APIClient.get_skill_trends(student_id)
- [ ] Handle empty results
- [ ] Display loading spinner

#### 5.4 Skills by Category Display
- [ ] Group skills by category: SEL, EF, 21st Century
- [ ] For each category, create expander
  - [ ] List skills in that category
  - [ ] For each skill, show mini timeline: E → D → P → A
  - [ ] Highlight current level
  - [ ] Show date of latest assessment

#### 5.5 Detailed Skill Chart
- [ ] Add skill selector dropdown
- [ ] When skill selected, display Plotly line chart:
  - [ ] X-axis: Date
  - [ ] Y-axis: Proficiency level (1=E, 2=D, 3=P, 4=A)
  - [ ] Line connecting data points
  - [ ] Markers for each assessment
  - [ ] Hover info: date, level, confidence score
  - [ ] Custom y-axis labels (E, D, P, A)

#### 5.6 Recent Assessments Table
- [ ] Display table of 5 most recent assessments for selected skill
- [ ] Columns: Date, Level, Confidence, Justification (truncated)
- [ ] Allow expanding justification
- [ ] Add "View Full Assessment" button

#### 5.7 Download Data
- [ ] Add button to download skill trends as CSV
- [ ] Convert data to pandas DataFrame
- [ ] Use st.download_button

#### 5.8 Navigation
- [ ] Add "Back to Overview" button
- [ ] Add "Review Assessments" button (go to page 3)

---

### 6. Page 3: Assessment Review (Correction Workflow)

- [ ] Create `frontend/pages/03_Assessment_Review.py` file

#### 6.1 Page Setup
- [ ] Import streamlit and APIClient
- [ ] Set page config
- [ ] Initialize session_state variables:
  - [ ] review_index (current assessment being reviewed)
  - [ ] assessments_to_review (filtered list)
  - [ ] filters_applied (track filter state)

#### 6.2 Filters Section
- [ ] Create sidebar with filters:
  - [ ] Student dropdown (all students)
  - [ ] Skill dropdown (all 17 skills)
  - [ ] "Low Confidence Only" checkbox
  - [ ] Confidence threshold slider (0.5-1.0)
  - [ ] "Apply Filters" button

#### 6.3 Fetch Assessments
- [ ] On filter apply, call APIClient.get_pending_assessments()
- [ ] Apply additional client-side filters (student, skill)
- [ ] Store filtered assessments in session_state
- [ ] Reset review_index to 0

#### 6.4 Assessment Display
- [ ] Check if assessments list is empty
  - [ ] If empty, display "No assessments to review"
  - [ ] Show button to reset filters
- [ ] Get current assessment: assessments[review_index]
- [ ] Display assessment details:
  - [ ] Student name
  - [ ] Skill name (category)
  - [ ] Current level (with colored badge)
  - [ ] Confidence score (with progress bar)
  - [ ] Date created
  - [ ] Source quote (in expandable section)
  - [ ] AI justification (full text)

#### 6.5 Rubric Reference
- [ ] Add expander: "View Rubric for This Skill"
- [ ] Load and display relevant rubric section for this skill
- [ ] Highlight current level descriptor

#### 6.6 Correction Form
- [ ] Add form with:
  - [ ] Level dropdown (E, D, P, A)
  - [ ] Pre-populate with current level
  - [ ] Justification text area
  - [ ] Pre-populate with AI justification (editable)
  - [ ] Teacher notes text area (optional)
  - [ ] Automatically set corrected_by from session_state.teacher_id

#### 6.7 Action Buttons
- [ ] Create 3-column layout for buttons:
  - [ ] Column 1: "Approve as-is" button
    - [ ] On click, call APIClient.approve_assessment()
    - [ ] Show success message
    - [ ] Advance to next assessment
  - [ ] Column 2: "Submit Correction" button
    - [ ] Validate form fields
    - [ ] Call APIClient.submit_correction()
    - [ ] Show success message
    - [ ] Advance to next assessment
  - [ ] Column 3: "Skip" button
    - [ ] Advance to next assessment without action

#### 6.8 Navigation Controls
- [ ] Display progress: "Assessment X of Y"
- [ ] Add "Previous" and "Next" buttons
- [ ] Disable Previous if at index 0
- [ ] Disable Next if at last assessment

#### 6.9 Completion Message
- [ ] If reached end of list, display:
  - [ ] "All assessments reviewed!"
  - [ ] Summary: X approved, Y corrected, Z skipped
  - [ ] "Review More" button to reset filters

#### 6.10 Error Handling
- [ ] Handle API errors gracefully
- [ ] Show error messages in st.error()
- [ ] Don't advance index on error
- [ ] Add retry button

---

### 7. Page 4: Target Assignment

- [ ] Create `frontend/pages/04_Target_Assignment.py` file

#### 7.1 Page Setup
- [ ] Import streamlit and APIClient
- [ ] Set page config
- [ ] Add page title: "Target Assignment"

#### 7.2 Student Selection
- [ ] Add student dropdown
- [ ] Fetch students for current teacher
- [ ] Store selected student_id in session_state

#### 7.3 Current Active Target Display
- [ ] Fetch student targets using APIClient.get_student_targets(completed=False)
- [ ] If active target exists:
  - [ ] Display target card:
    - [ ] Skill name (large header)
    - [ ] Starting level → Target level (formatted: "D → P")
    - [ ] Progress indicator
    - [ ] Date assigned
    - [ ] "Mark as Complete" button
- [ ] If no active target:
  - [ ] Display "No active target assigned"

#### 7.4 Suggested Next Skills
- [ ] Fetch student's latest assessments
- [ ] Identify skills at Developing or Proficient (ready to advance)
- [ ] Display suggested skills list:
  - [ ] Skill name
  - [ ] Current level
  - [ ] Suggested target level (current + 1)
  - [ ] "Assign This Target" quick button

#### 7.5 Manual Target Assignment Form
- [ ] Create form with:
  - [ ] Skill dropdown (all 17 skills)
  - [ ] Starting level dropdown (E, D, P)
  - [ ] Target level dropdown (D, P, A)
  - [ ] Validate target > starting
  - [ ] "Assign Target" button
- [ ] On submit:
  - [ ] Call APIClient.assign_target()
  - [ ] Show success message
  - [ ] Refresh current target display

#### 7.6 Completed Targets History
- [ ] Add expander: "View Completed Targets"
- [ ] Fetch completed targets
- [ ] Display table with:
  - [ ] Skill name
  - [ ] Starting → Target levels
  - [ ] Date assigned
  - [ ] Date completed
  - [ ] Badge earned (if applicable)

#### 7.7 Target Completion Action
- [ ] On "Mark as Complete" button:
  - [ ] Show confirmation dialog
  - [ ] Check if target level achieved (query latest assessment)
  - [ ] If achieved, prompt to grant badge
  - [ ] Call API to complete target
  - [ ] Show celebration message

#### 7.8 Badge Granting Integration
- [ ] After target completion, show badge grant form
- [ ] Pre-populate with target skill and level
- [ ] "Grant Badge" button
- [ ] Call APIClient.grant_badge()

#### 7.9 Error Handling
- [ ] Validate starting < target levels
- [ ] Handle duplicate target assignment
- [ ] Show user-friendly error messages

---

### 8. Home Page Enhancement

- [ ] Open/update `frontend/Home.py` file

#### 8.1 Teacher Dashboard Home
- [ ] Add title: "Flourish Skills Tracker - Teacher Dashboard"
- [ ] Add teacher selection (if not already set)
- [ ] Display welcome message with teacher name
- [ ] Show quick statistics:
  - [ ] Total students
  - [ ] Pending assessments count
  - [ ] Active targets count

#### 8.2 Quick Navigation
- [ ] Add navigation cards for each page:
  - [ ] Student Overview card
  - [ ] Skill Trends card
  - [ ] Assessment Review card
  - [ ] Target Assignment card
- [ ] Each card shows brief description and "Go" button

#### 8.3 Recent Activity Feed
- [ ] Display 5 most recent items:
  - [ ] New assessments
  - [ ] Corrections submitted
  - [ ] Targets assigned
  - [ ] Badges granted
- [ ] Show timestamp and student name

---

### 9. Session State Management

- [ ] Create `frontend/utils/session_utils.py` file

#### 9.1 Initialize Session State Function
- [ ] Write `initialize_session_state()` function
  - [ ] Check if teacher_id exists, default to T001
  - [ ] Check if selected_student exists, default to None
  - [ ] Check if review_index exists, default to 0
  - [ ] Check if assessments_to_review exists, default to []

#### 9.2 Navigation Helper Functions
- [ ] Write `navigate_to_student(student_id: str)` function
  - [ ] Set selected_student in session_state
  - [ ] Navigate to Skill Trends page

- [ ] Write `reset_review_state()` function
  - [ ] Reset review_index to 0
  - [ ] Clear assessments_to_review

---

### 10. Styling and UI Polish

#### 10.1 Custom CSS
- [ ] Create `frontend/assets/teacher_styles.css` file
- [ ] Add styles for:
  - [ ] Student cards (hover effects)
  - [ ] Badge displays
  - [ ] Assessment review cards
  - [ ] Progress indicators
  - [ ] Navigation buttons

#### 10.2 Load CSS in Pages
- [ ] Add CSS loading function in each page
  ```python
  with open('assets/teacher_styles.css') as f:
      st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
  ```

#### 10.3 Responsive Design
- [ ] Test on different screen sizes
- [ ] Adjust column widths for mobile
- [ ] Ensure charts are responsive

---

## Testing Checklist

### Page 1: Student Overview
- [ ] Start frontend: `docker-compose up frontend`
- [ ] Open http://localhost:8501
- [ ] Select Teacher: Ms. Rodriguez (T001)
- [ ] Verify students displayed in grid
- [ ] Verify student cards show correct data
- [ ] Click "View Details" on Eva
- [ ] Verify navigation to Skill Trends with Eva selected

### Page 2: Skill Trends
- [ ] Verify student dropdown populated
- [ ] Select student (Eva)
- [ ] Verify skills grouped by category
- [ ] Expand SEL category
- [ ] Verify mini timelines show current levels
- [ ] Select skill: Self-Awareness
- [ ] Verify detailed chart displays
- [ ] Verify chart shows progression over time
- [ ] Verify recent assessments table populates
- [ ] Test download CSV button

### Page 3: Assessment Review
- [ ] Navigate to Assessment Review
- [ ] Apply filters: Low Confidence Only
- [ ] Verify assessments filtered correctly
- [ ] Verify assessment details displayed
- [ ] Expand rubric reference
- [ ] Test "Approve as-is" button
  - [ ] Verify success message
  - [ ] Verify advances to next
- [ ] Test "Submit Correction" button
  - [ ] Change level to Proficient
  - [ ] Add teacher notes
  - [ ] Submit
  - [ ] Verify success message
  - [ ] Verify correction saved in database
- [ ] Test "Skip" button
- [ ] Test Previous/Next navigation

### Page 4: Target Assignment
- [ ] Navigate to Target Assignment
- [ ] Select student: Eva
- [ ] Verify current target displayed (if exists)
- [ ] Verify suggested skills list
- [ ] Assign new target:
  - [ ] Skill: Self-Management
  - [ ] Starting: Developing
  - [ ] Target: Proficient
  - [ ] Submit
- [ ] Verify target appears in current target section
- [ ] Test "Mark as Complete" button
- [ ] Verify badge grant prompt appears
- [ ] Grant badge
- [ ] Verify badge saved
- [ ] Check completed targets history

### API Client Testing
- [ ] Test each APIClient method independently
- [ ] Verify error handling for:
  - [ ] Network errors
  - [ ] 404 responses
  - [ ] 500 responses
  - [ ] Timeout errors
- [ ] Verify retry logic

### Session State Testing
- [ ] Navigate between pages
- [ ] Verify student selection persists
- [ ] Verify teacher selection persists
- [ ] Refresh page, verify state maintained
- [ ] Open new tab, verify independent state

### UI/UX Testing
- [ ] Verify all buttons clickable
- [ ] Verify no console errors (browser dev tools)
- [ ] Verify responsive layout on mobile
- [ ] Verify loading spinners appear during API calls
- [ ] Verify error messages are user-friendly

---

## Acceptance Criteria

- [ ] All 4 pages created and functional
- [ ] Teacher can select role (T001 or T002)
- [ ] Student Overview displays all students for selected teacher
- [ ] Student cards show name, grade, assessment count, growth indicator
- [ ] Skill Trends displays progression charts for all skills
- [ ] Charts correctly show level changes over time
- [ ] Assessment Review workflow allows approve/correct/skip actions
- [ ] Corrections save to database
- [ ] Corrections trigger few-shot learning update
- [ ] Target Assignment shows starting_level → target_level format
- [ ] Targets can be assigned and marked complete
- [ ] Badge system displays bronze/silver/gold colored badges
- [ ] Faded badges shown for Emerging (locked) skills
- [ ] Navigation between pages preserves state
- [ ] All API calls have error handling
- [ ] Loading states displayed during API calls
- [ ] User-friendly error messages shown
- [ ] CSS styling applied consistently

---

## Notes

- Use st.session_state for all persistent data between page loads
- APIClient centralizes all backend communication
- Badge colors: Gray (E), Bronze (D), Silver (P), Gold (A)
- Correction workflow is the core teacher interaction - prioritize UX here
- Target display format per clarification: "Self-Management: D → P"

**Next Shard:** [Shard 6: Student Dashboard](Shard_6_Tasks.md) (can work in parallel)
