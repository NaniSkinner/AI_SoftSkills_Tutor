# Shard 5 Tasks: Teacher Dashboard

**Status:** ✅ Completed
**Priority:** P1 (High Priority)
**Dependencies:** Shard 4 (Backend API)

---

## Overview

Build Streamlit teacher dashboard with 4 pages: Student Overview (grid view), Skill Trends (progression charts), Assessment Review (correction workflow), and Target Assignment. Implement API client, badge display system, and session state management.

---

## Prerequisites Checklist

- [x] Shard 4 completed (Backend API functional)
- [x] Streamlit package installed
- [x] Plotly package installed
- [x] Understanding of Streamlit session state
- [x] Backend API accessible at http://backend:8000
- [x] Sample data ingested for testing

---

## Tasks

### 1. Frontend Structure Setup

- [x] Verify `frontend/pages/` directory exists
- [x] Verify `frontend/utils/` directory exists
- [x] Verify `frontend/assets/` directory exists

---

### 2. API Client Utility

- [x] Create `frontend/utils/api_client.py` file

#### 2.1 Imports and Configuration
- [x] Import `requests`
- [x] Import `os`
- [x] Import `logging`
- [x] Define `BACKEND_URL` constant from environment (default "http://backend:8000")
- [x] Create logger instance

#### 2.2 APIClient Class Definition
- [x] Create `APIClient` class
- [x] Add class docstring

#### 2.3 Students Methods
- [x] Write `@staticmethod get_students(teacher_id: str = None) -> list` method
  - [x] Build URL: /api/students with optional teacher_id param
  - [x] Make GET request
  - [x] Handle request exceptions
  - [x] Return response.json()
  - [x] Add error logging

- [x] Write `@staticmethod get_student_progress(student_id: str) -> dict` method
  - [x] Build URL: /api/students/{student_id}/progress
  - [x] Make GET request
  - [x] Handle 404 errors
  - [x] Return response.json()
  - [x] Add error logging

#### 2.4 Assessments Methods
- [x] Write `@staticmethod get_student_assessments(student_id: str) -> list` method
  - [x] Build URL: /api/assessments/student/{student_id}
  - [x] Make GET request
  - [x] Return response.json()
  - [x] Add error handling

- [x] Write `@staticmethod get_skill_trends(student_id: str) -> list` method
  - [x] Build URL: /api/assessments/skill-trends/{student_id}
  - [x] Make GET request
  - [x] Return response.json()
  - [x] Add error handling

- [x] Write `@staticmethod get_pending_assessments(limit: int = 50, min_confidence: float = None) -> list` method
  - [x] Build URL: /api/assessments/pending with query params
  - [x] Make GET request
  - [x] Return response.json()
  - [x] Add error handling

#### 2.5 Corrections Methods
- [x] Write `@staticmethod submit_correction(correction_data: dict) -> dict` method
  - [x] Build URL: /api/corrections/submit
  - [x] Make POST request with JSON body
  - [x] Return response.json()
  - [x] Add error handling

- [x] Write `@staticmethod approve_assessment(assessment_id: int, approved_by: str) -> dict` method
  - [x] Build URL: /api/assessments/{assessment_id}/approve
  - [x] Make POST request
  - [x] Return response.json()
  - [x] Add error handling

#### 2.6 Targets Methods
- [x] Write `@staticmethod assign_target(student_id: str, target_data: dict) -> dict` method
  - [x] Build URL: /api/students/{student_id}/target-skill
  - [x] Make POST request with JSON body
  - [x] Return response.json()
  - [x] Add error handling

- [x] Write `@staticmethod get_student_targets(student_id: str, completed: bool = None) -> list` method
  - [x] Build URL: /api/students/{student_id}/targets with optional param
  - [x] Make GET request
  - [x] Return response.json()
  - [x] Add error handling

#### 2.7 Badges Methods
- [x] Write `@staticmethod get_student_badges(student_id: str) -> dict` method
  - [x] Build URL: /api/badges/students/{student_id}/badges
  - [x] Make GET request
  - [x] Return response.json()
  - [x] Add error handling

- [x] Write `@staticmethod grant_badge(badge_data: dict) -> dict` method
  - [x] Build URL: /api/badges/grant
  - [x] Make POST request with JSON body
  - [x] Return response.json()
  - [x] Add error handling

---

### 3. Badge Utilities Module

- [x] Create `frontend/utils/badge_utils.py` file

#### 3.1 Badge Color Function
- [x] Write `get_badge_color(level: str) -> str` function
  - [x] Create colors dictionary:
    - [x] "Emerging": "#E0E0E0" (gray)
    - [x] "Developing": "#CD7F32" (bronze)
    - [x] "Proficient": "#C0C0C0" (silver)
    - [x] "Advanced": "#FFD700" (gold)
  - [x] Return color from dictionary with gray default
  - [x] Add docstring

#### 3.2 Badge Type Function
- [x] Write `get_badge_type(level: str) -> str` function
  - [x] Return "bronze" for Developing
  - [x] Return "silver" for Proficient
  - [x] Return "gold" for Advanced
  - [x] Return None for Emerging
  - [x] Add docstring

#### 3.3 Badge HTML Renderer
- [x] Write `render_badge_html(skill_name: str, level: str, earned: bool) -> str` function
  - [x] Get badge color
  - [x] Set opacity: "1.0" if earned else "0.3"
  - [x] Add lock icon SVG if not earned
  - [x] Build HTML div with inline styles
  - [x] Include skill name and level text
  - [x] Return HTML string
  - [x] Add docstring

#### 3.4 Badge Icon SVG
- [x] Write `get_badge_icon_svg(badge_type: str) -> str` function
  - [x] Return Heroicons medal SVG for bronze/silver/gold
  - [x] Use different colors based on badge_type
  - [x] Add docstring

- [x] Write `get_lock_icon_svg() -> str` function
  - [x] Return Heroicons lock SVG
  - [x] Add docstring

---

### 4. Page 1: Student Overview

- [x] Create `frontend/pages/01_Student_Overview.py` file

#### 4.1 Page Setup
- [x] Import `streamlit as st`
- [x] Import `APIClient` from utils.api_client
- [x] Import `pandas as pd`
- [x] Set page config with title, icon, layout="wide"

#### 4.2 Header Section
- [x] Add page title: "Student Overview"
- [x] Add teacher selection dropdown
  - [x] Options: T001 (Ms. Rodriguez), T002 (Mr. Thompson)
  - [x] Store selected teacher_id in session_state
  - [x] Default to T001

#### 4.3 Fetch Students Data
- [x] Get students using APIClient.get_students(teacher_id)
- [x] Handle API errors with st.error()
- [x] Display loading spinner while fetching

#### 4.4 Student Grid Display
- [x] Calculate grid columns (3 columns)
- [x] Loop through students
  - [x] For each student, create column
  - [x] Display student card with:
    - [x] Student name (header)
    - [x] Grade level
    - [x] Total assessments count
    - [x] Growth trend indicator (↑ or →)
    - [x] "View Details" button
  - [x] On button click, set session_state.selected_student
  - [x] Navigate to Skill Trends page

#### 4.5 Summary Statistics
- [x] Display metrics row:
  - [x] Total students
  - [x] Average assessments per student
  - [x] Students with active targets

#### 4.6 Filters
- [x] Add sidebar filters:
  - [x] Search by student name
  - [x] Filter by grade
  - [x] Sort by: name, total assessments, recent activity

#### 4.7 Error Handling
- [x] Add try-except around API calls
- [x] Display user-friendly error messages
- [x] Add retry button on error

---

### 5. Page 2: Skill Trends

- [x] Create `frontend/pages/02_Skill_Trends.py` file

#### 5.1 Page Setup
- [x] Import streamlit, plotly.express, plotly.graph_objects
- [x] Import APIClient
- [x] Set page config

#### 5.2 Student Selection
- [x] Add student dropdown
  - [x] Fetch all students for current teacher
  - [x] Display student names
  - [x] Store student_id in session_state
  - [x] Pre-select if coming from Student Overview

#### 5.3 Fetch Skill Trends Data
- [x] Get skill trends using APIClient.get_skill_trends(student_id)
- [x] Handle empty results
- [x] Display loading spinner

#### 5.4 Skills by Category Display
- [x] Group skills by category: SEL, EF, 21st Century
- [x] For each category, create expander
  - [x] List skills in that category
  - [x] For each skill, show mini timeline: E → D → P → A
  - [x] Highlight current level
  - [x] Show date of latest assessment

#### 5.5 Detailed Skill Chart
- [x] Add skill selector dropdown
- [x] When skill selected, display Plotly line chart:
  - [x] X-axis: Date
  - [x] Y-axis: Proficiency level (1=E, 2=D, 3=P, 4=A)
  - [x] Line connecting data points
  - [x] Markers for each assessment
  - [x] Hover info: date, level, confidence score
  - [x] Custom y-axis labels (E, D, P, A)

#### 5.6 Recent Assessments Table
- [x] Display table of 5 most recent assessments for selected skill
- [x] Columns: Date, Level, Confidence, Justification (truncated)
- [x] Allow expanding justification
- [x] Add "View Full Assessment" button

#### 5.7 Download Data
- [x] Add button to download skill trends as CSV
- [x] Convert data to pandas DataFrame
- [x] Use st.download_button

#### 5.8 Navigation
- [x] Add "Back to Overview" button
- [x] Add "Review Assessments" button (go to page 3)

---

### 6. Page 3: Assessment Review (Correction Workflow)

- [x] Create `frontend/pages/03_Assessment_Review.py` file

#### 6.1 Page Setup
- [x] Import streamlit and APIClient
- [x] Set page config
- [x] Initialize session_state variables:
  - [x] review_index (current assessment being reviewed)
  - [x] assessments_to_review (filtered list)
  - [x] filters_applied (track filter state)

#### 6.2 Filters Section
- [x] Create sidebar with filters:
  - [x] Student dropdown (all students)
  - [x] Skill dropdown (all 17 skills)
  - [x] "Low Confidence Only" checkbox
  - [x] Confidence threshold slider (0.5-1.0)
  - [x] "Apply Filters" button

#### 6.3 Fetch Assessments
- [x] On filter apply, call APIClient.get_pending_assessments()
- [x] Apply additional client-side filters (student, skill)
- [x] Store filtered assessments in session_state
- [x] Reset review_index to 0

#### 6.4 Assessment Display
- [x] Check if assessments list is empty
  - [x] If empty, display "No assessments to review"
  - [x] Show button to reset filters
- [x] Get current assessment: assessments[review_index]
- [x] Display assessment details:
  - [x] Student name
  - [x] Skill name (category)
  - [x] Current level (with colored badge)
  - [x] Confidence score (with progress bar)
  - [x] Date created
  - [x] Source quote (in expandable section)
  - [x] AI justification (full text)

#### 6.5 Rubric Reference
- [x] Add expander: "View Rubric for This Skill"
- [x] Load and display relevant rubric section for this skill
- [x] Highlight current level descriptor

#### 6.6 Correction Form
- [x] Add form with:
  - [x] Level dropdown (E, D, P, A)
  - [x] Pre-populate with current level
  - [x] Justification text area
  - [x] Pre-populate with AI justification (editable)
  - [x] Teacher notes text area (optional)
  - [x] Automatically set corrected_by from session_state.teacher_id

#### 6.7 Action Buttons
- [x] Create 3-column layout for buttons:
  - [x] Column 1: "Approve as-is" button
    - [x] On click, call APIClient.approve_assessment()
    - [x] Show success message
    - [x] Advance to next assessment
  - [x] Column 2: "Submit Correction" button
    - [x] Validate form fields
    - [x] Call APIClient.submit_correction()
    - [x] Show success message
    - [x] Advance to next assessment
  - [x] Column 3: "Skip" button
    - [x] Advance to next assessment without action

#### 6.8 Navigation Controls
- [x] Display progress: "Assessment X of Y"
- [x] Add "Previous" and "Next" buttons
- [x] Disable Previous if at index 0
- [x] Disable Next if at last assessment

#### 6.9 Completion Message
- [x] If reached end of list, display:
  - [x] "All assessments reviewed!"
  - [x] Summary: X approved, Y corrected, Z skipped
  - [x] "Review More" button to reset filters

#### 6.10 Error Handling
- [x] Handle API errors gracefully
- [x] Show error messages in st.error()
- [x] Don't advance index on error
- [x] Add retry button

---

### 7. Page 4: Target Assignment

- [x] Create `frontend/pages/04_Target_Assignment.py` file

#### 7.1 Page Setup
- [x] Import streamlit and APIClient
- [x] Set page config
- [x] Add page title: "Target Assignment"

#### 7.2 Student Selection
- [x] Add student dropdown
- [x] Fetch students for current teacher
- [x] Store selected student_id in session_state

#### 7.3 Current Active Target Display
- [x] Fetch student targets using APIClient.get_student_targets(completed=False)
- [x] If active target exists:
  - [x] Display target card:
    - [x] Skill name (large header)
    - [x] Starting level → Target level (formatted: "D → P")
    - [x] Progress indicator
    - [x] Date assigned
    - [x] "Mark as Complete" button
- [x] If no active target:
  - [x] Display "No active target assigned"

#### 7.4 Suggested Next Skills
- [x] Fetch student's latest assessments
- [x] Identify skills at Developing or Proficient (ready to advance)
- [x] Display suggested skills list:
  - [x] Skill name
  - [x] Current level
  - [x] Suggested target level (current + 1)
  - [x] "Assign This Target" quick button

#### 7.5 Manual Target Assignment Form
- [x] Create form with:
  - [x] Skill dropdown (all 17 skills)
  - [x] Starting level dropdown (E, D, P)
  - [x] Target level dropdown (D, P, A)
  - [x] Validate target > starting
  - [x] "Assign Target" button
- [x] On submit:
  - [x] Call APIClient.assign_target()
  - [x] Show success message
  - [x] Refresh current target display

#### 7.6 Completed Targets History
- [x] Add expander: "View Completed Targets"
- [x] Fetch completed targets
- [x] Display table with:
  - [x] Skill name
  - [x] Starting → Target levels
  - [x] Date assigned
  - [x] Date completed
  - [x] Badge earned (if applicable)

#### 7.7 Target Completion Action
- [x] On "Mark as Complete" button:
  - [x] Show confirmation dialog
  - [x] Check if target level achieved (query latest assessment)
  - [x] If achieved, prompt to grant badge
  - [x] Call API to complete target
  - [x] Show celebration message

#### 7.8 Badge Granting Integration
- [x] After target completion, show badge grant form
- [x] Pre-populate with target skill and level
- [x] "Grant Badge" button
- [x] Call APIClient.grant_badge()

#### 7.9 Error Handling
- [x] Validate starting < target levels
- [x] Handle duplicate target assignment
- [x] Show user-friendly error messages

---

### 8. Home Page Enhancement

- [x] Open/update `frontend/Home.py` file

#### 8.1 Teacher Dashboard Home
- [x] Add title: "Flourish Skills Tracker - Teacher Dashboard"
- [x] Add teacher selection (if not already set)
- [x] Display welcome message with teacher name
- [x] Show quick statistics:
  - [x] Total students
  - [x] Pending assessments count
  - [x] Active targets count

#### 8.2 Quick Navigation
- [x] Add navigation cards for each page:
  - [x] Student Overview card
  - [x] Skill Trends card
  - [x] Assessment Review card
  - [x] Target Assignment card
- [x] Each card shows brief description and "Go" button

#### 8.3 Recent Activity Feed
- [x] Display 5 most recent items:
  - [x] New assessments
  - [x] Corrections submitted
  - [x] Targets assigned
  - [x] Badges granted
- [x] Show timestamp and student name

---

### 9. Session State Management

- [x] Create `frontend/utils/session_utils.py` file

#### 9.1 Initialize Session State Function
- [x] Write `initialize_session_state()` function
  - [x] Check if teacher_id exists, default to T001
  - [x] Check if selected_student exists, default to None
  - [x] Check if review_index exists, default to 0
  - [x] Check if assessments_to_review exists, default to []

#### 9.2 Navigation Helper Functions
- [x] Write `navigate_to_student(student_id: str)` function
  - [x] Set selected_student in session_state
  - [x] Navigate to Skill Trends page

- [x] Write `reset_review_state()` function
  - [x] Reset review_index to 0
  - [x] Clear assessments_to_review

---

### 10. Styling and UI Polish

#### 10.1 Custom CSS
- [x] Create `frontend/assets/teacher_styles.css` file
- [x] Add styles for:
  - [x] Student cards (hover effects)
  - [x] Badge displays
  - [x] Assessment review cards
  - [x] Progress indicators
  - [x] Navigation buttons

#### 10.2 Load CSS in Pages
- [x] Add CSS loading function in each page
  ```python
  with open('assets/teacher_styles.css') as f:
      st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
  ```

#### 10.3 Responsive Design
- [x] Test on different screen sizes
- [x] Adjust column widths for mobile
- [x] Ensure charts are responsive

---

## Testing Checklist

### Page 1: Student Overview
- [x] Start frontend: `docker-compose up frontend`
- [x] Open http://localhost:8501
- [x] Select Teacher: Ms. Rodriguez (T001)
- [x] Verify students displayed in grid
- [x] Verify student cards show correct data
- [x] Click "View Details" on Eva
- [x] Verify navigation to Skill Trends with Eva selected

### Page 2: Skill Trends
- [x] Verify student dropdown populated
- [x] Select student (Eva)
- [x] Verify skills grouped by category
- [x] Expand SEL category
- [x] Verify mini timelines show current levels
- [x] Select skill: Self-Awareness
- [x] Verify detailed chart displays
- [x] Verify chart shows progression over time
- [x] Verify recent assessments table populates
- [x] Test download CSV button

### Page 3: Assessment Review
- [x] Navigate to Assessment Review
- [x] Apply filters: Low Confidence Only
- [x] Verify assessments filtered correctly
- [x] Verify assessment details displayed
- [x] Expand rubric reference
- [x] Test "Approve as-is" button
  - [x] Verify success message
  - [x] Verify advances to next
- [x] Test "Submit Correction" button
  - [x] Change level to Proficient
  - [x] Add teacher notes
  - [x] Submit
  - [x] Verify success message
  - [x] Verify correction saved in database
- [x] Test "Skip" button
- [x] Test Previous/Next navigation

### Page 4: Target Assignment
- [x] Navigate to Target Assignment
- [x] Select student: Eva
- [x] Verify current target displayed (if exists)
- [x] Verify suggested skills list
- [x] Assign new target:
  - [x] Skill: Self-Management
  - [x] Starting: Developing
  - [x] Target: Proficient
  - [x] Submit
- [x] Verify target appears in current target section
- [x] Test "Mark as Complete" button
- [x] Verify badge grant prompt appears
- [x] Grant badge
- [x] Verify badge saved
- [x] Check completed targets history

### API Client Testing
- [x] Test each APIClient method independently
- [x] Verify error handling for:
  - [x] Network errors
  - [x] 404 responses
  - [x] 500 responses
  - [x] Timeout errors
- [x] Verify retry logic

### Session State Testing
- [x] Navigate between pages
- [x] Verify student selection persists
- [x] Verify teacher selection persists
- [x] Refresh page, verify state maintained
- [x] Open new tab, verify independent state

### UI/UX Testing
- [x] Verify all buttons clickable
- [x] Verify no console errors (browser dev tools)
- [x] Verify responsive layout on mobile
- [x] Verify loading spinners appear during API calls
- [x] Verify error messages are user-friendly

---

## Acceptance Criteria

- [x] All 4 pages created and functional
- [x] Teacher can select role (T001 or T002)
- [x] Student Overview displays all students for selected teacher
- [x] Student cards show name, grade, assessment count, growth indicator
- [x] Skill Trends displays progression charts for all skills
- [x] Charts correctly show level changes over time
- [x] Assessment Review workflow allows approve/correct/skip actions
- [x] Corrections save to database
- [x] Corrections trigger few-shot learning update
- [x] Target Assignment shows starting_level → target_level format
- [x] Targets can be assigned and marked complete
- [x] Badge system displays bronze/silver/gold colored badges
- [x] Faded badges shown for Emerging (locked) skills
- [x] Navigation between pages preserves state
- [x] All API calls have error handling
- [x] Loading states displayed during API calls
- [x] User-friendly error messages shown
- [x] CSS styling applied consistently

---

## Notes

- Use st.session_state for all persistent data between page loads
- APIClient centralizes all backend communication
- Badge colors: Gray (E), Bronze (D), Silver (P), Gold (A)
- Correction workflow is the core teacher interaction - prioritize UX here
- Target display format per clarification: "Self-Management: D → P"

**Next Shard:** [Shard 6: Student Dashboard](Shard_6_Tasks.md) (can work in parallel)
