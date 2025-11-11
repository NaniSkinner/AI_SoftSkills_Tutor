"""
Confidence Scoring Module

Calculates heuristic confidence scores for skill assessments based on multiple factors.
"""

from typing import Dict, Any


def calculate_confidence_score(data_entry: Dict[str, Any], assessment: Dict[str, Any]) -> float:
    """
    Calculate a confidence score for an assessment based on heuristic factors
    
    Factors considered:
    1. Quote length (longer quotes indicate more evidence)
    2. Rubric keyword matching in justification (alignment with rubric language)
    3. Data entry completeness (longer entries provide more context)
    4. Historical data points (multiple observations increase confidence)
    
    Args:
        data_entry: The original student data entry
        assessment: The generated skill assessment
        
    Returns:
        float: Confidence score between 0.5 and 1.0
    """
    # Base confidence
    confidence = 0.5
    
    # Factor 1: Quote Length
    # Longer quotes indicate more substantial evidence
    source_quote = assessment.get('source_quote', '')
    quote_word_count = len(source_quote.split())
    
    if quote_word_count >= 20:
        confidence += 0.15
    elif quote_word_count >= 10:
        confidence += 0.10
    
    # Factor 2: Rubric Keyword Matching
    # Presence of rubric-aligned language indicates deeper understanding
    justification = assessment.get('justification', '').lower()
    rubric_keywords = [
        'independently',
        'consistently',
        'with prompting',
        'with support',
        'beginning to',
        'developing',
        'demonstrates',
        'applies'
    ]
    
    keyword_matches = sum(1 for keyword in rubric_keywords if keyword in justification)
    confidence += min(keyword_matches * 0.05, 0.15)
    
    # Factor 3: Data Entry Completeness
    # Longer entries provide more context for accurate assessment
    content = data_entry.get('content', '')
    content_word_count = len(content.split())
    
    if content_word_count > 200:
        confidence += 0.10
    elif content_word_count > 100:
        confidence += 0.05
    
    # Factor 4: Historical Data Points
    # Multiple observations of the same skill increase confidence
    data_point_count = assessment.get('data_point_count', 1)
    if data_point_count >= 3:
        confidence += 0.10
    
    # Cap confidence at 1.0
    return min(confidence, 1.0)
