"""
Test Script for AI Inference Pipeline

Tests the GPT-4o skill assessment engine with sample student data.
"""

import sys
import os
from dotenv import load_dotenv

# Add /app to path (for Docker container) or parent directory (for local)
if os.path.exists('/app'):
    sys.path.insert(0, '/app')
else:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai import SkillInferenceEngine, load_rubric

# Load environment variables
load_dotenv()

# Setup
print("=" * 80)
print("AI Inference Pipeline Test")
print("=" * 80)
print()

# Load rubric
print("Loading rubric...")
rubric = load_rubric()
print(f"✓ Rubric loaded ({len(rubric)} characters)")
print()

# Get API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("ERROR: OPENAI_API_KEY not found in environment")
    sys.exit(1)

print("✓ OpenAI API key configured")
print()

# Create inference engine
print("Initializing inference engine...")
engine = SkillInferenceEngine(api_key=api_key, rubric=rubric)
print("✓ Inference engine ready")
print()

# Test data: Sample from Eva's group discussion
test_data = {
    "content": """
**Eva:** I organized all the research into categories - climate causes, effects, and solutions. 
I made a spreadsheet so we could track who's working on what.

**Marcus:** That's really helpful Eva. The spreadsheet makes it clear what I need to do.

**Teacher Note:** Eva demonstrated strong organizational skills and leadership. She took 
initiative to create systems that helped the entire group stay on track. The spreadsheet 
was well-structured with clear categories and assigned responsibilities.

**Eva:** I also set up a shared folder with subfolders for each section. That way we won't 
lose any files.

**Marcus:** Good idea. I was worried about keeping everything organized.

**Eva:** We should meet twice a week to check progress. I can send calendar invites if that helps.
    """,
    "metadata": {
        "type": "Group Discussion Transcript",
        "date": "2025-08-15",
        "context": "Climate change project planning session"
    }
}

print("Testing inference with sample data...")
print("-" * 80)
print(f"Data Type: {test_data['metadata']['type']}")
print(f"Context: {test_data['metadata']['context']}")
print("-" * 80)
print()

# Run inference
try:
    assessments = engine.assess_skills(test_data)
    
    print(f"✓ Generated {len(assessments)} skill assessments")
    print()
    
    if len(assessments) == 0:
        print("WARNING: No assessments generated. Check API response.")
    else:
        print("ASSESSMENTS:")
        print("=" * 80)
        
        for i, assessment in enumerate(assessments, 1):
            print(f"\n{i}. {assessment['skill_name']} ({assessment['skill_category']})")
            print(f"   Level: {assessment['level']}")
            print(f"   Confidence: {assessment.get('confidence_score', 0):.2f}")
            print(f"   Justification: {assessment['justification'][:150]}...")
            print(f"   Quote: \"{assessment['source_quote'][:100]}...\"")
        
        print()
        print("=" * 80)
        
        # Validation
        print("\nVALIDATION:")
        all_valid = True
        
        # Check required fields
        for assessment in assessments:
            required_fields = ['skill_name', 'skill_category', 'level', 'justification', 'source_quote']
            for field in required_fields:
                if field not in assessment or not assessment[field]:
                    print(f"✗ Missing required field: {field}")
                    all_valid = False
        
        # Check confidence scores
        for assessment in assessments:
            score = assessment.get('confidence_score', 0)
            if score < 0.5 or score > 1.0:
                print(f"✗ Invalid confidence score: {score}")
                all_valid = False
        
        if all_valid:
            print("✓ All assessments have required fields")
            print("✓ All confidence scores in valid range (0.5-1.0)")
        
        print()
        print("=" * 80)
        print("✅ Test completed successfully!")
        
except Exception as e:
    print(f"✗ ERROR during inference: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
