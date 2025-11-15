# Data Initialization Guide

## 🎯 Purpose
Load mock data into your deployed Render database to enable:
- 📊 Road to Skills interactive map
- 📈 Skill progress charts
- 🎖️ Badge displays
- 📉 Trend analysis

---

## ✅ Pre-Deployment Checklist

Before running initialization, verify:

1. **Backend is deployed and healthy**
   - URL: https://flourish-skills-backend.onrender.com/health
   - Should return: `{"status":"healthy","database":"connected","openai_configured":true}`

2. **Students exist in database**
   - URL: https://flourish-skills-backend.onrender.com/api/students/
   - Should return: 4 students (Eva, Lucas, Pat, Mia)

3. **Latest code is deployed**
   - Check Render dashboard shows: "Live" status
   - Latest commit should be: "Fix data ingestion blocker"

---

## 📋 What Will Be Loaded

### Data Files (32 total):
- **7 Transcripts** - Group discussions, presentations, debates
- **10 Reflections** - Student journal entries and self-assessments
- **9 Teacher Notes** - Classroom observations and anecdotal records
- **5 Peer Feedback** - Student-to-student evaluations
- **1 Parent Note** - Parent-teacher communication

### AI-Generated Data:
- **~544 Skill Assessments** (32 entries × 17 skills each)
  - Skill level: E (Emerging), D (Developing), P (Proficient), A (Advanced)
  - Confidence score: 0.0 - 1.0
  - Justification: AI-generated reasoning

### Skills Covered (17 total):
**SEL (5):** Self-Awareness, Self-Management, Social Awareness, Relationship Skills, Responsible Decision-Making

**Executive Function (8):** Working Memory, Inhibitory Control, Cognitive Flexibility, Planning & Prioritization, Organization, Task Initiation, Time Management, Metacognition

**21st Century (4):** Critical Thinking, Communication, Collaboration, Creativity & Innovation

---

## 🚀 Initialization Steps

### Step 1: Wait for Backend Redeploy (3-5 minutes)

After pushing the fix, Render auto-deploys the backend:
1. Go to: https://dashboard.render.com/
2. Click on: `flourish-skills-backend`
3. Watch for: Status changes to "Live"
4. Check logs for: "Build successful" message

### Step 2: Access API Documentation

Once backend shows "Live":
1. Open: https://flourish-skills-backend.onrender.com/docs
2. You'll see: Interactive Swagger UI
3. Scroll to: `POST /api/admin/initialize-data`

### Step 3: Execute Initialization

1. **Click** "Try it out" button
2. **Enter** admin_key parameter:
   ```
   flourish-admin-2024
   ```
3. **Click** "Execute" button
4. **Wait** 5-10 minutes (do NOT refresh or close the page)

### Step 4: Monitor Progress

The response will stream back showing:
```json
{
  "success": true,
  "message": "Data initialization completed successfully",
  "output": "Ingesting data for student S001...\n[1/32] Processing transcript_group_discussion...",
  "details": "All students and their data have been loaded into the database"
}
```

**What's happening behind the scenes:**
- Script discovers 32 markdown files in mock_data directory
- For each file:
  - Reads content and metadata
  - Calls `/api/data/ingest` endpoint
  - AI analyzes text against 17 skill rubrics
  - Generates assessments with levels and justifications
  - Stores in database
- Rate limiting: Pauses every 10 entries (5 seconds)
- Total time: 5-10 minutes

---

## ⏱️ Timeline

| Time | Activity |
|------|----------|
| 0:00 | Click "Execute" |
| 0:05 | First entry processed |
| 2:30 | ~15 entries done (rate limit pause) |
| 5:00 | ~30 entries done |
| 8:00 | All 32 entries complete |
| 8:05 | Summary statistics displayed |

---

## 💰 Cost Estimate

**OpenAI API Usage:**
- Model: GPT-4o (via OpenRouter or OpenAI)
- Calls: ~544 assessments
- Cost per assessment: ~$0.015
- **Total: ~$8-9** (one-time cost)

---

## ✅ Verification Steps

### After Initialization Completes:

**1. Check Data Entries**
```
GET https://flourish-skills-backend.onrender.com/api/assessments/student/S001
```
Should return: Array of assessments for Eva

**2. Check Student Progress**
```
GET https://flourish-skills-backend.onrender.com/api/students/S001/progress
```
Should return: Progress metrics with skill counts

**3. Test Frontend**

Visit: https://flourish-skills-frontend.onrender.com/Student_00_Home
1. Select student: "Eva (Grade 7)"
2. Pick an avatar
3. Click: "Start My Journey"
4. Navigate to: "My Journey Map" page

**Expected Result:** 🗺️ Road to Skills map displays with:
- Interactive SVG path
- Clickable skill nodes
- Current progress indicators
- Animations and visual feedback

**4. Test Skill Charts**

Visit Teacher Dashboard:
- https://flourish-skills-frontend.onrender.com
- Click: "Skill Trends"
- Select: Eva
- Should see: Line charts showing skill progression over time

---

## 🐛 Troubleshooting

### Issue: "Unauthorized - Invalid admin key"
**Cause:** Wrong admin key
**Fix:** Use exact key: `flourish-admin-2024`

### Issue: "Data initialization timed out after 5 minutes"
**Cause:** Too many entries or slow OpenAI API
**Fix:**
- Check OpenAI API status
- Try running manually via Render shell
- Increase timeout in main.py (line 114)

### Issue: "Failed to calculate checksum of ref"
**Cause:** mock_data directory not in Docker image
**Fix:**
- Check Dockerfile copies backend/ correctly
- Verify mock_data exists at /app/mock_data/

### Issue: Initialization succeeds but map still empty
**Cause:** Students need skill targets assigned
**Solution:**
- Assessments loaded but targets missing
- Use teacher interface to assign skill targets
- Or run separate script to auto-create targets

### Issue: "Connection refused" or "Cannot connect to backend"
**Cause:** Backend service not running
**Fix:**
- Check Render dashboard - backend should be "Live"
- Wait for deployment to complete
- Check backend logs for startup errors

---

## 📊 Expected Results

### After Successful Initialization:

**Database State:**
- `data_entries`: 32 records
- `assessments`: ~544 records
- `students`: 4 records (already existed)
- `badges`: 0 records (created when targets are met)
- `skill_targets`: 0 records (need to be assigned separately)

**Frontend Features Enabled:**
- ✅ Road to Skills map (if targets are assigned)
- ✅ Skill trend charts
- ✅ Progress dashboards
- ✅ Assessment history
- ✅ Skill level displays
- ⏳ Badge system (after targets are assigned)

---

## 🔄 Re-initialization

If you need to reload data (reset database):

**⚠️ WARNING: This will DELETE all existing data!**

**Option 1: Via Render PostgreSQL Dashboard**
1. Go to Render database dashboard
2. Connect via SQL console
3. Run: `TRUNCATE data_entries, assessments CASCADE;`
4. Re-run initialization endpoint

**Option 2: Full Database Reset**
1. Delete and recreate database in Render
2. Update DATABASE_URL in backend service
3. Re-run initialization

---

## 📝 Notes

- **One-time operation**: Only needs to run once per deployment
- **Idempotent**: Safe to run multiple times (won't duplicate data if entries already exist)
- **Rate Limited**: Respects OpenAI API rate limits
- **Logged**: All activity logged to backend console
- **Reversible**: Can clear database and re-run anytime

---

## 🎉 Success Indicators

You'll know it worked when:
1. ✅ API endpoint returns `"success": true`
2. ✅ Students endpoint shows assessment counts
3. ✅ Frontend displays skill data
4. ✅ Road to Skills map is interactive
5. ✅ Charts show skill progression

---

## 🆘 Need Help?

If initialization fails or map doesn't display:
1. Check backend logs in Render dashboard
2. Check browser console (F12) for frontend errors
3. Verify OPENAI_API_KEY is set correctly
4. Ensure all 4 students exist in database
5. Try running ingestion script manually via Render shell

---

**Last Updated:** November 13, 2025
**Status:** Ready to initialize after backend redeploy completes
