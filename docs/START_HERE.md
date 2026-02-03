# 🚀 START HERE - Complete Setup in 15 Minutes

## Welcome to SME Financial Compass! 🏦

This guide will get you from zero to deployed in **15 minutes**.

---

## ⚡ What You're Getting

A complete AI-powered financial analysis platform with:
- ✅ FastAPI backend (40+ endpoints)
- ✅ OpenRouter LLM (GPT-4/Claude)
- ✅ CSV/Excel/PDF processing
- ✅ Banking integrations (Plaid + Razorpay)
- ✅ Financial calculations & credit scoring
- ✅ Multilingual support (8 languages)
- ✅ FREE deployment (~$5-10/month for LLM only)

---

## 📋 Quick Checklist

### Before You Start (5 minutes)
```
□ Computer with internet
□ Email address for signups
□ GitHub account
□ Credit card for OpenRouter ($5 minimum - this is the only paid service)
```

---

## 🎯 Step-by-Step Guide

### STEP 1: Get Your API Keys (5 minutes)

#### 1A. Supabase (Required - FREE)
```
1. Go to: https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub
4. Click "New project"
5. Name: sme-financial-compass
6. Database Password: (choose strong password)
7. Region: Choose closest to you
8. Click "Create new project"
9. Wait 2 minutes for setup

📋 Save these (Settings → API):
   ✓ Project URL
   ✓ Anon public key
   ✓ Service role key
```

#### 1B. OpenRouter (Required - $5 minimum)
```
1. Go to: https://openrouter.ai
2. Click "Sign Up"
3. Sign up with email
4. Go to "Keys" tab
5. Click "Create Key"
6. Add $5 credits (Settings → Credits)

📋 Save:
   ✓ API Key (starts with sk-or-)
```

#### 1C. Plaid (Optional - FREE Sandbox)
```
1. Go to: https://plaid.com
2. Click "Get API keys"
3. Sign up
4. Use sandbox environment (free)

📋 Save:
   ✓ Client ID
   ✓ Secret (sandbox)
```

---

### STEP 2: Setup Database (2 minutes)

```
1. Go to Supabase Dashboard
2. Click "SQL Editor" (left sidebar)
3. Click "New query"
4. Copy SQL from: backend/app/database.py
   (Look for SCHEMA_SQL = """ ... """)
5. Paste entire SQL
6. Click "Run" (or press Cmd/Ctrl + Enter)
7. Wait for "Success"
8. Check "Table Editor" - you should see 8 tables

✅ Done! Database ready.
```

---

### STEP 3: Deploy Backend (5 minutes)

#### 3A. Push Code to GitHub
```bash
cd sme-financial-compass-main
git init
git add .
git commit -m "Initial deployment"
git branch -M main

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

#### 3B. Deploy on Render.com
```
1. Go to: https://render.com
2. Sign up with GitHub
3. Click "New +"
4. Select "Web Service"
5. Click "Connect" next to your repo
6. Configure:
   
   Name: sme-financial-compass-api
   Region: Oregon (or closest)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free

7. Click "Advanced" → Add Environment Variables:

   SECRET_KEY=<click "Generate" button>
   ENCRYPTION_KEY=<click "Generate" button>
   DEBUG=false
   SUPABASE_URL=<paste your Supabase URL>
   SUPABASE_KEY=<paste your Supabase anon key>
   SUPABASE_SERVICE_KEY=<paste your Supabase service key>
   OPENROUTER_API_KEY=<paste your OpenRouter key>
   
   Optional (if you have them):
   PLAID_CLIENT_ID=<your Plaid client ID>
   PLAID_SECRET=<your Plaid secret>
   PLAID_ENV=sandbox
   RAZORPAY_KEY_ID=<your Razorpay key>
   RAZORPAY_KEY_SECRET=<your Razorpay secret>

8. Click "Create Web Service"
9. Wait 5-8 minutes for deployment
10. Once deployed, copy your URL (looks like: https://your-app.onrender.com)

✅ Backend deployed!
```

---

### STEP 4: Deploy Frontend (3 minutes)

#### 4A. Install Vercel CLI
```bash
npm install -g vercel
```

#### 4B. Create Environment File
```bash
cd sme-financial-compass-main

# Create .env file
cat > .env << 'EOF'
VITE_API_URL=https://your-backend.onrender.com
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your-anon-key
VITE_SUPABASE_PROJECT_ID=your-project-id
EOF

# Replace the values above with your actual values!
```

#### 4C. Deploy
```bash
vercel

# Answer prompts:
→ Set up and deploy: Y
→ Which scope: (choose your account)
→ Link to existing project: N
→ Project name: sme-financial-compass
→ In which directory: ./
→ Want to override settings: N

# After first deploy, add to production:
vercel --prod
```

#### 4D. Add Environment Variables in Dashboard
```
1. Go to: vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable from your .env file
5. Redeploy: vercel --prod
```

✅ Frontend deployed!

---

### STEP 5: Final Configuration (1 minute)

#### Update CORS in Backend
```
1. Go to your GitHub repo
2. Edit: backend/app/config.py
3. Find CORS_ORIGINS list
4. Add your Vercel URL:
   "https://your-app.vercel.app"
5. Commit and push
6. Render will auto-redeploy (wait 2 min)
```

---

## 🎉 YOU'RE DONE! Test Your App

### Test Checklist
```
1. Visit: https://your-app.vercel.app
   ✓ Frontend loads

2. Click "Sign Up"
   ✓ Create account with email/password

3. Create Business Profile
   ✓ Fill in business details

4. Upload a File
   ✓ Try this sample CSV:

Date,Revenue,Expenses
2024-01-01,100000,75000
2024-02-01,120000,80000
2024-03-01,110000,78000

   ✓ File uploads successfully

5. Generate Analysis
   ✓ Click "Analyze"
   ✓ See health score, credit score

6. Try AI Chat
   ✓ Ask: "What are my key financial metrics?"
   ✓ Get AI response

7. Generate Report
   ✓ Download PDF report

✅ All working? Congratulations! 🎊
```

---

## 🆘 Troubleshooting

### Backend Issues

**"Service unavailable"**
```
→ Check Render dashboard for build logs
→ Verify all environment variables are set
→ Check database connection in Supabase
```

**"Database error"**
```
→ Did you run the SQL schema?
→ Check Supabase credentials are correct
→ Verify service key (not just anon key) is set
```

### Frontend Issues

**"Failed to fetch"**
```
→ Check API_URL in .env is correct
→ Verify CORS settings in backend
→ Open browser console for error details
```

**"Authentication failed"**
```
→ Check Supabase keys in frontend .env
→ Verify keys match your Supabase project
```

### LLM Issues

**"OpenRouter error"**
```
→ Verify API key is correct
→ Check you have credits: https://openrouter.ai/credits
→ Try with fallback model
```

---

## 💡 Pro Tips

1. **Save all your API keys** in a password manager
2. **Bookmark your deployments**:
   - Backend: https://your-app.onrender.com/api/docs
   - Frontend: https://your-app.vercel.app
3. **Monitor OpenRouter usage** to control costs
4. **Set up Supabase backups** (Settings → Database → Backups)
5. **Enable 2FA** on all accounts

---

## 📊 What You Have Now

| Feature | Status | URL |
|---------|--------|-----|
| Backend API | ✅ Live | your-app.onrender.com |
| Frontend App | ✅ Live | your-app.vercel.app |
| Database | ✅ Running | Supabase dashboard |
| AI Integration | ✅ Active | OpenRouter |
| API Docs | ✅ Available | /api/docs |

---

## 🚀 Next Steps

### Week 1
- [ ] Test all features thoroughly
- [ ] Invite team members
- [ ] Upload real financial data
- [ ] Generate first real reports

### Week 2
- [ ] Connect banking (Plaid setup)
- [ ] Set up custom domain
- [ ] Enable analytics
- [ ] Configure backups

### Month 1
- [ ] Optimize LLM usage (reduce costs)
- [ ] Add more industry benchmarks
- [ ] Customize for your region
- [ ] Scale up if needed

---

## 📞 Support & Resources

- **API Documentation**: https://your-backend.onrender.com/api/docs
- **Deployment Guide**: See DEPLOYMENT_GUIDE.md
- **Full Setup**: See SETUP_INSTRUCTIONS.md
- **Project Summary**: See PROJECT_SUMMARY.md

---

## ✨ Congratulations!

You now have a **production-ready AI financial platform**! 🎉

**Your app is live at**: https://your-app.vercel.app

Share it with your team and start analyzing your finances!

---

**Total Time**: ~15 minutes
**Total Cost**: ~$5-10/month
**Total Value**: Priceless! 💎

---

*Need help? Check the documentation files or create an issue on GitHub.*

**Happy analyzing! 📊💰**
