# Shard 6 Tasks: Student Dashboard

**Status:** ✅ Completed
**Priority:** P1 (High Priority)
**Dependencies:** Shard 4 (Backend API)

---

## Overview

Build Streamlit student dashboard with 4 pages: Student Home (character selection), My Journey Map (animated skill progression with visual timeline), Badge Collection (earned and locked badges display), and Current Goal (active target with age-appropriate tips). Implemented hand-drawn theme with earth tones, CSS animations, and kid-friendly UX for ages 9-14.

---

## Prerequisites Checklist

- [x] Shard 4 completed (Backend API functional)
- [x] Streamlit package installed
- [x] DiceBear Avatars API integrated for character selection
- [x] Badge utilities available
- [x] Sample data ingested with student progressions
- [x] Age-appropriate content (9-14 years old)

---

## Tasks

### 1. Student Dashboard Structure

- [ ] Create `frontend/pages/` subdirectory for student pages (if using separate structure)
- [ ] Or prefix student pages: `Student_01_`, `Student_02_`, `Student_03_`

---

### 2. Home Page: Student Selection

- [ ] Create `frontend/Student_Home.py` file (or update main Home.py)

#### 2.1 Page Setup
- [ ] Import streamlit
- [ ] Import APIClient from utils.api_client
- [ ] Set page config:
  - [ ] title="My Skills Journey"
  - [ ] icon="🎒"
  - [ ] layout="wide"

#### 2.2 Welcome Section
- [ ] Add title: "Welcome to Your Skills Journey!"
- [ ] Add subtitle explaining the dashboard
- [ ] Display motivational message

#### 2.3 Student Selection
- [ ] Create student selector dropdown
  - [ ] Fetch all students from API
  - [ ] Display format: "Eva - Grade 7"
  - [ ] Store tuple: (student_id, student_name)
  - [ ] No password for MVP (per clarification)
- [ ] On selection, store in session_state:
  - [ ] session_state.student_id
  - [ ] session_state.student_name

#### 2.4 Start Button
- [ ] Add "Start My Journey" button
- [ ] On click:
  - [ ] Verify student selected
  - [ ] Navigate to Journey Map page
  - [ ] Store entry timestamp for session tracking

#### 2.5 Quick Stats Preview
- [ ] After student selection, show preview metrics:
  - [ ] Total badges earned
  - [ ] Current level in most skills
  - [ ] Active goal (if any)

---

### 3. Page 1: My Journey Map

- [ ] Create `frontend/pages/Student_01_Journey_Map.py` file

#### 3.1 Page Setup
- [ ] Import streamlit, plotly
- [ ] Import APIClient
- [ ] Import badge_utils
- [ ] Set page config

#### 3.2 Student Info Header
- [ ] Display student name from session_state
- [ ] Add welcome back message
- [ ] Show date of last activity

#### 3.3 Fetch Student Progress Data
- [ ] Get student_id from session_state
- [ ] Call APIClient.get_skill_trends(student_id)
- [ ] Call APIClient.get_student_badges(student_id)
- [ ] Handle loading state with spinner
- [ ] Handle errors with friendly messages

#### 3.4 Skills by Category Tabs
- [ ] Create tabs: SEL, Executive Function, 21st Century Skills
- [ ] For each tab, display skills in that category

#### 3.5 Journey Map Visual (Per Skill)
- [ ] For each skill, create 4-column layout
- [ ] Define levels list: ["Emerging", "Developing", "Proficient", "Advanced"]
- [ ] Get current_level for student in this skill
- [ ] Find current_idx in levels list

#### 3.6 Progress Bar Stages
- [ ] Loop through 4 levels with enumerate
- [ ] For each level column:
  - [ ] If idx < current_idx (completed stages):
    - [ ] Display with checkmark: "✅ Emerging"
    - [ ] Use st.success() with completed styling
  - [ ] If idx == current_idx (current stage):
    - [ ] Display highlighted: "🎉 YOU ARE HERE!"
    - [ ] Show level name in bold
    - [ ] Use st.info() with highlight styling
    - [ ] If recently_advanced flag, trigger st.balloons()
  - [ ] If idx > current_idx (future stages):
    - [ ] Display faded badge with lock icon
    - [ ] Use custom HTML: `<div class="faded-badge">🔒 {level}</div>`
    - [ ] Apply grayscale filter and reduced opacity

#### 3.7 Recently Advanced Detection
- [ ] Compare current assessment date to previous assessment date
- [ ] If level changed within last 7 days, set recently_advanced=True
- [ ] Store in session_state to prevent repeated animations
- [ ] Trigger st.balloons() celebration animation

#### 3.8 Skill Details Expander
- [ ] For each skill, add expander: "View My Progress"
- [ ] Inside expander:
  - [ ] Show mini chart of level progression
  - [ ] Show dates of level changes
  - [ ] Show latest assessment justification
  - [ ] Show growth tips (3 suggestions)

#### 3.9 Overall Progress Summary
- [ ] Display metrics at top:
  - [ ] Total skills assessed
  - [ ] Skills at Proficient or Advanced
  - [ ] Skills improved this month
  - [ ] Current streak (days of progress)

#### 3.10 Navigation
- [ ] Add button: "View My Badges" → navigate to Badge Collection
- [ ] Add button: "See My Goal" → navigate to Current Goal

---

### 4. Page 2: Badge Collection

- [ ] Create `frontend/pages/Student_02_Badge_Collection.py` file

#### 4.1 Page Setup
- [ ] Import streamlit
- [ ] Import APIClient
- [ ] Import badge_utils
- [ ] Set page config

#### 4.2 Header Section
- [ ] Add title: "My Badge Collection"
- [ ] Add subtitle: "Earn badges by reaching new skill levels!"
- [ ] Display progress metric: "Badges Earned: X / 51"
  - [ ] 51 possible: 17 skills × 3 levels (D, P, A)

#### 4.3 Fetch Badges Data
- [ ] Get student_id from session_state
- [ ] Call APIClient.get_student_badges(student_id)
- [ ] Extract earned_badges and locked_badges from response
- [ ] Handle loading and errors

#### 4.4 Badge Display Grid
- [ ] Create toggle: "Show Locked Badges" checkbox
- [ ] Create 4-column grid layout
- [ ] Loop through all possible badges (earned + locked)

#### 4.5 Earned Badge Card
- [ ] For each earned badge:
  - [ ] Display badge icon (colored medal SVG)
  - [ ] Color based on level:
    - [ ] Bronze (#CD7F32) for Developing
    - [ ] Silver (#C0C0C0) for Proficient
    - [ ] Gold (#FFD700) for Advanced
  - [ ] Show skill name
  - [ ] Show level achieved
  - [ ] Show date earned
  - [ ] Full opacity (1.0)
  - [ ] Add hover effect (scale animation)

#### 4.6 Locked Badge Card
- [ ] For each locked badge (if toggle enabled):
  - [ ] Display faded badge icon
  - [ ] Grayscale filter
  - [ ] Reduced opacity (0.3)
  - [ ] Add lock icon overlay (Heroicons lock SVG)
  - [ ] Show skill name and level (grayed out)
  - [ ] Show "Not yet earned" text

#### 4.7 Badge Icon SVG Implementation
- [ ] Use Heroicons medal SVG (per clarification 4.2)
- [ ] Medal SVG path:
  ```html
  <svg class="badge-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2L9.5 8.5L2.5 9.5L7.25 14L6 21L12 17.5L18 21L16.75 14L21.5 9.5L14.5 8.5L12 2Z"/>
  </svg>
  ```
- [ ] Lock SVG for locked badges:
  ```html
  <svg class="lock-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2C9.24 2 7 4.24 7 7V10H6C4.9 10 4 10.9 4 12V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V12C20 10.9 19.1 10 18 10H17V7C17 4.24 14.76 2 12 2ZM9 7C9 5.34 10.34 4 12 4C13.66 4 15 5.34 15 7V10H9V7Z"/>
  </svg>
  ```

#### 4.8 Badge Categories
- [ ] Add tab view: All, SEL, Executive Function, 21st Century
- [ ] Filter badges by category when tab selected

#### 4.9 Recent Badges Section
- [ ] Show "Recently Earned" section at top
- [ ] Display 3 most recent badges with larger cards
- [ ] Add celebration confetti for newest badge (if earned today)

#### 4.10 Navigation
- [ ] Add "Back to Journey Map" button
- [ ] Add "View My Goal" button

---

### 5. Page 3: Current Goal

- [ ] Create `frontend/pages/Student_03_Current_Goal.py` file

#### 5.1 Page Setup
- [ ] Import streamlit, APIClient
- [ ] Set page config

#### 5.2 Fetch Active Target
- [ ] Get student_id from session_state
- [ ] Call APIClient.get_student_targets(student_id, completed=False)
- [ ] Handle case: no active target
- [ ] Handle case: active target exists

#### 5.3 No Active Goal Display
- [ ] If no active target:
  - [ ] Display message: "No goal assigned yet"
  - [ ] Suggest talking to teacher
  - [ ] Show general skill improvement tips
  - [ ] Display recent achievements instead

#### 5.4 Active Goal Display
- [ ] If active target exists:
  - [ ] Large header: "🎯 {SKILL NAME} 🎯"
  - [ ] Display in prominent card

#### 5.5 Goal Details (Updated Format per clarification 3.2)
- [ ] Show "Current Level:" with starting_level
  - [ ] Example: "Current Level: Developing (D)"
- [ ] Show "Goal:" with target_level
  - [ ] Example: "Goal: Reach Proficient (P)"
- [ ] Show progress indicator: "D → P"
  - [ ] Use arrow graphic or progress bar
  - [ ] Show as: starting_level → target_level
- [ ] Display date assigned
- [ ] Calculate days since assignment

#### 5.6 Rubric Description
- [ ] Display target level rubric description
- [ ] Example: "Proficient means you can apply the skill independently..."
- [ ] Use expandable section for full rubric text

#### 5.7 Tips to Improve
- [ ] Display "How to Reach Your Goal" section
- [ ] Show 3-5 actionable suggestions
- [ ] Suggestions based on skill and current/target levels
- [ ] Use friendly, encouraging language
- [ ] Add icons/emojis for visual appeal

#### 5.8 Progress Updates
- [ ] Show "Your Recent Progress" section
- [ ] Query recent assessments for this skill
- [ ] Display timeline of assessments:
  - [ ] Date
  - [ ] Level achieved
  - [ ] Confidence score (as stars rating)
  - [ ] Brief justification
- [ ] Show progress trend (improving/stable/declining)

#### 5.9 Celebration for Completed Goal
- [ ] If target recently completed (check completed_at):
  - [ ] Display celebration message
  - [ ] Show badge earned (if granted)
  - [ ] Trigger st.balloons() animation
  - [ ] Suggest viewing Badge Collection

#### 5.10 Navigation
- [ ] Add "Back to Journey Map" button
- [ ] Add "View My Badges" button

---

### 6. Badge CSS Styling

- [ ] Create `frontend/assets/badge_styles.css` file

#### 6.1 Badge Card Styles
- [ ] Define `.badge-card` class
  - [ ] border: 2px solid #ddd
  - [ ] border-radius: 10px
  - [ ] padding: 20px
  - [ ] text-align: center
  - [ ] transition: all 0.3s
  - [ ] box-shadow for depth

#### 6.2 Badge Hover Effect
- [ ] Define `.badge-card:hover` class
  - [ ] transform: scale(1.05)
  - [ ] box-shadow: 0 4px 8px rgba(0,0,0,0.2)

#### 6.3 Faded Badge Styles
- [ ] Define `.faded-badge` class
  - [ ] opacity: 0.3
  - [ ] filter: grayscale(100%)
  - [ ] position: relative

#### 6.4 Lock Icon Styles
- [ ] Define `.lock-icon` class
  - [ ] position: absolute
  - [ ] top: 10px
  - [ ] right: 10px
  - [ ] width: 24px
  - [ ] height: 24px
  - [ ] z-index: 10

#### 6.5 Badge Icon Styles
- [ ] Define `.badge-icon` class
  - [ ] width: 64px
  - [ ] height: 64px
  - [ ] margin: 0 auto
  - [ ] display: block

#### 6.6 Badge Colors
- [ ] Define `.badge-bronze` (color: #CD7F32)
- [ ] Define `.badge-silver` (color: #C0C0C0)
- [ ] Define `.badge-gold` (color: #FFD700)

#### 6.7 Journey Map Styles
- [ ] Define `.journey-stage` class for progress stages
- [ ] Define `.journey-current` for highlighted current stage
- [ ] Define `.journey-completed` for completed stages
- [ ] Define `.journey-locked` for future stages

#### 6.8 Goal Card Styles
- [ ] Define `.goal-card` class for Current Goal display
- [ ] Define `.progress-arrow` for D → P indicator
- [ ] Define `.tips-section` for improvement tips

#### 6.9 Load CSS Function
- [ ] Create helper function in utils to load CSS
  ```python
  def load_css(file_path):
      with open(file_path) as f:
          st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
  ```
- [ ] Call in each student page

---

### 7. Animation and Celebration System

- [ ] Create `frontend/utils/animations.py` file

#### 7.1 Celebration Trigger Function
- [ ] Write `trigger_celebration(celebration_type: str)` function
- [ ] Types: "new_level", "badge_earned", "goal_complete"
- [ ] Use st.balloons() for all types
- [ ] Store trigger in session_state to prevent repeats
- [ ] Add optional sound effect (browser notification)

#### 7.2 Progress Animation
- [ ] Write `animate_progress_bar(current: int, total: int)` function
- [ ] Return HTML/CSS for animated progress bar
- [ ] Use CSS transitions for smooth animation

#### 7.3 Badge Reveal Animation
- [ ] Write `reveal_badge(badge_data: dict)` function
- [ ] Display badge with fade-in effect
- [ ] Add scale animation
- [ ] Show congratulations message

#### 7.4 Recently Advanced Check
- [ ] Write `check_recently_advanced(skill_name: str, student_id: str) -> bool` function
- [ ] Query recent assessments
- [ ] Compare levels and dates
- [ ] Return True if advanced within last 7 days
- [ ] Cache result in session_state

---

### 8. Journey Map Visualization Enhancements

#### 8.1 Alternative Visual: Linear Progress Bar
- [ ] Create function to render linear progress bar
- [ ] 4 stages: E → D → P → A
- [ ] Filled stages in green
- [ ] Current stage highlighted in blue
- [ ] Future stages in gray
- [ ] Use HTML/CSS for custom rendering

#### 8.2 Alternative Visual: Circular Progress
- [ ] Create circular progress indicator
- [ ] 4 quarters representing 4 levels
- [ ] Fill quarters based on current level
- [ ] Add percentage text in center

#### 8.3 Skill Card Component
- [ ] Write reusable skill card component function
- [ ] Parameters: skill_name, current_level, recently_advanced
- [ ] Returns styled HTML card
- [ ] Includes mini chart, level indicator, tips button

---

### 9. Tips Generation System

- [ ] Create `frontend/utils/tips_generator.py` file

#### 9.1 Tips Database
- [ ] Create dictionary of tips by skill and level
- [ ] Structure: {skill_name: {target_level: [tip1, tip2, tip3]}}
- [ ] Example for Self-Awareness → Proficient:
  - [ ] "Practice naming your emotions when they happen"
  - [ ] "Keep a feelings journal"
  - [ ] "Ask yourself 'why' when you feel strong emotions"

#### 9.2 Get Tips Function
- [ ] Write `get_tips(skill_name: str, target_level: str) -> list` function
- [ ] Look up tips from database
- [ ] Return 3-5 relevant tips
- [ ] Add default tips if skill not in database

#### 9.3 Populate Tips for All 17 Skills
- [ ] Add tips for each SEL skill (5 skills × 3 levels)
- [ ] Add tips for each EF skill (6 skills × 3 levels)
- [ ] Add tips for each 21st Century skill (6 skills × 3 levels)
- [ ] Ensure tips are:
  - [ ] Actionable
  - [ ] Age-appropriate (middle school)
  - [ ] Encouraging
  - [ ] Specific

---

### 10. Responsive Design and Mobile Optimization

#### 10.1 Mobile-Friendly Layout
- [ ] Test all pages on mobile viewport
- [ ] Adjust column layouts for small screens
- [ ] Use st.columns with responsive ratios
- [ ] Ensure badges display in single column on mobile

#### 10.2 Touch-Friendly Buttons
- [ ] Increase button sizes for touch targets
- [ ] Add padding to clickable areas
- [ ] Test on tablet and phone

#### 10.3 Font Sizing
- [ ] Use relative font sizes (em, rem)
- [ ] Ensure headers are readable on small screens
- [ ] Test text wrapping

---

### 11. Session State Management for Students

#### 11.1 Initialize Student Session
- [ ] Add function to initialize student session state
- [ ] Store: student_id, student_name, login_time
- [ ] Store: viewed_pages (list of pages visited)
- [ ] Store: celebration_shown (dict of celebrations already displayed)

#### 11.2 Track Student Activity
- [ ] Log page visits
- [ ] Track time spent on each page
- [ ] Store last viewed skill
- [ ] Store filter preferences

#### 11.3 Persistent Data Across Pages
- [ ] Ensure student_id persists across all pages
- [ ] Cache API responses to reduce calls
- [ ] Store recently_advanced flags per skill

---

## Testing Checklist

### Page 1: My Journey Map
- [ ] Start frontend and navigate to Student Dashboard
- [ ] Select student: Eva
- [ ] Click "Start My Journey"
- [ ] Verify Journey Map loads
- [ ] Verify all skills displayed grouped by category
- [ ] Check SEL tab:
  - [ ] Verify 5 SEL skills shown
  - [ ] Verify progress stages displayed (E → D → P → A)
  - [ ] Verify current level highlighted
- [ ] Check a skill at Developing:
  - [ ] Verify completed stage (Emerging) shows checkmark
  - [ ] Verify current stage (Developing) highlighted
  - [ ] Verify future stages (P, A) shown faded with lock
- [ ] Test celebration animation:
  - [ ] Manually set recently_advanced flag
  - [ ] Reload page
  - [ ] Verify st.balloons() triggers

### Page 2: Badge Collection
- [ ] Navigate to Badge Collection
- [ ] Verify header shows total badges earned
- [ ] Verify earned badges displayed with:
  - [ ] Colored icons (bronze/silver/gold)
  - [ ] Full opacity
  - [ ] Skill name and level
  - [ ] Date earned
- [ ] Toggle "Show Locked Badges"
- [ ] Verify locked badges displayed with:
  - [ ] Faded appearance
  - [ ] Grayscale filter
  - [ ] Lock icon overlay
- [ ] Test badge categories tabs
- [ ] Verify filtering works
- [ ] Test hover effects on badge cards

### Page 3: Current Goal
- [ ] Navigate to Current Goal
- [ ] Test with student who has active target:
  - [ ] Verify goal card displays
  - [ ] Verify format: "Self-Management: D → P"
  - [ ] Verify starting level shown
  - [ ] Verify target level shown
  - [ ] Verify date assigned shown
- [ ] Verify tips section displays 3-5 tips
- [ ] Verify recent progress section shows assessments
- [ ] Test with student who has no active target:
  - [ ] Verify "no goal" message displays
  - [ ] Verify general tips shown

### Badge Styling
- [ ] Open browser dev tools
- [ ] Inspect badge elements
- [ ] Verify CSS classes applied correctly
- [ ] Verify colors match specification:
  - [ ] Bronze: #CD7F32
  - [ ] Silver: #C0C0C0
  - [ ] Gold: #FFD700
- [ ] Test hover animations
- [ ] Test on mobile viewport

### Animation System
- [ ] Test celebration triggers:
  - [ ] New level achievement → balloons
  - [ ] Badge earned → balloons
  - [ ] Goal completed → balloons
- [ ] Verify celebrations don't repeat on page refresh
- [ ] Verify session_state tracks shown celebrations

### Navigation Flow
- [ ] Start at Student Home
- [ ] Navigate to Journey Map
- [ ] Click "View My Badges" → Badge Collection
- [ ] Click "See My Goal" → Current Goal
- [ ] Click "Back to Journey Map" → Journey Map
- [ ] Verify all navigation works
- [ ] Verify student selection persists

### Mobile Testing
- [ ] Test on mobile viewport (375px width)
- [ ] Verify layouts adapt
- [ ] Verify badges display in single column
- [ ] Verify buttons are touch-friendly
- [ ] Test on actual mobile device if possible

### Data Accuracy
- [ ] Verify journey map reflects actual assessment data
- [ ] Verify badge collection matches database
- [ ] Verify current goal matches assigned target
- [ ] Verify tips are relevant to skill and level

---

## Acceptance Criteria

- [ ] All 3 student pages created and functional
- [ ] Student selection on homepage (simple name dropdown, no password)
- [ ] Journey Map displays progression for all 17 skills
- [ ] Progress stages shown as: E → D → P → A
- [ ] Current level highlighted with "🎉 YOU ARE HERE!"
- [ ] Completed stages show checkmarks
- [ ] Future stages shown faded with lock icon
- [ ] Celebration animation (st.balloons) triggers on new level
- [ ] Badge Collection displays earned + locked badges
- [ ] Badges styled with bronze/silver/gold colors
- [ ] Faded badges shown for locked skills
- [ ] Lock icon overlay on locked badges
- [ ] Current Goal shows starting_level → target_level format
- [ ] Goal display includes tips and progress updates
- [ ] CSS loaded and applied consistently
- [ ] Animations work without repeating inappropriately
- [ ] Navigation between pages works smoothly
- [ ] Session state persists student selection
- [ ] Mobile-friendly responsive layout
- [ ] All pages load without errors
- [ ] User-friendly error messages for API failures

---

## Notes

- Student dashboard should be engaging and encouraging
- Use positive, growth-oriented language throughout
- Animations should celebrate achievements but not be overwhelming
- Badge system provides tangible goals and motivation
- Journey Map visual metaphor helps students understand progression
- Mobile-first design since students may access on tablets/phones
- No authentication required for MVP (simple name selection)
- Faded badges per clarification 4.1: grayscale + reduced opacity
- Badge icons per clarification 4.2: Heroicons SVG (medal + lock)
- Target format per clarification 3.2: "D → P" with starting and target levels

**Next Shard:** [Shard 7: Data Ingestion & Testing](Shard_7_Tasks.md)
