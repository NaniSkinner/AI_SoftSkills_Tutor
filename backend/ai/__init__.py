"""
AI Inference Module

This module contains the GPT-4o powered inference engine for skill assessment.
"""

from .inference_engine import SkillInferenceEngine
from .rubric_loader import load_rubric, load_curriculum_context
from .few_shot_manager import FewShotManager
from .confidence_scoring import calculate_confidence_score

__all__ = [
    'SkillInferenceEngine',
    'load_rubric',
    'load_curriculum_context',
    'FewShotManager',
    'calculate_confidence_score'
]
