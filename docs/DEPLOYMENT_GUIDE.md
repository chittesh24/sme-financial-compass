# SME Financial Compass - Deployment Guide

## 🚀 Complete Deployment Instructions

This guide covers deploying both frontend and backend for **FREE**.

---

## 📋 Prerequisites

### Required API Keys (Get these first):

1. **Supabase** (Database + Auth) - FREE
   - Sign up: https://supabase.com
   - Create new project
   - Get: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`

2. **OpenRouter** (LLM API) - Pay-as-you-go
   - Sign up: https://openrouter.ai
   - Add credits ($5 minimum)
   - Get: `OPENROUTER_API_KEY`

3. **Banking APIs (Optional)**:
   - Plaid (Sandbox FREE): https://plaid.com
   - Razorpay (India): https://razorpay.com

---

## 🗄️ Step 1: Setup Supabase Database

### 1.1 Create Supabase Project
```bash
1. Go to https://supabase.com
2. Click "New Project"
3. Enter project name, password
4. Wait for project to be created (~2 minutes)
```

### 1.2 Run Database Schema
```sql
-- Go to Supabase Dashboard → SQL Editor
-- Copy and paste the SQL from backend/app/database.py (SCHEMA_SQL)
-- Execute the query
```

### 1.3 Get Credentials
```bash
# In Supabase Dashboard → Settings → API
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...
```

---

## 🔧 Step 2: Deploy Backend (FastAPI)

### Option A: Deploy on Render.com (Recommended - FREE)

#### 2.1 Push Code to GitHub
```bash
cd sme-financial-compass-main
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### 2.2 Deploy on Render
```bash
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: sme-financial-compass-api
   - Region: Oregon (US West)
   - Branch: main
   - Root Directory: backend
   - Runtime: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   - Plan: FREE
```

#### 2.3 Add Environment Variables
```bash
# In Render Dashboard → Environment
SECRET_KEY=<generate-random-32-char-string>
ENCRYPTION_KEY=<generate-random-32-char-string>
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-anon-key>
SUPABASE_SERVICE_KEY=<your-supabase-service-key>
OPENROUTER_API_KEY=<your-openrouter-key>
DEBUG=false
```

#### 2.4 Deploy
```bash
Click "Create Web Service"
Wait for deployment (~5-10 minutes)
Your API will be at: https://your-app.onrender.com
```

---

### Option B: Deploy on Railway.app (Alternative - FREE tier)

```bash
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables (same as above)
6. Deploy automatically
```

---

## 🎨 Step 3: Deploy Frontend (React)

### 3.1 Update Frontend Environment

Create `sme-financial-compass-main/.env`:
```env
VITE_API_URL=https://your-backend.onrender.com
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJxxx...
```

### 3.2 Deploy on Vercel (Recommended - FREE)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd sme-financial-compass-main
vercel

# Follow prompts:
# - Set up and deploy: Yes
# - Which scope: Your account
# - Link to existing project: No
# - Project name: sme-financial-compass
# - Directory: ./ (root)
# - Override settings: No

# Add environment variables in Vercel Dashboard
# Deploy to production
vercel --prod
```

### 3.3 Alternative: Deploy on Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod

# Add environment variables in Netlify Dashboard
```

---

## 🔗 Step 4: Connect Frontend to Backend

### 4.1 Update CORS in Backend

Edit `backend/app/config.py`:
```python
CORS_ORIGINS: List[str] = [
    "http://localhost:8080",
    "http://localhost:3000",
    "https://your-app.vercel.app",  # Add your Vercel URL
    "https://*.vercel.app",
    "https://*.netlify.app"
]
```

Redeploy backend after changes.

### 4.2 Test Connection

```bash
# Open your frontend URL
# Test file upload
# Test analysis generation
# Test chat functionality
```

---

## 📊 Step 5: Verify Complete Setup

### Test Checklist:
- [ ] Frontend loads at Vercel URL
- [ ] Backend health check: `https://your-api.onrender.com/api/health`
- [ ] User can sign up/login
- [ ] File upload works (CSV/Excel/PDF)
- [ ] Financial analysis generates
- [ ] AI chat responds
- [ ] Reports generate
- [ ] Multilingual translation works

---

## 🎯 Quick Deploy Commands (Summary)

```bash
# 1. Setup Supabase database (run SQL schema)

# 2. Deploy Backend
cd backend
git init && git add . && git commit -m "Backend"
# Push to GitHub, deploy on Render

# 3. Deploy Frontend
cd ..
npm install
vercel --prod

# 4. Add environment variables in both platforms

# 5. Test: Visit your Vercel URL
```

---

## 💰 Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| Supabase | Free Tier | $0/month |
| Render | Free Tier | $0/month |
| Vercel | Hobby | $0/month |
| OpenRouter | Pay-as-you-go | ~$5-10/month |
| Plaid (Sandbox) | Free | $0 |
| **Total** | | **~$5-10/month** |

---

## 🔐 Security Checklist

- [ ] Change all default secrets
- [ ] Enable Supabase Row Level Security (RLS)
- [ ] Use HTTPS only (automatic on Vercel/Render)
- [ ] Restrict CORS to your domains
- [ ] Don't commit `.env` files
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting in production

---

## 🐛 Troubleshooting

### Backend not starting:
```bash
# Check logs in Render dashboard
# Verify all environment variables are set
# Test locally: uvicorn main:app --reload
```

### Frontend can't connect to backend:
```bash
# Check CORS settings in backend
# Verify API_URL in frontend .env
# Check browser console for errors
```

### Database errors:
```bash
# Verify Supabase credentials
# Check if SQL schema was executed
# Test connection in Supabase SQL Editor
```

### LLM not responding:
```bash
# Verify OpenRouter API key
# Check API credits balance
# Test with curl:
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

---

## 📚 Additional Resources

- [Supabase Docs](https://supabase.com/docs)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)

---

## 🎉 Success!

Your SME Financial Compass is now deployed and ready to use!

**Frontend URL**: https://your-app.vercel.app
**Backend API**: https://your-api.onrender.com
**API Docs**: https://your-api.onrender.com/api/docs

---

## 🚀 Next Steps

1. **Test all features thoroughly**
2. **Set up monitoring** (Sentry, LogRocket)
3. **Add custom domain** (optional)
4. **Configure backups** (Supabase automatic)
5. **Set up CI/CD** (GitHub Actions)

---

Need help? Check the troubleshooting section or open an issue!
