import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.api_client import APIClient

# Page config
st.set_page_config(
    page_title="My Badge Collection",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Architects+Daughter&display=swap');

    .main {
        background: linear-gradient(135deg, #FFF9C4 0%, #FFF59D 100%);
        font-family: 'Patrick Hand', cursive;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .badge-title {
        font-family: 'Architects Daughter', cursive;
        font-size: 3rem;
        color: #F57F17;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 3px 3px 0px #FFE082;
    }

    /* Badge card */
    .badge-card {
        background: white;
        border: 3px solid #FFA000;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 6px 6px 0px #FFECB3;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        min-height: 200px;
    }

    .badge-card.earned {
        animation: badge-pop 0.5s ease-out;
    }

    .badge-card.earned:hover {
        transform: translateY(-10px) rotate(5deg);
        box-shadow: 10px 10px 0px #FFD54F;
    }

    .badge-card.locked {
        opacity: 0.4;
        filter: grayscale(80%);
    }

    .badge-card.locked:hover {
        opacity: 0.6;
    }

    @keyframes badge-pop {
        0% {
            transform: scale(0);
            opacity: 0;
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    /* Badge icon */
    .badge-icon {
        font-size: 4rem;
        margin: 1rem 0;
        animation: spin-slow 10s linear infinite;
    }

    .badge-icon.earned {
        animation: sparkle 2s ease-in-out infinite;
    }

    @keyframes sparkle {
        0%, 100% {
            transform: scale(1);
            filter: brightness(1);
        }
        50% {
            transform: scale(1.1);
            filter: brightness(1.3);
        }
    }

    @keyframes spin-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Badge name */
    .badge-name {
        font-size: 1.2rem;
        color: #F57F17;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    /* Badge level */
    .badge-level {
        font-size: 1rem;
        color: #FF8F00;
        margin: 0.3rem 0;
    }

    /* Badge type label */
    .badge-type {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .badge-type.bronze {
        background: #D7CCC8;
        color: #5D4037;
        border: 2px solid #8D6E63;
    }

    .badge-type.silver {
        background: #E0E0E0;
        color: #424242;
        border: 2px solid #757575;
    }

    .badge-type.gold {
        background: #FFD700;
        color: #F57F17;
        border: 2px solid #FFA000;
    }

    /* Progress section */
    .progress-section {
        background: white;
        border: 3px solid #FFA000;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 6px 6px 0px #FFECB3;
        text-align: center;
    }

    .progress-bar {
        width: 100%;
        height: 40px;
        background: #FFF9C4;
        border: 3px solid #FFA000;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
        margin: 1rem 0;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #FFD54F 0%, #FFA000 100%);
        transition: width 1s ease-out;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 1rem;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    /* Lock icon */
    .lock-icon {
        font-size: 2rem;
        opacity: 0.5;
    }

    /* Celebration message */
    .celebration {
        background: linear-gradient(135deg, #FFD54F 0%, #FFA726 100%);
        border: 3px solid #F57C00;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        font-size: 1.3rem;
        color: #E65100;
        box-shadow: 6px 6px 0px #FFCA28;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    /* Toggle button */
    .stCheckbox {
        font-family: 'Patrick Hand', cursive;
        font-size: 1.2rem;
        color: #F57F17;
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
        st.markdown(f'<img src="{st.session_state.avatar_url}" style="width:80px;height:80px;border-radius:50%;border:3px solid #FFA000;">', unsafe_allow_html=True)
with col2:
    st.markdown(f'<h1 class="badge-title">🏅 {student_name}\'s Badge Collection</h1>', unsafe_allow_html=True)
with col3:
    if st.button("🏠 Home"):
        st.switch_page("pages/Student_00_Home.py")

# Fetch badge data
try:
    with st.spinner("Loading your awesome badges..."):
        badge_data = APIClient.get_student_badges(student_id)

    earned_badges = badge_data.get('earned_badges', [])
    total_earned = len(earned_badges)
    total_possible = 51  # 17 skills × 3 levels (Bronze, Silver, Gold)

    # Progress section
    progress_percent = int((total_earned / total_possible) * 100) if total_possible > 0 else 0

    st.markdown(f"""
    <div class="progress-section">
        <h2 style="color: #F57F17; margin-top: 0;">Your Progress</h2>
        <h3 style="color: #FF8F00;">{total_earned} out of {total_possible} badges earned!</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percent}%">
                {progress_percent}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Celebration messages
    if total_earned == 0:
        st.markdown("""
        <div class="celebration">
            🌟 Your badge collection is ready to grow! Complete your goals to earn badges!
        </div>
        """, unsafe_allow_html=True)
    elif total_earned < 5:
        st.markdown("""
        <div class="celebration">
            🎉 Great start! You're building your collection!
        </div>
        """, unsafe_allow_html=True)
    elif total_earned < 15:
        st.markdown("""
        <div class="celebration">
            🌟 Amazing! You're really growing your skills!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="celebration">
            🏆 WOW! You're a badge-collecting superstar!
        </div>
        """, unsafe_allow_html=True)

    # Toggle to show locked badges
    show_locked = st.checkbox("Show badges I haven't earned yet", value=True)

    # Define all possible badges
    all_skills = [
        # SEL
        "Self-Awareness", "Self-Management", "Social Awareness", "Relationship Skills", "Responsible Decision-Making",
        # EF
        "Task Initiation", "Working Memory", "Organization", "Time Management", "Cognitive Flexibility", "Metacognition",
        # 21st Century
        "Critical Thinking", "Creativity", "Communication", "Collaboration", "Information Literacy", "Technology Skills"
    ]

    badge_levels = [
        ("Developing", "bronze", "🥉"),
        ("Proficient", "silver", "🥈"),
        ("Advanced", "gold", "🥇")
    ]

    # Create earned badges lookup
    earned_lookup = {(badge['skill_name'], badge['level_achieved']): badge for badge in earned_badges}

    # Display badges
    st.markdown("---")
    st.markdown("### 🎖️ Your Badges")

    # Group by level
    for level_name, badge_type, emoji in badge_levels:
        st.markdown(f"#### {emoji} {level_name} Badges ({badge_type.title()})")

        # Create columns for badges (4 per row)
        cols = st.columns(4)
        col_idx = 0

        for skill in all_skills:
            badge_key = (skill, level_name)
            is_earned = badge_key in earned_lookup

            # Only show if earned OR if show_locked is True
            if is_earned or show_locked:
                with cols[col_idx % 4]:
                    card_class = "badge-card earned" if is_earned else "badge-card locked"
                    icon = emoji if is_earned else "🔒"

                    if is_earned:
                        badge = earned_lookup[badge_key]
                        earned_date = badge.get('earned_date', '')[:10] if badge.get('earned_date') else ''

                        st.markdown(f"""
                        <div class="{card_class}">
                            <div class="badge-icon earned">{icon}</div>
                            <div class="badge-name">{skill}</div>
                            <div class="badge-type {badge_type}">{badge_type.title()}</div>
                            <div class="badge-level">Earned: {earned_date}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="{card_class}">
                            <div class="badge-icon">{icon}</div>
                            <div class="badge-name">{skill}</div>
                            <div class="badge-type {badge_type}">{badge_type.title()}</div>
                            <div class="badge-level" style="color: #999;">Not earned yet</div>
                        </div>
                        """, unsafe_allow_html=True)

                col_idx += 1

        st.markdown("---")

    # Navigation
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗺️ Back to Journey Map", use_container_width=True):
            st.switch_page("pages/Student_01_Journey_Map.py")

    with col2:
        if st.button("🎯 Check My Goal", use_container_width=True):
            st.switch_page("pages/Student_03_Current_Goal.py")

except Exception as e:
    st.error(f"Oops! We couldn't load your badges: {str(e)}")
    if st.button("← Try Again"):
        st.switch_page("pages/Student_00_Home.py")
