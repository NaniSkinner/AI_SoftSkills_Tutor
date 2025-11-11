"""
Corrections Router

Handles teacher corrections and approvals of AI assessments.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import CorrectionRequest, CorrectionResponse, ApprovalRequest
from database.connection import get_db_connection
from typing import List, Dict, Any
import logging

# Router setup
router = APIRouter(prefix="/api/corrections", tags=["Teacher Corrections"])
logger = logging.getLogger(__name__)


@router.post("/submit", response_model=CorrectionResponse)
async def submit_correction(correction: CorrectionRequest):
    """
    Submit a teacher correction for an AI-generated assessment
    
    The correction will be stored and used as a few-shot learning example
    for future AI inferences.
    
    Args:
        correction: CorrectionRequest with corrected level and justification
        
    Returns:
        CorrectionResponse with success status and correction ID
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        conn.autocommit = False
        
        # Verify assessment exists
        cursor.execute("SELECT level, justification FROM assessments WHERE id = %s", 
                      (correction.assessment_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, 
                              detail=f"Assessment {correction.assessment_id} not found")
        
        original_level = result['level']
        original_justification = result['justification']
        
        # Insert correction
        insert_sql = """
            INSERT INTO teacher_corrections (
                assessment_id, original_level, corrected_level,
                original_justification, corrected_justification,
                teacher_notes, corrected_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        cursor.execute(insert_sql, (
            correction.assessment_id,
            original_level,
            correction.corrected_level,
            original_justification,
            correction.corrected_justification or original_justification,
            correction.teacher_notes,
            correction.corrected_by
        ))
        
        correction_id = cursor.fetchone()['id']
        
        # Update assessment as corrected
        cursor.execute(
            "UPDATE assessments SET corrected = TRUE WHERE id = %s",
            (correction.assessment_id,)
        )
        
        conn.commit()
        
        logger.info(f"Correction {correction_id} submitted for assessment {correction.assessment_id}")
        
        return CorrectionResponse(
            success=True,
            correction_id=correction_id,
            message="Correction submitted successfully"
        )
        
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error submitting correction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to submit correction: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.post("/assessments/{assessment_id}/approve")
async def approve_assessment(assessment_id: int, approval: ApprovalRequest):
    """
    Approve an AI assessment as correct without making changes
    
    This marks the assessment as reviewed and validated by a teacher.
    
    Args:
        assessment_id: Assessment ID to approve
        approval: ApprovalRequest with teacher ID
        
    Returns:
        Success message
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify assessment exists
        cursor.execute("SELECT id FROM assessments WHERE id = %s", (assessment_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Assessment {assessment_id} not found")
        
        # Mark as corrected (approved)
        cursor.execute(
            "UPDATE assessments SET corrected = TRUE WHERE id = %s",
            (assessment_id,)
        )
        
        conn.commit()
        
        logger.info(f"Assessment {assessment_id} approved by {approval.approved_by}")
        
        return {
            "success": True,
            "message": f"Assessment {assessment_id} approved successfully"
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error approving assessment: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to approve assessment: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.get("/recent")
async def get_recent_corrections(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent teacher corrections
    
    Shows recent corrections with both original and corrected values.
    
    Args:
        limit: Maximum number of corrections to return (default 10)
        
    Returns:
        List of correction objects with assessment details
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                tc.id,
                tc.assessment_id,
                a.student_id,
                a.skill_name,
                tc.original_level,
                tc.corrected_level,
                tc.teacher_notes,
                tc.corrected_by,
                tc.corrected_at::text as corrected_at
            FROM teacher_corrections tc
            JOIN assessments a ON tc.assessment_id = a.id
            ORDER BY tc.corrected_at DESC
            LIMIT %s
        """
        
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        
        corrections = [dict(row) for row in results]
        
        logger.info(f"Retrieved {len(corrections)} recent corrections")
        return corrections
        
    except Exception as e:
        logger.error(f"Error retrieving corrections: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve corrections: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
