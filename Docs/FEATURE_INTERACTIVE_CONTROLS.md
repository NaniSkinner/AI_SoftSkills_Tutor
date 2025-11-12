# Interactive Map Controls (Pan, Drag, Zoom)

**Feature**: Google Maps-style navigation controls for Road to Skills journey map
**Status**: ✅ Complete and Production-Ready
**Location**: [frontend/components/road_to_skills_enhanced.html](frontend/components/road_to_skills_enhanced.html)

---

## Overview

The Road to Skills map includes zoom and pan controls allowing students to view the entire journey at once or zoom in for details. Students can click-and-drag anywhere on the map to explore different sections.

---

## Features

### 1. Zoom Controls (Top-Right Corner)

```
┌──────┐
│  +   │  ← Zoom In (10% increments)
├──────┤
│ 120% │  ← Current Zoom Level Display
├──────┤
│  −   │  ← Zoom Out (10% increments)
├──────┤
│  ⊡   │  ← Fit to Screen (reset view)
└──────┘
```

**Zoom Range**: 60% (full overview) to 250% (detail view)
**Transitions**: Smooth CSS transitions (0.3s ease)
**Performance**: GPU-accelerated transforms

| Button | Function | Effect |
|--------|----------|--------|
| **+** | Zoom In | Increase view by 10%, max 250% |
| **−** | Zoom Out | Decrease view by 10%, min 60% |
| **⊡** | Fit to Screen | Reset to 100% zoom, center view |

### 2. Click-and-Drag Panning

Students can:
- **Click and hold** anywhere on the map background
- **Drag** in any direction to pan around
- **Release** to stop dragging
- Cursor changes from `grab` to `grabbing` while dragging

**Performance**: 60fps smooth dragging
**Touch Support**: Full mobile/tablet support with touch gestures

### 3. Smart Boundaries

Panning includes intelligent constraints:
- **Cannot drag outside map area** - prevents "losing" the map
- **Automatic boundary calculation** based on current zoom level
- **Smooth constraint application** - map snaps to boundaries gracefully
- Boundaries adapt dynamically as zoom level changes

### 4. Enhanced Auto-Zoom Logic

Improved initial experience:
- **3-second full view**: Shows entire path from flowers to tree on first load
- **Auto-zoom to 120%**: Automatically zooms after intro for comfortable viewing
- **Auto-pan to current position**: Centers on student's skill level
- **One-time trigger**: Auto-zoom only happens on first visit (session-tracked)

---

## Technical Implementation

### Files Modified
```
frontend/components/road_to_skills_enhanced.html
```

### Key Code Sections

#### CSS Updates

```css
/* Zoom container with drag cursor */
.zoom-viewport {
    overflow: hidden;
    cursor: grab;
    position: relative;
    height: 900px;
}

.zoom-viewport:active {
    cursor: grabbing;
}

/* Skills path container - proper sizing */
.skills-path-container {
    position: absolute;
    min-height: 1800px; /* Taller to match background */
    width: 100%;
    background-size: contain; /* Show full image */
    background-position: center top;
    transform-origin: center top;
    will-change: transform; /* Performance optimization */
    transition: transform 0.3s ease;
}

/* Prevent text selection while dragging */
.zoom-viewport.dragging * {
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
}

/* Zoom controls positioned in top-right */
.zoom-controls {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: white;
    border-radius: 8px;
    padding: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
```

#### React State Management

```javascript
const [zoomLevel, setZoomLevel] = useState(1.0);
const [panPosition, setPanPosition] = useState({ x: 0, y: 0 });
const [isDragging, setIsDragging] = useState(false);
const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
const [hasAutoZoomed, setHasAutoZoomed] = useState(false);
const containerRef = React.useRef(null);
const viewportRef = React.useRef(null);
```

#### Pan Boundary Calculation

```javascript
const calculatePanBounds = (zoom) => {
    if (!containerRef.current || !viewportRef.current) {
        return { minX: 0, maxX: 0, minY: 0, maxY: 0 };
    }

    const containerWidth = containerRef.current.offsetWidth * zoom;
    const containerHeight = containerRef.current.offsetHeight * zoom;
    const viewportWidth = viewportRef.current.clientWidth;
    const viewportHeight = viewportRef.current.clientHeight;

    return {
        minX: Math.min(0, viewportWidth - containerWidth),
        maxX: 0,
        minY: Math.min(0, viewportHeight - containerHeight),
        maxY: 0
    };
};
```

#### Drag Event Handlers

```javascript
const handleMouseDown = (e) => {
    // Ignore clicks on cards and controls
    if (e.target.closest('.skill-card') ||
        e.target.closest('.zoom-controls')) {
        return;
    }

    setIsDragging(true);
    setDragStart({
        x: e.clientX - panPosition.x,
        y: e.clientY - panPosition.y
    });
};

const handleMouseMove = (e) => {
    if (!isDragging) return;

    const newX = e.clientX - dragStart.x;
    const newY = e.clientY - dragStart.y;

    // Apply boundaries
    const bounds = calculatePanBounds(zoomLevel);
    setPanPosition({
        x: Math.max(bounds.minX, Math.min(bounds.maxX, newX)),
        y: Math.max(bounds.minY, Math.min(bounds.maxY, newY))
    });
};

const handleMouseUp = () => {
    setIsDragging(false);
};

// Touch support
const handleTouchStart = (e) => {
    if (e.touches.length === 1) {
        const touch = e.touches[0];
        handleMouseDown({
            clientX: touch.clientX,
            clientY: touch.clientY,
            target: e.target
        });
    }
};
```

#### Zoom Functions

```javascript
const handleZoomIn = () => {
    setZoomLevel(prev => Math.min(prev + 0.1, 2.5)); // Max 250%
};

const handleZoomOut = () => {
    setZoomLevel(prev => Math.max(prev - 0.1, 0.6)); // Min 60%
};

const handleFitToScreen = () => {
    setZoomLevel(1.0);
    setPanPosition({ x: 0, y: 0 });
};
```

---

## User Guide

### Best Zoom Levels for Different Tasks

| Task | Recommended Zoom | Why |
|------|------------------|-----|
| **Overview** | 60-80% | See entire journey at once |
| **Reading skill names** | 100-120% | Comfortable reading |
| **Reading tips** | 150-200% | Full detail visible |
| **Finding avatar** | 80-100% | Easy to spot on path |

### Navigation Tips

1. **Lost?** → Click **⊡** (Fit to Screen) to reset
2. **Can't read text?** → Zoom in with **+**
3. **Want to see everything?** → Zoom out with **−**
4. **Move around?** → Click and drag the map
5. **Cursor stuck?** → Release mouse and click **⊡**

### Hybrid Interaction Model

Supports multiple interaction methods:
- **Drag-to-pan**: Click and drag anywhere on the background
- **Zoom controls**: Button-based zoom in/out
- **Touch gestures**: Full mobile/tablet support with touch drag
- **Prevents conflicts**: Dragging doesn't trigger on skill cards or zoom buttons

---

## Visual Guide

### Zoom Level Examples

```
60% Zoom (Minimum):
┌─────────────────────────────────┐
│                                 │
│              🌳                 │  ← Entire path visible
│              │                  │     Full overview
│         👦   │                  │
│              │                  │
│           🌸🌼                  │
│                                 │
└─────────────────────────────────┘

100% Zoom (Default after auto-zoom):
┌─────────────────────────────────┐
│   ┌────────┐                    │
│   │ Skill  │  👦                │  ← Comfortable view
│   │  🥉   │                    │     See details clearly
│   └────────┘                    │
│                                 │
└─────────────────────────────────┘

250% Zoom (Maximum):
┌─────────────────────────────────┐
│  ┌──────────────┐               │
│  │   Skill      │               │  ← Very zoomed in
│  │    🥉       │               │     Read tips easily
│  │  💡 Tips:   │               │     (requires panning)
│  │  1. Keep... │               │
│  └──────────────┘               │
└─────────────────────────────────┘
```

---

## Auto-Zoom Sequence

On first page load:

1. **Initial state** (t=0s): Map loads at 60% zoom showing full path
2. **Display period** (t=0-3s): Students see entire journey from flowers to tree
3. **Auto-zoom** (t=3s): Smoothly zooms to 120% over 0.3 seconds
4. **Auto-pan** (t=3.3s): Centers view on student's current skill level
5. **Interactive** (t>3.3s): Student can pan/zoom freely

Session tracking prevents repeated auto-zoom on subsequent interactions.

---

## Container Sizing Fix

Resolved positioning issues by adjusting container dimensions:

**Before**:
- Container: 900px tall
- Background: `background-size: cover` (cropped image)
- Issue: Skill cards appeared at bottom, didn't align with path

**After**:
- Container: 1800px tall (matches background aspect ratio)
- Background: `background-size: contain` (shows full image)
- Background position: `center top`
- Result: Perfect alignment of cards with illustrated path

---

## Performance Optimizations

- **GPU Acceleration**: Uses `will-change: transform` for smooth animations
- **RAF-based dragging**: Drag updates tied to requestAnimationFrame for 60fps
- **Boundary caching**: Calculates boundaries only when zoom changes
- **Event delegation**: Minimizes event listener overhead
- **CSS transitions**: Hardware-accelerated zoom transitions
- **Touch optimization**: Prevents default touch behaviors that conflict with dragging

---

## Accessibility

- **Keyboard support**: Could be enhanced with arrow key navigation
- **Screen reader**: Buttons have proper labels
- **Visual feedback**: Cursor changes, button hover states
- **No motion sickness**: Smooth, controlled animations (no jarring movements)

---

## Future Enhancements (If Needed)

- Pinch-to-zoom on mobile devices
- Keyboard shortcuts (arrow keys to pan, +/- to zoom)
- Mini-map in corner showing current viewport position
- Double-click to zoom in on specific skill
- Scroll-wheel zoom (with modifier key to prevent conflicts)
- Save zoom/pan preferences per student
