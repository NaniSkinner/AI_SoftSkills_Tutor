"""
Page 4: Target Assignment

Assign and manage skill growth targets for students.
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.api_client import APIClient
from utils.session_utils import initialize_session_state, get_teacher
from utils.badge_utils import format_level_transition, get_badge_color, get_level_emoji
from utils.icon_utils import render_icon, get_page_icon

# Page configuration
st.set_page_config(
    page_title="Target Assignment - Flourish Skills Tracker",
    page_icon="🌿",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Page header with icon
title_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 0;">
    {get_page_icon("targets", color="#3a5a44", size=44)}
    <h1 style="margin-left: 16px; margin-bottom: 0; color: #2c4733; font-family: 'DM Serif Display', serif;">
        Target Assignment
    </h1>
</div>
"""
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("### Set skill growth goals for students")
st.markdown("---")

# Student selection
st.markdown("### Select Student")

try:
    teacher_id, _ = get_teacher()
    students = APIClient.get_students(teacher_id=teacher_id)
    student_dict = {s["id"]: s["name"] for s in students}

    selected_student = st.selectbox(
        "Student",
        options=list(student_dict.keys()),
        format_func=lambda x: student_dict[x],
        key="target_student_selector"
    )

    student_name = student_dict[selected_student]

except Exception as e:
    st.error(f"Error loading students: {str(e)}")
    st.stop()

st.markdown("---")

# All skills organized by category
ALL_SKILLS_BY_CATEGORY = {
    "SEL (Social-Emotional Learning)": [
        "Self-Awareness", "Self-Management", "Social Awareness",
        "Relationship Skills", "Responsible Decision-Making"
    ],
    "EF (Executive Function)": [
        "Working Memory", "Inhibitory Control", "Cognitive Flexibility",
        "Planning & Prioritization", "Organization", "Task Initiation",
        "Time Management", "Metacognition"
    ],
    "21st Century Skills": [
        "Critical Thinking", "Communication", "Collaboration",
        "Creativity & Innovation"
    ]
}

ALL_SKILLS = []
for skills in ALL_SKILLS_BY_CATEGORY.values():
    ALL_SKILLS.extend(skills)

# Fetch current targets and assessments
try:
    with st.spinner("Loading student data..."):
        active_targets = APIClient.get_student_targets(selected_student, completed=False)
        completed_targets = APIClient.get_student_targets(selected_student, completed=True)
        skill_trends = APIClient.get_skill_trends(selected_student)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Display current active target
st.markdown(f"### 🎯 Current Target for {student_name}")

if active_targets:
    target = active_targets[0]  # Should only be one active target

    transition = format_level_transition(target["starting_level"], target["target_level"])
    target_icon = render_icon("target", color="white", size=32, inline=False)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #3a5a44 0%, #3d8a96 100%);
        padding: 28px;
        border-radius: 24px;
        color: white;
        margin: 24px 0;
        box-shadow: 0 6px 16px rgba(58, 90, 68, 0.25);
        border: 3px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            {target_icon}
            <h2 style="margin: 0 0 0 12px; color: white; font-family: 'DM Serif Display', serif;">{target['skill_name']}</h2>
        </div>
        <h3 style="margin: 12px 0; color: white; font-family: 'Inter', sans-serif; font-weight: 700;">{transition}</h3>
        <p style="margin: 6px 0; font-family: 'Inter', sans-serif;"><strong>Assigned:</strong> {target['assigned_at'][:10]}</p>
        <p style="margin: 6px 0; font-family: 'Inter', sans-serif;"><strong>Assigned by:</strong> {target['assigned_by']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Check if target is achieved
    target_skill_data = next(
        (s for s in skill_trends if s["skill_name"] == target["skill_name"]),
        None
    )

    if target_skill_data and target_skill_data["assessments"]:
        latest_level = target_skill_data["assessments"][-1]["level"]
        target_level = target["target_level"]

        level_order = ["Emerging", "Developing", "Proficient", "Advanced"]
        latest_level_idx = level_order.index(latest_level)
        target_level_idx = level_order.index(target_level)

        if latest_level_idx >= target_level_idx:
            st.success(f"🎉 Target achieved! {student_name} has reached {latest_level}!")

            # Complete target button
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("✅ Mark Target Complete", key="complete_target"):
                    try:
                        APIClient.complete_target(target["id"])
                        st.success("Target marked as complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error completing target: {str(e)}")

            with col2:
                # Badge granting
                if st.button("🏅 Grant Badge", key="grant_badge"):
                    try:
                        teacher_id, _ = get_teacher()
                        badge_data = {
                            "student_id": selected_student,
                            "skill_name": target["skill_name"],
                            "level": target_level,
                            "granted_by": teacher_id
                        }
                        APIClient.grant_badge(badge_data)
                        st.success(f"Badge granted for {target['skill_name']}!")
                    except Exception as e:
                        st.error(f"Error granting badge: {str(e)}")

        else:
            progress_pct = (latest_level_idx / target_level_idx) * 100
            st.markdown(f"**Current Level:** {latest_level}")
            st.progress(progress_pct / 100)
            st.markdown(f"*{progress_pct:.0f}% toward target*")

else:
    st.info(f"No active target assigned for {student_name}")

st.markdown("---")

# Suggested next skills
st.markdown("### 💡 Suggested Skills to Target")

suggested_skills = []

for skill_trend in skill_trends:
    skill_name = skill_trend["skill_name"]
    if not skill_trend["assessments"]:
        continue

    latest_assessment = skill_trend["assessments"][-1]
    current_level = latest_assessment["level"]

    # Suggest skills at Developing or Proficient that can advance
    if current_level in ["Developing", "Proficient"]:
        level_order = ["Emerging", "Developing", "Proficient", "Advanced"]
        current_idx = level_order.index(current_level)

        if current_idx < 3:  # Can advance
            next_level = level_order[current_idx + 1]
            suggested_skills.append({
                "skill_name": skill_name,
                "current_level": current_level,
                "suggested_target": next_level,
                "category": skill_trend["skill_category"]
            })

if suggested_skills:
    # Group by category
    for category, category_skills_list in ALL_SKILLS_BY_CATEGORY.items():
        category_suggestions = [
            s for s in suggested_skills
            if s["skill_name"] in category_skills_list
        ]

        if category_suggestions:
            with st.expander(f"**{category}** ({len(category_suggestions)} suggestions)"):
                for suggestion in category_suggestions:
                    col1, col2, col3 = st.columns([3, 2, 2])

                    with col1:
                        st.markdown(f"**{suggestion['skill_name']}**")

                    with col2:
                        transition = format_level_transition(
                            suggestion['current_level'],
                            suggestion['suggested_target']
                        )
                        st.markdown(f"{transition}")

                    with col3:
                        if st.button(
                            "Assign This",
                            key=f"assign_{suggestion['skill_name']}",
                            disabled=len(active_targets) > 0  # Only one active target at a time
                        ):
                            try:
                                teacher_id, _ = get_teacher()
                                target_data = {
                                    "student_id": selected_student,
                                    "skill_name": suggestion['skill_name'],
                                    "starting_level": suggestion['current_level'],
                                    "target_level": suggestion['suggested_target'],
                                    "assigned_by": teacher_id
                                }
                                APIClient.assign_target(selected_student, target_data)
                                st.success(f"Target assigned: {suggestion['skill_name']}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error assigning target: {str(e)}")
else:
    st.info("No skill suggestions at this time. Complete more assessments to unlock suggestions.")

st.markdown("---")

# Manual target assignment
st.markdown("### ✍️ Manual Target Assignment")

if len(active_targets) > 0:
    st.warning("⚠️ Cannot assign new target: student already has an active target")
else:
    with st.form("manual_target_form"):
        st.markdown("Assign a custom skill growth target")

        # Skill selection
        form_col1, form_col2 = st.columns(2)

        with form_col1:
            selected_skill = st.selectbox(
                "Skill",
                options=ALL_SKILLS,
                key="manual_skill"
            )

        with form_col2:
            # Get current level for this skill if available
            current_skill_data = next(
                (s for s in skill_trends if s["skill_name"] == selected_skill),
                None
            )

            default_starting = "Emerging"
            if current_skill_data and current_skill_data["assessments"]:
                default_starting = current_skill_data["assessments"][-1]["level"]

            starting_level = st.selectbox(
                "Starting Level",
                options=["Emerging", "Developing", "Proficient"],
                index=["Emerging", "Developing", "Proficient", "Advanced"].index(default_starting)
                    if default_starting != "Advanced" else 2
            )

        # Target level
        level_order = ["Emerging", "Developing", "Proficient", "Advanced"]
        starting_idx = level_order.index(starting_level)
        possible_targets = level_order[starting_idx + 1:]

        if not possible_targets:
            st.error("Cannot create target: already at Advanced level")
            submit_manual = None
        else:
            target_level = st.selectbox(
                "Target Level",
                options=possible_targets
            )

            submit_manual = st.form_submit_button("🎯 Assign Target", use_container_width=True)

        if submit_manual:
            try:
                teacher_id, _ = get_teacher()
                target_data = {
                    "student_id": selected_student,
                    "skill_name": selected_skill,
                    "starting_level": starting_level,
                    "target_level": target_level,
                    "assigned_by": teacher_id
                }
                APIClient.assign_target(selected_student, target_data)
                st.success(f"Target assigned: {selected_skill} ({format_level_transition(starting_level, target_level)})")
                st.rerun()
            except Exception as e:
                st.error(f"Error assigning target: {str(e)}")

st.markdown("---")

# Completed targets history
if completed_targets:
    with st.expander(f"📜 View Completed Targets ({len(completed_targets)})"):
        for target in completed_targets:
            transition = format_level_transition(target["starting_level"], target["target_level"])

            st.markdown(f"""
            **{target['skill_name']}**: {transition}
            - Assigned: {target['assigned_at'][:10]}
            - Completed: {target['completed_at'][:10] if target['completed_at'] else 'N/A'}
            - Assigned by: {target['assigned_by']}
            """)
            st.markdown("---")
