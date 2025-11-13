# 🚀 Quick Start - Deploy in 5 Minutes

## The FASTEST Way to Deploy

### Option 1: Railway.app (Recommended - Easiest)

1. **Push to GitHub** (if not done):
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push
   ```

2. **Go to Railway.app**:
   - Visit: https://railway.app
   - Click "Login with GitHub"

3. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Add PostgreSQL**:
   - Click "New"
   - Select "Database" → "Add PostgreSQL"
   - Database will auto-configure

5. **Configure Backend**:
   - Click on the backend service
   - Go to "Variables" tab
   - Add these variables:
     ```
     OPENAI_API_KEY=your-api-key-here
     OPENAI_MODEL=gpt-4o
     USE_LLM_CONFIDENCE=false
     ```
   - Railway automatically links DATABASE_URL from PostgreSQL

6. **Configure Frontend**:
   - Click "New" → "GitHub Repo" (same repo)
   - Click on service → "Settings"
   - Set "Root Directory" to `frontend`
   - Go to "Variables" tab
   - Add: `BACKEND_URL=` (paste your backend URL from step 5)

7. **Done!** 🎉
   - Frontend URL will be shown in the deployment
   - Usually: `https://your-app.up.railway.app`

**Total Time: 5 minutes**
**Cost: FREE for first $5/month, then ~$5/month**

---

### Option 2: Streamlit Cloud + Railway Backend (100% FREE)

**Backend (Railway):**
1. Follow steps 1-5 above for Railway
2. Deploy only the backend + database

**Frontend (Streamlit Cloud):**
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect GitHub
4. Set:
   - Repository: your-repo
   - Branch: master
   - Main file: `frontend/Home.py`
5. Click "Advanced settings"
6. Add secrets:
   ```toml
   BACKEND_URL = "your-railway-backend-url"
   ```
7. Click "Deploy"

**Total Time: 7 minutes**
**Cost: 100% FREE**

---

### Option 3: All on Render.com (100% FREE)

1. **Push to GitHub** (if not done)

2. **Create Render Account**: https://render.com

3. **Create Database**:
   - New → PostgreSQL
   - Name: `flourish-db`
   - Click "Create"
   - Copy "Internal Database URL"

4. **Deploy Backend**:
   - New → Web Service
   - Connect GitHub repo
   - Name: `flourish-backend`
   - Root Directory: `backend`
   - Environment: Docker
   - Add env vars:
     ```
     DATABASE_URL=(paste internal URL)
     OPENAI_API_KEY=your-key
     OPENAI_MODEL=gpt-4o
     USE_LLM_CONFIDENCE=false
     ```
   - Create

5. **Deploy Frontend**:
   - New → Web Service
   - Same repo
   - Name: `flourish-frontend`
   - Root Directory: `frontend`
   - Environment: Docker
   - Add env var:
     ```
     BACKEND_URL=your-backend-url
     ```
   - Create

6. **Initialize DB** (in backend shell):
   ```bash
   python -c "from database.connection import init_database; init_database()"
   ```

**Total Time: 10 minutes**
**Cost: 100% FREE (services sleep after 15min inactivity)**

---

## Which Option Should You Choose?

| Option | Cost | Speed | Reliability | Best For |
|--------|------|-------|-------------|----------|
| **Railway** | ~$5/mo | ⚡⚡⚡ | ⭐⭐⭐ | Production use |
| **Streamlit + Railway** | FREE | ⚡⚡ | ⭐⭐⭐ | Most users |
| **Render** | FREE | ⚡ | ⭐⭐ | Testing/Demo |

**Recommendation**: Start with **Streamlit Cloud + Railway Backend** (FREE + Fast)

---

## After Deployment Checklist

- [ ] Test the app - visit your frontend URL
- [ ] Check backend health - visit `your-backend-url/docs`
- [ ] Run database initialization if needed
- [ ] Add your OpenAI API key
- [ ] Test with sample data
- [ ] Share with users!

---

## Troubleshooting

**"Can't connect to backend"**
→ Check BACKEND_URL in frontend has no trailing `/`

**"Database error"**
→ Run init script: `python -c "from database.connection import init_database; init_database()"`

**"OpenAI error"**
→ Verify API key is set and has credits

**Need help?**
→ Check logs in Railway/Render dashboard

---

## Your URLs

After deployment, save these:

- **Frontend**: `https://_____.app`
- **Backend API**: `https://_____.app/docs`
- **Database**: (internal only, no public access needed)

---

**Ready to deploy? Pick an option above and let's go! 🚀**
