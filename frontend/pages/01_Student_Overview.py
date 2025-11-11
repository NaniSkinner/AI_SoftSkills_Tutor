"""
Page 1: Student Overview

Grid view of all students with key metrics and navigation.
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.api_client import APIClient
from utils.session_utils import initialize_session_state, set_teacher, set_selected_student
from utils.icon_utils import render_icon, get_page_icon

# Page configuration
st.set_page_config(
    page_title="Student Overview - Flourish Skills Tracker",
    page_icon="🌿",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page header with icon
title_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 0;">
    {get_page_icon("students", color="#3a5a44", size=44)}
    <h1 style="margin-left: 16px; margin-bottom: 0; color: #2c4733; font-family: 'DM Serif Display', serif;">
        Student Overview
    </h1>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("---")

# Teacher selection
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Select Your Role")

with col2:
    teacher_options = {
        "T001": "Ms. Rodriguez",
        "T002": "Mr. Thompson"
    }

    selected_teacher = st.selectbox(
        "Teacher",
        options=list(teacher_options.keys()),
        format_func=lambda x: teacher_options[x],
        index=0 if st.session_state.teacher_id == "T001" else 1,
        key="teacher_selector"
    )

    # Update session state if changed
    if selected_teacher != st.session_state.teacher_id:
        set_teacher(selected_teacher, teacher_options[selected_teacher])
        st.rerun()

st.markdown("---")

# Fetch students
try:
    with st.spinner("Loading students..."):
        students = APIClient.get_students(teacher_id=st.session_state.teacher_id)

    if not students:
        st.warning(f"No students found for {st.session_state.teacher_name}")
        st.stop()

    # Summary statistics
    st.markdown("### 📊 Summary")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    with stat_col1:
        st.metric("Total Students", len(students))

    # Calculate statistics
    students_with_targets = 0
    total_assessments = 0

    for student in students:
        try:
            progress = APIClient.get_student_progress(student["id"])
            total_assessments += progress.get("total_assessments", 0)
            if progress.get("active_targets", 0) > 0:
                students_with_targets += 1
        except:
            pass

    avg_assessments = total_assessments / len(students) if students else 0

    with stat_col2:
        st.metric("Avg Assessments", f"{avg_assessments:.1f}")

    with stat_col3:
        st.metric("Students with Active Targets", students_with_targets)

    with stat_col4:
        pending_assessments = len(APIClient.get_pending_assessments(limit=100))
        st.metric("Pending Reviews", pending_assessments)

    st.markdown("---")

    # Filters in sidebar
    st.sidebar.markdown("### 🔍 Filters")

    search_query = st.sidebar.text_input("Search by name", "")
    grade_filter = st.sidebar.selectbox("Filter by grade", ["All", "6", "7", "8"])
    sort_by = st.sidebar.selectbox(
        "Sort by",
        ["Name (A-Z)", "Name (Z-A)", "Most Assessments", "Recent Activity"]
    )

    # Apply filters
    filtered_students = students

    if search_query:
        filtered_students = [
            s for s in filtered_students
            if search_query.lower() in s["name"].lower()
        ]

    if grade_filter != "All":
        filtered_students = [
            s for s in filtered_students
            if str(s.get("grade", "")) == grade_filter
        ]

    # Sort students
    if sort_by == "Name (A-Z)":
        filtered_students = sorted(filtered_students, key=lambda x: x["name"])
    elif sort_by == "Name (Z-A)":
        filtered_students = sorted(filtered_students, key=lambda x: x["name"], reverse=True)

    # Display student grid
    st.markdown(f"### 👨‍🎓 Students ({len(filtered_students)})")

    if not filtered_students:
        st.info("No students match your filters.")
        st.stop()

    # Create 3-column grid
    cols_per_row = 3
    for i in range(0, len(filtered_students), cols_per_row):
        cols = st.columns(cols_per_row)

        for j, col in enumerate(cols):
            student_idx = i + j
            if student_idx < len(filtered_students):
                student = filtered_students[student_idx]

                with col:
                    # Student card with Flourish branding
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            border: 2px solid #6b8456;
                            border-radius: 24px;
                            padding: 24px;
                            margin-bottom: 20px;
                            background: linear-gradient(135deg, #faf7f2 0%, #f0ebe3 100%);
                            box-shadow: 0 4px 8px rgba(58, 90, 68, 0.12);
                            transition: all 0.3s ease;
                        ">
                            <h3 style="margin-top: 0; color: #2c4733; font-family: 'DM Serif Display', serif;">{student['name']}</h3>
                            <p style="color: #5a6b5c; font-size: 14px; font-family: 'Inter', sans-serif; font-weight: 500;">Grade {student.get('grade', 'N/A')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Fetch student progress
                        try:
                            progress = APIClient.get_student_progress(student["id"])

                            # Display metrics
                            metric_col1, metric_col2 = st.columns(2)

                            with metric_col1:
                                st.metric("Assessments", progress.get("total_assessments", 0))

                            with metric_col2:
                                st.metric("Badges", progress.get("total_badges", 0))

                            # Growth indicator with icon
                            recent_growth = progress.get("recent_growth", [])
                            if recent_growth:
                                growth_icon = render_icon("trending-up", color="#3a5a44", size=20, inline=True)
                                growth_text = "Growing"
                                growth_color = "#3a5a44"
                            else:
                                growth_icon = render_icon("arrow-right", color="#6b8456", size=20, inline=True)
                                growth_text = "Stable"
                                growth_color = "#6b8456"

                            st.markdown(f"""
                            <div style="text-align: center; margin-top: 8px;">
                                <span style="color: {growth_color}; font-weight: 600; font-family: 'Inter', sans-serif;">
                                    {growth_icon} {growth_text}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)

                            # Active targets with icon
                            active_targets = progress.get("active_targets", 0)
                            if active_targets > 0:
                                target_icon = render_icon("target", color="#d67e3a", size=18, inline=True)
                                st.markdown(f"""
                                <div style="background-color: #fef7ed; padding: 10px; border-radius: 12px;
                                             border-left: 4px solid #d67e3a; margin-top: 8px;
                                             font-family: 'Inter', sans-serif; font-size: 14px; color: #7a4f1a;">
                                    {target_icon} {active_targets} active target(s)
                                </div>
                                """, unsafe_allow_html=True)

                        except Exception as e:
                            st.error(f"Failed to load progress: {str(e)}")

                        # View Details button
                        if st.button(
                            "View Details",
                            key=f"view_{student['id']}",
                            use_container_width=True
                        ):
                            set_selected_student(student["id"], student["name"])
                            st.switch_page("pages/02_Skill_Trends.py")

except Exception as e:
    st.error(f"❌ Error loading students: {str(e)}")
    st.info("💡 Make sure the backend API is running and accessible.")

    if st.button("🔄 Retry"):
        st.rerun()
