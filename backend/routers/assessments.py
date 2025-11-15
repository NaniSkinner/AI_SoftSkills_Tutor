"""
Assessments Router

Handles retrieval and viewing of skill assessments.
"""

from fastapi import APIRouter, HTTPException, Query
from models.schemas import AssessmentResponse, SkillTrendResponse
from database.connection import get_db_connection, return_db_connection
from typing import List, Optional
import logging

# Router setup
router = APIRouter(prefix="/api/assessments", tags=["Assessments"])
logger = logging.getLogger(__name__)


@router.get("/student/{student_id}", response_model=List[AssessmentResponse])
async def get_student_assessments(student_id: str):
    """
    Get all assessments for a specific student
    
    Args:
        student_id: Student ID (e.g., "S001")
        
    Returns:
        List of AssessmentResponse objects ordered by date (newest first)
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                id, data_entry_id, student_id, skill_name, skill_category,
                level, confidence_score, justification, source_quote,
                data_point_count, rubric_version, corrected,
                created_at::text as created_at
            FROM assessments
            WHERE student_id = %s
            ORDER BY created_at DESC
        """
        
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        
        assessments = [
            AssessmentResponse(**dict(row)) for row in results
        ]
        
        logger.info(f"Retrieved {len(assessments)} assessments for student {student_id}")
        return assessments
        
    except Exception as e:
        logger.error(f"Error retrieving assessments: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve assessments: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)


@router.get("/skill-trends/{student_id}", response_model=List[SkillTrendResponse])
async def get_skill_trends(student_id: str):
    """
    Get skill trend data for charting student progress over time
    
    Groups assessments by skill and returns chronological data for each skill.
    
    Args:
        student_id: Student ID
        
    Returns:
        List of SkillTrendResponse objects with assessment history per skill
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                skill_name, skill_category, level, confidence_score,
                de.date
            FROM assessments a
            JOIN data_entries de ON a.data_entry_id = de.id
            WHERE a.student_id = %s
            ORDER BY skill_name, de.date ASC
        """
        
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        
        # Group by skill
        skills_data = {}
        level_map = {'Emerging': 1, 'Developing': 2, 'Proficient': 3, 'Advanced': 4}
        
        for row in results:
            skill_name = row['skill_name']
            
            if skill_name not in skills_data:
                skills_data[skill_name] = {
                    'skill_name': skill_name,
                    'skill_category': row['skill_category'],
                    'assessments': []
                }
            
            skills_data[skill_name]['assessments'].append({
                'date': row['date'],
                'level': row['level'],
                'level_numeric': level_map.get(row['level'], 0),
                'confidence': row['confidence_score']
            })
        
        trends = [
            SkillTrendResponse(**data) for data in skills_data.values()
        ]
        
        logger.info(f"Retrieved trends for {len(trends)} skills for student {student_id}")
        return trends
        
    except Exception as e:
        logger.error(f"Error retrieving skill trends: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve skill trends: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)


@router.get("/pending", response_model=List[AssessmentResponse])
async def get_pending_assessments(
    limit: int = Query(50, description="Maximum number of assessments to return"),
    min_confidence: Optional[float] = Query(None, description="Filter by minimum confidence score")
):
    """
    Get pending (uncorrected) assessments that need teacher review
    
    Sorted by confidence score (lowest first) to prioritize uncertain assessments.
    
    Args:
        limit: Maximum number to return (default 50)
        min_confidence: Optional filter for confidence threshold
        
    Returns:
        List of uncorrected AssessmentResponse objects
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = """
            SELECT 
                id, data_entry_id, student_id, skill_name, skill_category,
                level, confidence_score, justification, source_quote,
                data_point_count, rubric_version, corrected,
                created_at::text as created_at
            FROM assessments
            WHERE corrected = FALSE
        """
        
        if min_confidence is not None:
            base_query += f" AND confidence_score >= {min_confidence}"
        
        base_query += " ORDER BY confidence_score ASC, created_at DESC LIMIT %s"
        
        cursor.execute(base_query, (limit,))
        results = cursor.fetchall()
        
        assessments = [
            AssessmentResponse(**dict(row)) for row in results
        ]
        
        logger.info(f"Retrieved {len(assessments)} pending assessments")
        return assessments
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error retrieving pending assessments: {error_msg}", exc_info=True)

        # Provide helpful message if database schema is not initialized
        if "relation" in error_msg and "does not exist" in error_msg:
            raise HTTPException(
                status_code=500,
                detail="Database schema not initialized. Please contact administrator."
            )

        raise HTTPException(status_code=500, detail=f"Failed to retrieve pending assessments: {error_msg}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)


@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment_by_id(assessment_id: int):
    """
    Get a specific assessment by ID
    
    Args:
        assessment_id: Assessment ID
        
    Returns:
        AssessmentResponse object
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                id, data_entry_id, student_id, skill_name, skill_category,
                level, confidence_score, justification, source_quote,
                data_point_count, rubric_version, corrected,
                created_at::text as created_at
            FROM assessments
            WHERE id = %s
        """
        
        cursor.execute(query, (assessment_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Assessment {assessment_id} not found")
        
        return AssessmentResponse(**dict(result))
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving assessment: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve assessment: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)
