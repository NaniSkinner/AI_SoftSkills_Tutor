"""
Rubric Utilities

Helper functions for loading and displaying skill rubrics in the UI.
"""

from typing import Dict, Optional

# Rubric data for all 17 skills
RUBRIC_DATA = {
    # SEL Skills
    "Self-Awareness": {
        "category": "Social-Emotional Learning (SEL)",
        "Emerging": "Cannot identify or mislabels own emotions; unaware of personal strengths/weaknesses; blames external factors",
        "Developing": "Can name basic emotions (happy, sad, angry) when prompted; can state 1-2 strengths/weaknesses with guidance",
        "Proficient": "Accurately identifies complex emotions (frustration, anxiety); describes how emotions affect behavior; recognizes learning style",
        "Advanced": "Reflects on internal states for complex motivations; uses self-knowledge to adjust goals; demonstrates metacognition"
    },
    "Self-Management": {
        "category": "Social-Emotional Learning (SEL)",
        "Emerging": "Reacts impulsively; requires constant reminders; gives up quickly when faced with difficulty",
        "Developing": "Uses simple coping strategies when prompted; sustains effort on short tasks with reminders; manages stress with adult support",
        "Proficient": "Independently uses variety of strategies for emotions/stress; sets and works toward short-term goals; demonstrates persistence",
        "Advanced": "Proactively manages stress in high-pressure situations; adapts strategies; sets and monitors long-term complex goals"
    },
    "Social Awareness": {
        "category": "Social-Emotional Learning (SEL)",
        "Emerging": "Fails to notice others' emotional cues; makes insensitive comments; assumes own perspective is universal",
        "Developing": "Recognizes obvious emotional cues (crying, shouting); states others' perspectives when asked; understands basic social rules",
        "Proficient": "Accurately interprets subtle non-verbal cues/body language; expresses empathy; understands/respects diverse cultural norms",
        "Advanced": "Seeks to understand diverse perspectives and systemic issues; advocates for others; mediates conflicts; builds inclusive environments"
    },
    "Relationship Skills": {
        "category": "Social-Emotional Learning (SEL)",
        "Emerging": "Struggles to share/take turns; interrupts frequently; relies on avoidance/aggression; cannot ask for help appropriately",
        "Developing": "Participates in group work but needs structure; communicates needs with prompting; resolves minor conflicts with adult intervention",
        "Proficient": "Communicates clearly/respectfully; listens actively; offers constructive feedback; negotiates/compromises effectively",
        "Advanced": "Initiates positive relationships across groups; mentors peers; leads collaborative efforts; resolves group conflicts constructively"
    },
    "Responsible Decision-Making": {
        "category": "Social-Emotional Learning (SEL)",
        "Emerging": "Acts without considering consequences; makes choices for immediate gratification; ignores ethical concerns/safety rules",
        "Developing": "Lists potential consequences when prompted; makes safe choices in familiar, low-stakes situations",
        "Proficient": "Systematically considers ethical implications, safety, well-being before acting; uses problem-solving steps for sound choices",
        "Advanced": "Applies comprehensive ethical framework to complex novel problems; anticipates long-term consequences; advocates for community benefit"
    },

    # EF Skills
    "Working Memory": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Cannot follow multi-step directions (3+ steps); loses track of task goals; struggles to connect new info to prior knowledge",
        "Developing": "Follows 3-4 step directions with repetition; needs frequent task goal reminders; makes simple connections between ideas",
        "Proficient": "Follows complex multi-step instructions; holds/manipulates information for complex tasks (e.g., multi-paragraph essays)",
        "Advanced": "Integrates information from multiple sources (lectures, readings, discussions); manages multiple concurrent mental tasks without error"
    },
    "Inhibitory Control": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Easily distracted by noise/movement; blurts out; physically restless; cannot stop non-productive behavior without intervention",
        "Developing": "Ignores minor distractions with verbal reminders; pauses briefly before speaking; stops task when told",
        "Proficient": "Sustains attention despite moderate distractions; thinks before speaking/acting; delays gratification for necessary tasks",
        "Advanced": "Proactively identifies/minimizes distractions; maintains focus during long complex tasks; high self-control in emotionally charged situations"
    },
    "Cognitive Flexibility": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Upset/stuck when plan changes; insists on single problem-solving method; struggles to transition between subjects/tasks",
        "Developing": "Adjusts to minor changes with encouragement; tries second method if first fails, but needs prompting",
        "Proficient": "Easily transitions between tasks/subjects; generates/evaluates multiple perspectives/solutions; adapts strategy with evidence",
        "Advanced": "Thrives on ambiguity/novelty; spontaneously reframes problems for innovative solutions; holds conflicting ideas simultaneously"
    },
    "Planning & Prioritization": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Starts without plan; estimates time inaccurately; treats all tasks equally; misses deadlines frequently",
        "Developing": "Creates simple linear plans when directed; prioritizes 2-3 tasks with guidance; needs help breaking down large projects",
        "Proficient": "Independently creates detailed multi-step plans for long-term projects; accurately estimates time; prioritizes by urgency/importance",
        "Advanced": "Develops contingency plans; manages multiple long-term projects; allocates resources strategically for maximum efficiency"
    },
    "Organization": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Chaotic desk/locker/backpack; loses materials frequently; unsorted digital files; incomplete/disorganized notes",
        "Developing": "Keeps organized with daily adult checks; uses planner inconsistently; finds materials after brief search",
        "Proficient": "Maintains organized physical/digital workspace; consistently uses planner/digital tool; takes clear, structured notes",
        "Advanced": "Develops personalized systems maximizing efficiency; helps peers organize; maintains long-term information retrieval system"
    },
    "Task Initiation": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Procrastinates significantly; needs repeated prompts to start; struggles to generate initial ideas/first steps",
        "Developing": "Starts after 1-2 prompts; begins if first step is explicit; shows low motivation for difficult tasks",
        "Proficient": "Independently begins tasks promptly, even if challenging/uninteresting; breaks down large tasks into manageable first steps",
        "Advanced": "Eagerly initiates complex self-directed projects; motivates self and others; generates multiple viable starting points"
    },
    "Time Management": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Cannot estimate time needed; frequently late; misses deadlines; rushes or leaves tasks unfinished",
        "Developing": "Estimates time with moderate accuracy; completes short-term tasks on time with reminders; uses timers when prompted",
        "Proficient": "Accurately estimates time for tasks; meets deadlines consistently; balances multiple activities; uses time-management tools independently",
        "Advanced": "Optimizes schedule for peak productivity; builds in buffer time; helps others manage time; adjusts plans proactively"
    },
    "Metacognition": {
        "category": "Executive Functioning (EF)",
        "Emerging": "Cannot explain own thinking process; unaware of what helps learning; repeats ineffective strategies without reflection",
        "Developing": "Identifies strategies that work when prompted; reflects on performance with guidance; recognizes when confused",
        "Proficient": "Monitors own understanding; adjusts strategies when not working; explains reasoning clearly; reflects on learning process",
        "Advanced": "Consistently evaluates and refines thinking strategies; transfers metacognitive skills across contexts; coaches peers on reflection"
    },

    # 21st Century Skills
    "Critical Thinking": {
        "category": "21st Century Skills",
        "Emerging": "Accepts information at face value; struggles to distinguish fact from opinion; cannot identify simple argument flaws",
        "Developing": "Identifies basic facts/opinions; questions information when prompted; identifies 1-2 simple biases in source",
        "Proficient": "Analyzes information from multiple sources; evaluates source credibility; constructs well-reasoned arguments with evidence",
        "Advanced": "Synthesizes complex conflicting information for original insights; develops/tests hypotheses; challenges underlying assumptions"
    },
    "Communication": {
        "category": "21st Century Skills",
        "Emerging": "Expresses ideas unclearly/incompletely; avoids speaking in groups; written work disorganized with many errors",
        "Developing": "Conveys basic information clearly; participates when called upon; written work understandable but lacks structure/polish",
        "Proficient": "Articulates complex ideas clearly/persuasively orally and in writing; adapts to audience/purpose; uses appropriate digital media",
        "Advanced": "Commands sophisticated vocabulary/rhetorical style; inspires/influences through compelling communication; excels at cross-cultural communication"
    },
    "Collaboration": {
        "category": "21st Century Skills",
        "Emerging": "Dominates or withdraws from group work; refuses to compromise; focuses only on own part",
        "Developing": "Works with group but needs clear roles/supervision; contributes ideas when asked; compromises on minor points with encouragement",
        "Proficient": "Works effectively with diverse members; actively listens/integrates ideas; shares responsibility; helps group achieve goals",
        "Advanced": "Leads collaborative efforts; fosters inclusive environment; resolves conflicts constructively; elevates quality through shared vision"
    },
    "Creativity & Innovation": {
        "category": "21st Century Skills",
        "Emerging": "Prefers to copy existing ideas; struggles to generate new ideas; resists non-traditional approaches",
        "Developing": "Generates few new ideas with specific prompt; willing to try new approach if guided",
        "Proficient": "Generates original ideas/solutions; elaborates/refines based on feedback; applies creative thinking to solve problems",
        "Advanced": "Consistently produces novel, valuable solutions; connects unrelated concepts for innovation; inspires creative risk-taking"
    },
    "Digital Literacy": {
        "category": "21st Century Skills",
        "Emerging": "Uses technology only for entertainment; struggles with basic file management; unaware of online safety/privacy",
        "Developing": "Uses required school software; understands basic password safety; needs help evaluating online source reliability",
        "Proficient": "Uses variety of digital tools for research/organization/creation; practices safe, ethical, responsible online behavior (digital citizenship)",
        "Advanced": "Critically evaluates digital info/media for bias/accuracy; troubleshoots technical issues; uses advanced tools for complex projects"
    },
    "Global Awareness": {
        "category": "21st Century Skills",
        "Emerging": "Focuses only on local issues; little interest in/knowledge of other cultures; expresses ethnocentric views",
        "Developing": "Names few global issues/facts about other cultures; shows curiosity about diversity when exposed",
        "Proficient": "Understands interconnected global issues (climate change, economic interdependence); appreciates/respects diverse cultures/perspectives",
        "Advanced": "Researches/advocates for global challenge solutions; applies cross-cultural competence; views local issues through global lens"
    }
}


def get_skill_rubric(skill_name: str) -> Optional[Dict[str, str]]:
    """
    Get rubric descriptors for a specific skill.

    Args:
        skill_name: Name of the skill

    Returns:
        Dictionary with category and level descriptors, or None if not found
    """
    return RUBRIC_DATA.get(skill_name)


def render_rubric_html(skill_name: str, current_level: str = None) -> str:
    """
    Render rubric as HTML with optional highlighting of current level.

    Args:
        skill_name: Name of the skill
        current_level: Current proficiency level to highlight (optional)

    Returns:
        HTML string with rubric display
    """
    rubric = get_skill_rubric(skill_name)

    if not rubric:
        return f"<p>Rubric not found for skill: {skill_name}</p>"

    # Level emojis
    level_emojis = {
        "Emerging": "🌱",
        "Developing": "🥉",
        "Proficient": "🥈",
        "Advanced": "🥇"
    }

    html = f"""
    <div style="
        background: white;
        border: 2px solid #3a5a44;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 8px rgba(58, 90, 68, 0.1);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    ">
        <h3 style="
            color: #2c4733;
            margin-top: 0;
            margin-bottom: 8px;
            font-size: 1.3em;
            font-weight: 600;
        ">
            {skill_name}
        </h3>
        <p style="
            color: #6b8456;
            font-size: 0.95em;
            margin-bottom: 24px;
            margin-top: 0;
        ">
            Category: {rubric['category']}
        </p>
    """

    for level in ["Emerging", "Developing", "Proficient", "Advanced"]:
        is_current = (level == current_level)

        # Styling based on whether it's the current level
        if is_current:
            border_style = "4px solid #d67e3a"
            bg_color = "#fff7ed"
            box_shadow = "0 4px 16px rgba(214, 126, 58, 0.25)"
            current_badge = '<span style="background: #d67e3a; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; margin-left: 12px; font-weight: 600;">CURRENT LEVEL</span>'
        else:
            border_style = "2px solid #e8e5df"
            bg_color = "white"
            box_shadow = "0 2px 4px rgba(0, 0, 0, 0.05)"
            current_badge = ""

        html += f"""
        <div style="
            background: {bg_color};
            border: {border_style};
            border-radius: 12px;
            padding: 18px;
            margin: 16px 0;
            box-shadow: {box_shadow};
        ">
            <div style="
                font-weight: 600;
                color: #2c4733;
                margin-bottom: 12px;
                font-size: 1.1em;
                display: flex;
                align-items: center;
            ">
                <span style="margin-right: 8px; font-size: 1.3em;">{level_emojis[level]}</span>
                <span>{level}</span>
                {current_badge}
            </div>
            <div style="
                color: #4a5a4f;
                font-size: 1em;
                line-height: 1.7;
            ">
                {rubric[level]}
            </div>
        </div>
        """

    html += """
        <div style="
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #e8e5df;
            color: #6b8456;
            font-size: 0.9em;
        ">
            💡 <strong>Tip:</strong> Use this rubric to verify if the AI's assessment matches the student's actual performance level.
        </div>
    </div>
    """
    return html


def get_all_skill_names() -> list:
    """
    Get a list of all skill names with rubrics.

    Returns:
        List of skill names
    """
    return list(RUBRIC_DATA.keys())


def get_skills_by_category() -> Dict[str, list]:
    """
    Get skills organized by category.

    Returns:
        Dictionary mapping category names to lists of skill names
    """
    categories = {}

    for skill_name, rubric in RUBRIC_DATA.items():
        category = rubric['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(skill_name)

    return categories
