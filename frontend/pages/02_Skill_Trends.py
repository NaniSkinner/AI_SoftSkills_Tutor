"""
Page 2: Skill Trends

Detailed skill progression charts and assessment history for a student.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.api_client import APIClient
from utils.session_utils import initialize_session_state, get_selected_student
from utils.badge_utils import get_level_numeric, get_progress_color, render_badge_html
from utils.icon_utils import render_icon, get_page_icon

# Page configuration
st.set_page_config(
    page_title="Skill Trends - Flourish Skills Tracker",
    page_icon="🌿",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page header with icon
title_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 0;">
    {get_page_icon("trends", color="#3a5a44", size=44)}
    <h1 style="margin-left: 16px; margin-bottom: 0; color: #2c4733; font-family: 'DM Serif Display', serif;">
        Skill Trends & Progress
    </h1>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("---")

# Student selection
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### Select Student")

with col2:
    try:
        # Fetch all students for current teacher
        students = APIClient.get_students(teacher_id=st.session_state.teacher_id)
        student_dict = {s["id"]: s["name"] for s in students}

        # Pre-select if coming from overview
        selected_student_id, _ = get_selected_student()
        default_index = 0

        if selected_student_id and selected_student_id in student_dict:
            default_index = list(student_dict.keys()).index(selected_student_id)

        selected_student = st.selectbox(
            "Student",
            options=list(student_dict.keys()),
            format_func=lambda x: student_dict[x],
            index=default_index,
            key="student_selector"
        )

        student_name = student_dict[selected_student]

    except Exception as e:
        st.error(f"Error loading students: {str(e)}")
        st.stop()

st.markdown("---")

# Navigation buttons
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 4])

with nav_col1:
    if st.button("← Back to Overview"):
        st.switch_page("pages/01_Student_Overview.py")

with nav_col2:
    if st.button("Review Assessments →"):
        st.switch_page("pages/03_Assessment_Review.py")

st.markdown("---")

# Fetch skill trends
try:
    with st.spinner(f"Loading skill trends for {student_name}..."):
        skill_trends = APIClient.get_skill_trends(selected_student)
        progress = APIClient.get_student_progress(selected_student)

    if not skill_trends:
        st.warning(f"No assessment data found for {student_name}")
        st.info("Data will appear once assessments are generated for this student.")
        st.stop()

    # Display progress summary
    st.markdown(f"### 🎓 {student_name}'s Progress")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric("Total Assessments", progress.get("total_assessments", 0))

    with summary_col2:
        st.metric("Badges Earned", progress.get("total_badges", 0))

    with summary_col3:
        st.metric("Active Targets", progress.get("active_targets", 0))

    st.markdown("---")

    # Group skills by category
    skill_categories = {
        "SEL": [],
        "EF": [],
        "21st Century": []
    }

    for skill_trend in skill_trends:
        category = skill_trend["skill_category"]
        if category in skill_categories:
            skill_categories[category].append(skill_trend)

    # Display skills by category
    st.markdown("### 📚 Skills by Category")

    for category, skills in skill_categories.items():
        if not skills:
            continue

        with st.expander(f"**{category}** ({len(skills)} skills)", expanded=(category == "SEL")):
            for skill in skills:
                skill_name = skill["skill_name"]
                assessments = skill["assessments"]

                if not assessments:
                    continue

                # Get latest assessment
                latest = assessments[-1]
                current_level = latest["level"]

                # Create mini timeline
                col_skill, col_timeline, col_date = st.columns([2, 3, 2])

                with col_skill:
                    st.markdown(f"**{skill_name}**")

                with col_timeline:
                    # Show progression
                    levels_seen = list(set([a["level"] for a in assessments]))
                    level_order = ["Emerging", "Developing", "Proficient", "Advanced"]
                    ordered_levels = [l for l in level_order if l in levels_seen]

                    timeline_html = " → ".join([
                        f"<span style='color: {get_progress_color(l)}; font-weight: bold;'>{l[0]}</span>"
                        for l in ordered_levels
                    ])
                    st.markdown(timeline_html, unsafe_allow_html=True)

                with col_date:
                    latest_date = latest["date"]
                    st.markdown(f"*{latest_date}*")

    st.markdown("---")

    # Detailed skill chart
    st.markdown("### 📊 Detailed Skill Chart")

    # Skill selector
    skill_names = [s["skill_name"] for s in skill_trends]
    selected_skill = st.selectbox(
        "Select a skill to view detailed progression",
        options=skill_names,
        key="skill_chart_selector"
    )

    # Find selected skill data
    selected_skill_data = next(
        (s for s in skill_trends if s["skill_name"] == selected_skill),
        None
    )

    if selected_skill_data:
        assessments = selected_skill_data["assessments"]

        # Prepare chart data
        dates = [a["date"] for a in assessments]
        levels_numeric = [a["level_numeric"] for a in assessments]
        levels_text = [a["level"] for a in assessments]
        confidences = [a["confidence"] for a in assessments]

        # Create Plotly chart
        fig = go.Figure()

        # Add line and markers with Flourish green color
        fig.add_trace(go.Scatter(
            x=dates,
            y=levels_numeric,
            mode='lines+markers',
            name=selected_skill,
            line=dict(color='#3a5a44', width=3),
            marker=dict(size=12, color=confidences, colorscale='YlGn',
                       showscale=True, colorbar=dict(title="Confidence")),
            text=levels_text,
            hovertemplate="<b>%{text}</b><br>Date: %{x}<br>Confidence: %{marker.color:.2f}<extra></extra>"
        ))

        # Update layout
        fig.update_layout(
            title=f"{selected_skill} Progression Over Time",
            xaxis_title="Date",
            yaxis_title="Proficiency Level",
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3, 4],
                ticktext=["Emerging", "Developing", "Proficient", "Advanced"],
                range=[0.5, 4.5]
            ),
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Recent assessments table
        st.markdown(f"#### Recent Assessments for {selected_skill}")

        # Show last 5 assessments
        recent_assessments = assessments[-5:]

        assessment_data = []
        for a in reversed(recent_assessments):
            assessment_data.append({
                "Date": a["date"],
                "Level": a["level"],
                "Confidence": f"{a['confidence']:.2f}"
            })

        df = pd.DataFrame(assessment_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Recent growth highlights
    st.markdown("### 🌟 Recent Growth Highlights")

    recent_growth = progress.get("recent_growth", [])

    if recent_growth:
        for growth in recent_growth:
            skill_name = growth["skill_name"]
            from_level = growth["from_level"]
            to_level = growth["to_level"]
            date = growth["date"]

            st.success(f"**{skill_name}**: {from_level} → {to_level} (on {date})")
    else:
        st.info("No recent level changes. Keep observing and assessing!")

    st.markdown("---")

    # Download data
    st.markdown("### 💾 Download Data")

    # Prepare CSV data
    all_assessment_data = []
    for skill_trend in skill_trends:
        skill_name = skill_trend["skill_name"]
        category = skill_trend["skill_category"]

        for a in skill_trend["assessments"]:
            all_assessment_data.append({
                "Student": student_name,
                "Skill": skill_name,
                "Category": category,
                "Date": a["date"],
                "Level": a["level"],
                "Level_Numeric": a["level_numeric"],
                "Confidence": a["confidence"]
            })

    if all_assessment_data:
        df_download = pd.DataFrame(all_assessment_data)
        csv = df_download.to_csv(index=False)

        st.download_button(
            label="📥 Download All Skill Trends (CSV)",
            data=csv,
            file_name=f"{student_name.replace(' ', '_')}_skill_trends.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"❌ Error loading skill trends: {str(e)}")
    st.info("💡 Make sure the backend API is running and accessible.")

    if st.button("🔄 Retry"):
        st.rerun()
