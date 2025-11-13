# 🚀 Deployment Guide - Flourish Skills Tracker

## Fastest Method: Railway.app (5 minutes)

### Prerequisites
- GitHub account
- Railway account (free at [railway.app](https://railway.app))

### Step-by-Step Deployment

#### 1. Push Code to GitHub (if not already done)
```bash
git add .
git commit -m "Ready for deployment"
git push origin master
```

#### 2. Deploy Database
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy PostgreSQL"
4. Note the database credentials (will be auto-provided as env vars)

#### 3. Deploy Backend
1. Click "New Service" → "GitHub Repo"
2. Select your repository
3. Railway will detect the Dockerfile automatically
4. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: (auto-linked from PostgreSQL service)
   - `OPENAI_MODEL`: `gpt-4o`
   - `USE_LLM_CONFIDENCE`: `false`
5. Set **Root Directory** to `backend`
6. Click "Deploy"

#### 4. Deploy Frontend
1. Click "New Service" → "GitHub Repo"
2. Select same repository
3. Add environment variable:
   - `BACKEND_URL`: Your backend URL (from step 3)
4. Set **Root Directory** to `frontend`
5. Click "Deploy"

#### 5. Initialize Database
1. Click on your backend service
2. Go to "Settings" → "Deploy"
3. Add **Deploy Command**:
```bash
python -c "from database.connection import init_database; init_database()" && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Your App is Live! 🎉

Frontend URL: `https://your-frontend.railway.app`
Backend API: `https://your-backend.railway.app/docs`

---

## Alternative Method: Render.com (Free, More Steps)

### 1. Create Render Account
Sign up at [render.com](https://render.com)

### 2. Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `flourish-skills-db`
3. Plan: Free
4. Click "Create Database"
5. Copy the **Internal Database URL**

### 3. Deploy Backend
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Settings:
   - **Name**: `flourish-skills-backend`
   - **Root Directory**: `backend`
   - **Environment**: Docker
   - **Plan**: Free
4. Add Environment Variables:
   - `DATABASE_URL`: [Paste Internal Database URL]
   - `OPENAI_API_KEY`: [Your API key]
   - `OPENAI_MODEL`: `gpt-4o`
   - `USE_LLM_CONFIDENCE`: `false`
5. Click "Create Web Service"
6. Copy your backend URL: `https://flourish-skills-backend.onrender.com`

### 4. Deploy Frontend
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Settings:
   - **Name**: `flourish-skills-frontend`
   - **Root Directory**: `frontend`
   - **Environment**: Docker
   - **Plan**: Free
4. Add Environment Variable:
   - `BACKEND_URL`: `https://flourish-skills-backend.onrender.com`
5. Click "Create Web Service"

### 5. Initialize Database Schema
1. Go to your backend service on Render
2. Click "Shell" tab
3. Run:
```bash
python -c "from database.connection import init_database; init_database()"
```

### Your App is Live! 🎉

Access your app at: `https://flourish-skills-frontend.onrender.com`

---

## Alternative Method: Streamlit Community Cloud (Frontend Only)

If you want to use **free hosting for the frontend**:

### 1. Deploy Backend on Railway/Render (see above)

### 2. Deploy Frontend on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Settings:
   - **Main file path**: `frontend/Home.py`
   - **Python version**: 3.11
5. Advanced settings → Secrets:
```toml
[default]
BACKEND_URL = "https://your-backend-url.railway.app"
```
6. Click "Deploy"

Your Streamlit app will be at: `https://your-username-flourish-skills.streamlit.app`

---

## Environment Variables Reference

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
USE_LLM_CONFIDENCE=false
```

### Frontend (.env)
```env
BACKEND_URL=https://your-backend-url.com
```

---

## Troubleshooting

### Database Connection Issues
1. Ensure `DATABASE_URL` uses the **internal** URL (not external) for Railway/Render
2. Format: `postgresql://user:password@host:port/database`

### Frontend Can't Reach Backend
1. Check `BACKEND_URL` doesn't have trailing slash
2. Ensure backend is deployed and running (check /docs endpoint)
3. Check CORS settings in backend if needed

### OpenAI API Errors
1. Verify `OPENAI_API_KEY` is set correctly
2. Check API key has credits remaining
3. Verify model name is correct (`gpt-4o`)

### Database Schema Not Initialized
Run this in your backend shell:
```bash
python -c "from database.connection import init_database; init_database()"
```

---

## Cost Breakdown

### Railway.app
- **Free tier**: $5 credit/month
- Database: ~$1/month
- Backend: ~$2/month
- Frontend: ~$2/month
- **Total**: Free for first month, then ~$5/month

### Render.com
- **Completely Free** (with limitations)
- Services sleep after 15 min inactivity
- Wake up time: ~30 seconds

### Streamlit Cloud + Railway
- Frontend: **FREE** (Streamlit Cloud)
- Backend + DB: ~$3-5/month (Railway)

---

## Recommended Setup for Production

**Best Free Option:**
- Frontend: Streamlit Community Cloud (FREE)
- Backend: Render.com (FREE)
- Database: Render PostgreSQL (FREE)

**Best Paid Option ($5/month):**
- Everything on Railway.app
- Faster, no sleep
- Better performance

---

## Next Steps After Deployment

1. ✅ Test all features in production
2. ✅ Set up custom domain (optional)
3. ✅ Configure monitoring/alerts
4. ✅ Set up automated backups for database
5. ✅ Add authentication (if needed)
6. ✅ Review security settings

## Need Help?

If you encounter issues:
1. Check service logs in Railway/Render dashboard
2. Verify all environment variables are set
3. Test backend API directly at `/docs` endpoint
4. Check GitHub Issues for common problems

---

**Made with 🍵 by Nani Skinner**
