# Quick Test Guide - Pan & Drag Road Map

## 🚀 How to Test the New Features

### Step 1: Access the Dashboard
1. Open your browser to: http://localhost:8501/Student_00_Home
2. Select a student name from the dropdown
3. Choose any avatar (Boy, Girl, Robot, or Axolotl)
4. Click "🚀 Start My Journey!"

### Step 2: View the Road Map
1. Toggle to "🗺️ Road to Skills Map" (if not already selected)
2. **WAIT 3 SECONDS** - You'll see the auto-zoom animation:
   - First: Full path visible (flowers to tree)
   - Then: Zooms in and centers on your current level

### Step 3: Test Drag-to-Pan
1. **Click and hold** anywhere on the map background
2. **Drag** in any direction (up/down/left/right)
3. **Release** - the map stays where you left it
4. Try to **drag beyond the edges** - it should stop (boundaries work!)

### Step 4: Test Zoom with Pan
1. Click the **+ button** (top right) - zoom in
2. Click the **− button** - zoom out
3. Click the **⊡ button** - fit to screen (resets everything)
4. While zoomed in, **drag around** - should work smoothly

### Step 5: Test Card Interaction
1. **Drag the map** to a different position
2. **Click on a skill card** - tips should expand (not drag the map)
3. Click the card again - tips collapse
4. **Drag the map** - cards move with it (as expected)

---

## ✅ What to Look For

### Good Behavior
- ✅ Smooth dragging (no lag or stuttering)
- ✅ Cursor changes to "grabbing hand" while dragging
- ✅ Cannot drag map completely off screen
- ✅ Cards stay aligned with background path
- ✅ Clicking cards doesn't start dragging
- ✅ Auto-zoom happens once (not every time you pan)

### Issues to Report
- ❌ Map doesn't drag at all
- ❌ Cards positioned incorrectly (not next to path)
- ❌ Can drag map into empty space (boundaries not working)
- ❌ Clicking cards starts dragging instead of expanding
- ❌ Performance is choppy or slow
- ❌ Background image not visible

---

## 🔧 Quick Fixes

### "I don't see the background image"
- Refresh the page (Cmd+R or Ctrl+R)
- Check if Docker containers are running: `docker ps`
- Restart frontend: `docker restart ai_ms_softskills-frontend-1`

### "Dragging is laggy"
- Check CPU usage (Activity Monitor / Task Manager)
- Close other browser tabs
- Try a different browser (Chrome usually fastest)

### "Cards are in wrong positions"
- This is expected if you haven't set the PATH_COORDINATES to match your background
- See [PAN_DRAG_IMPLEMENTATION.md](./PAN_DRAG_IMPLEMENTATION.md) for coordinate adjustment

---

## 📱 Mobile Testing (Optional)

If you have a tablet or phone:
1. Connect to the same network as your computer
2. Find your computer's IP address: `ifconfig | grep inet`
3. Open browser on mobile: `http://YOUR_IP:8501/Student_00_Home`
4. Test touch drag gestures (single finger)

---

## 🎯 Key Features Implemented

| Feature | Status | Description |
|---------|--------|-------------|
| **Drag-to-pan** | ✅ | Click and drag anywhere on map |
| **Zoom controls** | ✅ | +/−/⊡ buttons to zoom in/out/reset |
| **Smart boundaries** | ✅ | Cannot drag map outside visible area |
| **Auto-zoom** | ✅ | 3-second preview, then focus on current level |
| **Touch gestures** | ✅ | Mobile/tablet drag support |
| **Card interaction** | ✅ | Click cards to expand tips (no drag) |
| **Performance** | ✅ | 60fps smooth animations |

---

## 📸 What You Should See

### Initial View (0-3 seconds)
```
┌─────────────────────────────────────┐
│           🗺️ Your Road to Skills   │
├─────────────────────────────────────┤
│                                     │
│            🌳  ← Tree (top)        │
│            │                        │
│        [Skill Cards]                │
│            │                        │
│          👧 ← Your avatar          │
│            │                        │
│        [Skill Cards]                │
│            │                        │
│         🌸🌼  ← Flowers (bottom)   │
│                                     │
│  [+] [80%] [−] [⊡] ← Zoom controls │
└─────────────────────────────────────┘
```

### After Auto-Zoom (after 3 seconds)
```
┌─────────────────────────────────────┐
│           🗺️ Your Road to Skills   │
├─────────────────────────────────────┤
│                                     │
│     ┌────────┐                     │
│     │ Skill  │  👧 ← YOU ARE HERE │
│     │  🥉   │                     │
│     └────────┘                     │
│                                     │
│     ┌────────┐                     │
│     │ Skill  │                     │
│     │  🥈   │                     │
│     └────────┘                     │
│                                     │
│  [+] [120%] [−] [⊡] ← Zoomed in   │
└─────────────────────────────────────┘
```

### While Dragging
```
Cursor: ✊ (grabbing hand)
Map: Moves smoothly with your mouse/finger
Cards: Move with the map (stay in position)
```

---

## 🐛 Reporting Issues

If you find bugs, note:
1. **What you did**: "I clicked and dragged up"
2. **What happened**: "Map disappeared"
3. **What you expected**: "Map should stop at boundary"
4. **Browser**: Chrome / Safari / Firefox
5. **Screenshot**: If possible

Send to Claude or file in project issues!

---

**Happy Testing!** 🎉
