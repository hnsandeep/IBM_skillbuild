# How IBM Bob (Kiro AI) Was Used in SafeInbox AI

> This document is required by the IBM SkillsBuild submission guidelines.
> It explains how IBM Bob was used as the primary AI development tool in this project.

---

## Overview

IBM Bob (powered by Kiro AI) served as the senior engineering partner throughout the entire
development lifecycle of SafeInbox AI — from initial architecture design to final documentation.
It was not used just for code generation; it read existing files before writing new ones,
diagnosed root causes of bugs, and applied production-grade engineering judgment at every step.

---

## 1. Architecture & System Design

IBM Bob was consulted before any code was written to define the full technical architecture:

- Proposed the **two-layer intelligence pipeline**: LLM linguistic analysis (Claude) + real-time URL threat intelligence (Google Safe Browsing)
- Recommended `asyncio.gather()` to run both API calls **in parallel**, reducing response time by 1–2 seconds per request
- Advised `asyncio.to_thread()` to offload blocking synchronous SDK calls from the async event loop, preventing request starvation under load
- Designed the **Pydantic v2 data models** with `HttpUrl` validation, `max_length=10_000` as a prompt injection guard, and `field_validator` for input sanitization
- Structured the project as a clean monorepo with backend at root and frontend in a subdirectory

---

## 2. Backend Development (`main.py`)

IBM Bob wrote the complete FastAPI backend including:

| Feature | IBM Bob Contribution |
|---------|---------------------|
| LLM Prompt Engineering | Designed the system prompt to mandate strict JSON output, define risk thresholds, and enumerate phishing signals |
| Concurrent API calls | Implemented `asyncio.gather(llm_task, sb_task)` for parallel execution |
| Input validation | Pydantic `HttpUrl` type, 10k char cap, whitespace stripping |
| Score boost logic | `score = min(100, score + 30)` when Safe Browsing confirms malicious URL |
| Global error handler | Returns structured JSON — never exposes Python tracebacks to clients |
| Startup logging | Warns at startup when API keys are missing |
| Uptime tracking | `time.time()` at module load; reported in `/health` endpoint |

---

## 3. Senior-Level Code Audit & Bug Fixes

IBM Bob performed a full audit of all project files and identified and fixed **15 bugs**:

**Backend bugs fixed:**
1. `load_dotenv()` was never called — `.env` was silently ignored in local development
2. `url` field was `Optional[str]` — any garbage string accepted; changed to `Optional[HttpUrl]`
3. No message length cap — prompt injection risk; added `max_length=10_000`
4. LLM call blocked the async event loop — fixed with `asyncio.to_thread()`
5. LLM + Safe Browsing ran sequentially — fixed with `asyncio.gather()` (parallel)
6. `allow_credentials=True` + `allow_origins="*"` violates browser CORS spec — fixed
7. `render.yaml` missing Python version pin — added `pythonVersion: "3.11.9"`
8. No startup warnings when API keys missing — added `logger.warning()`

**Frontend bugs fixed:**
1. `animate-fade-in` and `animate-grow-x` used in JSX but `@keyframes` never defined — added to `index.css` and `tailwind.config.js`
2. No request cancellation on Reset — added `AbortController` wired to axios `signal`
3. Render cold-start gave 60 s of silence — added slow-start banner after 5 s
4. `key={i}` on red flags list — changed to stable key value
5. No character counter on textarea — added live counter with orange warning near limit
6. `vercel.json` missing SPA rewrite rule — added; hard refresh no longer 404s
7. `index.html` had no meta/OG tags — added `description`, `theme-color`, Open Graph

---

## 4. Frontend Development (`App.jsx`)

IBM Bob designed and built the complete single-page React application:

- All components: `RiskMeter`, `RiskBadge`, `ResultCard`, `Spinner`, `SectionHeading`
- Tailwind CSS dark security theme (`slate-900` background, `indigo-500` accents)
- Animated risk bar using CSS `scaleX` keyframe with `transform-origin: left`
- Fade-in result card entrance animation
- URL auto-extraction from pasted message text via `useEffect` + regex
- Cold-start awareness banner via `setTimeout` at 5,000 ms
- Full accessibility: `role="progressbar"`, `aria-live`, `role="alert"`, `aria-label`, `role="status"`
- Fully responsive layout using Tailwind breakpoint prefixes

---

## 5. DevOps & Deployment Configuration

IBM Bob generated all deployment and infrastructure files:

| File | Purpose |
|------|---------|
| `render.yaml` | Infrastructure-as-code: Python version pin, health check path, worker count, env var declarations |
| `vercel.json` | SPA rewrite rule, security headers (X-Content-Type-Options, X-Frame-Options, Referrer-Policy) |
| `.gitignore` | Prevents `.env`, `__pycache__`, `node_modules`, `dist` from being committed |
| `DEPLOYMENT.md` | 6-step deployment guide with exact commands for GitHub → Render → Vercel, troubleshooting section |

---

## 6. Documentation & Reporting

IBM Bob generated all project documentation:

| Document | Description |
|----------|-------------|
| `README.md` | 47 KB, 24-section comprehensive project report |
| `DEPLOYMENT.md` | Step-by-step deployment guide with troubleshooting |
| `generate_ppt.py` | Python script that auto-generates a 20-slide PowerPoint presentation using `python-pptx` |
| `SafeInbox_AI_Presentation.pptx` | Generated 20-slide industry-level presentation |
| `SUBMISSION_ANSWERS.md` | All IBM SkillsBuild submission form answers |
| `IBM_BOB_USAGE.md` | This document |

---

## Summary

Every file in this repository was designed, written, reviewed, and documented with IBM Bob
as the primary AI engineering assistant. IBM Bob's ability to read existing code before making
changes, identify root causes rather than applying incremental patches, and produce
production-grade output with proper error handling and documentation made it the most
critical tool in the SafeInbox AI development workflow.

---

*SafeInbox AI · IBM SkillsBuild Capstone · 2026*
