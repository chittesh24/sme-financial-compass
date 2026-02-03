# 🚀 Quick Setup Guide - SME Financial Compass

## ⚡ 5-Minute Setup

### Step 1: Get API Keys (3 minutes)

#### 1.1 Supabase (Required)
```bash
1. Visit https://supabase.com
2. Sign up → New Project
3. Copy these values:
   - Project URL (Settings → API)
   - Anon public key
   - Service role key (keep secret!)
```

#### 1.2 OpenRouter (Required)
```bash
1. Visit https://openrouter.ai
2. Sign up → Get API Key
3. Add $5 credits
4. Copy API key
```

#### 1.3 Banking APIs (Optional)
```bash
Plaid: https://plaid.com (Sandbox is free)
Razorpay: https://razorpay.com (For India)
```

---

### Step 2: Setup Database (2 minutes)

```bash
1. Go to Supabase Dashboard
2. Click SQL Editor
3. Copy SQL from backend/app/database.py (lines with CREATE TABLE)
4. Paste and run
5. Verify tables created in Table Editor
```

---

### Step 3: Deploy Backend (5 minutes)

#### Using Render.com (Easiest):

```bash
# 1. Push to GitHub
cd sme-financial-compass-main
git init
git add .
git commit -m "Deploy"
git branch -M main
git remote add origin YOUR_GITHUB_URL
git push -u origin main

# 2. Go to https://render.com
# 3. New Web Service → Connect GitHub repo
# 4. Configure:
   Root Directory: backend
   Build: pip install -r requirements.txt
   Start: uvicorn main:app --host 0.0.0.0 --port $PORT

# 5. Add environment variables:
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
OPENROUTER_API_KEY=your-openrouter-key
DEBUG=false

# 6. Click "Create Web Service"
# 7. Wait ~5 minutes for deployment
```

---

### Step 4: Deploy Frontend (3 minutes)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Create .env file
cd sme-financial-compass-main
cat > .env << EOF
VITE_API_URL=https://your-backend.onrender.com
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_PUBLISHABLE_KEY=your-anon-key
EOF

# 3. Deploy
vercel --prod

# Follow prompts, then add environment variables in Vercel Dashboard
```

---

### Step 5: Test Everything (2 minutes)

```bash
# 1. Visit your Vercel URL
# 2. Sign up with email
# 3. Create business profile
# 4. Upload CSV file
# 5. Generate analysis
# 6. Test AI chat

✅ If all works, you're done!
```

---

## 🔥 Ultra-Quick Local Testing

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn main:app --reload

# Frontend (new terminal)
cd ..
npm install
npm run dev

# Visit http://localhost:8080
```

---

## 📝 Environment Variables Reference

### Backend (.env)
```env
# Required
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx
SUPABASE_SERVICE_KEY=eyJxxx
OPENROUTER_API_KEY=sk-or-xxx
SECRET_KEY=random-32-char-string
ENCRYPTION_KEY=random-32-char-string

# Optional
PLAID_CLIENT_ID=xxx
PLAID_SECRET=xxx
RAZORPAY_KEY_ID=xxx
RAZORPAY_KEY_SECRET=xxx
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJxxx
```

---

## 🆘 Common Issues

### "Module not found" error
```bash
pip install -r requirements.txt
# or
npm install
```

### "Database connection failed"
```bash
# Check Supabase credentials
# Verify SQL schema was executed
```

### "CORS error"
```bash
# Add your frontend URL to backend/app/config.py CORS_ORIGINS
```

### "OpenRouter API error"
```bash
# Check API key is valid
# Verify you have credits
```

---

## 💡 Pro Tips

1. **Use `.env.local` for local development**
2. **Never commit `.env` files**
3. **Test with sandbox APIs first**
4. **Monitor OpenRouter usage**
5. **Set up Supabase backups**

---

## ✅ Deployment Checklist

- [ ] Supabase project created
- [ ] Database schema executed
- [ ] OpenRouter API key obtained
- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Test upload working
- [ ] Test analysis working
- [ ] Test AI chat working
- [ ] Test multilingual support

---

## 🎯 What's Included

✅ FastAPI backend with all services
✅ React frontend (existing)
✅ OpenRouter LLM integration (GPT-4/Claude)
✅ CSV/Excel/PDF processing
✅ Financial calculations & ratios
✅ Credit score & risk assessment
✅ Plaid & Razorpay banking APIs
✅ Multilingual support (8 languages)
✅ JWT authentication & encryption
✅ Supabase database with full schema
✅ Comprehensive API documentation
✅ Free deployment configuration

---

## 📞 Support

**Documentation**: See DEPLOYMENT_GUIDE.md for detailed instructions

**API Docs**: `https://your-backend.onrender.com/api/docs`

**Frontend**: `https://your-app.vercel.app`

---

Happy deploying! 🚀
