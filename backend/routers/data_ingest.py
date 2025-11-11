"""
Data Ingestion Router

Handles ingestion of student data and AI-powered skill assessment generation.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import DataEntryRequest, DataEntryResponse
from database.connection import get_db_connection
from ai import SkillInferenceEngine, load_rubric, FewShotManager
import os
import logging
import json
from psycopg2 import IntegrityError

# Router setup
router = APIRouter(prefix="/api/data", tags=["Data Ingestion"])
logger = logging.getLogger(__name__)


@router.post("/ingest", response_model=DataEntryResponse)
async def ingest_data_entry(entry: DataEntryRequest):
    """
    Ingest a new student data entry and generate AI skill assessments
    
    This endpoint:
    1. Stores the data entry in the database
    2. Runs AI inference to generate skill assessments
    3. Stores the assessments in the database
    4. Returns the created assessment IDs
    
    Args:
        entry: DataEntryRequest with student observation data
        
    Returns:
        DataEntryResponse with success status and assessment IDs
    """
    conn = None
    cursor = None
    
    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Begin transaction
        conn.autocommit = False
        
        # Insert data entry
        logger.info(f"Ingesting data entry: {entry.data_entry_id}")
        
        insert_entry_sql = """
            INSERT INTO data_entries (id, student_id, teacher_id, type, date, content, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(insert_entry_sql, (
                entry.data_entry_id,
                entry.student_id,
                entry.teacher_id,
                entry.type,
                entry.date,
                entry.content,
                json.dumps(entry.metadata)
            ))
        except IntegrityError as e:
            conn.rollback()
            logger.error(f"Duplicate entry ID: {entry.data_entry_id}")
            raise HTTPException(status_code=400, detail=f"Data entry {entry.data_entry_id} already exists")
        
        # Commit the data entry insertion
        conn.commit()
        logger.info(f"Data entry saved: {entry.data_entry_id}")
        
        # Run AI inference
        logger.info("Starting AI inference...")
        
        # Load rubric
        rubric = load_rubric()
        
        # Get few-shot examples from corrections
        few_shot_manager = FewShotManager()
        few_shot_examples = few_shot_manager.get_recent_corrections(limit=5)
        
        # Get API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        # Create inference engine
        engine = SkillInferenceEngine(
            api_key=api_key,
            rubric=rubric,
            few_shot_examples=few_shot_examples
        )
        
        # Prepare student data
        student_data = {
            "content": entry.content,
            "metadata": {
                "type": entry.type,
                "date": entry.date,
                "context": entry.metadata.get("context", "N/A")
            }
        }
        
        # Run inference
        assessments = engine.assess_skills(student_data)
        logger.info(f"AI generated {len(assessments)} assessments")
        
        # Insert assessments into database
        assessment_ids = []
        
        if len(assessments) > 0:
            insert_assessment_sql = """
                INSERT INTO assessments (
                    data_entry_id, student_id, skill_name, skill_category, 
                    level, confidence_score, justification, source_quote, 
                    data_point_count, rubric_version
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            
            for assessment in assessments:
                cursor.execute(insert_assessment_sql, (
                    entry.data_entry_id,
                    entry.student_id,
                    assessment['skill_name'],
                    assessment['skill_category'],
                    assessment['level'],
                    assessment.get('confidence_score', 0.5),
                    assessment['justification'],
                    assessment['source_quote'],
                    assessment.get('data_point_count', 1),
                    assessment.get('rubric_version', '1.0')
                ))
                
                result = cursor.fetchone()
                assessment_ids.append(result['id'])
            
            # Commit assessments
            conn.commit()
            logger.info(f"Saved {len(assessment_ids)} assessments to database")
        
        # Return success response
        return DataEntryResponse(
            success=True,
            data_entry_id=entry.data_entry_id,
            assessments_created=len(assessment_ids),
            assessment_ids=assessment_ids
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Rollback on any error
        if conn:
            conn.rollback()
        
        logger.error(f"Error during data ingestion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Data ingestion failed: {str(e)}")
    
    finally:
        # Clean up
        if cursor:
            cursor.close()
        if conn:
            conn.close()
