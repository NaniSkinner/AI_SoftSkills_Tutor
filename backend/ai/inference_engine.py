"""
GPT-4o Powered Skill Inference Engine

Main module for analyzing student data and generating skill assessments.
"""

import openai
import json
import os
import logging
from typing import List, Dict, Any

from .prompts import SYSTEM_PROMPT_TEMPLATE, build_few_shot_section, build_user_prompt
from .rubric_loader import load_rubric
from .confidence_scoring import calculate_confidence_score

# Setup logging
logger = logging.getLogger(__name__)


class SkillInferenceEngine:
    """
    GPT-4o powered skill assessment engine
    
    Analyzes student data entries and generates skill-level assessments
    based on a comprehensive rubric and optional few-shot learning examples.
    """
    
    def __init__(self, api_key: str, rubric: str, few_shot_examples: List[Dict] = None):
        """
        Initialize the inference engine

        Args:
            api_key: OpenAI API key (or OpenRouter key starting with sk-or-v1-)
            rubric: Complete rubric content as string
            few_shot_examples: Optional list of teacher-corrected examples
        """
        # Detect if using OpenRouter (key starts with sk-or-v1-)
        if api_key.startswith('sk-or-v1-'):
            # Use OpenRouter endpoint
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            logger.info("Using OpenRouter endpoint")
        else:
            # Use standard OpenAI endpoint
            self.client = openai.OpenAI(api_key=api_key)
            logger.info("Using OpenAI endpoint")

        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
        self.rubric = rubric
        self.few_shot_examples = few_shot_examples if few_shot_examples else []
    
    def assess_skills(self, student_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze student data and generate skill assessments
        
        Args:
            student_data: Dictionary with structure:
                {
                    "content": "transcript or observation text...",
                    "metadata": {
                        "type": "Group Discussion",
                        "date": "2025-08-15",
                        "context": "Climate change debate"
                    }
                }
        
        Returns:
            List of assessment dictionaries, each containing:
            - skill_name
            - skill_category
            - level
            - justification
            - source_quote
            - confidence_score
            - data_point_count
        """
        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = build_user_prompt(student_data)
        
        try:
            # Call GPT-4o API
            # Temperature set low (0.3) for consistent, deterministic assessments
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=4000,
                response_format={"type": "json_object"}  # Enforce JSON output
            )
            
            # Extract and parse response
            content = response.choices[0].message.content
            logger.info(f"Raw API response: {content[:500]}...")  # Log first 500 chars for debugging
            result = json.loads(content)

            # Handle multiple response formats
            if isinstance(result, list):
                # Already an array of assessments
                assessments = result
            elif isinstance(result, dict):
                if 'assessments' in result:
                    # Wrapped in {"assessments": [...]}
                    assessments = result['assessments']
                elif 'skill_name' in result:
                    # Single assessment object - wrap it in an array
                    assessments = [result]
                else:
                    # Unknown structure
                    logger.warning(f"Unexpected response structure. Keys: {result.keys()}")
                    assessments = []
            else:
                assessments = []
            
            # Calculate confidence scores for assessments that don't have them
            for assessment in assessments:
                if 'confidence_score' not in assessment or assessment['confidence_score'] is None:
                    assessment['confidence_score'] = calculate_confidence_score(
                        student_data, 
                        assessment
                    )
            
            logger.info(f"Generated {len(assessments)} skill assessments")
            return assessments
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GPT-4o response as JSON: {e}")
            logger.error(f"Response content: {content}")
            return []
        
        except Exception as e:
            logger.error(f"Error during skill inference: {e}")
            raise
    
    def _build_system_prompt(self) -> str:
        """
        Build the complete system prompt with rubric and few-shot examples
        
        Returns:
            str: Formatted system prompt
        """
        # Use only the last 5 few-shot examples to avoid prompt bloat
        few_shot_section = build_few_shot_section(self.few_shot_examples[-5:])
        
        return SYSTEM_PROMPT_TEMPLATE.format(
            rubric_content=self.rubric,
            few_shot_examples=few_shot_section
        )
