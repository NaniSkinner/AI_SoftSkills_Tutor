import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.api_client import APIClient

# Page config
st.set_page_config(
    page_title="My Current Goal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Age-appropriate tips for each skill (ages 9-14)
SKILL_TIPS = {
    "Self-Awareness": [
        "Keep a feelings journal! Write down how you feel each day and why.",
        "Ask yourself: What am I good at? What do I want to get better at?",
        "Notice when you're upset. Take 3 deep breaths before reacting."
    ],
    "Self-Management": [
        "Make a daily checklist. Check off tasks as you finish them!",
        "Set a timer for homework. Take 5-minute breaks every 20 minutes.",
        "Create a calm-down corner with things that help you relax."
    ],
    "Social Awareness": [
        "Pay attention to how others feel. Look at their face and body language.",
        "Practice active listening: look at the person and nod to show you understand.",
        "Think about how your words might make someone else feel."
    ],
    "Relationship Skills": [
        "Use 'I feel...' statements when something bothers you.",
        "Be a good friend: share, take turns, and include others.",
        "Solve problems together. Ask: 'What can we both agree on?'"
    ],
    "Responsible Decision-Making": [
        "Stop and think before acting. Ask: Is this safe? Is it kind? Is it fair?",
        "Think about consequences. What might happen if I do this?",
        "When stuck, ask a trusted adult for help making the choice."
    ],
    "Task Initiation": [
        "Break big tasks into tiny steps. Do just the first step to start!",
        "Set up your workspace before you begin. Get everything you need ready.",
        "Use the '5-minute rule': commit to working for just 5 minutes to get started."
    ],
    "Working Memory": [
        "Write things down right away! Use sticky notes or a planner.",
        "Repeat information out loud or in your head to remember it.",
        "Make up silly rhymes or songs to help you remember facts."
    ],
    "Organization": [
        "Use different colored folders for each subject at school.",
        "Clean your backpack every Friday. Throw away old papers.",
        "Keep a weekly planner. Write down all homework and activities."
    ],
    "Time Management": [
        "Guess how long tasks will take, then time yourself. Were you right?",
        "Use timers and alarms to help you stay on schedule.",
        "Do the hardest thing first when your brain is freshest."
    ],
    "Cognitive Flexibility": [
        "When Plan A doesn't work, think of Plan B! Always have a backup.",
        "Try seeing things from someone else's point of view.",
        "Play strategy games that make you think in new ways."
    ],
    "Metacognition": [
        "After finishing work, ask yourself: What did I do well? What can I improve?",
        "Figure out HOW you learn best: by reading, listening, or doing?",
        "When you don't understand, stop and ask yourself: What am I confused about?"
    ],
    "Critical Thinking": [
        "Ask 'Why?' at least 3 times to really understand something.",
        "Look for evidence. Don't just believe everything you hear!",
        "Compare and contrast: How are these things similar? How are they different?"
    ],
    "Creativity": [
        "Give yourself time to daydream and imagine new ideas.",
        "Combine two different things to create something new and unique.",
        "Don't worry about being perfect. Let yourself make 'mistakes' while creating!"
    ],
    "Communication": [
        "Speak clearly and look at the person you're talking to.",
        "Before speaking, organize your thoughts: Beginning, Middle, End.",
        "Listen more than you talk. Give others a chance to share too."
    ],
    "Collaboration": [
        "Everyone has strengths! Let each person do what they're good at.",
        "Compromise means both people give a little. Find the middle ground.",
        "Celebrate the team's success, not just your own."
    ],
    "Information Literacy": [
        "Check if information is true by looking at 2-3 different sources.",
        "Ask: Who wrote this? Why did they write it? Can I trust them?",
        "Organize information using charts, lists, or graphic organizers."
    ],
    "Technology Skills": [
        "Learn keyboard shortcuts to work faster on the computer.",
        "Always save your work! Use clear file names so you can find things later.",
        "If something isn't working, try restarting or asking for help."
    ]
}

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Architects+Daughter&display=swap');

    .main {
        background: linear-gradient(135deg, #E8EAF6 0%, #C5CAE9 100%);
        font-family: 'Patrick Hand', cursive;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .goal-title {
        font-family: 'Architects Daughter', cursive;
        font-size: 3rem;
        color: #3F51B5;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 3px 3px 0px #9FA8DA;
    }

    /* Goal card */
    .goal-card {
        background: white;
        border: 4px solid #5C6BC0;
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 8px 8px 0px #9FA8DA;
        position: relative;
    }

    .goal-skill {
        font-size: 2.5rem;
        color: #3F51B5;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Level progression arrow */
    .level-progression {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        font-size: 1.5rem;
    }

    .level-box {
        background: #E8EAF6;
        border: 3px solid #5C6BC0;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: bold;
        color: #3F51B5;
    }

    .level-box.current {
        background: #FFE082;
        border-color: #FFA000;
        color: #F57F17;
    }

    .level-box.target {
        background: #81C784;
        border-color: #388E3C;
        color: #1B5E20;
        animation: pulse-target 2s infinite;
    }

    @keyframes pulse-target {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    .arrow {
        font-size: 2rem;
        color: #5C6BC0;
        animation: slide-right 1.5s infinite;
    }

    @keyframes slide-right {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(10px); }
    }

    /* Tips section */
    .tips-section {
        background: #FFF9C4;
        border: 3px solid #FBC02D;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        box-shadow: 6px 6px 0px #FFF59D;
    }

    .tips-title {
        font-size: 1.8rem;
        color: #F57F17;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }

    .tip-item {
        background: white;
        border: 2px solid #FBC02D;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.8rem 0;
        display: flex;
        align-items: start;
        gap: 1rem;
        transition: all 0.3s ease;
    }

    .tip-item:hover {
        transform: translateX(10px);
        box-shadow: 4px 4px 0px #FFE082;
    }

    .tip-number {
        background: #FBC02D;
        color: white;
        border-radius: 50%;
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        flex-shrink: 0;
    }

    .tip-text {
        font-size: 1.1rem;
        color: #5D4037;
        line-height: 1.5;
    }

    /* Teacher info */
    .teacher-info {
        background: #E1F5FE;
        border: 2px dashed #0288D1;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.1rem;
        color: #01579B;
    }

    /* No goal message */
    .no-goal-message {
        background: white;
        border: 4px solid #9E9E9E;
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        margin: 3rem 0;
        box-shadow: 8px 8px 0px #E0E0E0;
    }

    .no-goal-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
    }

    .no-goal-text {
        font-size: 1.5rem;
        color: #616161;
        margin: 1rem 0;
    }

    /* Progress tracker */
    .progress-tracker {
        background: white;
        border: 3px solid #5C6BC0;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 6px 6px 0px #9FA8DA;
    }

    .days-working {
        font-size: 1.3rem;
        color: #3F51B5;
        text-align: center;
        font-weight: bold;
    }

    /* Motivation box */
    .motivation-box {
        background: linear-gradient(135deg, #81C784 0%, #66BB6A 100%);
        border: 3px solid #388E3C;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        color: white;
        font-size: 1.3rem;
        box-shadow: 6px 6px 0px #A5D6A7;
    }
</style>
""", unsafe_allow_html=True)

# Check if student is selected
if 'student_id' not in st.session_state or not st.session_state.student_id:
    st.warning("Please select your name first!")
    if st.button("← Back to Home"):
        st.switch_page("pages/Student_00_Home.py")
    st.stop()

# Get student info
student_name = st.session_state.student_name
student_id = st.session_state.student_id

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if 'avatar_url' in st.session_state:
        st.markdown(f'<img src="{st.session_state.avatar_url}" style="width:80px;height:80px;border-radius:50%;border:3px solid #5C6BC0;">', unsafe_allow_html=True)
with col2:
    st.markdown(f'<h1 class="goal-title">🎯 {student_name}\'s Current Goal</h1>', unsafe_allow_html=True)
with col3:
    if st.button("🏠 Home"):
        st.switch_page("pages/Student_00_Home.py")

# Fetch active targets
try:
    with st.spinner("Loading your goal..."):
        active_targets = APIClient.get_student_targets(student_id, completed=False)

    if not active_targets:
        # No active goal
        st.markdown("""
        <div class="no-goal-message">
            <div class="no-goal-icon">🎯</div>
            <div class="no-goal-text">You don't have an active goal right now!</div>
            <div style="font-size: 1.2rem; color: #757575; margin-top: 1rem;">
                Your teacher will help you set a new goal soon. Keep working on your skills!
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="motivation-box">
            💪 Keep learning and growing! Every day you're getting stronger!
        </div>
        """, unsafe_allow_html=True)

    else:
        # Display active goal
        target = active_targets[0]  # Show first active target

        skill_name = target['skill_name']
        starting_level = target['starting_level']
        target_level = target['target_level']
        assigned_by = target.get('assigned_by', 'Your teacher')
        assigned_at = target.get('assigned_at', '')

        # Calculate days working on goal
        if assigned_at:
            try:
                assigned_date = datetime.fromisoformat(assigned_at.replace('Z', '+00:00'))
                days_working = (datetime.now() - assigned_date).days
            except:
                days_working = 0
        else:
            days_working = 0

        # Display goal card
        st.markdown(f"""
        <div class="goal-card">
            <div class="goal-skill">📚 {skill_name}</div>

            <div class="teacher-info">
                👨‍🏫 Your teacher {assigned_by} believes in you!
            </div>

            <div class="level-progression">
                <div class="level-box current">{starting_level}</div>
                <div class="arrow">➜</div>
                <div class="level-box target">{target_level}</div>
            </div>

            <div class="progress-tracker">
                <div class="days-working">
                    📅 You've been working on this goal for {days_working} day{"s" if days_working != 1 else ""}!
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Motivational message
        if days_working < 7:
            message = "🌱 You're just getting started! Every expert was once a beginner!"
        elif days_working < 30:
            message = "🌿 Great progress! You're building this skill step by step!"
        else:
            message = "🌳 Wow! You've been working hard on this goal! Keep it up!"

        st.markdown(f"""
        <div class="motivation-box">
            {message}
        </div>
        """, unsafe_allow_html=True)

        # Tips section
        tips = SKILL_TIPS.get(skill_name, [
            "Practice this skill a little bit every day.",
            "Ask your teacher for feedback on how you're doing.",
            "Notice when you use this skill - celebrate those moments!"
        ])

        st.markdown(f"""
        <div class="tips-section">
            <div class="tips-title">💡 Tips to Reach Your Goal</div>
        """, unsafe_allow_html=True)

        for idx, tip in enumerate(tips, 1):
            st.markdown(f"""
            <div class="tip-item">
                <div class="tip-number">{idx}</div>
                <div class="tip-text">{tip}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Want to learn more section
        st.markdown("---")
        st.markdown("### 🤔 Want to Learn More?")

        learn_more_text = {
            "Self-Awareness": "Self-awareness means knowing your feelings, strengths, and what makes you 'you'! The more you understand yourself, the better choices you can make.",
            "Self-Management": "Self-management is about staying organized and in control of your actions. It helps you finish things you start!",
            "Social Awareness": "Social awareness means understanding how others feel and what they need. It helps you be a better friend!",
            "Relationship Skills": "Relationship skills help you make friends, work with others, and solve problems peacefully.",
            "Responsible Decision-Making": "Making good decisions means thinking carefully about choices and their consequences.",
            "Task Initiation": "Task initiation means getting started without putting things off. The hardest part is often just beginning!",
            "Working Memory": "Working memory is like your brain's notepad - it helps you remember things while you're using them.",
            "Organization": "Being organized means having a system to keep track of your stuff and your time.",
            "Time Management": "Time management helps you get things done when they need to be done.",
            "Cognitive Flexibility": "Cognitive flexibility means being able to think in new ways and adapt when things change.",
            "Metacognition": "Metacognition is thinking about your own thinking! It's how you learn to learn better.",
            "Critical Thinking": "Critical thinking means asking questions, looking for evidence, and not accepting everything at face value.",
            "Creativity": "Creativity is about coming up with new ideas and unique solutions to problems.",
            "Communication": "Communication is sharing your ideas clearly so others understand you.",
            "Collaboration": "Collaboration means working together as a team to achieve something great!",
            "Information Literacy": "Information literacy helps you find good information and know what to trust.",
            "Technology Skills": "Technology skills help you use computers and digital tools effectively and safely."
        }

        description = learn_more_text.get(skill_name, f"{skill_name} is an important skill that will help you succeed!")

        st.info(f"**What is {skill_name}?**\n\n{description}")

    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗺️ Back to Journey Map", use_container_width=True):
            st.switch_page("pages/Student_01_Journey_Map.py")

    with col2:
        if st.button("🏅 See My Badges", use_container_width=True):
            st.switch_page("pages/Student_02_Badge_Collection.py")

except Exception as e:
    st.error(f"Oops! We couldn't load your goal: {str(e)}")
    if st.button("← Try Again"):
        st.switch_page("pages/Student_00_Home.py")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #999; padding: 10px; font-size: 0.85em;'>
        Made with 🍵 by <strong>Nani Skinner</strong>
    </div>
    """,
    unsafe_allow_html=True
)
