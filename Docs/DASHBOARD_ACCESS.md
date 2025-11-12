# Dashboard Access Guide

## Teacher Dashboard
**URL**: `http://localhost:8501`

This is the main entry point and loads automatically when accessing the application.

**Pages:**
1. Student Overview (`http://localhost:8501/01_Student_Overview`)
2. Skill Trends (`http://localhost:8501/02_Skill_Trends`)
3. Assessment Review (`http://localhost:8501/03_Assessment_Review`)
4. Target Assignment (`http://localhost:8501/04_Target_Assignment`)

---

## Student Dashboard
**URL**: `http://localhost:8501/Student_00_Home`

Students can access their dashboard by navigating to this URL directly.

**Pages:**
1. **Home / Character Selection** (`http://localhost:8501/Student_00_Home`)
   - Select your name from the dropdown
   - Choose your character avatar
   - Click "Start My Journey" to begin

2. **Journey Map** (`http://localhost:8501/Student_01_Journey_Map`)
   - **TWO VIEW MODES** (toggle at top of page):
     - **📊 Classic Progress Bars**: Traditional horizontal bars showing E→D→P→A
     - **🗺️ Road to Skills Map**: NEW! Interactive journey map with:
       - Whimsical winding paths for each skill category
       - Floating skill cards you can click to expand
       - 3-5 kid-friendly tips for each skill level
       - Student avatar moving along the path
       - Auto-focus on active teacher-assigned goals
       - Zoom modes: Overview (all skills) and Focused (single skill detail)
   - Progress stats (skills tracked, strong skills, badges earned)
   - Skills organized by category (SEL, EF, 21st Century)
   - Visual progression: 🌱 Emerging → 🥉 Developing → 🥈 Proficient → 🥇 Advanced

3. **Badge Collection** (`http://localhost:8501/Student_02_Badge_Collection`)
   - All 51 possible badges displayed
   - Bronze, Silver, Gold tiers
   - Progress bar showing completion percentage
   - Toggle to show/hide locked badges

4. **Current Goal** (`http://localhost:8501/Student_03_Current_Goal`)
   - Active skill target display
   - Age-appropriate tips (3 per skill)
   - Progress tracking (days working on goal)
   - Motivational messages

---

## Navigation Flow

### Teacher Dashboard Flow:
```
Home → 01_Student_Overview → 02_Skill_Trends → 03_Assessment_Review → 04_Target_Assignment
```

### Student Dashboard Flow:
```
Student_00_Home → Student_01_Journey_Map → Student_02_Badge_Collection → Student_03_Current_Goal
                    ↑                           ↑                           ↑
                    └───────────────────────────┴───────────────────────────┘
                              (All pages have "Home" button)
```

---

## Road to Skills Map - User Guide

### How to Use the Interactive Map

1. **Choosing Your View**
   - At the top of the Journey Map page, click the toggle to switch between:
     - 📊 **Classic Progress Bars**: Simple horizontal bars (familiar view)
     - 🗺️ **Road to Skills Map**: Interactive journey map (new feature!)

2. **Understanding the Icons**
   - 🌱 **Emerging**: You're just beginning - like a little plant starting to grow!
   - 🥉 **Developing**: You're making progress - you earned a Bronze medal!
   - 🥈 **Proficient**: You're doing great - you earned a Silver medal!
   - 🥇 **Advanced**: You're an expert - you earned a Gold medal!

3. **Exploring Skills in Overview Mode**
   - See all 17 skills at once on winding paths
   - Skills are grouped by type:
     - Orange/peach paths: Social-Emotional Learning (SEL)
     - Purple paths: Executive Function (EF)
     - Teal paths: 21st Century Skills
   - Click any skill card to see helpful tips
   - Click again to zoom into that skill's detailed journey

4. **Using Focused Mode**
   - Shows one skill's full journey: Emerging → Developing → Proficient → Advanced
   - Your current level glows with a special animation
   - Future levels are locked (shown with 🔒)
   - Past levels show checkmarks (✅)
   - Click each level to see 3-5 specific tips to help you grow

5. **Active Goals**
   - If your teacher assigns you a goal, the map automatically focuses on that skill
   - You'll see a yellow banner showing: "Starting Level → Target Level"
   - The target level pulses to show where you're headed

6. **Getting Tips**
   - Click any skill card to expand it
   - Read 3-5 kid-friendly, actionable tips
   - Tips are specific to your current level
   - Use the tips in daily life to improve that skill!

7. **Navigation**
   - **"All My Skills"** button: Return to overview showing all skills
   - **"[Skill Name] Journey"** button: View focused detail for that skill
   - Bottom of page: Links to Badges and Current Goal pages
   - Top right: Home button returns to student home

### Tips for a Great Experience
- Try both Classic and Road Map views to see which you like better!
- Revisit the map often to track your progress
- Read the tips for skills you're working on
- Celebrate when you level up to a new medal!

## Troubleshooting

### "Please select your name first" Error
If you navigate directly to a student page (Journey Map, Badges, or Goal) without selecting a student first, you'll see this message. Click the "Back to Home" button to return to the student home page and select your name.

### Road to Skills Map Not Loading
If the interactive map shows a spinning loader but never loads:
1. Check your internet connection (needed for React libraries)
2. Refresh the page
3. Switch to Classic view and back to Road Map
4. Check browser console for errors (F12 → Console tab)

### Tips Not Showing When Clicking Cards
If skill cards don't expand when clicked:
1. Make sure you're not in "locked" status (🔒 icon)
2. Try clicking directly on the card body, not the icon
3. Refresh the page if cards are unresponsive

### Avatar Not Appearing
If your chosen avatar doesn't show on the map:
1. Go back to Student Home and reselect your avatar
2. Make sure you clicked "Start My Journey" after selecting
3. Check that your internet connection is stable

### Session State
Student selection is stored in Streamlit's session state. If you refresh the page or navigate directly to a URL, you'll need to select your student again from the Student Home page.

### Page Not Found
All student pages are now located in the `/app/pages/` directory with proper naming:
- `Student_00_Home.py` - Character selection with avatar
- `Student_01_Journey_Map.py` - Skill progression (Classic + Road Map views)
- `Student_02_Badge_Collection.py` - Badge gallery
- `Student_03_Current_Goal.py` - Active goal with tips

---

## Quick Access Links

For local development:

**Teacher Dashboard**: [http://localhost:8501](http://localhost:8501)
**Student Dashboard**: [http://localhost:8501/Student_00_Home](http://localhost:8501/Student_00_Home)
**API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

*Last Updated: November 11, 2025*
