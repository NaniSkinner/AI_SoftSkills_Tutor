"""
API Client Utility

Centralized client for communicating with the FastAPI backend.
Handles all HTTP requests to the backend REST API.
"""

import requests
import os
import logging
from typing import Optional, Dict, Any, List

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
logger = logging.getLogger(__name__)


class APIClient:
    """
    Static client for making API requests to the backend.

    All methods return response data directly or raise exceptions on error.
    """

    # ================== Students Methods ==================

    @staticmethod
    def get_students(teacher_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all students, optionally filtered by teacher.

        Args:
            teacher_id: Optional teacher ID to filter students

        Returns:
            List of student dictionaries
        """
        try:
            url = f"{BACKEND_URL}/api/students/"
            params = {}
            if teacher_id:
                params["teacher_id"] = teacher_id

            logger.info(f"Fetching students (teacher_id={teacher_id})")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching students: {str(e)}")
            raise Exception(f"Failed to fetch students: {str(e)}")

    @staticmethod
    def get_student_progress(student_id: str) -> Dict[str, Any]:
        """
        Get comprehensive progress metrics for a student.

        Args:
            student_id: Student ID

        Returns:
            Student progress dictionary with metrics
        """
        try:
            url = f"{BACKEND_URL}/api/students/{student_id}/progress"

            logger.info(f"Fetching progress for student {student_id}")
            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                raise Exception(f"Student {student_id} not found")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching student progress: {str(e)}")
            raise Exception(f"Failed to fetch student progress: {str(e)}")

    # ================== Assessments Methods ==================

    @staticmethod
    def get_student_assessments(student_id: str) -> List[Dict[str, Any]]:
        """
        Get all assessments for a specific student.

        Args:
            student_id: Student ID

        Returns:
            List of assessment dictionaries
        """
        try:
            url = f"{BACKEND_URL}/api/assessments/student/{student_id}"

            logger.info(f"Fetching assessments for student {student_id}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching assessments: {str(e)}")
            raise Exception(f"Failed to fetch assessments: {str(e)}")

    @staticmethod
    def get_skill_trends(student_id: str) -> List[Dict[str, Any]]:
        """
        Get skill trend data for charting student progress over time.

        Args:
            student_id: Student ID

        Returns:
            List of skill trend dictionaries
        """
        try:
            url = f"{BACKEND_URL}/api/assessments/skill-trends/{student_id}"

            logger.info(f"Fetching skill trends for student {student_id}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching skill trends: {str(e)}")
            raise Exception(f"Failed to fetch skill trends: {str(e)}")

    @staticmethod
    def get_pending_assessments(limit: int = 50, min_confidence: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Get pending (uncorrected) assessments that need teacher review.

        Args:
            limit: Maximum number of assessments to return
            min_confidence: Optional minimum confidence score filter

        Returns:
            List of pending assessment dictionaries
        """
        try:
            url = f"{BACKEND_URL}/api/assessments/pending"
            params = {"limit": limit}
            if min_confidence is not None:
                params["min_confidence"] = min_confidence

            logger.info(f"Fetching pending assessments (limit={limit})")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching pending assessments: {str(e)}")
            raise Exception(f"Failed to fetch pending assessments: {str(e)}")

    @staticmethod
    def get_assessment_by_id(assessment_id: int) -> Dict[str, Any]:
        """
        Get a specific assessment by ID.

        Args:
            assessment_id: Assessment ID

        Returns:
            Assessment dictionary
        """
        try:
            url = f"{BACKEND_URL}/api/assessments/{assessment_id}"

            logger.info(f"Fetching assessment {assessment_id}")
            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                raise Exception(f"Assessment {assessment_id} not found")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching assessment: {str(e)}")
            raise Exception(f"Failed to fetch assessment: {str(e)}")

    # ================== Corrections Methods ==================

    @staticmethod
    def submit_correction(correction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a teacher correction for an AI-generated assessment.

        Args:
            correction_data: Dictionary with correction details
                - assessment_id (int)
                - corrected_level (str)
                - corrected_justification (str, optional)
                - teacher_notes (str, optional)
                - corrected_by (str)

        Returns:
            Correction response dictionary with success status
        """
        try:
            url = f"{BACKEND_URL}/api/corrections/submit"

            logger.info(f"Submitting correction for assessment {correction_data.get('assessment_id')}")
            response = requests.post(url, json=correction_data, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error submitting correction: {str(e)}")
            raise Exception(f"Failed to submit correction: {str(e)}")

    @staticmethod
    def approve_assessment(assessment_id: int, approved_by: str) -> Dict[str, Any]:
        """
        Approve an AI assessment as correct without making changes.

        Args:
            assessment_id: Assessment ID to approve
            approved_by: Teacher ID approving the assessment

        Returns:
            Success response dictionary
        """
        try:
            url = f"{BACKEND_URL}/api/corrections/assessments/{assessment_id}/approve"
            data = {
                "assessment_id": assessment_id,
                "approved_by": approved_by
            }

            logger.info(f"Approving assessment {assessment_id}")
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error approving assessment: {str(e)}")
            raise Exception(f"Failed to approve assessment: {str(e)}")

    @staticmethod
    def get_recent_corrections(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent teacher corrections.

        Args:
            limit: Maximum number of corrections to return

        Returns:
            List of correction dictionaries
        """
        try:
            url = f"{BACKEND_URL}/api/corrections/recent"
            params = {"limit": limit}

            logger.info(f"Fetching recent corrections (limit={limit})")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching corrections: {str(e)}")
            raise Exception(f"Failed to fetch corrections: {str(e)}")

    # ================== Targets Methods ==================

    @staticmethod
    def assign_target(student_id: str, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assign a skill growth target to a student.

        Args:
            student_id: Student ID
            target_data: Dictionary with target details
                - student_id (str)
                - skill_name (str)
                - starting_level (str)
                - target_level (str)
                - assigned_by (str)

        Returns:
            Target response dictionary
        """
        try:
            url = f"{BACKEND_URL}/api/students/{student_id}/target-skill"

            logger.info(f"Assigning target to student {student_id}: {target_data.get('skill_name')}")
            response = requests.post(url, json=target_data, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error assigning target: {str(e)}")
            raise Exception(f"Failed to assign target: {str(e)}")

    @staticmethod
    def get_student_targets(student_id: str, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Get all skill targets for a student.

        Args:
            student_id: Student ID
            completed: Optional filter for completed/active targets

        Returns:
            List of target dictionaries
        """
        try:
            url = f"{BACKEND_URL}/api/students/{student_id}/targets"
            params = {}
            if completed is not None:
                params["completed"] = str(completed).lower()

            logger.info(f"Fetching targets for student {student_id}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching targets: {str(e)}")
            raise Exception(f"Failed to fetch targets: {str(e)}")

    @staticmethod
    def complete_target(target_id: int) -> Dict[str, Any]:
        """
        Mark a skill target as completed.

        Args:
            target_id: Target ID to complete

        Returns:
            Success response dictionary
        """
        try:
            url = f"{BACKEND_URL}/api/students/targets/{target_id}/complete"

            logger.info(f"Completing target {target_id}")
            response = requests.put(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error completing target: {str(e)}")
            raise Exception(f"Failed to complete target: {str(e)}")

    # ================== Badges Methods ==================

    @staticmethod
    def get_student_badges(student_id: str) -> Dict[str, Any]:
        """
        Get all badges (earned and locked) for a student.

        Args:
            student_id: Student ID

        Returns:
            Badge collection dictionary with earned and locked badges
        """
        try:
            url = f"{BACKEND_URL}/api/badges/students/{student_id}/badges"

            logger.info(f"Fetching badges for student {student_id}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching badges: {str(e)}")
            raise Exception(f"Failed to fetch badges: {str(e)}")

    @staticmethod
    def grant_badge(badge_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Grant a badge to a student.

        Args:
            badge_data: Dictionary with badge details
                - student_id (str)
                - skill_name (str)
                - level (str)
                - granted_by (str)

        Returns:
            Badge response dictionary
        """
        try:
            url = f"{BACKEND_URL}/api/badges/grant"

            logger.info(f"Granting badge to student {badge_data.get('student_id')}: {badge_data.get('skill_name')}")
            response = requests.post(url, json=badge_data, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error granting badge: {str(e)}")
            raise Exception(f"Failed to grant badge: {str(e)}")

    @staticmethod
    def get_badge_progress(student_id: str) -> Dict[str, Any]:
        """
        Get badge progress summary for a student.

        Args:
            student_id: Student ID

        Returns:
            Badge progress dictionary with totals by type
        """
        try:
            url = f"{BACKEND_URL}/api/badges/students/{student_id}/badge-progress"

            logger.info(f"Fetching badge progress for student {student_id}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching badge progress: {str(e)}")
            raise Exception(f"Failed to fetch badge progress: {str(e)}")
