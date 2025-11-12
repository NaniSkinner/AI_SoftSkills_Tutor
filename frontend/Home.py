"""
Flourish Skills Tracker - Teacher Dashboard Home Page
"""
import streamlit as st
import sys
import os

# Add current directory to path for utils imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils.api_client import APIClient
from utils.session_utils import initialize_session_state, set_teacher, get_teacher
from utils.icon_utils import render_icon, get_page_icon

# Page configuration
st.set_page_config(
    page_title="Flourish Skills Tracker - Teacher Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Get backend URL from environment
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# Title and welcome message with icon
title_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 0;">
    {get_page_icon("home", color="#3a5a44", size=48)}
    <h1 style="margin-left: 16px; margin-bottom: 0; color: #2c4733; font-family: 'DM Serif Display', serif;">
        Flourish Skills Tracker
    </h1>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("### Teacher Dashboard - AI-Powered Soft Skills Assessment")

st.markdown("---")

# Teacher selection
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Welcome!")

with col2:
    teacher_options = {
        "T001": "Ms. Rodriguez",
        "T002": "Mr. Thompson"
    }

    selected_teacher = st.selectbox(
        "Select Your Role",
        options=list(teacher_options.keys()),
        format_func=lambda x: teacher_options[x],
        index=0 if st.session_state.teacher_id == "T001" else 1,
        key="home_teacher_selector"
    )

    # Update session state if changed
    if selected_teacher != st.session_state.teacher_id:
        set_teacher(selected_teacher, teacher_options[selected_teacher])

teacher_id, teacher_name = get_teacher()
st.markdown(f"**Logged in as:** {teacher_name}")

st.markdown("---")

# Quick statistics
st.markdown("### 📊 Quick Overview")

try:
    # Fetch data
    students = APIClient.get_students(teacher_id=teacher_id)
    pending_assessments = APIClient.get_pending_assessments(limit=100)

    # Calculate stats
    total_students = len(students)
    pending_count = len(pending_assessments)

    # Count students with active targets
    students_with_targets = 0
    for student in students:
        try:
            targets = APIClient.get_student_targets(student["id"], completed=False)
            if targets:
                students_with_targets += 1
        except:
            pass

    # Display metrics
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Your Students", total_students)

    with metric_col2:
        st.metric("Pending Reviews", pending_count)

    with metric_col3:
        st.metric("Active Targets", students_with_targets)

    with metric_col4:
        # Recent corrections
        try:
            corrections = APIClient.get_recent_corrections(limit=10)
            recent_corrections = len([c for c in corrections if c.get("corrected_by") == teacher_id])
        except:
            recent_corrections = 0

        st.metric("Your Corrections", recent_corrections)

except Exception as e:
    st.warning("⚠️ Could not load statistics. Make sure the backend is running.")

st.markdown("---")

# Navigation cards
st.markdown("### 🚀 Quick Navigation")

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    students_icon = render_icon("users", color="white", size=32, inline=False)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3a5a44 0%, #6b8456 100%);
        padding: 28px;
        border-radius: 24px;
        margin: 12px 0;
        color: white;
        box-shadow: 0 5px 12px rgba(58, 90, 68, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            {students_icon}
            <h3 style="margin: 0 0 0 12px; color: white; font-family: 'DM Serif Display', serif;">Student Overview</h3>
        </div>
        <p style="margin: 0; font-family: 'Inter', sans-serif;">View all students with progress summaries and quick navigation</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Student Overview →", key="nav_overview", use_container_width=True):
        st.switch_page("pages/01_Student_Overview.py")

    trends_icon = render_icon("trending-up", color="white", size=32, inline=False)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #6b8456 0%, #8ba068 100%);
        padding: 28px;
        border-radius: 24px;
        margin: 12px 0;
        color: white;
        box-shadow: 0 5px 12px rgba(58, 90, 68, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            {trends_icon}
            <h3 style="margin: 0 0 0 12px; color: white; font-family: 'DM Serif Display', serif;">Skill Trends</h3>
        </div>
        <p style="margin: 0; font-family: 'Inter', sans-serif;">Interactive charts showing student skill progression over time</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Skill Trends →", key="nav_trends", use_container_width=True):
        st.switch_page("pages/02_Skill_Trends.py")

with nav_col2:
    review_icon = render_icon("clipboard-check", color="white", size=32, inline=False)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3d8a96 0%, #50a3b0 100%);
        padding: 28px;
        border-radius: 24px;
        margin: 12px 0;
        color: white;
        box-shadow: 0 5px 12px rgba(58, 90, 68, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            {review_icon}
            <h3 style="margin: 0 0 0 12px; color: white; font-family: 'DM Serif Display', serif;">Assessment Review</h3>
        </div>
        <p style="margin: 0; font-family: 'Inter', sans-serif;">Review and correct AI-generated assessments to improve accuracy</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Assessment Review →", key="nav_review", use_container_width=True):
        st.switch_page("pages/03_Assessment_Review.py")

    target_icon = render_icon("target", color="white", size=32, inline=False)
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #d67e3a 0%, #ef9f32 100%);
        padding: 28px;
        border-radius: 24px;
        margin: 12px 0;
        color: white;
        box-shadow: 0 5px 12px rgba(214, 126, 58, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            {target_icon}
            <h3 style="margin: 0 0 0 12px; color: white; font-family: 'DM Serif Display', serif;">Target Assignment</h3>
        </div>
        <p style="margin: 0; font-family: 'Inter', sans-serif;">Set skill growth goals and track student progress toward targets</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Target Assignment →", key="nav_targets", use_container_width=True):
        st.switch_page("pages/04_Target_Assignment.py")

st.markdown("---")

# System information
st.markdown("### 💡 About This System")

with st.expander("**What is Flourish Skills Tracker?**"):
    st.markdown("""
    Flourish Skills Tracker is an AI-powered assessment system that helps teachers track student
    soft skills development across **17 key competencies**:

    **Social-Emotional Learning (SEL):**
    - Self-Awareness, Self-Management, Social Awareness, Relationship Skills, Responsible Decision-Making

    **Executive Function (EF):**
    - Working Memory, Inhibitory Control, Cognitive Flexibility, Planning & Prioritization,
      Organization, Task Initiation, Time Management, Metacognition

    **21st Century Skills:**
    - Critical Thinking, Communication, Collaboration, Creativity & Innovation

    The system uses GPT-4 to analyze student observations (transcripts, reflections, peer feedback)
    and automatically assess skill levels. Teachers can review and correct these assessments,
    which helps the AI learn and improve over time.
    """)

with st.expander("**How does the AI work?**"):
    st.markdown("""
    The system uses a **few-shot learning** approach:

    1. **Data Collection**: Teachers input student observations (class discussions, reflections, etc.)
    2. **AI Assessment**: GPT-4 analyzes the data against skill rubrics and assigns levels (E/D/P/A)
    3. **Teacher Review**: Teachers approve or correct the AI's assessments
    4. **Continuous Learning**: Corrections are used as examples for future assessments

    This creates a feedback loop where the AI becomes more accurate over time, adapting to
    your teaching context and assessment style.
    """)

with st.expander("**What are the skill levels?**"):
    st.markdown("""
    Each skill is assessed on a 4-level rubric:

    - 🌱 **Emerging (E)**: Beginning to show awareness; needs significant support
    - 🥉 **Developing (D)**: Shows capability with guidance; developing consistency
    - 🥈 **Proficient (P)**: Demonstrates skill independently; consistent application
    - 🥇 **Advanced (A)**: Excels in skill; can teach others; innovates

    Students earn badges when they reach Developing, Proficient, or Advanced levels.
    """)

st.markdown("---")

# Backend health check
st.markdown("### 🔧 System Status")

try:
    response = APIClient.get_students(teacher_id=teacher_id)
    col1, col2 = st.columns(2)

    with col1:
        st.success("✅ Backend API: Connected")
    with col2:
        st.success("✅ Database: Connected")

except Exception as e:
    st.error("❌ System Error: Cannot connect to backend")
    st.info(f"Make sure the backend is running at: {BACKEND_URL}")
    st.code(str(e))

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        Flourish Skills Tracker v1.0.0 | Teacher Dashboard | Powered by GPT-4o via OpenRouter
    </div>
    <div style='text-align: center; color: #999; padding: 10px; font-size: 0.85em;'>
        Made with 🍵 by <strong>Nani Skinner</strong>
    </div>
    """,
    unsafe_allow_html=True
)
