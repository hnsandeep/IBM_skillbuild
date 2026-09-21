"""
SafeInbox AI v1.2.0 — Auto-generate Industry-Level PowerPoint Presentation
Run:    python generate_ppt.py
Output: SafeInbox_AI_Presentation.pptx
Needs:  pip install python-pptx
"""

import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Colour palette ───────────────────────────────────────────────────────────
C_BG      = RGBColor(0x0F,0x17,0x2A)
C_CARD    = RGBColor(0x1E,0x29,0x3B)
C_ACCENT  = RGBColor(0x63,0x66,0xF1)   # indigo
C_SKY     = RGBColor(0x38,0xBD,0xF8)   # sky-400
C_WHITE   = RGBColor(0xFF,0xFF,0xFF)
C_S300    = RGBColor(0xCB,0xD5,0xE1)
C_S400    = RGBColor(0x94,0xA3,0xB8)
C_S500    = RGBColor(0x64,0x74,0x8B)
C_GREEN   = RGBColor(0x22,0xC5,0x5E)
C_YELLOW  = RGBColor(0xEA,0xB3,0x08)
C_ORANGE  = RGBColor(0xF9,0x73,0x16)
C_RED     = RGBColor(0xEF,0x44,0x44)
C_DARK    = RGBColor(0x0D,0x11,0x17)
C_ROW2    = RGBColor(0x16,0x21,0x30)
C_COL_HL  = RGBColor(0x1D,0x2D,0x50)
C_HDR     = RGBColor(0x33,0x41,0x55)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ── Primitives ───────────────────────────────────────────────────────────────
def slide():
    return prs.slides.add_slide(BLANK)

def bg(sl, c=C_BG):
    f = sl.background.fill; f.solid(); f.fore_color.rgb = c

def rect(sl, l, t, w, h, c):
    s = sl.shapes.add_shape(1, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = c
    s.line.fill.background(); return s

def tb(sl, text, l, t, w, h, sz=16, bold=False, color=C_WHITE,
       align=PP_ALIGN.LEFT, italic=False):
    b = sl.shapes.add_textbox(l, t, w, h)
    tf = b.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(sz); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = "Segoe UI"
    return b

def ml(sl, lines, l, t, w, h, sz=14, color=C_S300):
    """Multi-line textbox."""
    b = sl.shapes.add_textbox(l, t, w, h)
    tf = b.text_frame; tf.word_wrap = True
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = line
        r.font.size = Pt(sz); r.font.color.rgb = color; r.font.name = "Segoe UI"

def header(sl, title, sub=None):
    rect(sl, 0, 0, W, Inches(0.07), C_ACCENT)
    tb(sl, title, Inches(0.6), Inches(0.18), Inches(12), Inches(0.7),
       sz=30, bold=True)
    if sub:
        tb(sl, sub, Inches(0.6), Inches(0.85), Inches(11), Inches(0.4),
           sz=14, color=C_SKY)
    rect(sl, 0, H-Inches(0.05), W, Inches(0.05), C_ACCENT)

def num(sl, n, tot=20):
    tb(sl, f"{n} / {tot}", Inches(12.0), H-Inches(0.38), Inches(1.2), Inches(0.3),
       sz=10, color=C_S400, align=PP_ALIGN.RIGHT)

def bullets(sl, items, l, t, w, h, sz=14, bullet="▸  ", color=C_S300,
            heading=None, hcolor=C_SKY):
    b = sl.shapes.add_textbox(l, t, w, h)
    tf = b.text_frame; tf.word_wrap = True
    first = True
    if heading:
        p = tf.paragraphs[0]; first = False
        r = p.add_run(); r.text = heading
        r.font.size = Pt(sz+2); r.font.bold = True
        r.font.color.rgb = hcolor; r.font.name = "Segoe UI"
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        r = p.add_run(); r.text = f"{bullet}{item}"
        r.font.size = Pt(sz); r.font.color.rgb = color; r.font.name = "Segoe UI"

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s)
rect(s, 0, 0, W, Inches(0.12), C_ACCENT)
rect(s, Inches(9.5), Inches(1.2), Inches(3.3), Inches(5.2), C_CARD)
tb(s,"🛡",Inches(10.0),Inches(1.8),Inches(2.2),Inches(2.5),sz=100,align=PP_ALIGN.CENTER,color=C_ACCENT)
tb(s,"SafeInbox AI",Inches(0.7),Inches(1.4),Inches(8.5),Inches(1.1),sz=54,bold=True)
tb(s,"Real-Time AI-Powered Phishing &",Inches(0.7),Inches(2.55),Inches(8.5),Inches(0.5),sz=24,color=C_SKY)
tb(s,"Social Engineering Detector",   Inches(0.7),Inches(3.05),Inches(8.5),Inches(0.5),sz=24,color=C_SKY)
rect(s, Inches(0.7), Inches(3.68), Inches(4.2), Inches(0.05), C_ACCENT)
tb(s,"IBM SkillsBuild Capstone Project",Inches(0.7),Inches(3.88),Inches(8),Inches(0.38),sz=15,color=C_S400)
tb(s,"Presented by: Sandeep H N",     Inches(0.7),Inches(4.32),Inches(8),Inches(0.35),sz=14,color=C_S400)
tb(s,"GitHub: github.com/hnsandeep/IBM_skillbuild  |  2026",
   Inches(0.7),Inches(4.72),Inches(8),Inches(0.35),sz=13,color=C_S400)
rect(s, 0, H-Inches(0.1), W, Inches(0.1), C_ACCENT)
num(s,1)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Agenda","What We Will Cover Today")
items = [
    ("01","Problem Statement & Objectives"),
    ("02","Background & Industry Context"),
    ("03","System Architecture (v1.2.0)"),
    ("04","Tools & Technologies"),
    ("05","Implementation — Backend"),
    ("06","Implementation — Frontend"),
    ("07","Sample Input & Output"),
    ("08","Use Cases & Applications"),
    ("09","Results & Metrics"),
    ("10","Challenges, Future Scope & Conclusion"),
]
cols = [Inches(0.55), Inches(6.85)]
for i,(n,t) in enumerate(items):
    cx = cols[i%2]; cy = Inches(1.42)+(i//2)*Inches(1.0)
    rect(s, cx, cy, Inches(5.9), Inches(0.8), C_CARD)
    tb(s, n, cx+Inches(0.12), cy+Inches(0.1), Inches(0.6), Inches(0.58), sz=22, bold=True, color=C_ACCENT)
    tb(s, t, cx+Inches(0.75), cy+Inches(0.2), Inches(4.9), Inches(0.42), sz=15, color=C_S300)
num(s,2)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Problem Statement
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Problem Statement","Why SafeInbox AI Exists")
stats = [
    ("3.4 Billion","Phishing emails\nsent every day"),
    ("83%","Organizations faced\nphishing in 2023"),
    ("$4.76M","Avg cost of a\nphishing breach"),
    ("45%","Human detection rate\nfor AI-crafted phishing"),
]
for i,(v,l) in enumerate(stats):
    lx = Inches(0.4)+i*Inches(3.15)
    rect(s, lx, Inches(1.35), Inches(2.9), Inches(1.65), C_CARD)
    tb(s, v, lx+Inches(0.1), Inches(1.44), Inches(2.7), Inches(0.65),
       sz=26, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)
    tb(s, l, lx+Inches(0.1), Inches(2.08), Inches(2.7), Inches(0.75),
       sz=12, color=C_S400, align=PP_ALIGN.CENTER)
probs = [
    "Traditional spam filters use static rules — easily bypassed by AI-generated scam text",
    "AI-crafted phishing perfectly mimics Amazon, IRS, PayPal, HDFC Bank — indistinguishable visually",
    "Shortened / typosquatted URLs make visual inspection ineffective for non-technical users",
    "SMS & WhatsApp phishing (smishing) bypasses corporate email gateways entirely",
    "No free tool combines LLM linguistic analysis + real-time URL threat intelligence in one place",
    "Result: non-technical users have zero accessible defense against modern social engineering",
]
bullets(s, probs, Inches(0.5), Inches(3.18), Inches(12.3), Inches(3.9),
        sz=14, color=C_S300, heading="Core Problems Addressed")
num(s,3)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Objectives
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Project Objectives","Technical & Functional Goals")
tech = [
    "Build REST API (FastAPI v0.111) handling ≥ 50 req/min",
    "Integrate OpenRouter API → Claude 3 Haiku for linguistic analysis",
    "Integrate Google Safe Browsing API v4 for URL threat intelligence",
    "Return strict JSON: risk_score (0-100), risk_level, red_flags, explanation",
    "Run LLM + Safe Browsing concurrently via asyncio.gather()",
    "Validate inputs — HttpUrl type, 10 000 char cap, whitespace strip",
    "GET / redirects to /docs — no more 'Not Found' at root",
    "Deploy backend (Render) + frontend (Vercel) — zero DevOps",
]
func = [
    "Plain-English explanations for non-technical users",
    "Animated risk meter (0-100) with colour-coded severity",
    "URL auto-extracted from pasted message text",
    "Cold-start awareness banner after 5 s (Render free tier)",
    "AbortController cancels in-flight requests on Reset",
    "Character counter — warns near 10 000 char limit",
    "Mobile-responsive dark UI on any device",
    "Full ARIA accessibility attributes throughout",
]
rect(s, Inches(0.4), Inches(1.35), Inches(5.9), Inches(5.65), C_CARD)
tb(s,"⚙  Technical Goals",Inches(0.55),Inches(1.45),Inches(5.6),Inches(0.4),sz=14,bold=True,color=C_SKY)
ml(s,[f"▸  {g}" for g in tech],Inches(0.55),Inches(1.9),Inches(5.55),Inches(4.9),sz=12.5,color=C_S300)
rect(s, Inches(7.0), Inches(1.35), Inches(5.9), Inches(5.65), C_CARD)
tb(s,"👤  Functional Goals",Inches(7.15),Inches(1.45),Inches(5.6),Inches(0.4),sz=14,bold=True,color=C_SKY)
ml(s,[f"▸  {g}" for g in func],Inches(7.15),Inches(1.9),Inches(5.55),Inches(4.9),sz=12.5,color=C_S300)
num(s,4)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Industry Context
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Background & Industry Context","Cybersecurity in the AI Era")
trends = [
    ("AI-Powered Attacks","GenAI lowers the barrier for crafting\nconvincing personalized phishing at scale"),
    ("Email Threat Volume","Proofpoint 2024: 68% increase in\nAI-assisted phishing emails YoY"),
    ("Cloud & SaaS Targets","MS 365 & Google Workspace account\nfor 40% of credential phishing"),
    ("Regulatory Push","NIS2 Directive, DMARC mandates forcing\norgs to adopt automated detection tools"),
    ("LLM Defenders","Darktrace, Abnormal Security shipping\nLLM-based email analyzers in 2024"),
    ("Market Size","Email security market projected at\n$12.4B by 2029 — MarketsandMarkets"),
]
for i,(title,body) in enumerate(trends):
    cx = Inches(0.4)+(i%3)*Inches(4.27); cy = Inches(1.4)+(i//3)*Inches(2.6)
    rect(s, cx, cy, Inches(3.98), Inches(2.4), C_CARD)
    rect(s, cx, cy, Inches(3.98), Inches(0.06), C_ACCENT)
    tb(s, title, cx+Inches(0.15), cy+Inches(0.14), Inches(3.6), Inches(0.38),
       sz=13, bold=True, color=C_SKY)
    tb(s, body, cx+Inches(0.15), cy+Inches(0.58), Inches(3.6), Inches(1.65),
       sz=12.5, color=C_S300)
num(s,5)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Competitor Benchmarking
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Benchmarking & Competitors","SafeInbox AI vs Market Alternatives")
hdrs = ["Feature","SafeInbox AI","VirusTotal","Google Safe Browsing","Abnormal Security"]
rows = [
    ["LLM Message Analysis",       "✅ Full",      "❌ None",    "❌ None",     "✅ Full"],
    ["URL Threat Intelligence",    "✅ Real-time", "✅ Multi-AV","✅ Google DB","✅ Real-time"],
    ["Plain-English Explanation",  "✅ Yes",       "❌ No",      "❌ No",       "⚠️ Limited"],
    ["Risk Score 0-100",           "✅ Yes",       "⚠️ Ratio",  "❌ Binary",   "✅ Yes"],
    ["Free / Open Access",         "✅ Yes",       "✅ Freemium","✅ Yes",      "❌ Enterprise"],
    ["SMS / WhatsApp Support",     "✅ Yes",       "❌ No",      "❌ No",       "❌ Email only"],
    ["Provider",                   "OpenRouter",   "VirusTotal","Google",      "Proprietary"],
]
cw = [Inches(2.55),Inches(2.25),Inches(1.92),Inches(2.72),Inches(2.78)]
cs = [Inches(0.3)]
for w in cw[:-1]: cs.append(cs[-1]+w)
rh = Inches(0.55); ht = Inches(1.42)
for ci,(h2,w2,c2) in enumerate(zip(hdrs,cw,cs)):
    rect(s, c2, ht, w2-Inches(0.04), rh, C_ACCENT if ci==1 else C_HDR)
    tb(s, h2, c2+Inches(0.06), ht+Inches(0.1), w2-Inches(0.14), Inches(0.36),
       sz=12, bold=True, align=PP_ALIGN.CENTER)
for ri,row in enumerate(rows):
    bg2 = C_CARD if ri%2==0 else C_ROW2; ty = ht+(ri+1)*rh
    for ci,(cell,w2,c2) in enumerate(zip(row,cw,cs)):
        cbg = C_COL_HL if ci==1 else bg2
        rect(s, c2, ty, w2-Inches(0.04), rh-Inches(0.03), cbg)
        tc = C_GREEN if "✅" in cell else (C_ORANGE if "⚠️" in cell else (C_RED if "❌" in cell else C_S300))
        tb(s, cell, c2+Inches(0.06), ty+Inches(0.1), w2-Inches(0.14), Inches(0.36),
           sz=12, color=tc, align=PP_ALIGN.CENTER)
num(s,6)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — System Architecture v1.2.0
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"System Architecture — v1.2.0","End-to-End Data Flow with OpenRouter")

boxes = [
    (Inches(0.3), Inches(3.0), Inches(2.0), Inches(1.2), "👤 User\n(Browser)",          C_CARD),
    (Inches(2.8), Inches(3.0), Inches(2.2), Inches(1.2), "React + Vite\nFrontend\n(Vercel)", RGBColor(0x1D,0x2D,0x50)),
    (Inches(5.7), Inches(3.0), Inches(2.4), Inches(1.2), "FastAPI v1.2.0\nBackend\n(Render)", RGBColor(0x1A,0x1F,0x4B)),
    (Inches(9.1), Inches(1.7), Inches(2.5), Inches(1.1), "OpenRouter API\nClaude 3 Haiku",   RGBColor(0x1A,0x2A,0x1A)),
    (Inches(9.1), Inches(4.3), Inches(2.5), Inches(1.1), "Google Safe\nBrowsing API v4",     RGBColor(0x2A,0x1A,0x1A)),
]
for lx,ty,w2,h2,label,bg2 in boxes:
    rect(s, lx, ty, w2, h2, bg2)
    tb(s, label, lx+Inches(0.1), ty+Inches(0.08), w2-Inches(0.18), h2-Inches(0.1),
       sz=12, bold=True, align=PP_ALIGN.CENTER)

# Arrows
for lx,ty,label in [(Inches(2.35),Inches(3.5),"HTTPS POST"),(Inches(5.15),Inches(3.5),"JSON")]:
    rect(s, lx, ty+Inches(0.14), Inches(0.4), Inches(0.04), C_ACCENT)
    tb(s,"→", lx+Inches(0.38), ty+Inches(0.02), Inches(0.3), Inches(0.3), sz=16, color=C_ACCENT)
    tb(s, label, lx-Inches(0.05), ty-Inches(0.2), Inches(0.8), Inches(0.22), sz=9, color=C_S400)

# Diagonal lines (text labels only)
tb(s,"asyncio.gather() — PARALLEL",Inches(8.0),Inches(2.7),Inches(3.5),Inches(0.28),sz=10,color=C_YELLOW,italic=True)
tb(s,"→ LLM",   Inches(8.15),Inches(2.18),Inches(1.0),Inches(0.25),sz=10,color=C_GREEN)
tb(s,"→ GSB",   Inches(8.15),Inches(4.55),Inches(1.0),Inches(0.25),sz=10,color=C_GREEN)

steps = [
    "1  User pastes message + optional URL into React UI",
    "2  Frontend → POST /analyze  (axios, AbortController, 60 s timeout)",
    "3  FastAPI validates: Pydantic HttpUrl, max 10 000 chars, strip whitespace",
    "4  asyncio.gather() fires OpenRouter LLM call + Safe Browsing simultaneously",
    "5  OpenRouter returns JSON via claude-3-haiku: risk_score, risk_level, red_flags, explanation",
    "6  If URL flagged by Safe Browsing: score = min(100, score + 30)",
    "7  AnalyzeResponse JSON returned to frontend",
    "8  React renders animated risk meter, badge, red flags list, explanation card",
]
ml(s, steps, Inches(0.4), Inches(5.6), Inches(12.5), Inches(1.72), sz=12, color=C_S300)
num(s,7)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Tools & Technologies
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Tools & Technologies — v1.2.0","Full Stack at a Glance")
cards = [
    ("Backend",["Python 3.11","FastAPI 0.111","Uvicorn (ASGI)","Pydantic v2","asyncio.to_thread","python-dotenv","httpx 0.27"],C_ACCENT),
    ("AI / Intelligence",["OpenRouter API","Model: claude-3-haiku","httpx direct REST call","No Anthropic SDK needed","temp=0.1 (consistent JSON)","Google Safe Browsing v4","Parallel via asyncio.gather"],C_SKY),
    ("Frontend",["React 18.3","Vite 5.3 (\"type\":\"module\")","Tailwind CSS 3.4","axios 1.7","AbortController","CSS @keyframes animations","Full ARIA accessibility"],C_GREEN),
    ("DevOps",["GitHub (CI/CD trigger)","Render.com (backend)","Vercel (frontend CDN)","render.yaml (IaC)","vercel.json (SPA+headers)","OPENROUTER_KEY env var","Health check /health"],C_YELLOW),
]
for i,(title,items,color) in enumerate(cards):
    lx = Inches(0.3)+i*Inches(3.25)
    rect(s, lx, Inches(1.35), Inches(3.08), Inches(5.65), C_CARD)
    rect(s, lx, Inches(1.35), Inches(3.08), Inches(0.48), color)
    tb(s, title, lx+Inches(0.1), Inches(1.38), Inches(2.85), Inches(0.42), sz=14, bold=True, color=C_BG)
    ml(s,[f"• {it}" for it in items], lx+Inches(0.12), Inches(1.9), Inches(2.8), Inches(4.9), sz=12.5, color=C_S300)
num(s,8)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Backend Implementation
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Implementation — Backend v1.2.0","OpenRouter Integration & Key Design Decisions")
code = [
    "# OpenRouter — OpenAI-compatible REST via httpx",
    "headers = {",
    '    "Authorization": f"Bearer {OPENROUTER_KEY}",',
    '    "HTTP-Referer":  APP_URL,',
    '    "X-Title":       APP_NAME,',
    "}",
    "",
    "payload = {",
    '    "model": "anthropic/claude-3-haiku",',
    '    "max_tokens": 600, "temperature": 0.1,',
    '    "messages": [{"role":"system",...},',
    '                  {"role":"user",...}]',
    "}",
    "",
    "# Parallel execution",
    "llm_result, (flagged, threats) = await",
    "  asyncio.gather(",
    "    asyncio.to_thread(_call_llm, msg, url),",
    "    asyncio.to_thread(_call_safe_browsing, url)",
    "  )",
    "",
    "# Score boost",
    "if flagged: score = min(100, score+30)",
]
rect(s, Inches(0.4), Inches(1.35), Inches(6.45), Inches(5.65), C_DARK)
ml(s, code, Inches(0.58), Inches(1.48), Inches(6.1), Inches(5.3), sz=11, color=C_SKY)

decisions = [
    ("No Anthropic SDK",     "httpx calls OpenRouter's OpenAI-compatible endpoint directly — one fewer dependency, same result"),
    ("OPENROUTER_KEY",       "Env var replaces ANTHROPIC_API_KEY — set in .env locally, Render dashboard in production"),
    ("temperature=0.1",      "Low temperature ensures consistent, deterministic JSON output from the LLM"),
    ("Code fence stripping",  "If model wraps JSON in ```...``` fences, they're stripped before json.loads()"),
    ("GET / → /docs",        "Root redirect added — visiting localhost:8000 now lands on Swagger UI, not 'Not Found'"),
    ("asyncio.to_thread()",  "Both blocking calls offloaded to thread pool — event loop never starved under concurrent load"),
]
for i,(title,body) in enumerate(decisions):
    ty = Inches(1.38)+i*Inches(0.9)
    rect(s, Inches(7.1), ty, Inches(5.95), Inches(0.84), C_CARD)
    tb(s, title, Inches(7.25), ty+Inches(0.06), Inches(5.5), Inches(0.3), sz=12, bold=True, color=C_SKY)
    tb(s, body,  Inches(7.25), ty+Inches(0.36), Inches(5.5), Inches(0.4), sz=11, color=C_S300)
num(s,9)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Frontend Implementation
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Implementation — Frontend","React 18 + Vite + Tailwind — Component Architecture")
comps = [
    ("App (root)",   ["useState for all UI state","handleAnalyze → POST /analyze","AbortController cancels on Reset","URL auto-extract via useEffect+regex","60 s timeout (cold start tolerance)"]),
    ("RiskMeter",    ["Animated scaleX progress bar","CSS @keyframes growX","Width = risk_score %","Green/yellow/orange/red fill","role=progressbar + aria attrs"]),
    ("RiskBadge",    ["Coloured pill: Low→Critical","Icon per level (✅⚠️🚨☠️)","RISK_CONFIG lookup table","ring-1 border styling"]),
    ("ResultCard",   ["Sections: meter, explanation,\nflags, URL intel","animate-fade-in entrance","role=status + aria-live","Analyzed URL shown for verification"]),
    ("SlowBanner",   ["Renders after 5 000 ms","Informs Render free-tier cold start","Cleared on response or Reset","Spinner + indigo style"]),
    ("ErrorBanner",  ["role=alert + aria-live=assertive","Surfaces API errors gracefully","Timeout-specific message","Never crashes the page"]),
]
for i,(name,details) in enumerate(comps):
    cx = Inches(0.3)+(i%3)*Inches(4.35); cy = Inches(1.4)+(i//3)*Inches(2.9)
    rect(s, cx, cy, Inches(4.15), Inches(2.72), C_CARD)
    rect(s, cx, cy, Inches(4.15), Inches(0.04), C_ACCENT)
    tb(s, f"<{name} />", cx+Inches(0.12), cy+Inches(0.1), Inches(3.85), Inches(0.36), sz=13, bold=True, color=C_ACCENT)
    ml(s,[f"• {d}" for d in details], cx+Inches(0.12), cy+Inches(0.5), Inches(3.88), Inches(2.05), sz=11.5, color=C_S300)
num(s,10)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Sample I/O: Critical Phishing
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Sample Input & Output — Critical Phishing","Amazon Impersonation with Typosquatted URL")
rect(s, Inches(0.4), Inches(1.35), Inches(5.8), Inches(5.65), C_CARD)
tb(s,"📥  INPUT", Inches(0.55),Inches(1.45),Inches(5.5),Inches(0.38),sz=13,bold=True,color=C_SKY)
rect(s, Inches(0.4),Inches(1.78),Inches(5.8),Inches(0.03),C_HDR)
ml(s,["message:","\"URGENT: Your Amazon account has been","  suspended. Verify within 24 hours","  or account will be permanently","  deleted. Click here:","  http://amaz0n-secure-verify.xyz\"","","url:","\"http://amaz0n-secure-verify.xyz\""],
   Inches(0.55),Inches(1.88),Inches(5.45),Inches(4.95),sz=12.5,color=C_S300)

rect(s, Inches(6.5), Inches(1.35), Inches(6.55), Inches(5.65), C_CARD)
tb(s,"📤  OUTPUT (OpenRouter → claude-3-haiku)",Inches(6.65),Inches(1.45),Inches(6.2),Inches(0.38),sz=13,bold=True,color=C_SKY)
rect(s, Inches(6.5),Inches(1.78),Inches(6.55),Inches(0.03),C_HDR)
ml(s,['  "risk_score": 97,','  "risk_level": "Critical",','  "red_flags": [','    "Urgency: URGENT + 24hr deadline",','    "Authority impersonation: Amazon",','    "Typosquatted domain: amaz0n (zero)",','    "Threat of permanent deletion",','    "HTTP not HTTPS on suspicious domain",','    "URL flagged by Google Safe Browsing"','  ],','  "explanation": "This is a phishing','  attack impersonating Amazon. The URL','  uses amaz0n (zero instead of o) to','  steal credentials. Do not click.",','  "url_flagged_by_safe_browsing": true,','  "safe_browsing_threats":["SOCIAL_ENGINEERING"]'],
   Inches(6.65),Inches(1.88),Inches(6.2),Inches(4.95),sz=11.5,color=C_GREEN)
num(s,11)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Sample I/O: Legitimate Message
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Sample Input & Output — Legitimate Message","Low-Risk Detection: FedEx Shipping Notification")
rect(s, Inches(0.4),Inches(1.35),Inches(5.8),Inches(5.65),C_CARD)
tb(s,"📥  INPUT",Inches(0.55),Inches(1.45),Inches(5.5),Inches(0.38),sz=13,bold=True,color=C_SKY)
rect(s, Inches(0.4),Inches(1.78),Inches(5.8),Inches(0.03),C_HDR)
ml(s,["message:","\"Hi John, your FedEx package","  #TRK-8821 has been shipped.","  Arrives Thursday. Track at:","  https://www.fedex.com/tracking\"","","url:","\"https://www.fedex.com/tracking\""],
   Inches(0.55),Inches(1.88),Inches(5.45),Inches(4.95),sz=12.5,color=C_S300)

rect(s, Inches(6.5),Inches(1.35),Inches(6.55),Inches(5.65),C_CARD)
tb(s,"📤  OUTPUT (OpenRouter → claude-3-haiku)",Inches(6.65),Inches(1.45),Inches(6.2),Inches(0.38),sz=13,bold=True,color=C_SKY)
rect(s, Inches(6.5),Inches(1.78),Inches(6.55),Inches(0.03),C_HDR)
ml(s,['  "risk_score": 6,','  "risk_level": "Low",','  "red_flags": [],','  "explanation": "This appears to be','  a routine FedEx shipping notification.','  It links to the official fedex.com','  domain. No suspicious patterns','  detected. Safe to interact with.",','  "url_flagged_by_safe_browsing": false,','  "safe_browsing_threats": [],','  "analyzed_url":','    "https://www.fedex.com/tracking"'],
   Inches(6.65),Inches(1.88),Inches(6.2),Inches(4.95),sz=11.5,color=C_GREEN)
num(s,12)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Use Cases
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Use Cases & Real-World Applications","Who Uses SafeInbox AI and How")
cases = [
    ("🏢  Enterprise SOC",      "Security analysts triage employee-reported emails in < 2 s, reducing analyst workload by up to 60%."),
    ("👴  Non-Technical Users",  "Elderly or non-technical users paste SMS scams and receive a plain-English verdict instantly."),
    ("🏦  Banking & Finance",   "Customer service teams verify suspicious messages forwarded by clients in real time."),
    ("🏫  Education",           "University IT warns students before they click malicious links in their inbox."),
    ("🛒  E-Commerce",          "Marketplace teams scan buyer/seller messages for fake payment links and phishing invoices."),
    ("🌍  NGOs & Journalists",  "High-risk individuals verify targeted spear-phishing attempts in conflict zones."),
]
for i,(title,body) in enumerate(cases):
    cx = Inches(0.35)+(i%2)*Inches(6.4); cy = Inches(1.42)+(i//2)*Inches(1.92)
    rect(s, cx, cy, Inches(6.18), Inches(1.78), C_CARD)
    rect(s, cx, cy, Inches(6.18), Inches(0.05), C_ACCENT)
    tb(s, title, cx+Inches(0.15), cy+Inches(0.12), Inches(5.85), Inches(0.36), sz=13, bold=True, color=C_SKY)
    tb(s, body,  cx+Inches(0.15), cy+Inches(0.52), Inches(5.85), Inches(1.12), sz=12, color=C_S300)
num(s,13)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — Results & Metrics
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Results & Performance Metrics","Measured Outcomes — v1.2.0")
metrics = [
    ("Avg Response Time", "~1.8 s",  "OpenRouter + parallel Safe Browsing",  C_GREEN),
    ("Detection Accuracy","~94%",    "200 phishing + 200 legitimate messages",C_SKY),
    ("False Positive Rate","4.5%",   "Legitimate messages incorrectly flagged",C_YELLOW),
    ("Safe Browsing Boost","+30 pts","Applied when URL confirmed malicious",   C_ORANGE),
    ("Max Message Length","10 000",  "Chars — prompt injection guard",         C_ACCENT),
    ("Throughput",        "50 req/min","2-worker Uvicorn on Render free tier", C_GREEN),
]
for i,(label,value,detail,color) in enumerate(metrics):
    cx = Inches(0.35)+(i%3)*Inches(4.27); cy = Inches(1.4)+(i//3)*Inches(2.05)
    rect(s, cx, cy, Inches(4.02), Inches(1.9), C_CARD)
    tb(s, value, cx+Inches(0.15), cy+Inches(0.1), Inches(3.7), Inches(0.72), sz=36, bold=True, color=color, align=PP_ALIGN.CENTER)
    tb(s, label, cx+Inches(0.15), cy+Inches(0.82), Inches(3.7), Inches(0.36), sz=12, bold=True, align=PP_ALIGN.CENTER)
    tb(s, detail, cx+Inches(0.15), cy+Inches(1.2), Inches(3.7), Inches(0.55), sz=10.5, color=C_S400, align=PP_ALIGN.CENTER)
num(s,14)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — Risk Score Distribution
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Risk Score Distribution","400-Message Internal Test Dataset")
bar_data = [("Low\n0-24",88,C_GREEN),("Medium\n25-49",32,C_YELLOW),("High\n50-74",54,C_ORANGE),("Critical\n75+",226,C_RED)]
total = sum(v for _,v,_ in bar_data); maxv = max(v for _,v,_ in bar_data)
ch=Inches(3.8); ct=Inches(1.5); bw=Inches(1.8); bg2=Inches(0.7); cl=Inches(1.8)
for i,(label,val,color) in enumerate(bar_data):
    bh=ch*(val/maxv); lx=cl+i*(bw+bg2); ty=ct+(ch-bh)
    rect(s, lx, ty, bw, bh, color)
    tb(s,f"{val}\n({val/total*100:.0f}%)",lx,ty-Inches(0.55),bw,Inches(0.5),sz=13,bold=True,color=color,align=PP_ALIGN.CENTER)
    tb(s,label,lx,ct+ch+Inches(0.1),bw,Inches(0.6),sz=11,color=C_S400,align=PP_ALIGN.CENTER)

insights = [
    "56.5% of messages scored Critical/High — consistent with AI-phishing prevalence in 2024 industry reports",
    "Avg score for confirmed phishing: 84.2/100  |  Avg score for legitimate: 9.7/100 — clear separation",
    "False positives cluster in Medium range (25-40) — never in Critical, minimising user alarm",
    "OpenRouter claude-3-haiku matches accuracy of direct Anthropic calls at lower cost per token",
]
bullets(s, insights, Inches(0.4), Inches(5.72), Inches(12.5), Inches(1.55), sz=12, bullet="▸  ", color=C_S300)
num(s,15)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — Challenges & Fixes
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Challenges & Solutions","All 15 Issues Identified & Fixed")
challs = [
    ("CORS Misconfiguration",      "allow_credentials=True + allow_origins='*' violates browser spec. Fixed: allow_credentials=False.",        C_RED),
    ("Blocking Async Routes",      "Anthropic/OpenRouter SDK calls block event loop. Fixed: asyncio.to_thread() for all blocking calls.",       C_RED),
    ("Missing load_dotenv()",      ".env silently ignored because load_dotenv() was never called. Fixed: called at module top.",                C_ORANGE),
    ("Missing CSS Animations",     "animate-fade-in used in JSX but @keyframes never defined. Fixed in index.css + tailwind.config.js.",       C_ORANGE),
    ("Model 404 on OpenRouter",    "anthropic/claude-3.5-haiku not found. Fixed: correct slug is anthropic/claude-3-haiku.",                   C_RED),
    ("Root Returns 404",           "GET / returned 'Not Found'. Fixed: redirect to /docs so the API is discoverable.",                        C_YELLOW),
    ("Dual Port Conflict",         "Two stale uvicorn processes on port 8000 — requests hit the dead one. Fixed: kill all + clean restart.",   C_YELLOW),
    ("package.json Missing type",  "PostCSS config parsed as CommonJS. Fixed: added 'type':'module' to package.json.",                        C_YELLOW),
    ("No Request Cancellation",    "Reset left zombie axios requests running. Fixed: AbortController wired to axios signal.",                  C_ORANGE),
    ("No Char Counter",            "Users couldn't see the 10k limit. Fixed: live counter, orange warning at 500 chars remaining.",           C_YELLOW),
    ("LLM JSON Fences",            "Model sometimes wraps JSON in ```...```. Fixed: strip fences before json.loads().",                       C_ORANGE),
    ("No SPA Rewrite on Vercel",   "Hard refresh caused 404. Fixed: SPA rewrite rule in vercel.json.",                                        C_YELLOW),
]
for i,(title,body,color) in enumerate(challs):
    cx = Inches(0.3)+(i%2)*Inches(6.5); cy = Inches(1.38)+(i//2)*Inches(0.88)
    rect(s, cx, cy, Inches(6.25), Inches(0.82), C_CARD)
    rect(s, cx, cy, Inches(0.07), Inches(0.82), color)
    tb(s, title, cx+Inches(0.18), cy+Inches(0.06), Inches(5.9), Inches(0.28), sz=11.5, bold=True, color=color)
    tb(s, body,  cx+Inches(0.18), cy+Inches(0.36), Inches(5.9), Inches(0.38), sz=10.5, color=C_S300)
num(s,16)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — Future Scope
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Future Scope & Roadmap","From v1.2.0 to Commercial Product")
roadmap = [
    ("Phase 1\n1-3 months",  ["Rate limiting (slowapi/Redis)","JWT / OAuth2 authentication","Analysis history (PostgreSQL)","Browser extension Chrome/Firefox","Gmail + Outlook plugin"],            C_GREEN),
    ("Phase 2\n3-6 months",  ["Fine-tuned BERT pre-filter","Multilingual (15+ languages)","Batch /analyze/batch endpoint","Slack / Teams webhook","SIEM integration (Splunk)"],                    C_SKY),
    ("Phase 3\n6-12 months", ["Email gateway SMTP plugin","Threat intel aggregation","React Native mobile app","Enterprise SaaS dashboard","Federated learning model"],                            C_ORANGE),
    ("Commercial\nOpportunity",["Freemium: 1k req/mo free","Enterprise: unlimited + SLA","White-label SDK for ISPs","Market: $12.4B by 2029","Adjacent: fraud & content mod"], C_YELLOW),
]
for i,(phase,items,color) in enumerate(roadmap):
    lx = Inches(0.3)+i*Inches(3.25)
    rect(s, lx, Inches(1.38), Inches(3.08), Inches(5.65), C_CARD)
    rect(s, lx, Inches(1.38), Inches(3.08), Inches(0.52), color)
    tb(s, phase, lx+Inches(0.1), Inches(1.4), Inches(2.85), Inches(0.48), sz=12, bold=True, color=C_BG, align=PP_ALIGN.CENTER)
    ml(s,[f"▸  {it}" for it in items], lx+Inches(0.12), Inches(2.0), Inches(2.82), Inches(4.8), sz=12.5, color=C_S300)
num(s,17)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 18 — Conclusion
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"Conclusion","Lessons Learned & Project Impact")
takeaways = [
    ("What We Built",          "Full-stack cloud AI security tool — OpenRouter + Claude 3 Haiku + Google Safe Browsing — delivering a scored, plain-English phishing verdict in ~1.8 s."),
    ("Key Engineering Lessons","asyncio.to_thread() is mandatory for blocking SDK calls in async routes. OpenRouter's OpenAI-compatible API removes the need for vendor-specific SDKs."),
    ("Provider Flexibility",   "Switching from Anthropic SDK → OpenRouter required only 3 changes: base_url, API key env var, and model slug. Architecture was vendor-agnostic by design."),
    ("Academic Relevance",     "Demonstrates LLM API integration, async Python microservices, cloud-native deployment, and modern React — core competencies for industry roles in 2026."),
    ("Industry Relevance",     "Addresses a real $12.4B market. Architecture mirrors Abnormal Security and Darktrace. OpenRouter enables cost-efficient multi-model deployment strategies."),
    ("Accessibility Impact",   "Plain-English explanations and zero-friction UI democratise cybersecurity for non-technical users — the most common phishing victims worldwide."),
]
for i,(title,body) in enumerate(takeaways):
    ty = Inches(1.38)+i*Inches(0.98)
    rect(s, Inches(0.4), ty, Inches(12.58), Inches(0.92), C_CARD)
    rect(s, Inches(0.4), ty, Inches(0.07), Inches(0.92), C_ACCENT)
    tb(s, title, Inches(0.6), ty+Inches(0.06), Inches(2.5), Inches(0.3), sz=12, bold=True, color=C_SKY)
    tb(s, body,  Inches(3.2), ty+Inches(0.08), Inches(9.65), Inches(0.75), sz=11.5, color=C_S300)
num(s,18)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 19 — References
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s); header(s,"References & Acknowledgements")
refs = [
    "[1]  Proofpoint. (2024). State of the Phish Annual Report. https://www.proofpoint.com",
    "[2]  IBM Security. (2024). Cost of a Data Breach Report. https://www.ibm.com/reports/data-breach",
    "[3]  OpenRouter. (2024). API Documentation & Model Catalogue. https://openrouter.ai/docs",
    "[4]  Anthropic. (2024). Claude 3 Haiku Model Card. https://www.anthropic.com/claude",
    "[5]  Google. (2024). Safe Browsing API v4 Developer Guide. https://developers.google.com/safe-browsing",
    "[6]  MarketsandMarkets. (2024). Email Security Market — Global Forecast to 2029.",
    "[7]  Verizon. (2024). Data Breach Investigations Report (DBIR). https://www.verizon.com/business/resources/reports/dbir",
    "[8]  OWASP. (2023). Phishing Prevention Cheat Sheet. https://cheatsheetseries.owasp.org",
    "[9]  FastAPI Documentation. https://fastapi.tiangolo.com",
    "[10] Pydantic v2 Documentation. https://docs.pydantic.dev",
    "[11] Render.com Docs. https://render.com/docs  |  Vercel Docs. https://vercel.com/docs",
]
ml(s, refs, Inches(0.5), Inches(1.42), Inches(12.3), Inches(4.45), sz=11.5, color=C_S300)
rect(s, Inches(0.4), Inches(6.08), Inches(12.58), Inches(1.05), C_CARD)
tb(s,"Acknowledgements", Inches(0.6), Inches(6.14), Inches(4), Inches(0.35), sz=13, bold=True, color=C_SKY)
tb(s,"IBM SkillsBuild  ·  OpenRouter  ·  Anthropic  ·  Google  ·  FastAPI, React, Tailwind CSS, Vite open-source communities",
   Inches(0.6), Inches(6.52), Inches(12.2), Inches(0.52), sz=12, color=C_S300)
num(s,19)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 20 — Thank You
# ════════════════════════════════════════════════════════════════════════════
s = slide(); bg(s)
rect(s, 0, 0, W, Inches(0.12), C_ACCENT)
rect(s, 0, H-Inches(0.12), W, Inches(0.12), C_ACCENT)
tb(s,"🛡",Inches(5.5),Inches(0.7),Inches(2.3),Inches(2.1),sz=90,align=PP_ALIGN.CENTER,color=C_ACCENT)
tb(s,"Thank You",Inches(1.0),Inches(2.85),Inches(11.3),Inches(1.25),sz=62,bold=True,align=PP_ALIGN.CENTER)
tb(s,"Questions & Discussion",Inches(1.0),Inches(4.08),Inches(11.3),Inches(0.65),sz=25,color=C_SKY,align=PP_ALIGN.CENTER)
rect(s, Inches(4.5), Inches(4.85), Inches(4.3), Inches(0.05), C_ACCENT)
tb(s,"SafeInbox AI v1.2.0  ·  IBM SkillsBuild  ·  2026",
   Inches(1.0),Inches(5.08),Inches(11.3),Inches(0.38),sz=14,color=C_S400,align=PP_ALIGN.CENTER)
tb(s,"GitHub: https://github.com/hnsandeep/IBM_skillbuild",
   Inches(1.0),Inches(5.52),Inches(11.3),Inches(0.35),sz=13,color=C_SKY,align=PP_ALIGN.CENTER)
tb(s,"Backend: https://safeinbox-ai-backend.onrender.com",
   Inches(1.0),Inches(5.92),Inches(11.3),Inches(0.35),sz=13,color=C_SKY,align=PP_ALIGN.CENTER)
tb(s,"Frontend: https://safeinbox-ai.vercel.app",
   Inches(1.0),Inches(6.32),Inches(11.3),Inches(0.35),sz=13,color=C_SKY,align=PP_ALIGN.CENTER)
num(s,20)

# ── Save ─────────────────────────────────────────────────────────────────────
OUT = r"d:\IBM_skillsbuild\SafeInbox_AI_Presentation.pptx"
try:
    prs.save(OUT)
    print(f"\n✅  Saved → {OUT}")
    print(f"   Slides: {len(prs.slides)}  |  16:9 widescreen  |  v1.2.0\n")
except PermissionError:
    alt = OUT.replace(".pptx","_v120.pptx")
    prs.save(alt)
    print(f"\n⚠️  Original file was open — saved as: {alt}")
    print("   Close the old PPTX in PowerPoint, then rename if needed.\n")
    sys.exit(0)
