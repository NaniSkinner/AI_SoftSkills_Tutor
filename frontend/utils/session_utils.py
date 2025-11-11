"""
Session State Management Utilities

Helper functions for managing Streamlit session state across pages.
"""

import streamlit as st
from typing import Optional


def initialize_session_state():
    """
    Initialize all session state variables with default values.

    Call this at the start of each page to ensure consistent state.
    """
    # Teacher context
    if "teacher_id" not in st.session_state:
        st.session_state.teacher_id = "T001"  # Default to Ms. Rodriguez

    if "teacher_name" not in st.session_state:
        st.session_state.teacher_name = "Ms. Rodriguez"

    # Student selection
    if "selected_student" not in st.session_state:
        st.session_state.selected_student = None

    if "selected_student_name" not in st.session_state:
        st.session_state.selected_student_name = None

    # Assessment review state
    if "review_index" not in st.session_state:
        st.session_state.review_index = 0

    if "assessments_to_review" not in st.session_state:
        st.session_state.assessments_to_review = []

    if "filters_applied" not in st.session_state:
        st.session_state.filters_applied = False

    # Review statistics
    if "reviews_approved" not in st.session_state:
        st.session_state.reviews_approved = 0

    if "reviews_corrected" not in st.session_state:
        st.session_state.reviews_corrected = 0

    if "reviews_skipped" not in st.session_state:
        st.session_state.reviews_skipped = 0


def set_teacher(teacher_id: str, teacher_name: str):
    """
    Set the current teacher context.

    Args:
        teacher_id: Teacher ID (e.g., "T001")
        teacher_name: Teacher display name
    """
    st.session_state.teacher_id = teacher_id
    st.session_state.teacher_name = teacher_name


def get_teacher() -> tuple[str, str]:
    """
    Get the current teacher context.

    Returns:
        Tuple of (teacher_id, teacher_name)
    """
    initialize_session_state()
    return st.session_state.teacher_id, st.session_state.teacher_name


def set_selected_student(student_id: str, student_name: str):
    """
    Set the currently selected student for detailed views.

    Args:
        student_id: Student ID (e.g., "S001")
        student_name: Student display name
    """
    st.session_state.selected_student = student_id
    st.session_state.selected_student_name = student_name


def get_selected_student() -> tuple[Optional[str], Optional[str]]:
    """
    Get the currently selected student.

    Returns:
        Tuple of (student_id, student_name) or (None, None)
    """
    initialize_session_state()
    return st.session_state.selected_student, st.session_state.selected_student_name


def navigate_to_student(student_id: str, student_name: str):
    """
    Set student selection and prepare for navigation to student details.

    Args:
        student_id: Student ID
        student_name: Student display name
    """
    set_selected_student(student_id, student_name)
    # Note: Actual page navigation is handled by Streamlit page navigation
    # This just sets the state


def reset_review_state():
    """
    Reset the assessment review state to start fresh.
    """
    st.session_state.review_index = 0
    st.session_state.assessments_to_review = []
    st.session_state.filters_applied = False
    st.session_state.reviews_approved = 0
    st.session_state.reviews_corrected = 0
    st.session_state.reviews_skipped = 0


def increment_review_stat(stat_type: str):
    """
    Increment a review statistic counter.

    Args:
        stat_type: One of "approved", "corrected", "skipped"
    """
    if stat_type == "approved":
        st.session_state.reviews_approved += 1
    elif stat_type == "corrected":
        st.session_state.reviews_corrected += 1
    elif stat_type == "skipped":
        st.session_state.reviews_skipped += 1


def advance_review_index():
    """
    Move to the next assessment in the review queue.
    """
    if st.session_state.review_index < len(st.session_state.assessments_to_review) - 1:
        st.session_state.review_index += 1
        return True
    return False


def go_to_previous_review():
    """
    Move to the previous assessment in the review queue.
    """
    if st.session_state.review_index > 0:
        st.session_state.review_index -= 1
        return True
    return False


def get_review_progress() -> dict:
    """
    Get the current review session progress.

    Returns:
        Dictionary with review statistics
    """
    initialize_session_state()
    return {
        "current_index": st.session_state.review_index,
        "total_assessments": len(st.session_state.assessments_to_review),
        "approved": st.session_state.reviews_approved,
        "corrected": st.session_state.reviews_corrected,
        "skipped": st.session_state.reviews_skipped,
        "completed": st.session_state.reviews_approved + st.session_state.reviews_corrected
    }


def is_review_complete() -> bool:
    """
    Check if all assessments in the review queue have been processed.

    Returns:
        True if at the end of the review queue
    """
    initialize_session_state()
    return st.session_state.review_index >= len(st.session_state.assessments_to_review) - 1
