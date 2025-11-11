"""
Pydantic Schemas for API Request/Response Validation

This module defines all data models used in the Flourish Skills Tracker API.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime


# ============================================================================
# DATA INGESTION SCHEMAS
# ============================================================================

class DataEntryRequest(BaseModel):
    """
    Request schema for ingesting new student data entries
    """
    data_entry_id: str = Field(..., example="S001_group_disc_2025-08-15")
    student_id: str = Field(..., example="S001")
    teacher_id: str = Field(..., example="T001")
    type: str = Field(..., example="Group Discussion Transcript")
    date: str = Field(..., example="2025-08-15", description="YYYY-MM-DD format")
    content: str = Field(..., example="Student participated actively in climate change discussion...")
    metadata: Dict[str, Any] = Field(default_factory=dict, example={"context": "Climate change debate"})
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v):
        """Validate date is in YYYY-MM-DD format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        """Validate type is one of the allowed types"""
        allowed_types = [
            'Group Discussion Transcript',
            'Reflection Journal',
            'Teacher Observation',
            'Peer Feedback',
            'Project Presentation',
            'Parent Note'
        ]
        if v not in allowed_types:
            raise ValueError(f'Type must be one of: {", ".join(allowed_types)}')
        return v


class DataEntryResponse(BaseModel):
    """
    Response schema for data ingestion
    """
    success: bool
    data_entry_id: str
    assessments_created: int
    assessment_ids: List[int]


# ============================================================================
# ASSESSMENT SCHEMAS
# ============================================================================

class AssessmentResponse(BaseModel):
    """
    Response schema for skill assessments
    """
    id: int
    data_entry_id: str
    student_id: str
    skill_name: str
    skill_category: str
    level: str
    confidence_score: float
    justification: str
    source_quote: str
    data_point_count: int
    rubric_version: str
    corrected: bool
    created_at: str


class SkillTrendResponse(BaseModel):
    """
    Response schema for skill trend data (for charting)
    """
    skill_name: str
    skill_category: str
    assessments: List[Dict[str, Any]]  # [{date, level, level_numeric, confidence}, ...]


# ============================================================================
# CORRECTION SCHEMAS
# ============================================================================

class CorrectionRequest(BaseModel):
    """
    Request schema for teacher corrections
    """
    assessment_id: int = Field(..., example=1)
    corrected_level: str = Field(..., example="Proficient")
    corrected_justification: Optional[str] = Field(None, example="Student demonstrated consistent ability...")
    teacher_notes: Optional[str] = Field(None, example="Good evidence but level should be Proficient")
    corrected_by: str = Field(..., example="T001")
    
    @field_validator('corrected_level')
    @classmethod
    def validate_level(cls, v):
        """Validate level is one of: E, D, P, A"""
        if v not in ['E', 'D', 'P', 'A', 'Emerging', 'Developing', 'Proficient', 'Advanced']:
            raise ValueError('Level must be one of: E, D, P, A, Emerging, Developing, Proficient, Advanced')
        # Normalize to full names
        level_map = {'E': 'Emerging', 'D': 'Developing', 'P': 'Proficient', 'A': 'Advanced'}
        return level_map.get(v, v)


class CorrectionResponse(BaseModel):
    """
    Response schema for correction submission
    """
    success: bool
    correction_id: int
    message: str


class ApprovalRequest(BaseModel):
    """
    Request schema for approving an assessment as-is
    """
    assessment_id: int = Field(..., example=1)
    approved_by: str = Field(..., example="T001")


# ============================================================================
# STUDENT & TARGET SCHEMAS
# ============================================================================

class StudentResponse(BaseModel):
    """
    Response schema for student information
    """
    id: str
    name: str
    grade: int
    teacher_id: str
    created_at: str


class StudentProgressResponse(BaseModel):
    """
    Response schema for student progress metrics
    """
    student_id: str
    student_name: str
    total_assessments: int
    total_badges: int
    active_targets: int
    recent_growth: List[Dict[str, Any]]  # [{skill_name, from_level, to_level, date}, ...]


class TargetAssignmentRequest(BaseModel):
    """
    Request schema for assigning a skill target to a student
    """
    student_id: str = Field(..., example="S001")
    skill_name: str = Field(..., example="Organization")
    starting_level: str = Field(..., example="Developing")
    target_level: str = Field(..., example="Proficient")
    assigned_by: str = Field(..., example="T001")
    
    @field_validator('starting_level', 'target_level')
    @classmethod
    def validate_level(cls, v):
        """Validate levels"""
        if v not in ['Emerging', 'Developing', 'Proficient', 'Advanced']:
            raise ValueError('Level must be: Emerging, Developing, Proficient, or Advanced')
        return v


class TargetResponse(BaseModel):
    """
    Response schema for skill targets
    """
    id: int
    student_id: str
    skill_name: str
    starting_level: str
    target_level: str
    assigned_by: str
    assigned_at: str
    completed: bool
    completed_at: Optional[str]


# ============================================================================
# BADGE SCHEMAS
# ============================================================================

class BadgeResponse(BaseModel):
    """
    Response schema for badges
    """
    id: int
    student_id: str
    skill_name: str
    skill_category: str
    level_achieved: str
    badge_type: str  # bronze, silver, gold
    granted_by: str
    earned_date: str
    created_at: str


class BadgeGrantRequest(BaseModel):
    """
    Request schema for granting a badge
    """
    student_id: str = Field(..., example="S001")
    skill_name: str = Field(..., example="Organization")
    skill_category: str = Field(..., example="EF")
    level_achieved: str = Field(..., example="Proficient")
    granted_by: str = Field(..., example="T001")
    earned_date: str = Field(..., example="2025-10-15")
    
    @field_validator('level_achieved')
    @classmethod
    def validate_level(cls, v):
        """Validate level is D, P, or A (no badges for Emerging)"""
        if v not in ['Developing', 'Proficient', 'Advanced', 'D', 'P', 'A']:
            raise ValueError('Badge level must be: Developing, Proficient, or Advanced')
        level_map = {'D': 'Developing', 'P': 'Proficient', 'A': 'Advanced'}
        return level_map.get(v, v)
    
    @field_validator('skill_category')
    @classmethod
    def validate_category(cls, v):
        """Validate category is SEL, EF, or 21st Century"""
        if v not in ['SEL', 'EF', '21st Century']:
            raise ValueError('Category must be: SEL, EF, or 21st Century')
        return v


class BadgeCollectionResponse(BaseModel):
    """
    Response schema for a student's badge collection
    """
    student_id: str
    earned_badges: List[BadgeResponse]
    locked_badges: List[Dict[str, Any]]  # [{skill_name, level, badge_type}, ...]
    total_earned: int
    total_possible: int


# ============================================================================
# ERROR RESPONSE SCHEMA
# ============================================================================

class HTTPErrorResponse(BaseModel):
    """
    Standard error response format
    """
    detail: str
    error_code: Optional[str] = None
