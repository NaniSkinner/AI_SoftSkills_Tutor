"""
Students Router

Handles student data, progress tracking, and skill target management.
"""

from fastapi import APIRouter, HTTPException, Query
from models.schemas import (
    StudentResponse, StudentProgressResponse, 
    TargetAssignmentRequest, TargetResponse
)
from database.connection import get_db_connection
from typing import List, Optional, Dict, Any
import logging

# Router setup
router = APIRouter(prefix="/api/students", tags=["Students"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[StudentResponse])
async def get_students(teacher_id: Optional[str] = Query(None, description="Filter by teacher ID")):
    """
    Get all students, optionally filtered by teacher
    
    Args:
        teacher_id: Optional teacher ID to filter students
        
    Returns:
        List of StudentResponse objects
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if teacher_id:
            query = """
                SELECT id, name, grade, teacher_id, created_at::text as created_at
                FROM students
                WHERE teacher_id = %s
                ORDER BY name ASC
            """
            cursor.execute(query, (teacher_id,))
        else:
            query = """
                SELECT id, name, grade, teacher_id, created_at::text as created_at
                FROM students
                ORDER BY name ASC
            """
            cursor.execute(query)
        
        results = cursor.fetchall()
        students = [StudentResponse(**dict(row)) for row in results]
        
        logger.info(f"Retrieved {len(students)} students")
        return students
        
    except Exception as e:
        logger.error(f"Error retrieving students: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve students: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.get("/{student_id}/progress", response_model=StudentProgressResponse)
async def get_student_progress(student_id: str):
    """
    Get comprehensive progress metrics for a student
    
    Includes total assessments, badges, active targets, and recent growth.
    
    Args:
        student_id: Student ID
        
    Returns:
        StudentProgressResponse with progress metrics
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get student info
        cursor.execute("SELECT name FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        student_name = student['name']
        
        # Count total assessments
        cursor.execute("SELECT COUNT(*) as count FROM assessments WHERE student_id = %s", (student_id,))
        total_assessments = cursor.fetchone()['count']
        
        # Count total badges
        cursor.execute("SELECT COUNT(*) as count FROM badges WHERE student_id = %s", (student_id,))
        total_badges = cursor.fetchone()['count']
        
        # Count active targets
        cursor.execute(
            "SELECT COUNT(*) as count FROM skill_targets WHERE student_id = %s AND completed = FALSE",
            (student_id,)
        )
        active_targets = cursor.fetchone()['count']
        
        # Get recent growth (last 5 skill level changes)
        growth_query = """
            WITH ranked_assessments AS (
                SELECT 
                    skill_name, level, 
                    de.date,
                    LAG(level) OVER (PARTITION BY skill_name ORDER BY de.date) as prev_level
                FROM assessments a
                JOIN data_entries de ON a.data_entry_id = de.id
                WHERE a.student_id = %s
            )
            SELECT skill_name, prev_level as from_level, level as to_level, date
            FROM ranked_assessments
            WHERE prev_level IS NOT NULL AND prev_level != level
            ORDER BY date DESC
            LIMIT 5
        """
        
        cursor.execute(growth_query, (student_id,))
        growth_results = cursor.fetchall()
        recent_growth = [dict(row) for row in growth_results]
        
        return StudentProgressResponse(
            student_id=student_id,
            student_name=student_name,
            total_assessments=total_assessments,
            total_badges=total_badges,
            active_targets=active_targets,
            recent_growth=recent_growth
        )
        
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving student progress: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve student progress: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.post("/{student_id}/target-skill", response_model=TargetResponse)
async def assign_target_skill(student_id: str, target: TargetAssignmentRequest):
    """
    Assign a skill growth target to a student
    
    Sets a goal for the student to grow from a starting level to a target level.
    
    Args:
        student_id: Student ID
        target: TargetAssignmentRequest with skill and level details
        
    Returns:
        TargetResponse with the created target
    """
    conn = None
    cursor = None
    
    try:
        # Validate student_id matches
        if student_id != target.student_id:
            raise HTTPException(status_code=400, detail="Student ID mismatch")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        conn.autocommit = False
        
        # Check if active target already exists for this skill
        cursor.execute(
            """
            SELECT id FROM skill_targets 
            WHERE student_id = %s AND skill_name = %s AND completed = FALSE
            """,
            (student_id, target.skill_name)
        )
        
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail=f"Active target already exists for skill '{target.skill_name}'"
            )
        
        # Insert new target
        insert_sql = """
            INSERT INTO skill_targets (
                student_id, skill_name, starting_level, target_level, assigned_by
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, assigned_at::text as assigned_at
        """
        
        cursor.execute(insert_sql, (
            target.student_id,
            target.skill_name,
            target.starting_level,
            target.target_level,
            target.assigned_by
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        logger.info(f"Target assigned: {target.skill_name} for student {student_id}")
        
        return TargetResponse(
            id=result['id'],
            student_id=target.student_id,
            skill_name=target.skill_name,
            starting_level=target.starting_level,
            target_level=target.target_level,
            assigned_by=target.assigned_by,
            assigned_at=result['assigned_at'],
            completed=False,
            completed_at=None
        )
        
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error assigning target: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to assign target: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.get("/{student_id}/targets", response_model=List[TargetResponse])
async def get_student_targets(
    student_id: str,
    completed: Optional[bool] = Query(None, description="Filter by completion status")
):
    """
    Get all skill targets for a student
    
    Args:
        student_id: Student ID
        completed: Optional filter for completed/active targets
        
    Returns:
        List of TargetResponse objects
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        base_query = """
            SELECT 
                id, student_id, skill_name, starting_level, target_level,
                assigned_by, assigned_at::text as assigned_at, completed,
                completed_at::text as completed_at
            FROM skill_targets
            WHERE student_id = %s
        """
        
        if completed is not None:
            base_query += f" AND completed = {completed}"
        
        base_query += " ORDER BY assigned_at DESC"
        
        cursor.execute(base_query, (student_id,))
        results = cursor.fetchall()
        
        targets = [TargetResponse(**dict(row)) for row in results]
        
        logger.info(f"Retrieved {len(targets)} targets for student {student_id}")
        return targets
        
    except Exception as e:
        logger.error(f"Error retrieving targets: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve targets: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@router.put("/targets/{target_id}/complete")
async def complete_target(target_id: int):
    """
    Mark a skill target as completed
    
    Args:
        target_id: Target ID to complete
        
    Returns:
        Success message
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE skill_targets 
            SET completed = TRUE, completed_at = NOW()
            WHERE id = %s
            RETURNING id
            """,
            (target_id,)
        )
        
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Target {target_id} not found")
        
        conn.commit()
        
        logger.info(f"Target {target_id} marked as completed")
        
        return {
            "success": True,
            "message": f"Target {target_id} completed successfully"
        }
        
    except HTTPException:
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error completing target: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to complete target: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
