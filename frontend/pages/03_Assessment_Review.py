"""
Page 3: Assessment Review

Teacher workflow for reviewing and correcting AI-generated assessments.
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.api_client import APIClient
from utils.session_utils import (
    initialize_session_state, get_teacher,
    increment_review_stat, advance_review_index, go_to_previous_review,
    get_review_progress, reset_review_state
)
from utils.badge_utils import get_badge_color, get_level_emoji
from utils.icon_utils import render_icon, get_page_icon

# Page configuration
st.set_page_config(
    page_title="Assessment Review - Flourish Skills Tracker",
    page_icon="🌿",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page header with icon
title_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 0;">
    {get_page_icon("review", color="#3a5a44", size=44)}
    <h1 style="margin-left: 16px; margin-bottom: 0; color: #2c4733; font-family: 'DM Serif Display', serif;">
        Assessment Review
    </h1>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("### Review and correct AI-generated skill assessments")
st.markdown("---")

# Sidebar filters
st.sidebar.markdown("### 🔍 Filters")

# Fetch students for filter
try:
    teacher_id, _ = get_teacher()
    students = APIClient.get_students(teacher_id=teacher_id)
    student_dict = {"All": "All Students"}
    student_dict.update({s["id"]: s["name"] for s in students})
except:
    student_dict = {"All": "All Students"}

filter_student = st.sidebar.selectbox(
    "Student",
    options=list(student_dict.keys()),
    format_func=lambda x: student_dict[x],
    key="filter_student"
)

# All 17 skills
ALL_SKILLS = [
    "Self-Awareness", "Self-Management", "Social Awareness",
    "Relationship Skills", "Responsible Decision-Making",
    "Working Memory", "Inhibitory Control", "Cognitive Flexibility",
    "Planning & Prioritization", "Organization", "Task Initiation",
    "Time Management", "Metacognition",
    "Critical Thinking", "Communication", "Collaboration",
    "Creativity & Innovation"
]

filter_skill = st.sidebar.selectbox(
    "Skill",
    options=["All"] + ALL_SKILLS,
    key="filter_skill"
)

low_confidence_only = st.sidebar.checkbox(
    "Low Confidence Only (<0.7)",
    value=False
)

confidence_threshold = st.sidebar.slider(
    "Minimum Confidence",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

if st.sidebar.button("🔍 Apply Filters", use_container_width=True):
    with st.spinner("Loading assessments..."):
        try:
            # Fetch pending assessments
            limit = 100
            min_conf = confidence_threshold if not low_confidence_only else 0.0

            assessments = APIClient.get_pending_assessments(
                limit=limit,
                min_confidence=min_conf
            )

            # Apply client-side filters
            if filter_student != "All":
                assessments = [a for a in assessments if a["student_id"] == filter_student]

            if filter_skill != "All":
                assessments = [a for a in assessments if a["skill_name"] == filter_skill]

            if low_confidence_only:
                assessments = [a for a in assessments if a["confidence_score"] < 0.7]

            # Store in session state
            st.session_state.assessments_to_review = assessments
            st.session_state.review_index = 0
            st.session_state.filters_applied = True

            # Reset stats
            st.session_state.reviews_approved = 0
            st.session_state.reviews_corrected = 0
            st.session_state.reviews_skipped = 0

            st.success(f"Found {len(assessments)} assessments to review")
            st.rerun()

        except Exception as e:
            st.error(f"Error loading assessments: {str(e)}")

if st.sidebar.button("🔄 Reset Filters"):
    reset_review_state()
    st.rerun()

st.markdown("---")

# Main review area
if not st.session_state.filters_applied or not st.session_state.assessments_to_review:
    st.info("👈 Apply filters in the sidebar to load assessments for review")
    st.markdown("""
    ### How to use this page:

    1. **Apply Filters**: Select student, skill, and confidence criteria
    2. **Review Assessment**: Read the AI's assessment and justification
    3. **Choose Action**:
       - ✅ **Approve** - AI assessment is correct
       - ✏️ **Correct** - Adjust the level or justification
       - ⏭️ **Skip** - Move to next without action
    4. **Track Progress**: See how many assessments you've reviewed

    Your corrections will help the AI learn and improve future assessments!
    """)
    st.stop()

# Get current assessment
progress = get_review_progress()
assessments = st.session_state.assessments_to_review

if progress["current_index"] >= len(assessments):
    # Completed review
    st.success("🎉 All assessments reviewed!")

    st.markdown(f"""
    ### Review Session Summary

    - ✅ **Approved**: {progress['approved']}
    - ✏️ **Corrected**: {progress['corrected']}
    - ⏭️ **Skipped**: {progress['skipped']}
    - **Total Processed**: {progress['completed']}
    """)

    if st.button("Review More Assessments"):
        reset_review_state()
        st.rerun()

    st.stop()

current_assessment = assessments[progress["current_index"]]

# Progress indicator
st.markdown(f"### Assessment {progress['current_index'] + 1} of {len(assessments)}")

prog_col1, prog_col2 = st.columns([3, 1])

with prog_col1:
    progress_pct = ((progress["current_index"] + 1) / len(assessments)) * 100
    st.progress(progress_pct / 100)

with prog_col2:
    st.markdown(f"**{progress['completed']}** completed")

st.markdown("---")

# Display assessment details
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📋 Assessment Details")

    # Student and skill
    st.markdown(f"**Student:** {current_assessment['student_id']}")
    st.markdown(f"**Skill:** {current_assessment['skill_name']} ({current_assessment['skill_category']})")
    st.markdown(f"**Date Created:** {current_assessment['created_at'][:10]}")

    # Current level with badge - Flourish styled
    level = current_assessment['level']

    # Map abbreviations to full level names if needed
    level_map = {
        "E": "Emerging",
        "D": "Developing",
        "P": "Proficient",
        "A": "Advanced"
    }
    full_level_name = level_map.get(level, level)  # Use abbreviation mapping or original if already full name

    level_emoji = get_level_emoji(full_level_name)

    # Map level to Flourish colors
    level_colors = {
        "Emerging": "background: #e8e5df; color: #2c3e30; border: 2px solid #6b8456;",
        "Developing": "background: linear-gradient(135deg, #6b8456, #8ba068); color: white;",
        "Proficient": "background: linear-gradient(135deg, #3a5a44, #3d8a96); color: white;",
        "Advanced": "background: linear-gradient(135deg, #d67e3a, #ef9f32); color: white;"
    }
    level_style = level_colors.get(full_level_name, "background: #e8e5df; color: #2c3e30;")

    st.markdown(f"""
    <div style="
        {level_style}
        padding: 18px;
        border-radius: 24px;
        text-align: center;
        margin: 12px 0;
        box-shadow: 0 4px 8px rgba(58, 90, 68, 0.15);
    ">
        <h2 style="margin: 0; font-family: 'DM Serif Display', serif;">{level_emoji} {full_level_name}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Confidence score with Flourish colors
    confidence = current_assessment['confidence_score']
    confidence_color = "#3a5a44" if confidence >= 0.7 else "#d67e3a"

    st.markdown(f"**Confidence Score:** {confidence:.2f}")
    st.progress(confidence)

    if confidence < 0.7:
        warning_icon = render_icon("alert-circle", color="#d67e3a", size=20, inline=True)
        st.markdown(f"""
        <div style="background-color: #fef7ed; padding: 12px; border-radius: 12px;
                     border-left: 4px solid #d67e3a; margin-top: 8px;
                     font-family: 'Inter', sans-serif; color: #7a4f1a;">
            {warning_icon} Low confidence - AI is uncertain about this assessment
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 📊 Statistics")
    st.metric("✅ Approved", progress['approved'])
    st.metric("✏️ Corrected", progress['corrected'])
    st.metric("⏭️ Skipped", progress['skipped'])

st.markdown("---")

# AI Justification
st.markdown("### 💭 AI Justification")
st.markdown(current_assessment['justification'])

# Source quote
if current_assessment.get('source_quote'):
    with st.expander("📝 View Source Quote"):
        st.markdown(current_assessment['source_quote'])

st.markdown("---")

# Correction form
st.markdown("### ✏️ Review Action")

action_tabs = st.tabs(["✅ Approve", "✏️ Correct", "⏭️ Skip"])

with action_tabs[0]:
    # Approve action
    st.markdown("""
    **Approve this assessment as correct**

    The AI's level and justification are accurate. This assessment will be marked as reviewed.
    """)

    if st.button("✅ Approve Assessment", key="approve_btn", use_container_width=True):
        try:
            teacher_id, _ = get_teacher()
            APIClient.approve_assessment(
                assessment_id=current_assessment['id'],
                approved_by=teacher_id
            )

            increment_review_stat("approved")
            advance_review_index()

            st.success("✅ Assessment approved!")
            st.rerun()

        except Exception as e:
            st.error(f"Error approving assessment: {str(e)}")

with action_tabs[1]:
    # Correction action
    st.markdown("**Correct the AI's assessment**")

    with st.form("correction_form"):
        # Corrected level
        # Map abbreviations to full level names if needed
        level_map = {
            "E": "Emerging",
            "D": "Developing",
            "P": "Proficient",
            "A": "Advanced"
        }
        full_level = level_map.get(level, level)  # Use abbreviation mapping or original if already full name

        corrected_level = st.selectbox(
            "Corrected Level",
            options=["Emerging", "Developing", "Proficient", "Advanced"],
            index=["Emerging", "Developing", "Proficient", "Advanced"].index(full_level)
        )

        # Corrected justification
        corrected_justification = st.text_area(
            "Corrected Justification",
            value=current_assessment['justification'],
            height=150
        )

        # Teacher notes
        teacher_notes = st.text_area(
            "Teacher Notes (Optional)",
            placeholder="Why did you make this correction?",
            height=100
        )

        # Submit correction
        submit_correction = st.form_submit_button(
            "✏️ Submit Correction",
            use_container_width=True
        )

        if submit_correction:
            try:
                teacher_id, _ = get_teacher()

                correction_data = {
                    "assessment_id": current_assessment['id'],
                    "corrected_level": corrected_level,
                    "corrected_justification": corrected_justification,
                    "teacher_notes": teacher_notes,
                    "corrected_by": teacher_id
                }

                APIClient.submit_correction(correction_data)

                increment_review_stat("corrected")
                advance_review_index()

                st.success("✏️ Correction submitted!")
                st.rerun()

            except Exception as e:
                st.error(f"Error submitting correction: {str(e)}")

with action_tabs[2]:
    # Skip action
    st.markdown("""
    **Skip this assessment**

    Move to the next assessment without taking action. You can come back to this later.
    """)

    if st.button("⏭️ Skip to Next", key="skip_btn", use_container_width=True):
        increment_review_stat("skipped")
        advance_review_index()
        st.rerun()

st.markdown("---")

# Navigation controls
nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if st.button("← Previous", disabled=(progress["current_index"] == 0)):
        go_to_previous_review()
        st.rerun()

with nav_col3:
    if st.button("Next →", disabled=(progress["current_index"] >= len(assessments) - 1)):
        advance_review_index()
        st.rerun()
