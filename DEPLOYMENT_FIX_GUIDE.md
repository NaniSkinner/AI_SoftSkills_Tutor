# Deployment Fix Guide - Data Loading Issue

## Problem Summary
The production deployment on Render is not showing any student data because the database has not been populated with initial data. This guide provides step-by-step instructions to fix the issue.

## What Was Changed

### 1. Build Configuration Updates
- **File**: [render.yaml](render.yaml)
  - Changed `dockerContext: ./backend` to `dockerContext: .` (line 8)
  - Added `ALLOWED_ORIGINS` environment variable for CORS (line 21-22)
  - Added `ADMIN_INIT_KEY` environment variable for secure initialization (line 23-24)

### 2. Backend Docker Configuration
- **File**: [backend/Dockerfile](backend/Dockerfile)
  - Updated to copy from `backend/` directory explicitly (line 15)
  - Added explicit copy of `mock_data/` from root directory (line 18)
  - Updated requirements path to `backend/requirements.txt` (line 11)

### 3. Data Initialization Endpoint
- **File**: [backend/main.py](backend/main.py)
  - Added new POST endpoint `/api/admin/initialize-data` (lines 82-144)
  - This endpoint runs the data ingestion script with admin key protection
  - Updated CORS configuration to use environment variable (lines 33-38)

### 4. Improved Error Logging
- **File**: [frontend/utils/api_client.py](frontend/utils/api_client.py)
  - Enhanced `get_students()` method with detailed logging (lines 44-60)
  - Added backend URL logging
  - Added response status and error details logging

- **File**: [frontend/pages/Student_00_Home.py](frontend/pages/Student_00_Home.py)
  - Added backend URL verification logging (lines 184-186)

## Deployment Steps

### Step 1: Commit and Push Changes
```bash
git add render.yaml backend/Dockerfile backend/main.py frontend/utils/api_client.py frontend/pages/Student_00_Home.py DEPLOYMENT_FIX_GUIDE.md
git commit -m "Fix data loading issue on Render deployment

- Update docker context to include mock_data directory
- Add data initialization endpoint with admin protection
- Improve error logging for debugging
- Update CORS configuration for production"
git push origin master
```

### Step 2: Wait for Render Auto-Deploy
- Render will automatically detect the changes and start a new deployment
- Go to your Render Dashboard: https://dashboard.render.com/
- Navigate to `flourish-skills-backend` service
- Watch the deployment logs - it should take 3-5 minutes

### Step 3: Initialize the Database

Once the backend is deployed successfully, you need to run the data initialization **one time**:

#### Option A: Using the API Docs Interface (Recommended)
1. Open your backend API docs: `https://flourish-skills-backend.onrender.com/docs`
2. Scroll down to find the `POST /api/admin/initialize-data` endpoint
3. Click "Try it out"
4. Enter the admin key: `flourish-admin-2024`
5. Click "Execute"
6. Wait for the response (may take 1-2 minutes)
7. You should see a success message with output from the ingestion script

#### Option B: Using curl
```bash
curl -X POST "https://flourish-skills-backend.onrender.com/api/admin/initialize-data?admin_key=flourish-admin-2024"
```

### Step 4: Verify Data Was Loaded

1. **Check the API directly**:
   - Go to: `https://flourish-skills-backend.onrender.com/docs`
   - Try the `GET /api/students/` endpoint
   - You should see 4 students returned: Eva, Lucas, Pat, and Mia

2. **Check the frontend**:
   - Go to your frontend URL: `https://flourish-skills-frontend.onrender.com`
   - The student home page should now show 4 students in the dropdown
   - You should see the Road to Skills map

### Step 5: Test the Application

1. Select a student from the dropdown (e.g., Eva)
2. Pick an avatar
3. Click "Start My Journey"
4. Navigate through different pages:
   - Journey Map should display the interactive road map
   - Skills Progress should show skill data
   - Badges should display earned badges

## Troubleshooting

### If the initialization endpoint fails:

1. **Check the backend logs**:
   - Go to Render Dashboard > flourish-skills-backend > Logs
   - Look for error messages during initialization

2. **Common issues**:
   - **"mock_data directory not found"**: The Docker build may have failed to copy the directory. Check build logs.
   - **"Database connection error"**: Ensure the PostgreSQL database is running and connected.
   - **"Timeout error"**: The ingestion script is taking too long. You may need to run it manually via shell.

### If data still doesn't show after initialization:

1. **Check backend logs** for API errors when frontend tries to fetch students
2. **Check frontend logs** in browser console (F12)
3. **Verify BACKEND_URL** environment variable is set correctly in frontend service:
   - Should be: `https://flourish-skills-backend.onrender.com`

### Manual Data Loading (Fallback):

If the initialization endpoint doesn't work, you can run the script manually:

1. Go to Render Dashboard > flourish-skills-backend > Shell
2. Run:
   ```bash
   cd /app
   python scripts/ingest_all_data.py --backend-url http://localhost:8000
   ```
3. Wait for completion (shows progress for each student)

## Environment Variables to Verify

### Backend Service (`flourish-skills-backend`):
- `DATABASE_URL` - Auto-set by Render from database connection
- `OPENAI_API_KEY` - Your OpenAI or OpenRouter API key
- `OPENAI_MODEL` - `gpt-4o`
- `USE_LLM_CONFIDENCE` - `false`
- `ALLOWED_ORIGINS` - `https://flourish-skills-frontend.onrender.com,*`
- `ADMIN_INIT_KEY` - `flourish-admin-2024`

### Frontend Service (`flourish-skills-frontend`):
- `BACKEND_URL` - Auto-set from backend service external URL

## Success Indicators

After completing all steps, you should see:
1. ✅ Backend health check returns "healthy" status
2. ✅ GET /api/students/ returns 4 students
3. ✅ Frontend loads without errors
4. ✅ Student dropdown shows 4 names
5. ✅ Journey map displays correctly
6. ✅ Skills and badges data loads for each student

## Security Note

The `ADMIN_INIT_KEY` is currently set to `flourish-admin-2024` for initial setup. For production use, you should:
1. Change this to a strong, random key
2. Update the environment variable in Render
3. Store it securely (password manager or secrets vault)

## Future Deployments

After the initial data load, you only need to run the initialization endpoint again if:
- You want to reset all data to the original mock data
- You've added new students to the mock_data directory
- The database was wiped or recreated

For normal code updates, just push to git and Render will auto-deploy. The data will persist in the PostgreSQL database.

## Contact

If you encounter any issues not covered in this guide, check:
1. Render deployment logs (both backend and frontend)
2. Browser console logs (F12 > Console)
3. Backend API documentation at `/docs` endpoint
