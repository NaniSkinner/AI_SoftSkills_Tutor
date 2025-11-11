"""
Few-Shot Learning Manager Module

Manages retrieval of teacher-corrected assessments from the database for few-shot learning.
"""

import sys
import os
from typing import List, Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_db_connection


class FewShotManager:
    """
    Manages few-shot learning examples from teacher corrections
    """
    
    def get_recent_corrections(self, skill_name: str = None, limit: int = 5) -> List[Dict]:
        """
        Retrieve recent teacher-corrected assessments from the database
        
        Args:
            skill_name: Optional skill name to filter by (e.g., "Social Awareness")
            limit: Maximum number of corrections to retrieve (default 5)
            
        Returns:
            List of correction dictionaries with keys:
            - skill_name
            - skill_category
            - level (corrected level)
            - justification (corrected justification)
            - source_quote
            - teacher_notes
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Base query: Join assessments with teacher_corrections
        base_query = """
            SELECT 
                a.skill_name,
                a.skill_category,
                tc.corrected_level as level,
                tc.corrected_justification as justification,
                a.source_quote,
                tc.teacher_notes
            FROM assessments a
            JOIN teacher_corrections tc ON a.id = tc.assessment_id
            WHERE tc.teacher_notes IS NOT NULL
        """
        
        # Add skill filter if specified
        if skill_name:
            query = base_query + " AND a.skill_name = %s ORDER BY tc.corrected_at DESC LIMIT %s"
            cursor.execute(query, (skill_name, limit))
        else:
            query = base_query + " ORDER BY tc.corrected_at DESC LIMIT %s"
            cursor.execute(query, (limit,))
        
        # Fetch all corrections
        corrections = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Build examples list
        examples = []
        for correction in corrections:
            examples.append({
                'skill_name': correction['skill_name'],
                'skill_category': correction['skill_category'],
                'level': correction['level'],
                'justification': correction['justification'],
                'source_quote': correction['source_quote'],
                'teacher_notes': correction['teacher_notes']
            })
        
        return examples
