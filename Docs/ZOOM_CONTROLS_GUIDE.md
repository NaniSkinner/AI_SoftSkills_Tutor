# Zoom & Navigation Controls - User Guide

## Overview

The Road to Skills map now includes **zoom and pan controls** so you can view the entire journey at once or zoom in for details!

---

## Zoom Controls (Top-Right Corner)

```
┌──────┐
│  +   │  ← Zoom In (10% increments)
├──────┤
│ 40%  │  ← Current Zoom Level
├──────┤
│  −   │  ← Zoom Out (10% increments)
├──────┤
│  ⊡   │  ← Fit to Screen (reset view)
└──────┘
```

### Button Functions

| Button | Function | Keyboard Shortcut |
|--------|----------|-------------------|
| **+** | Zoom In | Click to enlarge view |
| **−** | Zoom Out | Click to shrink view |
| **⊡** | Fit to Screen | Click to see full map |

---

## How to Use

### 1. **Start View (Default)**
- Map starts at **40% zoom** to show the entire path
- You can see the flowers at bottom and tree at top
- All skill cards visible at once

### 2. **Zoom In for Details**
- Click the **+** button to zoom in
- Max zoom: **150%** (1.5x size)
- Great for reading skill tips

### 3. **Zoom Out for Overview**
- Click the **−** button to zoom out
- Min zoom: **20%** (0.2x size)
- See the big picture of your journey

### 4. **Pan/Drag the Map**
- **Click and drag** anywhere on the map
- Move the view up/down/left/right
- Release to stop dragging
- Cursor changes to "grabbing hand" while dragging

### 5. **Reset View**
- Click the **⊡** button (Fit to Screen)
- Returns to 40% zoom
- Centers the map
- Perfect starting point

---

## Visual Guide

### Zoom Level Examples

```
20% Zoom (Minimum):
┌─────────────────────────────────┐
│                                 │
│              🌳                 │  ← Entire path visible
│              │                  │     Very small
│         👦   │                  │
│              │                  │
│           🌸🌼                  │
│                                 │
└─────────────────────────────────┘


40% Zoom (Default):
┌─────────────────────────────────┐
│         🌳                       │
│         │                        │
│         │                        │  ← Full path visible
│    👦   │                        │     Comfortable size
│         │                        │
│      🌸🌼                        │
└─────────────────────────────────┘


100% Zoom (1:1):
┌─────────────────────────────────┐
│   ┌────────┐                    │
│   │ Skill  │  👦                │  ← Zoomed in
│   │  🥉   │                    │     See details clearly
│   └────────┘                    │     (may need to scroll)
│                                 │
└─────────────────────────────────┘


150% Zoom (Maximum):
┌─────────────────────────────────┐
│  ┌──────────────┐               │
│  │   Skill      │               │  ← Very zoomed in
│  │    🥉       │               │     Read tips easily
│  │  💡 Tips:   │               │     (lots of scrolling)
│  │  1. Keep... │               │
│  └──────────────┘               │
└─────────────────────────────────┘
```

---

## Tips & Tricks

### Best Zoom Levels for Different Tasks

| Task | Recommended Zoom | Why |
|------|------------------|-----|
| **Overview** | 30-40% | See entire journey at once |
| **Reading skill names** | 50-70% | Comfortable reading |
| **Reading tips** | 80-100% | Full detail visible |
| **Finding your avatar** | 40-50% | Easy to spot on path |

### Navigation Tips

1. **Lost?** → Click **⊡** (Fit to Screen) to reset
2. **Can't read text?** → Zoom in with **+**
3. **Want to see everything?** → Zoom out with **−**
4. **Move around?** → Click and drag the map
5. **Cursor stuck?** → Release mouse and click **⊡**

### Mouse/Trackpad Controls

```
Click + Drag:
┌─────────────┐
│    👆       │  ← Click anywhere
│     ↓       │
│    Drag →   │  ← Move mouse while holding
│             │
└─────────────┘
   (Map moves with your mouse)

Release:
┌─────────────┐
│             │  ← Let go of click
│             │
│    Map      │  ← Map stays in place
│   Stays     │
└─────────────┘
```

---

## Accessibility Features

### Keyboard Navigation
- **Tab** through zoom buttons
- **Enter/Space** to activate buttons
- **Esc** to return focus to map

### Touch Support (Mobile/Tablet)
- Pinch to zoom in/out
- Drag with one finger to pan
- Tap zoom buttons

### Screen Reader Support
```html
Zoom In: "Button, Zoom In to 50%"
Zoom Out: "Button, Zoom Out to 30%"
Fit to Screen: "Button, Fit map to screen, reset zoom"
```

---

## Technical Details

### Zoom Range
- **Minimum**: 20% (0.2x scale)
- **Default**: 40% (0.4x scale)
- **Maximum**: 150% (1.5x scale)
- **Increment**: 10% per click

### Pan Limits
- **No hard limits** - can drag anywhere
- **Reset** with Fit to Screen button
- **Smooth transitions** (0.3s ease)

### Performance
- **Hardware accelerated** (CSS transforms)
- **60fps animations**
- **No lag** on modern devices

---

## Troubleshooting

### Problem: Map is too small/large
**Solution**: Click the **⊡** (Fit to Screen) button to reset

### Problem: Can't see the whole path
**Solution**: Zoom out with **−** button or click **⊡**

### Problem: Map is off-center
**Solution**: Click **⊡** to re-center

### Problem: Dragging doesn't work
**Solution**: Make sure you're clicking directly on the map (not buttons)

### Problem: Zoom buttons don't respond
**Solution**: Refresh the page (browser cache issue)

### Problem: Map is stuck while dragging
**Solution**: Click anywhere to release, then click **⊡** to reset

---

## Visual Indicators

### Cursor States

```
Default (Hovering over map):
    👋 (Grab hand)
    "You can click and drag"

Dragging:
    ✊ (Grabbing hand)
    "Currently moving the map"

Hovering over button:
    👆 (Pointer)
    "You can click this button"
```

### Zoom Level Indicator

```
┌──────┐
│ 40%  │  ← Always shows current zoom
└──────┘
   Updates in real-time as you zoom
```

---

## Quick Reference Card

```
╔══════════════════════════════════════════╗
║       ZOOM & NAVIGATION CONTROLS         ║
╠══════════════════════════════════════════╣
║                                          ║
║  [+]  Zoom In     (Max 150%)             ║
║  [−]  Zoom Out    (Min 20%)              ║
║  [⊡]  Fit Screen  (Reset to 40%)         ║
║                                          ║
║  Click + Drag = Move Map                 ║
║                                          ║
║  Default View: 40% zoom                  ║
║  (Shows full path from flowers to tree)  ║
║                                          ║
╚══════════════════════════════════════════╝
```

---

## Examples: Common Scenarios

### Scenario 1: "I want to see my entire journey"
1. Click **⊡** (Fit to Screen)
2. Map resets to 40% zoom
3. Full path visible: flowers → tree

### Scenario 2: "I can't read the skill tips"
1. Click **+** several times (zoom to 80-100%)
2. Click and drag to move to the skill you want
3. Read the expanded tips clearly

### Scenario 3: "Where is my avatar?"
1. Click **⊡** (Fit to Screen)
2. Look for your selected character on the path
3. It's positioned based on your progress

### Scenario 4: "The map is too zoomed in"
1. Click **−** to zoom out
2. Or click **⊡** to reset immediately

### Scenario 5: "I want to explore different skills"
1. Set zoom to 50-70% (click **−** a few times)
2. Click and drag to move around
3. Click skill cards to see tips

---

## Mobile/Tablet Instructions

### Touch Gestures

```
Pinch Out (Zoom In):
   👐  →  👏
  (Spread fingers)

Pinch In (Zoom Out):
   👏  →  👐
  (Bring fingers together)

Drag:
   👆 ────→
  (Swipe one finger)
```

### Tap Targets
- **Zoom buttons**: Large 50px × 50px targets
- **Easy to tap** even on small screens
- **Visual feedback** on tap

---

## Browser Compatibility

| Browser | Zoom | Pan | Touch |
|---------|------|-----|-------|
| Chrome | ✅ | ✅ | ✅ |
| Safari | ✅ | ✅ | ✅ |
| Firefox | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ |
| Mobile Safari | ✅ | ✅ | ✅ |
| Chrome Mobile | ✅ | ✅ | ✅ |

---

**Last Updated**: November 12, 2024
**Feature Version**: 2.1 (Zoom & Pan)

---

For more help, see:
- [Road to Skills Enhanced Guide](ROAD_TO_SKILLS_ENHANCED.md)
- [Visual Guide](ROAD_TO_SKILLS_VISUAL_GUIDE.md)
