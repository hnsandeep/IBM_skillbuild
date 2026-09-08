# SafeInbox AI — Complete Deployment Guide

> Backend → Render.com (free tier)  
> Frontend → Vercel  
> Source → GitHub

---

## Prerequisites

| Tool | Install |
|------|---------|
| Git | https://git-scm.com/downloads |
| Node.js ≥ 18 | https://nodejs.org |
| Python 3.11 | https://python.org/downloads |
| Vercel CLI | `npm install -g vercel` |
| GitHub account | https://github.com |
| Render account | https://render.com |
| Vercel account | https://vercel.com |
| Anthropic API key | https://console.anthropic.com |
| Google Safe Browsing key | https://developers.google.com/safe-browsing/v4/get-started |

---

## Project Structure (final)

```
safeinbox-ai/                  ← repo root
├── main.py                    ← FastAPI backend
├── requirements.txt
├── render.yaml                ← Render deployment config
├── .env.example               ← backend env template
├── .gitignore
└── frontend/                  ← Vite + React frontend
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── public/
    │   └── shield.svg
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── vercel.json
    ├── .env                   ← NOT committed (gitignored)
    └── .env.example
```

---

## STEP 1 — Set Up Local Environment

### 1a. Backend (Python)

```bash
cd d:\IBM_skillsbuild

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows CMD
# source venv/bin/activate     # Mac / Linux

# Install dependencies
pip install -r requirements.txt

# Copy env template and fill in your real keys
copy .env.example .env
```

Open `.env` and set:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
SAFE_BROWSING_KEY=AIzaxxxxxxxxxxxxxxxx
```

Test the backend locally:
```bash
uvicorn main:app --reload
# Visit http://localhost:8000/health
# Visit http://localhost:8000/docs  (Swagger UI)
```

### 1b. Frontend (Node)

```bash
cd d:\IBM_skillsbuild\frontend

# Install dependencies
npm install

# Confirm .env points to local backend
# frontend/.env should contain:
# VITE_API_URL=http://localhost:8000

# Start dev server
npm run dev
# Visit http://localhost:5173
```

Test end-to-end locally before deploying.

---

## STEP 2 — Push to GitHub

```bash
cd d:\IBM_skillsbuild

# Initialize git repo (skip if already done)
git init

# Stage everything (.gitignore excludes .env, node_modules, __pycache__)
git add .

# Verify .env files are NOT staged (should show nothing for these)
git status | findstr ".env"

# Commit
git commit -m "feat: SafeInbox AI v1.1.0 — initial commit"

# Create repo on GitHub first at https://github.com/new
# Name it: safeinbox-ai   (public or private, your choice)
# Do NOT initialize with README (you already have files)

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/safeinbox-ai.git
git branch -M main
git push -u origin main
```

---

## STEP 3 — Deploy Backend to Render

### 3a. Connect GitHub to Render

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"** → authorize GitHub
4. Select your **safeinbox-ai** repository → click **Connect**

### 3b. Configure the Service

Render will auto-detect `render.yaml`. Confirm these settings:

| Field | Value |
|-------|-------|
| Name | `safeinbox-ai-backend` |
| Runtime | `Python 3` |
| Region | `Oregon (US West)` |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2` |
| Plan | `Free` |

### 3c. Set Environment Variables

In the Render dashboard → your service → **"Environment"** tab → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `ANTHROPIC_API_KEY` | `sk-ant-xxxxxxxxxxxxxxxx` |
| `SAFE_BROWSING_KEY` | `AIzaxxxxxxxxxxxxxxxx` |

Click **"Save Changes"**.

### 3d. Deploy

```
Render dashboard → your service → "Manual Deploy" → "Deploy latest commit"
```

Watch the build logs. A successful deploy ends with:
```
Your service is live 🎉
```

### 3e. Note Your Backend URL

It will look like:
```
https://safeinbox-ai-backend.onrender.com
```

Test it:
```bash
curl https://safeinbox-ai-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "SafeInbox AI",
  "version": "1.1.0",
  "uptime_seconds": 4.2,
  "anthropic_configured": true,
  "safe_browsing_configured": true
}
```

> ⚠️ **Free tier note:** Render spins the service down after 15 minutes of inactivity.
> The first request after sleep takes ~30 seconds. The frontend handles this gracefully
> with a "Backend is waking up…" banner.

---

## STEP 4 — Deploy Frontend to Vercel

### 4a. Install Vercel CLI (if not already)

```bash
npm install -g vercel
```

### 4b. Login to Vercel

```bash
vercel login
# Choose: "Continue with GitHub"
# Authorize in the browser window that opens
```

### 4c. Deploy

```bash
cd d:\IBM_skillsbuild\frontend

vercel
```

Answer the prompts:

```
? Set up and deploy "frontend"? → Y
? Which scope? → (select your personal account)
? Link to existing project? → N
? What's your project's name? → safeinbox-ai
? In which directory is your code located? → ./
? Want to modify these settings? → N
```

### 4d. Set the Backend URL Environment Variable

```bash
# Add the production env variable pointing to your Render backend
vercel env add VITE_API_URL production
# When prompted, paste:
# https://safeinbox-ai-backend.onrender.com
# Press Enter
```

### 4e. Redeploy to Production with the Env Var Applied

```bash
vercel --prod
```

Wait for output like:
```
✅  Production: https://safeinbox-ai.vercel.app [3s]
```

### 4f. Verify

Open your Vercel URL in a browser and run a test analysis.

```bash
# Quick smoke test from terminal
curl -X POST https://safeinbox-ai.vercel.app/../api/analyze \
  # (use the Render URL directly for API testing)

curl -X POST https://safeinbox-ai-backend.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"URGENT: Your PayPal account is suspended. Verify now: http://paypa1-secure.xyz\", \"url\": \"http://paypa1-secure.xyz\"}"
```

---

## STEP 5 — Verify Full Stack

| Check | URL | Expected |
|-------|-----|----------|
| Backend health | `https://safeinbox-ai-backend.onrender.com/health` | `{"status":"ok"}` |
| API docs | `https://safeinbox-ai-backend.onrender.com/docs` | Swagger UI |
| Frontend | `https://safeinbox-ai.vercel.app` | App loads |
| Analysis | Paste a message in the app → click Analyze | Risk score returned |

---

## STEP 6 — Future Deployments (CI/CD)

Both platforms auto-deploy on every `git push` once connected:

```bash
# Make changes, then:
git add .
git commit -m "fix: your change description"
git push origin main
# Render and Vercel both pick up the push automatically
```

---

## Environment Variables Reference

### Backend (set in Render Dashboard → Environment)

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | Claude API key from console.anthropic.com |
| `SAFE_BROWSING_KEY` | ⚠️ Optional | Google Safe Browsing key — URL checks disabled if absent |

### Frontend (set via `vercel env add` or Vercel Dashboard)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | ✅ Yes | Full URL of deployed backend, no trailing slash |

---

## Troubleshooting

### Backend won't start on Render
- Check build logs for `pip install` errors
- Ensure `ANTHROPIC_API_KEY` is set in Render Environment tab
- Verify `render.yaml` is in the **repo root**, not inside `frontend/`

### Frontend shows "Network Error"
- Confirm `VITE_API_URL` is set in Vercel (not just `.env`)
- After adding/changing env vars, always run `vercel --prod` again to redeploy
- Check browser DevTools → Network tab for the actual error

### 502 on /analyze
- `ANTHROPIC_API_KEY` is missing or invalid
- Check Render logs: Dashboard → your service → **"Logs"** tab

### CORS errors in browser
- Confirm `VITE_API_URL` has no trailing slash: ✅ `https://...onrender.com` not `https://...onrender.com/`
- Backend CORS is set to `allow_origins=["*"]` — should accept all origins

### Render cold start timeout
- The frontend already shows a "waking up" banner after 5 s
- First request after 15 min idle takes ~30 s — this is normal on the free tier
- Upgrade to Render's **Starter** plan ($7/mo) to eliminate cold starts

---

## Useful Commands Cheat Sheet

```bash
# ── Local dev ──────────────────────────────────────
uvicorn main:app --reload                         # start backend
cd frontend && npm run dev                        # start frontend

# ── Git ────────────────────────────────────────────
git add . && git commit -m "msg" && git push      # push changes

# ── Vercel ─────────────────────────────────────────
vercel --prod                                     # deploy frontend
vercel logs                                       # view recent logs
vercel env ls                                     # list env variables
vercel env add VITE_API_URL production            # add/update env var

# ── Render (via API or dashboard) ──────────────────
# Trigger manual redeploy from:
# https://dashboard.render.com → your service → Manual Deploy

# ── Test API directly ──────────────────────────────
curl https://YOUR_RENDER_URL.onrender.com/health

curl -X POST https://YOUR_RENDER_URL.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Your account has been compromised. Click here immediately.\",\"url\":\"http://evil-phish.xyz\"}"
```

---

*SafeInbox AI — Built with FastAPI, Claude (Anthropic), Google Safe Browsing, React, Vite, Tailwind CSS*
