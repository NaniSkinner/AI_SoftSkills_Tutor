import streamlit as st
import streamlit.components.v1 as components
import sys
import json
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.api_client import APIClient

# Page config
st.set_page_config(
    page_title="My Journey Map",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Architects+Daughter&display=swap');

    .main {
        background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%);
        font-family: 'Patrick Hand', cursive;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .journey-title {
        font-family: 'Architects Daughter', cursive;
        font-size: 3rem;
        color: #00695C;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 2px 2px 0px #80CBC4;
    }

    /* Skill card with hand-drawn style */
    .skill-card {
        background: white;
        border: 3px solid #00897B;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 6px 6px 0px #80CBC4;
        transition: all 0.3s ease;
        position: relative;
    }

    .skill-card:hover {
        transform: translateX(10px);
        box-shadow: 8px 8px 0px #4DB6AC;
    }

    /* Level indicators */
    .level-path {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1.5rem 0;
        position: relative;
    }

    .level-step {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 4px solid #B2DFDB;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
    }

    .level-step.completed {
        background: #66BB6A;
        border-color: #388E3C;
        animation: pulse 2s infinite;
    }

    .level-step.current {
        background: linear-gradient(135deg, #FFD54F 0%, #FFA726 100%);
        border-color: #F57C00;
        box-shadow: 0 0 20px #FFA726;
        animation: glow 2s infinite, bounce-slow 3s infinite;
        transform: scale(1.2);
    }

    .level-step.locked {
        background: #E0E0E0;
        border-color: #9E9E9E;
        opacity: 0.5;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px #FFA726; }
        50% { box-shadow: 0 0 30px #FF6F00; }
    }

    @keyframes bounce-slow {
        0%, 100% { transform: scale(1.2) translateY(0); }
        50% { transform: scale(1.2) translateY(-10px); }
    }

    /* Path connecting levels */
    .level-connector {
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 4px;
        background: repeating-linear-gradient(
            90deg,
            #80CBC4 0px,
            #80CBC4 10px,
            transparent 10px,
            transparent 20px
        );
        z-index: 1;
    }

    .level-connector.completed {
        background: #66BB6A;
    }

    /* Level labels */
    .level-label {
        text-align: center;
        font-size: 0.9rem;
        color: #00695C;
        margin-top: 0.5rem;
        font-weight: bold;
    }

    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: bold;
        margin: 0.5rem;
        border: 2px solid;
    }

    .category-SEL {
        background: #FFE0B2;
        border-color: #FF9800;
        color: #E65100;
    }

    .category-EF {
        background: #E1BEE7;
        border-color: #9C27B0;
        color: #4A148C;
    }

    .category-21st {
        background: #B2DFDB;
        border-color: #00897B;
        color: #004D40;
    }

    /* Stats box */
    .stats-box {
        background: white;
        border: 3px solid #00897B;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 6px 6px 0px #80CBC4;
        margin: 1rem 0;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: bold;
        color: #00695C;
    }

    .stat-label {
        font-size: 1.2rem;
        color: #00897B;
    }

    /* Progress message */
    .progress-message {
        background: linear-gradient(135deg, #FFE57F 0%, #FFD54F 100%);
        border: 3px solid #F57C00;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
        font-size: 1.3rem;
        color: #E65100;
        box-shadow: 6px 6px 0px #FFCA28;
    }

    /* Navigation buttons */
    .nav-button {
        background: linear-gradient(135deg, #7FA99B 0%, #5D8B7F 100%);
        border: 3px solid #00695C;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-size: 1.2rem;
        color: white;
        font-family: 'Architects Daughter', cursive;
        cursor: pointer;
        box-shadow: 4px 4px 0px #80CBC4;
        transition: all 0.3s ease;
    }

    .nav-button:hover {
        transform: translateY(-3px);
        box-shadow: 6px 6px 0px #4DB6AC;
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

# Initialize view mode in session state
if 'journey_view_mode' not in st.session_state:
    st.session_state.journey_view_mode = 'classic'

# Header with avatar
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if 'avatar_url' in st.session_state:
        st.markdown(f'<img src="{st.session_state.avatar_url}" style="width:80px;height:80px;border-radius:50%;border:3px solid #00897B;">', unsafe_allow_html=True)
with col2:
    st.markdown(f'<h1 class="journey-title">🗺️ {student_name}\'s Journey Map</h1>', unsafe_allow_html=True)
with col3:
    if st.button("🏠 Home"):
        st.switch_page("pages/Student_00_Home.py")

# View mode toggle
st.markdown("---")
view_mode = st.radio(
    "Choose your view:",
    ["📊 Classic Progress Bars", "🗺️ Road to Skills Map"],
    horizontal=True,
    key="view_mode_selector"
)
st.session_state.journey_view_mode = 'road' if view_mode == "🗺️ Road to Skills Map" else 'classic'
st.markdown("---")

# Fetch student data
try:
    with st.spinner("Loading your amazing progress..."):
        skill_trends = APIClient.get_skill_trends(student_id)
        progress_data = APIClient.get_student_progress(student_id)
        active_targets = APIClient.get_student_targets(student_id, completed=False)

    if not skill_trends:
        st.info("Your journey is just beginning! Ask your teacher to add some activities.")
        st.stop()

    # Conditional rendering based on view mode
    if st.session_state.journey_view_mode == 'road':
        # Load Road to Skills interactive map (enhanced version with background)
        component_path = Path(__file__).parent.parent / 'components' / 'road_to_skills_enhanced.html'
        skill_tips_path = Path(__file__).parent.parent / 'data' / 'skill_tips.json'
        visual_config_path = Path(__file__).parent.parent / 'data' / 'skill_visuals.json'
        background_img_path = Path(__file__).parent.parent / 'assets' / 'backgrounds' / 'road_map_background.png'

        # Load JSON data
        with open(skill_tips_path, 'r') as f:
            skill_tips_data = json.load(f)
        with open(visual_config_path, 'r') as f:
            visual_config_data = json.load(f)

        # Convert background image to base64
        import base64
        with open(background_img_path, 'rb') as f:
            background_base64 = base64.b64encode(f.read()).decode()
        background_data_url = f"data:image/png;base64,{background_base64}"

        # Load HTML template
        with open(component_path, 'r') as f:
            component_html = f.read()

        # Replace placeholders with actual data
        component_html = component_html.replace('%SKILL_TIPS_DATA%', json.dumps(skill_tips_data))
        component_html = component_html.replace('%VISUAL_CONFIG_DATA%', json.dumps(visual_config_data))
        component_html = component_html.replace('%BACKGROUND_IMAGE%', background_data_url)

        # Prepare data for component
        current_goal = active_targets[0] if active_targets else {}
        avatar_url = st.session_state.get('avatar_url', '')

        # Inject data as JavaScript variables before the App render
        data_injection = f"""
        <script>
            window.STUDENT_DATA = {json.dumps(skill_trends)};
            window.CURRENT_GOAL = {json.dumps(current_goal)};
            window.AVATAR_URL = '{avatar_url}';
        </script>
        """

        # Insert data injection before closing body tag
        component_html = component_html.replace('</body>', f'{data_injection}</body>')

        # Add cache-busting meta tag
        cache_buster = f'<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" /><meta http-equiv="Pragma" content="no-cache" /><meta http-equiv="Expires" content="0" />'
        component_html = component_html.replace('<head>', f'<head>{cache_buster}')

        # Render component with increased height for scrolling
        components.html(component_html, height=1200, scrolling=True)

    else:
        # Show classic progress bars view
        # Progress stats
        st.markdown("### 📊 Your Progress at a Glance")
        stat_col1, stat_col2, stat_col3 = st.columns(3)

        with stat_col1:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stat-number">{progress_data.get('total_assessments', 0)}</div>
                <div class="stat-label">Skills Tracked</div>
            </div>
            """, unsafe_allow_html=True)

        with stat_col2:
            # Count skills at Proficient or Advanced
            high_level_skills = sum(1 for skill in skill_trends
                                   if skill['assessments'] and
                                   skill['assessments'][-1]['level'] in ['P', 'Proficient', 'A', 'Advanced'])
            st.markdown(f"""
            <div class="stats-box">
                <div class="stat-number">{high_level_skills}</div>
                <div class="stat-label">Strong Skills</div>
            </div>
            """, unsafe_allow_html=True)

        with stat_col3:
            st.markdown(f"""
            <div class="stats-box">
                <div class="stat-number">{progress_data.get('total_badges', 0)}</div>
                <div class="stat-label">Badges Earned</div>
            </div>
            """, unsafe_allow_html=True)

        # Motivational message
        if high_level_skills > 0:
            st.markdown(f"""
            <div class="progress-message">
                🌟 Amazing! You're getting stronger in {high_level_skills} skill{"s" if high_level_skills != 1 else ""}! Keep up the great work!
            </div>
            """, unsafe_allow_html=True)

        # Group skills by category
        skills_by_category = {
            "Social-Emotional Learning (SEL)": [],
            "Executive Function (EF)": [],
            "21st Century Skills": []
        }

        for skill in skill_trends:
            category = skill['skill_category']
            if category == "SEL":
                skills_by_category["Social-Emotional Learning (SEL)"].append(skill)
            elif category == "EF":
                skills_by_category["Executive Function (EF)"].append(skill)
            elif category == "21st Century":
                skills_by_category["21st Century Skills"].append(skill)

        # Display skills by category
        st.markdown("---")
        st.markdown("### 🌈 Your Skills by Type")

        category_icons = {
            "Social-Emotional Learning (SEL)": "❤️",
            "Executive Function (EF)": "🧠",
            "21st Century Skills": "🚀"
        }

        category_classes = {
            "Social-Emotional Learning (SEL)": "category-SEL",
            "Executive Function (EF)": "category-EF",
            "21st Century Skills": "category-21st"
        }

        for category_name, skills in skills_by_category.items():
            if skills:
                icon = category_icons.get(category_name, "⭐")
                badge_class = category_classes.get(category_name, "")

                st.markdown(f'<span class="category-badge {badge_class}">{icon} {category_name}</span>', unsafe_allow_html=True)

                for skill in skills:
                    skill_name = skill['skill_name']
                    assessments = skill['assessments']

                    if assessments:
                        current_assessment = assessments[-1]
                        current_level = current_assessment['level']

                        # Normalize level
                        level_map = {'E': 'Emerging', 'D': 'Developing', 'P': 'Proficient', 'A': 'Advanced'}
                        current_level_full = level_map.get(current_level, current_level)

                        # Determine which levels are completed
                        levels = ['Emerging', 'Developing', 'Proficient', 'Advanced']
                        level_emojis = {'Emerging': '🌱', 'Developing': '🌿', 'Proficient': '🌳', 'Advanced': '🏆'}
                        current_idx = levels.index(current_level_full) if current_level_full in levels else 0

                        # Create skill card
                        st.markdown(f"""
                        <div class="skill-card">
                            <h3 style="color: #00695C; margin-top: 0;">{skill_name}</h3>
                            <div class="level-path">
                                <div class="level-connector{'completed' if current_idx > 0 else ''}"></div>
                        """, unsafe_allow_html=True)

                        # Create level steps
                        level_cols = st.columns(4)
                        for idx, (level, emoji) in enumerate(zip(levels, level_emojis.values())):
                            with level_cols[idx]:
                                if idx < current_idx:
                                    status_class = "completed"
                                    status_text = "✓"
                                elif idx == current_idx:
                                    status_class = "current"
                                    status_text = emoji
                                else:
                                    status_class = "locked"
                                    status_text = "🔒"

                                st.markdown(f"""
                                <div style="text-align: center;">
                                    <div class="level-step {status_class}">{status_text}</div>
                                    <div class="level-label">{level[:3]}</div>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("</div></div>", unsafe_allow_html=True)

    # Navigation (outside both view modes)
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏅 See My Badges", use_container_width=True):
            st.switch_page("pages/Student_02_Badge_Collection.py")

    with col2:
        if st.button("🎯 Check My Goal", use_container_width=True):
            st.switch_page("pages/Student_03_Current_Goal.py")

except Exception as e:
    st.error(f"Oops! We couldn't load your journey: {str(e)}")
    if st.button("← Try Again"):
        st.switch_page("pages/Student_00_Home.py")
