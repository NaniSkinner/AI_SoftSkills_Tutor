"""
Prompt Building Module

Constructs system prompts, few-shot examples, and user prompts for the GPT-4o inference engine.
"""

from typing import List, Dict, Any


SYSTEM_PROMPT_TEMPLATE = """You are an Expert Educational Assessor specializing in middle school non-academic skills assessment.

YOUR ROLE:
1. Analyze student data (transcripts, observations, reflections, peer feedback) to identify behavioral evidence of skill development
2. Match observed behaviors to specific proficiency levels using a detailed rubric
3. Provide clear, evidence-based justifications for each assessment
4. Use kind, growth-oriented language that respects student dignity
5. Only assess skills for which you have direct, observable evidence

THE 17 SKILLS YOU ASSESS:

Social-Emotional Learning (SEL):
1. Self-Awareness
2. Self-Management
3. Social Awareness
4. Relationship Skills
5. Responsible Decision-Making

Executive Functioning (EF):
6. Working Memory
7. Inhibitory Control
8. Cognitive Flexibility
9. Planning & Prioritization
10. Organization
11. Task Initiation

21st Century Skills:
12. Critical Thinking
13. Communication
14. Collaboration
15. Creativity & Innovation
16. Digital Literacy
17. Global Awareness

PROFICIENCY LEVELS:
- **Emerging (E):** Needs significant, consistent support; skill application is inconsistent or absent
- **Developing (D):** Applies the skill with frequent prompting or scaffolding; inconsistent success
- **Proficient (P):** Applies the skill independently and consistently in familiar contexts; generally successful
- **Advanced (A):** Applies the skill flexibly and strategically in novel or challenging contexts; models the skill for others

COMPLETE RUBRIC:
{rubric_content}

ASSESSMENT RULES:
1. **Evidence-Based:** Only assess a skill if there is clear, observable evidence in the student data
2. **Specific Skill Focus:** Match behavior to the most specific skill (e.g., "organized materials" → Organization, not Self-Management)
3. **Level Justification:** Explain WHY the student is at this level using rubric criteria and observable behaviors
4. **Quote Selection:** Include a verbatim quote from the data that demonstrates the skill level
5. **No Assumptions:** Do not infer skills from demographics, context, or unstated factors
6. **Kind Language:** Use growth-oriented, respectful language that honors student effort
7. **Confidence Threshold:** If evidence is ambiguous or minimal, do not make an assessment

OUTPUT FORMAT:
Return ONLY a JSON array of assessment objects. Each assessment must include:

{{
  "skill_name": "exact skill name from the 17 skills list",
  "skill_category": "SEL" or "EF" or "21st Century",
  "level": "E" or "D" or "P" or "A",
  "justification": "clear explanation of why this level, referencing rubric criteria",
  "source_quote": "verbatim quote from student data demonstrating this skill",
  "data_point_count": 1
}}

Example:
[
  {{
    "skill_name": "Social Awareness",
    "skill_category": "SEL",
    "level": "P",
    "justification": "Student accurately interpreted subtle emotional cues when they noticed their peer was upset and asked if they needed help. This demonstrates proficient social awareness as defined in the rubric.",
    "source_quote": "I could tell Marcus was feeling left out so I asked if he wanted to join our group",
    "data_point_count": 1
  }}
]

{few_shot_examples}

Now analyze the following student data and return ONLY the JSON array of assessments.
"""


def build_few_shot_section(examples: List[Dict[str, Any]]) -> str:
    """
    Build the few-shot learning section from teacher-corrected examples
    
    Args:
        examples: List of validated assessments from teacher corrections
        
    Returns:
        str: Formatted few-shot section, or empty string if no examples
    """
    if not examples or len(examples) == 0:
        return ""
    
    section = "\n\nFEW-SHOT LEARNING EXAMPLES:\n"
    section += "The following are examples of validated assessments that have been reviewed and approved by teachers. Use these as reference for assessment quality and accuracy.\n\n"
    
    for i, example in enumerate(examples, 1):
        section += f"EXAMPLE {i}:\n"
        section += f"Skill: {example.get('skill_name', 'N/A')}\n"
        section += f"Level: {example.get('level', 'N/A')}\n"
        section += f"Justification: {example.get('justification', 'N/A')}\n"
        section += f"Source Quote: \"{example.get('source_quote', 'N/A')}\"\n"
        
        if 'teacher_notes' in example and example['teacher_notes']:
            section += f"Teacher Note: {example['teacher_notes']}\n"
        
        section += "\n" + ("-" * 80) + "\n\n"
    
    return section


def build_user_prompt(data_entry: Dict[str, Any]) -> str:
    """
    Build the user prompt from a student data entry
    
    Args:
        data_entry: Dictionary with 'content' and 'metadata' keys
        
    Returns:
        str: Formatted user prompt with student data
    """
    metadata = data_entry.get('metadata', {})
    
    prompt = "STUDENT DATA TO ANALYZE:\n\n"
    prompt += f"Type: {metadata.get('type', 'N/A')}\n"
    prompt += f"Date: {metadata.get('date', 'N/A')}\n"
    prompt += f"Context: {metadata.get('context', 'N/A')}\n\n"
    prompt += "---\n\n"
    prompt += data_entry.get('content', '')
    prompt += "\n\n---\n\n"
    prompt += "Return the JSON array of skill assessments based on the evidence above."
    
    return prompt
