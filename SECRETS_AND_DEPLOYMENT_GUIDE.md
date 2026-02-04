# 🔐 Secrets Management & Deployment Impact Guide

## 📋 Table of Contents
1. [Public vs Secret Keys](#public-vs-secret-keys)
2. [Environment Variables Breakdown](#environment-variables-breakdown)
3. [Deployment Impact](#deployment-impact)
4. [Security Best Practices](#security-best-practices)
5. [How to Configure](#how-to-configure)

---

## 🔑 Public vs Secret Keys

### ✅ **PUBLIC KEYS** (Safe to expose in frontend/browser)

These keys are prefixed with `VITE_` and are embedded in your frontend JavaScript bundle. Anyone can view them by inspecting your website's source code.

| Variable | Type | Safe to Expose? | Used In |
|----------|------|-----------------|---------|
| `VITE_SUPABASE_URL` | Public | ✅ YES | Frontend |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | Public (Anon Key) | ✅ YES | Frontend |
| `VITE_API_URL` | Public | ✅ YES | Frontend |

**Why are these safe?**
- Supabase Anon Key has Row Level Security (RLS) protection
- Users can only access data they're authorized to see
- These keys are meant to be public-facing

---

### ⚠️ **SECRET KEYS** (NEVER expose to frontend/browser)

These keys have admin privileges and MUST be kept secret on the backend only.

| Variable | Type | Risk Level | Used In |
|----------|------|------------|---------|
| `SECRET_KEY` | JWT Secret | 🔴 CRITICAL | Backend |
| `ENCRYPTION_KEY` | Encryption | 🔴 CRITICAL | Backend |
| `SUPABASE_SERVICE_KEY` | Admin Key | 🔴 CRITICAL | Backend |
| `DATABASE_URL` | DB Connection | 🔴 CRITICAL | Backend |
| `OPENROUTER_API_KEY` | API Key | 🟠 HIGH | Backend |
| `PLAID_SECRET` | Banking API | 🟠 HIGH | Backend |
| `RAZORPAY_KEY_SECRET` | Payment API | 🟠 HIGH | Backend |

**Why are these dangerous if exposed?**
- Full database access without restrictions
- Can bypass all security rules
- Cost money if abused (API keys)
- Can access/modify/delete ANY user's data

---

## 📦 Environment Variables Breakdown

### **Frontend Variables** (`.env` in `financial-compass/`)

```env
# ✅ PUBLIC - These are embedded in your frontend build
VITE_SUPABASE_URL=https://evbijbadhkeorxtkymxk.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJhbGc...your-anon-key
VITE_API_URL=http://localhost:8000  # or your deployed backend URL
```

**⚠️ NEVER add secrets here!** Anything with `VITE_` prefix becomes public.

### **Backend Variables** (`backend/.env`)

```env
# 🔴 SECRETS - Never commit these to git!
SECRET_KEY=min-32-char-random-string-for-jwt-signing
ENCRYPTION_KEY=another-random-string-for-data-encryption

# Database (Admin Access)
SUPABASE_URL=https://evbijbadhkeorxtkymxk.supabase.co
SUPABASE_KEY=your-anon-key  # Used for some operations
SUPABASE_SERVICE_KEY=your-service-role-key-KEEP-SECRET
DATABASE_URL=postgresql://postgres:[password]@db.xxx.supabase.co:5432/postgres

# API Keys
OPENROUTER_API_KEY=sk-or-v1-...
PLAID_CLIENT_ID=your-client-id
PLAID_SECRET=your-plaid-secret
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=your-razorpay-secret

# Configuration
DEBUG=false
PORT=8000
```

---

## 🚀 Deployment Impact

### **Frontend Deployment** (Vercel/Netlify)

**What to add as secrets:**
- Nothing! Frontend variables are public by design
- Add environment variables in Vercel/Netlify dashboard:
  ```
  VITE_SUPABASE_URL=https://evbijbadhkeorxtkymxk.supabase.co
  VITE_SUPABASE_PUBLISHABLE_KEY=eyJ...
  VITE_API_URL=https://your-backend.railway.app
  ```

**Impact:**
- ✅ No security risk - these are meant to be public
- ✅ Can be committed to git (already in `.env`)
- ⚠️ Update `VITE_API_URL` to point to deployed backend

### **Backend Deployment** (Railway/Render/Heroku)

**What to add as secrets:**
- ⚠️ ALL backend environment variables are secrets
- Add these in your platform's secret/environment variable manager:

**Railway:**
1. Go to your service → Variables tab
2. Add each variable from `backend/.env.example`
3. Railway automatically secures these

**Render:**
1. Go to Environment → Environment Variables
2. Mark sensitive ones as "Secret"
3. Add all backend variables

**Vercel (Serverless Functions):**
1. Settings → Environment Variables
2. Mark as "Sensitive" (hidden in logs)
3. Add all backend secrets

**Impact of adding secrets:**
- ✅ **Required for functionality** - app won't work without them
- ✅ **Enables features:**
  - `SUPABASE_SERVICE_KEY` → Database access, authentication
  - `OPENROUTER_API_KEY` → AI insights, recommendations
  - `PLAID_SECRET` → Banking integration
  - `RAZORPAY_KEY_SECRET` → Payment processing
- ⚠️ **Cost implications:**
  - API keys can incur charges if abused
  - Always set rate limits and usage alerts
- 🔒 **Security enhanced** - secrets stored securely by platform

---

## 🛡️ Security Best Practices

### 1. **Never Commit Secrets to Git**
```bash
# ✅ These files are in .gitignore
financial-compass/.env
financial-compass/backend/.env

# ❌ Never commit these
.env
*.env
!.env.example  # Only example files are OK
```

### 2. **Generate Strong Secrets**
```bash
# Generate SECRET_KEY (32+ characters)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use this online (trusted):
# https://generate-secret.vercel.app/32
```

### 3. **Rotate Keys Regularly**
- Change `SECRET_KEY` every 90 days
- Rotate API keys if you suspect exposure
- Update `SUPABASE_SERVICE_KEY` if leaked

### 4. **Use Different Keys for Environments**
```
Development:  Different set of keys
Staging:      Different set of keys
Production:   Different set of keys (most secure)
```

### 5. **Monitor API Usage**
- Set up billing alerts on OpenRouter, Plaid, Razorpay
- Monitor Supabase auth requests
- Check for unusual patterns

---

## 🔧 How to Configure

### **Step 1: Get Your Supabase Keys**

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project: `evbijbadhkeorxtkymxk`
3. Go to Settings → API
4. Copy these keys:
   - **Anon/Public Key** → `VITE_SUPABASE_PUBLISHABLE_KEY` (frontend)
   - **Service Role Key** → `SUPABASE_SERVICE_KEY` (backend) ⚠️ SECRET!
   - **URL** → Both `VITE_SUPABASE_URL` and `SUPABASE_URL`

### **Step 2: Configure Email Confirmation**

**Option A: Disable for Development**
1. Supabase Dashboard → Authentication → Settings
2. Turn OFF "Enable email confirmations"
3. Users can login immediately after signup

**Option B: Enable with Email Service**
1. Supabase Dashboard → Authentication → Settings
2. Turn ON "Enable email confirmations"
3. Configure email templates in Email Templates section
4. Update redirect URL to your domain
5. SMTP settings (optional - Supabase provides default email)

### **Step 3: Create Environment Files**

```bash
# Frontend
cd financial-compass
cp .env.example .env
# Edit .env and add your Supabase keys

# Backend
cd backend
cp .env.example .env
# Edit .env and add ALL secret keys
```

### **Step 4: Deploy with Secrets**

**Frontend (Vercel):**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy with environment variables
vercel --prod
# Vercel will prompt for environment variables
# Or add them in Vercel dashboard: Settings → Environment Variables
```

**Backend (Railway):**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and init
railway login
railway init

# Add environment variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set SUPABASE_SERVICE_KEY="your-service-key"
# ... add all other variables

# Deploy
railway up
```

---

## 📊 Deployment Checklist

### Frontend Deployment
- [ ] Add `VITE_SUPABASE_URL`
- [ ] Add `VITE_SUPABASE_PUBLISHABLE_KEY`
- [ ] Update `VITE_API_URL` to backend URL
- [ ] Test signup/login flow
- [ ] Verify API calls to backend work

### Backend Deployment
- [ ] Add `SECRET_KEY` (32+ characters)
- [ ] Add `ENCRYPTION_KEY`
- [ ] Add `SUPABASE_URL`
- [ ] Add `SUPABASE_SERVICE_KEY` ⚠️
- [ ] Add `OPENROUTER_API_KEY` (for AI features)
- [ ] Add `PLAID_SECRET` (for banking)
- [ ] Add `RAZORPAY_KEY_SECRET` (for payments)
- [ ] Set `DEBUG=false`
- [ ] Configure CORS origins to include frontend URL
- [ ] Test health endpoint: `/api/health`
- [ ] Test authentication endpoints

### Security Verification
- [ ] `.env` files are in `.gitignore`
- [ ] No secrets in git history
- [ ] Secrets marked as "hidden" in deployment platform
- [ ] Row Level Security enabled in Supabase
- [ ] Rate limiting configured (if applicable)
- [ ] Monitoring/alerts set up for API usage

---

## 🆘 Troubleshooting

### "Unable to receive confirmation email"
1. Check Supabase Dashboard → Logs for email delivery errors
2. Verify email confirmation is enabled
3. Check spam folder
4. **Quick fix:** Disable email confirmation in Supabase settings

### "Backend returns 401 Unauthorized"
1. Verify `SUPABASE_SERVICE_KEY` is set in backend
2. Check backend logs for authentication errors
3. Ensure frontend `VITE_API_URL` points to correct backend

### "Cannot logout"
1. Clear browser localStorage manually: `localStorage.clear()`
2. Check browser console for errors
3. Verify logout endpoint works: `POST /api/auth/logout`

---

## 🎯 Summary

### Which Keys Can Be Public?
✅ **VITE_SUPABASE_URL** - Yes (public)
✅ **VITE_SUPABASE_PUBLISHABLE_KEY** - Yes (anon key, RLS protected)
✅ **VITE_API_URL** - Yes (just a URL)

### Which Keys MUST Be Secret?
🔴 **SUPABASE_SERVICE_KEY** - Has admin access to database
🔴 **SECRET_KEY** - Used to sign JWT tokens
🔴 **ENCRYPTION_KEY** - Encrypts sensitive data
🔴 **OPENROUTER_API_KEY** - Costs money if exposed
🔴 **PLAID_SECRET** - Banking data access
🔴 **RAZORPAY_KEY_SECRET** - Payment processing

### Deployment Impact
- **Frontend**: No secrets, safe to deploy anywhere
- **Backend**: ALL variables are secrets, must be stored securely
- **Cost**: API keys can incur charges if leaked/abused
- **Security**: Service keys bypass all security rules - guard them carefully

---

**Last Updated:** February 4, 2026
**Project:** Financial Compass - SME Financial Health Platform
