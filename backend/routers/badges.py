"""
Badges Router

Handles badge management and gamification features.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import BadgeResponse, BadgeGrantRequest, BadgeCollectionResponse
from database.connection import get_db_connection, return_db_connection
from typing import List, Dict, Any
import logging

# Router setup
router = APIRouter(prefix="/api/badges", tags=["Badges"])
logger = logging.getLogger(__name__)

# All 17 skills for badge generation
ALL_SKILLS = {
    'SEL': [
        'Self-Awareness', 'Self-Management', 'Social Awareness',
        'Relationship Skills', 'Responsible Decision-Making'
    ],
    'EF': [
        'Working Memory', 'Inhibitory Control', 'Cognitive Flexibility',
        'Planning & Prioritization', 'Organization', 'Task Initiation'
    ],
    '21st Century': [
        'Critical Thinking', 'Communication', 'Collaboration',
        'Creativity & Innovation', 'Digital Literacy', 'Global Awareness'
    ]
}


@router.get("/students/{student_id}/badges", response_model=BadgeCollectionResponse)
async def get_student_badges(student_id: str):
    """
    Get a student's complete badge collection (earned and locked)
    
    Args:
        student_id: Student ID
        
    Returns:
        BadgeCollectionResponse with earned and locked badges
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get earned badges
        query = """
            SELECT 
                id, student_id, skill_name, skill_category, level_achieved,
                badge_type, granted_by, earned_date, created_at::text as created_at
            FROM badges
            WHERE student_id = %s
            ORDER BY earned_date DESC
        """
        
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        
        earned_badges = [BadgeResponse(**dict(row)) for row in results]
        
        # Generate all possible badges (17 skills × 3 levels = 51 possible badges)
        all_possible_badges = []
        level_badge_map = {
            'Developing': 'bronze',
            'Proficient': 'silver',
            'Advanced': 'gold'
        }
        
        for category, skills in ALL_SKILLS.items():
            for skill in skills:
                for level, badge_type in level_badge_map.items():
                    all_possible_badges.append({
                        'skill_name': skill,
                        'skill_category': category,
                        'level': level,
                        'badge_type': badge_type
                    })
        
        # Filter out earned badges to get locked badges
        earned_keys = {
            (b.skill_name, b.level_achieved) for b in earned_badges
        }
        
        locked_badges = [
            badge for badge in all_possible_badges
            if (badge['skill_name'], badge['level']) not in earned_keys
        ]
        
        return BadgeCollectionResponse(
            student_id=student_id,
            earned_badges=earned_badges,
            locked_badges=locked_badges,
            total_earned=len(earned_badges),
            total_possible=len(all_possible_badges)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving badges: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve badges: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)


@router.post("/grant", response_model=BadgeResponse)
async def grant_badge(badge: BadgeGrantRequest):
    """
    Grant a badge to a student (teacher action)
    
    Validates the level and determines badge type automatically.
    
    Args:
        badge: BadgeGrantRequest with student and skill details
        
    Returns:
        BadgeResponse with the granted badge
    """
    conn = None
    cursor = None
    
    try:
        # Determine badge type from level
        badge_type_map = {
            'Developing': 'bronze',
            'Proficient': 'silver',
            'Advanced': 'gold'
        }
        
        badge_type = badge_type_map.get(badge.level_achieved)
        
        if not badge_type:
            raise HTTPException(
                status_code=400,
                detail="Invalid level. Badges can only be granted for Developing, Proficient, or Advanced"
            )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        conn.autocommit = False
        
        # Check if badge already exists
        cursor.execute(
            """
            SELECT id FROM badges 
            WHERE student_id = %s AND skill_name = %s AND level_achieved = %s
            """,
            (badge.student_id, badge.skill_name, badge.level_achieved)
        )
        
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail=f"Badge already granted for {badge.skill_name} at {badge.level_achieved} level"
            )
        
        # Insert badge
        insert_sql = """
            INSERT INTO badges (
                student_id, skill_name, skill_category, level_achieved,
                badge_type, granted_by, earned_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at::text as created_at
        """
        
        cursor.execute(insert_sql, (
            badge.student_id,
            badge.skill_name,
            badge.skill_category,
            badge.level_achieved,
            badge_type,
            badge.granted_by,
            badge.earned_date
        ))
        
        result = cursor.fetchone()
        conn.commit()
        
        logger.info(f"Badge granted: {badge.skill_name} ({badge_type}) to {badge.student_id}")
        
        return BadgeResponse(
            id=result['id'],
            student_id=badge.student_id,
            skill_name=badge.skill_name,
            skill_category=badge.skill_category,
            level_achieved=badge.level_achieved,
            badge_type=badge_type,
            granted_by=badge.granted_by,
            earned_date=badge.earned_date,
            created_at=result['created_at']
        )
        
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error granting badge: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to grant badge: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)


@router.get("/students/{student_id}/badge-progress")
async def get_badge_progress(student_id: str) -> Dict[str, Any]:
    """
    Get badge progress statistics for a student
    
    Shows counts by category and badge type.
    
    Args:
        student_id: Student ID
        
    Returns:
        Dictionary with badge progress metrics
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count by category
        cursor.execute(
            """
            SELECT skill_category, COUNT(*) as count
            FROM badges
            WHERE student_id = %s
            GROUP BY skill_category
            """,
            (student_id,)
        )
        
        category_counts = {row['skill_category']: row['count'] for row in cursor.fetchall()}
        
        # Count by badge type
        cursor.execute(
            """
            SELECT badge_type, COUNT(*) as count
            FROM badges
            WHERE student_id = %s
            GROUP BY badge_type
            """,
            (student_id,)
        )
        
        badge_type_counts = {row['badge_type']: row['count'] for row in cursor.fetchall()}
        
        # Total counts
        total_earned = sum(category_counts.values())
        total_possible = 51  # 17 skills × 3 levels
        
        return {
            'student_id': student_id,
            'total_earned': total_earned,
            'total_possible': total_possible,
            'completion_percentage': round((total_earned / total_possible) * 100, 1),
            'by_category': {
                'SEL': category_counts.get('SEL', 0),
                'EF': category_counts.get('EF', 0),
                '21st Century': category_counts.get('21st Century', 0)
            },
            'by_type': {
                'bronze': badge_type_counts.get('bronze', 0),
                'silver': badge_type_counts.get('silver', 0),
                'gold': badge_type_counts.get('gold', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Error retrieving badge progress: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve badge progress: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_db_connection(conn)
