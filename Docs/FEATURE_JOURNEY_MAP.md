# Student Journey Map Feature

**Feature**: Interactive Road to Skills Journey Map
**Status**: ✅ Complete and Production-Ready
**Location**: [frontend/pages/Student_01_Journey_Map.py](frontend/pages/Student_01_Journey_Map.py)

---

## Overview

An interactive, game-like visualization that transforms student skill progression into an engaging journey map. Students see their progress along a whimsical illustrated path from flowers (beginning) to a tree (mastery), with their chosen avatar positioned at their current level.

---

## Key Features

### 1. **Whimsical Background**
- Hand-drawn illustration featuring:
  - Winding cream-colored path ascending a gentle hill
  - Flowers and mushrooms at the bottom
  - Fluffy clouds, rainbow arc
  - Majestic tree at the peak
- Soft pastel color palette (mint green, sage, cream)

### 2. **View Modes**

#### Overview Mode (All Skills)
- Displays all 17 skills across parallel winding paths
- Color-coded by category:
  - 🧡 Orange/Peach: Social-Emotional Learning (SEL) - 5 skills
  - 💜 Purple: Executive Function (EF) - 6 skills
  - 💚 Teal: 21st Century Skills - 6 skills
- Floating skill cards with hover animations
- Click-to-expand cards showing 3-5 actionable tips

#### Focused Mode (Single Skill Detail)
- Zoomed view of one skill's E→D→P→A progression
- Four milestone cards representing each proficiency level
- Current level highlighted with pulsing glow animation
- Future levels locked (greyed out with padlock)
- Past levels marked as achieved (checkmarks)

### 3. **Visual Progression System**

| Level | Icon | Color | Description |
|-------|------|-------|-------------|
| **Emerging (E)** | 🌱 | Green (#81C784) | "Just beginning - like a little plant!" |
| **Developing (D)** | 🥉 | Bronze (#CD7F32) | "Making progress - Bronze medal!" |
| **Proficient (P)** | 🥈 | Silver (#C0C0C0) | "Doing great - Silver medal!" |
| **Advanced (A)** | 🥇 | Gold (#FFD700) | "Expert level - Gold medal!" |

### 4. **Custom Avatars**
Four kid-friendly avatar options:
- **Boy**: Energetic character with brown curly hair (589KB)
- **Girl**: Cheerful character with orange wavy hair in floral dress (656KB)
- **Robot**: Friendly blue and white robot with headphones (550KB)
- **Axolotl**: Cute pink axolotl (811KB)

Stored in: [frontend/assets/avatars/](frontend/assets/avatars/)

### 5. **Interactive Controls**

#### Zoom Controls
- **Zoom In (+)**: Increase detail view
- **Zoom Out (−)**: See more of the map
- **Fit to Screen (⊡)**: Reset to full view
- Zoom range: 60% (full overview) to 250% (detail view)
- Smooth CSS transitions (0.3s ease)

#### Pan & Drag
- Click-and-drag to navigate anywhere on the map
- Cursor feedback (grab → grabbing)
- Smart boundaries (can't drag outside map)
- Touch gesture support for mobile
- 60fps smooth dragging performance

### 6. **Auto-Focus on Teacher Goals**
- Detects active teacher-assigned targets on page load
- Automatically switches to focused mode for goal skill
- Displays banner: "🎯 Your current goal: [Skill Name] - [Start Level] → [Target Level]"
- Highlights target level with pulsing animation
- Students can manually navigate back to overview

---

## Technical Architecture

### Component Stack
```
┌─────────────────────────────────────┐
│   Streamlit (Python)                │
│   - Student_01_Journey_Map.py       │
│   - View mode toggle (Classic/Road) │
│   - Data fetching from API          │
│   - Session state management        │
└─────────────────────────────────────┘
                ↓
        st.components.v1.html()
                ↓
┌─────────────────────────────────────┐
│   React Component (JavaScript)      │
│   - Self-contained HTML file        │
│   - CDN dependencies (no build)     │
│   - Framer Motion animations        │
│   - Dynamic data injection          │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│   Data Sources                      │
│   - skill_tips.json (68 tip sets)   │
│   - skill_visuals.json (config)     │
│   - Backend API (student data)      │
└─────────────────────────────────────┘
```

### Files
```
frontend/
├── components/
│   └── road_to_skills_enhanced.html     # Main React component
├── assets/
│   ├── avatars/
│   │   ├── avatar1.png (Boy)
│   │   ├── avatar2.png (Girl)
│   │   ├── avatar3.png (Robot)
│   │   └── avatar4.png (Axolotl)
│   └── backgrounds/
│       └── road_map_background.png      # Whimsical path illustration (2.7MB)
├── data/
│   ├── skill_tips.json                  # 17 skills × 4 levels = 68 tip sets
│   └── skill_visuals.json               # Visual configuration
└── pages/
    └── Student_01_Journey_Map.py        # Main page component
```

### Path Positioning System
```javascript
// 12 key positions along the winding path
// Bottom (y=85%) → Top near tree (y=8%)
const PATH_COORDINATES = [
  { x: 30%, y: 85%, level: 'Emerging' },      // Left side, starting point
  { x: 70%, y: 78%, level: 'Emerging' },      // Right side
  { x: 30%, y: 71%, level: 'Emerging' },
  { x: 70%, y: 64%, level: 'Developing' },
  { x: 35%, y: 57%, level: 'Developing' },
  { x: 65%, y: 50%, level: 'Developing' },
  { x: 35%, y: 43%, level: 'Proficient' },
  { x: 65%, y: 36%, level: 'Proficient' },
  { x: 40%, y: 29%, level: 'Proficient' },
  { x: 60%, y: 22%, level: 'Advanced' },
  { x: 45%, y: 15%, level: 'Advanced' },
  { x: 50%, y: 8%, level: 'Advanced' }        // Center near tree (goal!)
];
```

---

## Kid-Friendly Tips Database

Created comprehensive tips library covering:
- **17 skills** × **4 proficiency levels** = **68 unique tip sets**
- Each tip set contains 3-5 actionable suggestions
- Language tailored for ages 9-14
- Derived from professional rubric but simplified

**Example Tips for Self-Awareness - Developing:**
- "Keep a feelings journal - write down how you feel each day and why"
- "Name specific emotions like frustrated, anxious, or excited (not just happy/sad)"
- "Think about one thing you're good at and one thing you want to improve"

---

## Avatar Behavior

The student's chosen avatar:
- Positioned at the center of their current skill cards
- Size: 160×160px (desktop), 120×120px (mobile)
- Side-to-side sway animation (±8px horizontal, ±3° rotation)
- Animation duration: 2.5 seconds
- Drop shadow for depth

---

## Student Experience

### 1. Avatar Selection (Home Page)
Students choose their identity and avatar at [Student_00_Home.py](frontend/pages/Student_00_Home.py)

### 2. Journey Map Toggle
Choose between:
- 📊 Classic Progress Bars (traditional view)
- 🗺️ Road to Skills Map (interactive journey)

### 3. Explore Progress
- See all skills at once or focus on one
- Click cards to reveal growth tips
- Pan and zoom to explore details
- Watch avatar position update as skills improve

---

## Performance

- Auto-zoom animation shows full path for 3 seconds on first load
- Automatically zooms to 120% after intro
- 60fps smooth animations and interactions
- Optimized asset loading (base64 encoded background)
- Responsive design works on all screen sizes

---

## Future Enhancements (If Needed)

- Animated path progress (dotted line showing journey so far)
- Celebration animations when reaching new levels
- Collectible badges or stickers along the path
- Sound effects for interactions (optional, user-controlled)
- Share progress feature (export journey map image)
