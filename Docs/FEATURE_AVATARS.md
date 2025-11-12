# Student Avatar System

**Feature**: Custom kid-friendly avatars for student identity and journey map visualization
**Status**: ✅ Complete and Production-Ready
**Locations**:
- Selection: [frontend/pages/Student_00_Home.py](frontend/pages/Student_00_Home.py)
- Display: [frontend/components/road_to_skills_enhanced.html](frontend/components/road_to_skills_enhanced.html)

---

## Overview

The avatar system allows students to choose a personalized character that represents them throughout their learning journey. The chosen avatar appears on the journey map, animated to show their position along the path to skill mastery.

---

## Available Avatars

Four custom kid-friendly avatar options:

| Avatar | File | Size | Description |
|--------|------|------|-------------|
| **Boy** | avatar1.png | 589KB | Energetic character with brown curly hair |
| **Girl** | avatar2.png | 656KB | Cheerful character with orange wavy hair in floral dress |
| **Robot** | avatar3.png | 550KB | Friendly blue and white robot with headphones |
| **Axolotl** | avatar4.png | 811KB | Cute pink axolotl (salamander) character |

**Storage Location**: [frontend/assets/avatars/](frontend/assets/avatars/)

---

## Avatar Selection Flow

### 1. Student Home Page
Students select their avatar on the [Student_00_Home.py](frontend/pages/Student_00_Home.py) page:

```python
# Avatar selection interface
st.markdown("### 🎨 Choose Your Avatar!")

avatar_options = {
    "avatar1": "👦 Boy",
    "avatar2": "👧 Girl",
    "avatar3": "🤖 Robot",
    "avatar4": "🦎 Axolotl"
}

cols = st.columns(4)
for i, (avatar_id, avatar_name) in enumerate(avatar_options.items()):
    with cols[i]:
        if st.button(avatar_name, key=f"avatar_{avatar_id}"):
            st.session_state.selected_avatar = avatar_id
```

### 2. Session Storage
Selected avatar is stored in Streamlit session state:

```python
# Session state initialization
if 'selected_avatar' not in st.session_state:
    st.session_state.selected_avatar = 'avatar1'  # Default
```

### 3. Journey Map Display
Avatar is passed to the journey map component and displayed on the path.

---

## Avatar Display Specifications

### Size

**Desktop/Tablet**:
- Width: 160px
- Height: 160px

**Mobile (≤768px)**:
- Width: 120px
- Height: 120px

### Positioning

The avatar is positioned at the **center of the student's skill cards** (middle card position):

```javascript
// Calculate avatar position based on student's skill cards
const numSkills = Math.min(transformedSkills.length, PATH_COORDINATES.length);

if (numSkills > 0) {
    // Position avatar at the middle of the student's skill cards
    const middleCardIndex = Math.floor(numSkills / 2);
    const pathPos = PATH_COORDINATES[middleCardIndex];

    // Center the avatar horizontally on the path
    const avatarPos = {
        x: 50, // Center of the path (50% from left)
        y: pathPos.y // Same vertical position as middle card
    };
    setAvatarPosition(avatarPos);
}
```

**Example**: If a student has 6 skills, the avatar appears at the position of the 3rd card (middle).

---

## Avatar Animation

### Side-to-Side Sway

The avatar has a gentle swaying animation to give it a "floating" feel:

```css
@keyframes avatar-sway {
    0%, 100% {
        transform: translateX(-8px) rotate(-3deg);
    }
    50% {
        transform: translateX(8px) rotate(3deg);
    }
}

.student-avatar {
    animation: avatar-sway 2.5s ease-in-out infinite;
}
```

**Animation Properties**:
- **Movement**: ±8px horizontal (left-right)
- **Rotation**: ±3° tilt (subtle natural sway)
- **Duration**: 2.5 seconds per cycle
- **Easing**: ease-in-out (smooth)
- **Loop**: Infinite

### Visual Representation

```
Animation Cycle (2.5 seconds):

0.0s:  \👧/  (tilted left -3°, -8px)
       ↓
0.6s:   |👧| (center 0°, 0px)
       ↓
1.25s: /👧\ (tilted right +3°, +8px)
       ↓
1.9s:   |👧| (center 0°, 0px)
       ↓
2.5s:  \👧/  (tilted left -3°, -8px) [repeat]
```

---

## CSS Implementation

```css
.student-avatar {
    position: absolute;
    width: 160px;
    height: 160px;
    border-radius: 50%;
    object-fit: cover;
    z-index: 10;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    animation: avatar-sway 2.5s ease-in-out infinite;
    pointer-events: none; /* Don't interfere with map interactions */
}

@media (max-width: 768px) {
    .student-avatar {
        width: 120px;
        height: 120px;
    }
}

@keyframes avatar-sway {
    0%, 100% {
        transform: translateX(-8px) rotate(-3deg);
    }
    50% {
        transform: translateX(8px) rotate(3deg);
    }
}
```

---

## Avatar Positioning Fix History

### Original Issue (Fixed)

**Problem**: Avatar appeared at the top of the map (near the tree) instead of near the student's actual skill cards.

**Cause**: Avatar position was calculated based on an average of all skill levels, which didn't correspond to where cards were placed.

**Solution**: Changed logic to position avatar at the **middle of the student's skill cards**.

### Before Fix (Incorrect)

```javascript
// Old logic - calculated abstract average
const avgProgress = transformedSkills.reduce((sum, s) => {
    const levelMap = { 'Emerging': 0, 'Developing': 1, 'Proficient': 2, 'Advanced': 3 };
    return sum + (levelMap[s.currentLevel] || 0);
}, 0) / transformedSkills.length;

const progressIndex = Math.floor(avgProgress * (PATH_COORDINATES.length / 4));
const pathPos = PATH_COORDINATES[Math.min(progressIndex, PATH_COORDINATES.length - 1)];
```

### After Fix (Correct)

```javascript
// New logic - use middle card position
const numSkills = Math.min(transformedSkills.length, PATH_COORDINATES.length);
const middleCardIndex = Math.floor(numSkills / 2);
const pathPos = PATH_COORDINATES[middleCardIndex];

const avatarPos = {
    x: 50, // Center horizontally
    y: pathPos.y // Middle card vertical position
};
```

---

## Visual Comparison

### Before Fix
```
🌳 ← Tree
│
👧 ← Avatar here (wrong - calculated position)
│
┌────────┐
│ Card 1 │ ← Actual student cards
└────────┘
│
┌────────┐
│ Card 2 │
└────────┘
│
🌸🌼 ← Flowers
```

### After Fix
```
🌳 ← Tree
│
┌────────┐
│ Card 1 │
└────────┘
│
   👧     ← Avatar here (correct - middle of cards)
│
┌────────┐
│ Card 2 │
└────────┘
│
🌸🌼 ← Flowers
```

---

## Avatar Update History

### Update 2 - November 12, 2024 at 15:05
- Updated avatar3 (Robot): File size reduced 559KB → 550KB
- Updated avatar4 (Axolotl): File size reduced 796KB → 811KB (later optimized)
- Deployed latest versions to production

### Update 1 - November 12, 2024 at 14:59
- Replaced all 4 avatars with custom kid-friendly versions
- Increased size from 80×80px to 160×160px (2x larger)
- Changed animation from vertical bounce to side-to-side sway
- Added rotation effect (±3°) for natural movement

---

## File Structure

```
frontend/
├── assets/
│   └── avatars/
│       ├── avatar1.png (Boy - 589KB)
│       ├── avatar2.png (Girl - 656KB)
│       ├── avatar3.png (Robot - 550KB)
│       └── avatar4.png (Axolotl - 811KB)
├── pages/
│   └── Student_00_Home.py (selection interface)
└── components/
    └── road_to_skills_enhanced.html (display logic)
```

---

## Integration with Journey Map

### Data Flow

```
1. Student selects avatar
   ↓
2. Avatar ID stored in session state
   ↓
3. Session state passed to Journey Map page
   ↓
4. Journey Map component loads avatar image
   ↓
5. Avatar positioned at middle card location
   ↓
6. Animation starts (side-to-side sway)
```

### React Component Integration

```javascript
// Load avatar from session data
const selectedAvatar = sessionData.selected_avatar || 'avatar1';
const avatarSrc = `/assets/avatars/${selectedAvatar}.png`;

// Render avatar on map
<img
    src={avatarSrc}
    className="student-avatar"
    alt="Your avatar"
    style={{
        left: `${avatarPosition.x}%`,
        top: `${avatarPosition.y}%`,
        transform: `translate(-50%, -50%)`
    }}
/>
```

---

## Performance Considerations

- **Image Optimization**: Avatar files are already optimized (550-811KB each)
- **Lazy Loading**: Not needed - avatars are core UI elements
- **Animation Performance**: Uses CSS transforms (GPU-accelerated)
- **No Layout Shift**: Avatar size fixed at load time
- **Pointer Events**: Set to `none` to prevent interfering with map drag

---

## Accessibility

- **Alt Text**: All avatar images have descriptive alt text
- **Color Contrast**: Not applicable (decorative images)
- **Keyboard Navigation**: Avatar selection buttons are keyboard accessible
- **Screen Readers**: Avatar selection announces button labels ("Boy", "Girl", etc.)

---

## Future Enhancements (If Needed)

- Avatar customization (color picker, accessories)
- Upload custom avatar images
- More avatar options (animals, fantasy characters)
- Avatar unlocking system (earn new avatars through achievements)
- Avatar poses that change based on skill level
- Multiple avatars per student for different contexts
- Avatar "emotions" reflecting progress (happy, focused, celebrating)
