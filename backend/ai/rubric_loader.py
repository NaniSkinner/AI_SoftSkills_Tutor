"""
Rubric and Curriculum Loader Module

Loads the rubric and curriculum context from the Docs/ directory.
"""

import os


def load_rubric() -> str:
    """
    Load the skill rubric from Docs/Rubric.md

    Returns:
        str: The complete rubric content as a string

    Raises:
        FileNotFoundError: If Rubric.md does not exist
    """
    # Construct path: find project root by looking for Docs directory
    # This handles both local development and Docker container paths
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Try Docker path first (/app/ai -> /app/Docs)
    project_root = os.path.dirname(current_dir)  # /app/ai -> /app
    rubric_path = os.path.join(project_root, 'Docs', 'Rubric.md')

    # If that doesn't exist, try local development path (backend/ai -> Docs)
    if not os.path.exists(rubric_path):
        alt_root = os.path.dirname(project_root)  # backend -> root
        rubric_path = os.path.join(alt_root, 'Docs', 'Rubric.md')

    try:
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric_content = f.read()
        return rubric_content
    except FileNotFoundError:
        raise FileNotFoundError(f"Rubric file not found at: {rubric_path}")


def load_curriculum_context() -> str:
    """
    Load the curriculum context from Docs/Curriculum.md

    Returns:
        str: The complete curriculum content as a string

    Raises:
        FileNotFoundError: If Curriculum.md does not exist
    """
    # Construct path: find project root by looking for Docs directory
    # This handles both local development and Docker container paths
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Try Docker path first (/app/ai -> /app/Docs)
    project_root = os.path.dirname(current_dir)  # /app/ai -> /app
    curriculum_path = os.path.join(project_root, 'Docs', 'Curriculum.md')

    # If that doesn't exist, try local development path (backend/ai -> Docs)
    if not os.path.exists(curriculum_path):
        alt_root = os.path.dirname(project_root)  # backend -> root
        curriculum_path = os.path.join(alt_root, 'Docs', 'Curriculum.md')

    try:
        with open(curriculum_path, 'r', encoding='utf-8') as f:
            curriculum_content = f.read()
        return curriculum_content
    except FileNotFoundError:
        raise FileNotFoundError(f"Curriculum file not found at: {curriculum_path}")
