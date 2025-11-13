import streamlit as st
import sys
import os
import logging
from pathlib import Path
from st_clickable_images import clickable_images

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))
from utils.api_client import APIClient

# Page config
st.set_page_config(
    page_title="My Skills Journey",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for hand-drawn theme with earth tones
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Architects+Daughter&display=swap');

    /* Global styles */
    .main {
        background: linear-gradient(135deg, #FFF8E7 0%, #F5E6D3 100%);
        font-family: 'Patrick Hand', cursive;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Title animation */
    .student-title {
        font-family: 'Architects Daughter', cursive;
        font-size: 3.5rem;
        color: #5D4E37;
        text-align: center;
        margin: 2rem 0;
        animation: bounce 1s ease-in-out;
        text-shadow: 3px 3px 0px #E8C5A5;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    /* Subtitle */
    .subtitle {
        font-family: 'Patrick Hand', cursive;
        font-size: 1.5rem;
        color: #7FA99B;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Avatar card with hand-drawn border */
    .avatar-card {
        background: white;
        border: 3px solid #8B7355;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 8px 8px 0px #A0937D;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }

    .avatar-card:hover {
        transform: translateY(-10px) rotate(2deg);
        box-shadow: 12px 12px 0px #7FA99B;
    }

    .avatar-card.selected {
        border: 4px solid #7FA99B;
        background: #FFF8E7;
        box-shadow: 12px 12px 0px #5D4E37;
    }

    /* Style for clickable avatar images */
    .clickable-images img:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
    }

    /* Avatar image */
    .avatar-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 3px solid #E8C5A5;
        margin: 0 auto;
        display: block;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Avatar name */
    .avatar-name {
        text-align: center;
        font-size: 1.3rem;
        color: #5D4E37;
        margin-top: 0.5rem;
        font-weight: bold;
    }

    /* Start button */
    .start-button {
        background: linear-gradient(135deg, #7FA99B 0%, #5D8B7F 100%);
        border: 3px solid #5D4E37;
        border-radius: 15px;
        padding: 1rem 3rem;
        font-size: 1.5rem;
        color: white;
        font-family: 'Architects Daughter', cursive;
        cursor: pointer;
        box-shadow: 6px 6px 0px #A0937D;
        transition: all 0.3s ease;
        margin: 2rem auto;
        display: block;
    }

    .start-button:hover {
        transform: translateY(-5px);
        box-shadow: 8px 8px 0px #8B7355;
    }

    /* Student dropdown */
    .stSelectbox {
        font-family: 'Patrick Hand', cursive;
        font-size: 1.2rem;
    }

    .stSelectbox > div > div {
        border: 3px solid #8B7355;
        border-radius: 15px;
        background: white;
        box-shadow: 4px 4px 0px #A0937D;
    }

    /* Doodle decorations */
    .doodle {
        position: absolute;
        opacity: 0.3;
        pointer-events: none;
    }

    /* Info box */
    .info-box {
        background: #FFF8E7;
        border: 3px dashed #7FA99B;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem auto;
        max-width: 600px;
        text-align: center;
        font-size: 1.2rem;
        color: #5D4E37;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_avatar' not in st.session_state:
    st.session_state.selected_avatar = None
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = None

# Title
st.markdown('<h1 class="student-title">🎒 Welcome to Your Skills Journey!</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Let\'s explore how amazing you are!</p>', unsafe_allow_html=True)

# Step 1: Select student
st.markdown("### 👋 First, who are you?")

# Debug: Log backend URL being used
backend_url = os.getenv("BACKEND_URL", "http://backend:8000")
logger.info(f"Using BACKEND_URL: {backend_url}")

try:
    students = APIClient.get_students()

    if students:
        # Create student options
        student_options = {f"{s['name']} (Grade {s['grade']})": s for s in students}

        selected_option = st.selectbox(
            "Pick your name:",
            options=["Choose your name..."] + list(student_options.keys()),
            key="student_selector"
        )

        if selected_option != "Choose your name...":
            student = student_options[selected_option]
            st.session_state.student_id = student['id']
            st.session_state.student_name = student['name']

            # Step 2: Choose avatar
            st.markdown("---")
            st.markdown(f"### 🎨 Awesome, {student['name']}! Pick your avatar:")

            # Avatar options with local images
            import base64
            from pathlib import Path

            def get_image_base64(img_path):
                """Convert image to base64 for embedding"""
                with open(img_path, "rb") as f:
                    return base64.b64encode(f.read()).decode()

            assets_path = Path(__file__).parent.parent / "assets" / "avatars"

            avatar_styles = [
                {
                    "name": "Boy",
                    "file": "avatar1.png",
                    "path": assets_path / "avatar1.png"
                },
                {
                    "name": "Girl",
                    "file": "avatar2.png",
                    "path": assets_path / "avatar2.png"
                },
                {
                    "name": "Robot",
                    "file": "avatar3.png",
                    "path": assets_path / "avatar3.png"
                },
                {
                    "name": "Axolotl",
                    "file": "avatar4.png",
                    "path": assets_path / "avatar4.png"
                }
            ]

            # Convert images to base64 for embedding
            for avatar in avatar_styles:
                if avatar['path'].exists():
                    avatar['url'] = f"data:image/png;base64,{get_image_base64(avatar['path'])}"
                else:
                    st.error(f"Avatar image not found: {avatar['path']}")
                    avatar['url'] = ""

            # Display clickable avatars
            avatar_urls = [avatar['url'] for avatar in avatar_styles]

            clicked = clickable_images(
                avatar_urls,
                titles=[f"Select {avatar['name']}" for avatar in avatar_styles],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap", "gap": "20px"},
                img_style={"width": "150px", "height": "150px", "border-radius": "50%", "border": "3px solid #E8C5A5", "cursor": "pointer", "transition": "transform 0.3s ease"}
            )

            # Handle avatar click
            if clicked > -1:
                # Save avatar selection and go directly to dashboard
                st.session_state.selected_avatar = avatar_styles[clicked]['name']
                st.session_state.avatar_url = avatar_styles[clicked]['url']
                st.session_state.avatar_file = avatar_styles[clicked]['file']
                st.switch_page("pages/Student_01_Journey_Map.py")
        else:
            st.markdown("""
            <div class="info-box">
                👆 Pick your name from the dropdown above to get started!
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No students found. Please contact your teacher!")

except Exception as e:
    st.error(f"Oops! Something went wrong: {str(e)}")
    st.info("Please refresh the page or contact your teacher for help.")

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
