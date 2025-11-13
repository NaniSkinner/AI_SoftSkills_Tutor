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

# Fetch active skills progress
try:
    with st.spinner(f"Loading active skills progress for {student_name}..."):
        active_skills = APIClient.get_active_skills_progress(selected_student)
        progress = APIClient.get_student_progress(selected_student)

    if not active_skills:
        st.warning(f"No active skill targets found for {student_name}")
        st.info("Assign skill targets to this student to see their progress here.")
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

    # Active Skills Progress Chart
    st.markdown("### 📊 Active Skills Progress")
    st.markdown("*Showing current proficiency levels for all active skill targets*")

    # Prepare data for horizontal bar chart
    skill_names = [skill["skill_name"] for skill in active_skills]
    current_levels = [skill["current_level_numeric"] for skill in active_skills]
    current_level_text = [skill["current_level"] for skill in active_skills]
    target_levels = [skill["target_level_numeric"] for skill in active_skills]
    target_level_text = [skill["target_level"] for skill in active_skills]

    # Define color mapping for proficiency levels
    level_colors = {
        1: '#fbbf24',  # Emerging - Yellow
        2: '#fb923c',  # Developing - Orange
        3: '#60a5fa',  # Proficient - Blue
        4: '#34d399'   # Advanced - Green
    }

    # Create bar colors based on current level
    bar_colors = [level_colors.get(level, '#9ca3af') for level in current_levels]

    # Create horizontal bar chart
    fig = go.Figure()

    # Add current level bars
    fig.add_trace(go.Bar(
        y=skill_names,
        x=current_levels,
        orientation='h',
        name='Current Level',
        marker=dict(
            color=bar_colors,
            line=dict(color='#374151', width=1)
        ),
        text=current_level_text,
        textposition='auto',
        hovertemplate="<b>%{y}</b><br>Current: %{text}<br>Level: %{x}<extra></extra>"
    ))

    # Add target level markers
    fig.add_trace(go.Scatter(
        y=skill_names,
        x=target_levels,
        mode='markers',
        name='Target Level',
        marker=dict(
            symbol='diamond',
            size=14,
            color='#ef4444',
            line=dict(color='#7f1d1d', width=2)
        ),
        text=target_level_text,
        hovertemplate="<b>%{y}</b><br>Target: %{text}<br>Level: %{x}<extra></extra>"
    ))

    # Update layout
    fig.update_layout(
        title=f"{student_name}'s Active Skill Targets Progress",
        xaxis_title="Proficiency Level",
        yaxis_title="",
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4],
            ticktext=["Emerging", "Developing", "Proficient", "Advanced"],
            range=[0, 4.5]
        ),
        height=max(400, len(skill_names) * 60),  # Dynamic height based on number of skills
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True)

    # Skills summary table
    st.markdown("#### Skills Summary")

    summary_data = []
    for skill in active_skills:
        summary_data.append({
            "Skill": skill["skill_name"],
            "Category": skill["skill_category"],
            "Current Level": skill["current_level"],
            "Target Level": skill["target_level"]
        })

    df = pd.DataFrame(summary_data)
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
    download_data = []
    for skill in active_skills:
        download_data.append({
            "Student": student_name,
            "Skill": skill["skill_name"],
            "Category": skill["skill_category"],
            "Current_Level": skill["current_level"],
            "Current_Level_Numeric": skill["current_level_numeric"],
            "Target_Level": skill["target_level"],
            "Target_Level_Numeric": skill["target_level_numeric"]
        })

    if download_data:
        df_download = pd.DataFrame(download_data)
        csv = df_download.to_csv(index=False)

        st.download_button(
            label="📥 Download Active Skills Progress (CSV)",
            data=csv,
            file_name=f"{student_name.replace(' ', '_')}_active_skills_progress.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"❌ Error loading active skills progress: {str(e)}")
    st.info("💡 Make sure the backend API is running and accessible.")

    if st.button("🔄 Retry"):
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #999; padding: 10px; font-size: 0.85em;'>
        Made with 🍵 by <strong>Nani Skinner</strong>
    </div>
    """,
    unsafe_allow_html=True
)
