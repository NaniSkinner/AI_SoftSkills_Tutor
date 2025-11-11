"""
Badge Utilities

Helper functions for rendering and managing badges in the UI.
"""

from typing import Optional


def get_badge_color(level: str) -> str:
    """
    Get the display color for a skill level badge.

    Args:
        level: Skill level (Emerging, Developing, Proficient, Advanced)

    Returns:
        Hex color code for the badge
    """
    colors = {
        "Emerging": "#E0E0E0",      # Gray
        "Developing": "#CD7F32",    # Bronze
        "Proficient": "#C0C0C0",    # Silver
        "Advanced": "#FFD700"       # Gold
    }
    return colors.get(level, "#E0E0E0")  # Default to gray


def get_badge_type(level: str) -> Optional[str]:
    """
    Get the badge type from a skill level.

    Note: Emerging level does not earn badges.

    Args:
        level: Skill level (Emerging, Developing, Proficient, Advanced)

    Returns:
        Badge type ("bronze", "silver", "gold") or None if no badge
    """
    badge_types = {
        "Developing": "bronze",
        "Proficient": "silver",
        "Advanced": "gold"
    }
    return badge_types.get(level)


def get_level_emoji(level: str) -> str:
    """
    Get an emoji representation for a skill level.

    Args:
        level: Skill level

    Returns:
        Emoji string
    """
    emojis = {
        "Emerging": "🌱",
        "Developing": "🥉",
        "Proficient": "🥈",
        "Advanced": "🥇"
    }
    return emojis.get(level, "⭐")


def render_badge_html(skill_name: str, level: str, earned: bool = True) -> str:
    """
    Render a badge as HTML with inline styles.

    Args:
        skill_name: Name of the skill
        level: Skill level
        earned: Whether the badge has been earned (affects opacity)

    Returns:
        HTML string for the badge
    """
    color = get_badge_color(level)
    opacity = "1.0" if earned else "0.3"
    badge_emoji = get_level_emoji(level)

    # Lock icon for unearned badges
    lock_icon = "" if earned else "🔒 "

    html = f"""
    <div style="
        display: inline-block;
        background: linear-gradient(135deg, {color}, {color}dd);
        color: #333;
        padding: 12px 20px;
        border-radius: 10px;
        margin: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        opacity: {opacity};
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        min-width: 150px;
    ">
        <div style="font-size: 32px; margin-bottom: 5px;">
            {lock_icon}{badge_emoji}
        </div>
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 3px;">
            {skill_name}
        </div>
        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">
            {level}
        </div>
    </div>
    """
    return html


def render_badge_grid(badges: list, title: str = "Badges") -> str:
    """
    Render a grid of badges as HTML.

    Args:
        badges: List of badge dictionaries with skill_name, level, earned
        title: Optional title for the badge grid

    Returns:
        HTML string with badge grid
    """
    badge_html_items = [
        render_badge_html(badge["skill_name"], badge["level"], badge.get("earned", True))
        for badge in badges
    ]

    html = f"""
    <div style="margin: 20px 0;">
        <h3 style="margin-bottom: 15px;">{title}</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            {"".join(badge_html_items)}
        </div>
    </div>
    """
    return html


def get_progress_color(level: str) -> str:
    """
    Get a color suitable for progress indicators based on level.

    Args:
        level: Skill level

    Returns:
        Hex color code
    """
    colors = {
        "Emerging": "#ff6b6b",      # Red
        "Developing": "#ffd43b",    # Yellow
        "Proficient": "#51cf66",    # Green
        "Advanced": "#339af0"       # Blue
    }
    return colors.get(level, "#868e96")  # Default gray


def format_level_transition(from_level: str, to_level: str) -> str:
    """
    Format a level transition for display (e.g., "D → P").

    Args:
        from_level: Starting level
        to_level: Target level

    Returns:
        Formatted string
    """
    level_abbr = {
        "Emerging": "E",
        "Developing": "D",
        "Proficient": "P",
        "Advanced": "A"
    }

    from_abbr = level_abbr.get(from_level, from_level[0])
    to_abbr = level_abbr.get(to_level, to_level[0])

    return f"{from_abbr} → {to_abbr}"


def get_level_numeric(level: str) -> int:
    """
    Convert a skill level to a numeric value for charts.

    Args:
        level: Skill level

    Returns:
        Numeric value (1-4)
    """
    level_map = {
        "Emerging": 1,
        "Developing": 2,
        "Proficient": 3,
        "Advanced": 4
    }
    return level_map.get(level, 0)
