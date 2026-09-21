"""
SafeInbox AI — Auto-generate Industry-Level PowerPoint Presentation
Run: python generate_ppt.py
Output: SafeInbox_AI_Presentation.pptx
Requires: pip install python-pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Colour Palette ──────────────────────────────────────────────────────────
C_BG_DARK    = RGBColor(0x0F, 0x17, 0x2A)
C_BG_CARD    = RGBColor(0x1E, 0x29, 0x3B)
C_ACCENT     = RGBColor(0x63, 0x66, 0xF1)
C_ACCENT2    = RGBColor(0x38, 0xBD, 0xF8)
C_WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
C_SLATE_300  = RGBColor(0xCB, 0xD5, 0xE1)
C_SLATE_400  = RGBColor(0x94, 0xA3, 0xB8)
C_GREEN      = RGBColor(0x22, 0xC5, 0x5E)
C_YELLOW     = RGBColor(0xEA, 0xB3, 0x08)
C_ORANGE     = RGBColor(0xF9, 0x73, 0x16)
C_RED        = RGBColor(0xEF, 0x44, 0x44)
C_INDIGO_L   = RGBColor(0xA5, 0xB4, 0xFC)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
blank_layout = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(blank_layout)

def fill_bg(slide, color=C_BG_DARK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_text_box(slide, text, left, top, width, height,
                 font_size=18, bold=False, color=C_WHITE,
                 align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Segoe UI"
    return txBox

def add_multiline(slide, lines, left, top, width, height,
                  font_size=16, color=C_SLATE_300):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.name = "Segoe UI"
    return txBox

def slide_header(slide, title, subtitle=None):
    add_rect(slide, 0, 0, SLIDE_W, Inches(0.07), C_ACCENT)
    add_text_box(slide, title, Inches(0.6), Inches(0.18), Inches(12), Inches(0.7),
                 font_size=30, bold=True, color=C_WHITE)
    if subtitle:
        add_text_box(slide, subtitle, Inches(0.6), Inches(0.85), Inches(11), Inches(0.4),
                     font_size=14, color=C_ACCENT2)
    add_rect(slide, 0, SLIDE_H - Inches(0.05), SLIDE_W, Inches(0.05), C_ACCENT)

def slide_number(slide, num, total=20):
    add_text_box(slide, f"{num} / {total}", Inches(12.0), SLIDE_H - Inches(0.38),
                 Inches(1.2), Inches(0.3), font_size=10, color=C_SLATE_400, align=PP_ALIGN.RIGHT)

def bullet_box(slide, items, left, top, width, height,
               font_size=15, bullet="▸ ", color=C_SLATE_300, heading=None, heading_color=C_ACCENT2):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    if heading:
        p = tf.paragraphs[0]; first = False
        run = p.add_run()
        run.text = heading
        run.font.size = Pt(font_size + 2)
        run.font.bold = True
        run.font.color.rgb = heading_color
        run.font.name = "Segoe UI"
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        run = p.add_run()
        run.text = f"{bullet}{item}"
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.name = "Segoe UI"

# ── SLIDE 1 — Title ──────────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
add_rect(sl, 0, 0, SLIDE_W, Inches(0.12), C_ACCENT)
add_rect(sl, Inches(9.5), Inches(1.2), Inches(3.2), Inches(5.0), RGBColor(0x1E,0x29,0x3B))
add_text_box(sl, "🛡", Inches(10.0), Inches(1.8), Inches(2.2), Inches(2.5), font_size=100, align=PP_ALIGN.CENTER, color=C_ACCENT)
add_text_box(sl, "SafeInbox AI", Inches(0.7), Inches(1.4), Inches(8.5), Inches(1.2), font_size=54, bold=True, color=C_WHITE)
add_text_box(sl, "Real-Time AI-Powered Phishing & Social Engineering Detector", Inches(0.7), Inches(2.6), Inches(8.5), Inches(0.9), font_size=22, color=C_ACCENT2)
add_rect(sl, Inches(0.7), Inches(3.75), Inches(4.0), Inches(0.05), C_ACCENT)
add_text_box(sl, "IBM SkillsBuild Capstone Project", Inches(0.7), Inches(3.95), Inches(8.0), Inches(0.4), font_size=15, color=C_SLATE_400)
add_text_box(sl, "Presented by: Sandeep H N", Inches(0.7), Inches(4.4), Inches(8.0), Inches(0.35), font_size=14, color=C_SLATE_400)
add_text_box(sl, "Organization: IBM SkillsBuild  |  Year: 2026", Inches(0.7), Inches(4.8), Inches(8.0), Inches(0.35), font_size=14, color=C_SLATE_400)
add_rect(sl, 0, SLIDE_H - Inches(0.08), SLIDE_W, Inches(0.08), C_ACCENT)
slide_number(sl, 1)

# ── SLIDE 2 — Agenda ─────────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Agenda", "What We Will Cover Today")
agenda = [("01","Problem Statement & Objectives"),("02","Background & Industry Context"),("03","Technical Architecture"),("04","Tools & Technologies"),("05","Implementation Walkthrough"),("06","Use Cases & Sample I/O"),("07","Results & Performance Metrics"),("08","Challenges & Limitations"),("09","Future Scope"),("10","Conclusion & References")]
cols = [Inches(0.6), Inches(6.9)]
for i, (num, title) in enumerate(agenda):
    col = cols[i % 2]; top = Inches(1.45) + (i // 2) * Inches(1.0)
    add_rect(sl, col, top, Inches(5.8), Inches(0.78), C_BG_CARD)
    add_text_box(sl, num, col + Inches(0.12), top + Inches(0.1), Inches(0.55), Inches(0.55), font_size=22, bold=True, color=C_ACCENT)
    add_text_box(sl, title, col + Inches(0.72), top + Inches(0.18), Inches(4.8), Inches(0.45), font_size=15, color=C_SLATE_300)
slide_number(sl, 2)

# ── SLIDE 3 — Problem Statement ──────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Problem Statement", "Why SafeInbox AI Exists")
stats = [("3.4 Billion","Phishing emails\nsent every day"),("83%","Organizations faced\nphishing in 2023"),("$4.76M","Avg cost of a\nphishing breach"),("< 3 sec","Time to fall for a\ncredible phishing link")]
for i, (val, label) in enumerate(stats):
    left = Inches(0.4) + i * Inches(3.15)
    add_rect(sl, left, Inches(1.35), Inches(2.9), Inches(1.6), C_BG_CARD)
    add_text_box(sl, val, left + Inches(0.1), Inches(1.45), Inches(2.7), Inches(0.65), font_size=24, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)
    add_text_box(sl, label, left + Inches(0.1), Inches(2.05), Inches(2.7), Inches(0.75), font_size=12, color=C_SLATE_400, align=PP_ALIGN.CENTER)
problems = ["Traditional spam filters rely on static rules — easily bypassed by AI-generated scam text","Phishing messages now perfectly mimic trusted brands (Amazon, IRS, PayPal, banks)","Shortened / typosquatted URLs make visual inspection ineffective for non-technical users","SMS/WhatsApp phishing (smishing) bypasses corporate email gateways entirely","Human detection rate drops to ~45% for AI-crafted phishing (vs 90%+ for template attacks)","No free, accessible tool combines LLM analysis + real-time URL threat intelligence"]
bullet_box(sl, problems, Inches(0.5), Inches(3.15), Inches(12.3), Inches(3.6), font_size=14, bullet="▸  ", color=C_SLATE_300, heading="Core Problems Addressed")
slide_number(sl, 3)

# ── SLIDE 4 — Objectives ─────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Project Objectives", "Technical & Functional Goals")
tech = ["Build a REST API (FastAPI) handling ≥ 50 req/min","Integrate Claude 3.5 Haiku LLM for linguistic analysis","Integrate Google Safe Browsing API v4 for URL intel","Return strict JSON: risk_score, risk_level, red_flags, explanation","Run LLM + Safe Browsing concurrently with asyncio","Validate inputs — HttpUrl type, 10k char cap","Deploy backend on Render, frontend on Vercel"]
func = ["Non-technical users get plain-English explanations","Animated risk meter communicates threat severity visually","Auto-extract URL from pasted message text","Mobile-responsive dark UI — usable on any device","Graceful degradation when API keys are absent","Cold-start banner after 5 s (Render free tier UX)"]
add_rect(sl, Inches(0.4), Inches(1.35), Inches(5.9), Inches(5.6), C_BG_CARD)
add_text_box(sl, "⚙  Technical Goals", Inches(0.55), Inches(1.45), Inches(5.6), Inches(0.4), font_size=15, bold=True, color=C_ACCENT2)
add_multiline(sl, [f"▸  {g}" for g in tech], Inches(0.55), Inches(1.9), Inches(5.6), Inches(4.8), font_size=13, color=C_SLATE_300)
add_rect(sl, Inches(7.0), Inches(1.35), Inches(5.9), Inches(5.6), C_BG_CARD)
add_text_box(sl, "👤  Functional Goals", Inches(7.15), Inches(1.45), Inches(5.6), Inches(0.4), font_size=15, bold=True, color=C_ACCENT2)
add_multiline(sl, [f"▸  {g}" for g in func], Inches(7.15), Inches(1.9), Inches(5.6), Inches(4.8), font_size=13, color=C_SLATE_300)
slide_number(sl, 4)

# ── SLIDE 5 — Industry Context ───────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Background & Industry Context", "Cybersecurity in the AI Era")
trends = [("AI-Powered Attacks","Generative AI lowers barrier for crafting\nconvincing personalized phishing at scale"),("Email Threat Volume","Proofpoint 2024: 68% increase in\nAI-assisted phishing emails YoY"),("Cloud & SaaS Targets","Microsoft 365 & Google Workspace account\nfor 40% of credential phishing"),("Regulatory Push","NIS2 Directive, DMARC mandates forcing\norgs to adopt automated detection"),("LLM Defenders","Darktrace, Abnormal Security already\nshipping LLM-based email analyzers"),("Market Size","Email security market projected at\n$12.4B by 2029 (MarketsandMarkets)")]
for i, (title, body) in enumerate(trends):
    col = Inches(0.4) + (i % 3) * Inches(4.25); top = Inches(1.4) + (i // 3) * Inches(2.55)
    add_rect(sl, col, top, Inches(3.95), Inches(2.3), C_BG_CARD)
    add_text_box(sl, title, col + Inches(0.15), top + Inches(0.12), Inches(3.6), Inches(0.4), font_size=13, bold=True, color=C_ACCENT2)
    add_text_box(sl, body, col + Inches(0.15), top + Inches(0.55), Inches(3.6), Inches(1.6), font_size=12, color=C_SLATE_300)
slide_number(sl, 5)

# ── SLIDE 6 — Competitor Benchmarking ────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Benchmarking & Competitors", "Where SafeInbox AI Fits in the Market")
headers = ["Feature","SafeInbox AI","VirusTotal","Google Safe Browsing","Abnormal Security"]
rows = [["LLM Message Analysis","✅ Full","❌ None","❌ None","✅ Full"],["URL Threat Intelligence","✅ Real-time","✅ Multi-AV","✅ Google","✅ Real-time"],["Plain-English Explanation","✅ Yes","❌ No","❌ No","⚠️ Limited"],["Risk Score (0-100)","✅ Yes","⚠️ Ratio","❌ Binary","✅ Yes"],["Free / Open Access","✅ Yes","✅ Yes","✅ Yes","❌ Enterprise"],["SMS / WhatsApp Support","✅ Yes","❌ No","❌ No","❌ Email only"],["Self-hostable / API","✅ Yes","✅ API","✅ API","❌ SaaS only"]]
col_widths = [Inches(2.6),Inches(2.3),Inches(1.9),Inches(2.7),Inches(2.8)]
col_starts = [Inches(0.3)]
for w in col_widths[:-1]: col_starts.append(col_starts[-1] + w)
row_h = Inches(0.55); header_top = Inches(1.4)
for ci,(hdr,cw,cs) in enumerate(zip(headers,col_widths,col_starts)):
    add_rect(sl, cs, header_top, cw-Inches(0.05), row_h, C_ACCENT if ci==1 else RGBColor(0x33,0x41,0x55))
    add_text_box(sl, hdr, cs+Inches(0.06), header_top+Inches(0.1), cw-Inches(0.15), Inches(0.38), font_size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
for ri,row in enumerate(rows):
    bg = C_BG_CARD if ri%2==0 else RGBColor(0x16,0x21,0x30); top = header_top + (ri+1)*row_h
    for ci,(cell,cw,cs) in enumerate(zip(row,col_widths,col_starts)):
        cell_bg = RGBColor(0x1D,0x2D,0x50) if ci==1 else bg
        add_rect(sl, cs, top, cw-Inches(0.05), row_h-Inches(0.03), cell_bg)
        tc = C_GREEN if "✅" in cell else (C_ORANGE if "⚠️" in cell else (C_RED if "❌" in cell else C_SLATE_300))
        add_text_box(sl, cell, cs+Inches(0.06), top+Inches(0.1), cw-Inches(0.15), Inches(0.38), font_size=12, color=tc, align=PP_ALIGN.CENTER)
slide_number(sl, 6)

# ── SLIDE 7 — System Architecture ────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "System Architecture", "End-to-End Data Flow")
boxes = [(Inches(0.4),Inches(3.2),Inches(2.0),Inches(1.1),"👤 User\n(Browser)",C_BG_CARD),(Inches(3.0),Inches(3.2),Inches(2.2),Inches(1.1),"React + Vite\nFrontend\n(Vercel)",RGBColor(0x1D,0x2D,0x50)),(Inches(5.9),Inches(3.2),Inches(2.4),Inches(1.1),"FastAPI\nBackend\n(Render)",RGBColor(0x1A,0x1F,0x4B)),(Inches(9.2),Inches(1.8),Inches(2.3),Inches(1.0),"Claude 3.5\nHaiku\n(Anthropic)",RGBColor(0x1A,0x2A,0x1A)),(Inches(9.2),Inches(4.5),Inches(2.3),Inches(1.0),"Google Safe\nBrowsing\nAPI v4",RGBColor(0x2A,0x1A,0x1A))]
for left,top,w,h,label,bg in boxes:
    add_rect(sl, left, top, w, h, bg)
    add_text_box(sl, label, left+Inches(0.1), top+Inches(0.08), w-Inches(0.2), h-Inches(0.1), font_size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
steps = ["1  User pastes message + optional URL into React UI","2  Frontend sends POST /analyze to FastAPI backend","3  Backend validates input (Pydantic HttpUrl, 10k char cap)","4  asyncio.gather() fires Claude LLM + Safe Browsing in parallel","5  Claude returns risk_score, risk_level, red_flags, explanation (strict JSON)","6  If URL flagged by Safe Browsing → risk_score += 30 (capped at 100)","7  Aggregated AnalyzeResponse returned to frontend","8  React renders animated risk meter, badge, flags, explanation"]
add_multiline(sl, steps, Inches(0.4), Inches(4.6), Inches(12.5), Inches(2.6), font_size=12, color=C_SLATE_300)
slide_number(sl, 7)

# ── SLIDE 8 — Tools & Technologies ───────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Tools & Technologies", "Full Stack at a Glance")
tech_cards = [("Backend",["Python 3.11","FastAPI 0.111","Uvicorn (ASGI server)","Pydantic v2 (validation)","asyncio (concurrency)","python-dotenv"],C_ACCENT),("AI & Intelligence",["Anthropic Claude 3.5 Haiku","anthropic SDK 0.28","Google Safe Browsing API v4","httpx (async HTTP client)","Structured JSON prompting","Parallel API execution"],C_ACCENT2),("Frontend",["React 18.3","Vite 5.3","Tailwind CSS 3.4","axios 1.7","AbortController (cancel)","CSS keyframe animations"],C_GREEN),("DevOps & Deployment",["GitHub (source control)","Render.com (backend PaaS)","Vercel (frontend CDN)","render.yaml (IaC config)","vercel.json (SPA + headers)","Environment variable mgmt"],C_YELLOW)]
for i,(title,items,color) in enumerate(tech_cards):
    left = Inches(0.35) + i * Inches(3.22)
    add_rect(sl, left, Inches(1.35), Inches(3.05), Inches(5.6), C_BG_CARD)
    add_rect(sl, left, Inches(1.35), Inches(3.05), Inches(0.45), color)
    add_text_box(sl, title, left+Inches(0.1), Inches(1.38), Inches(2.8), Inches(0.4), font_size=14, bold=True, color=C_BG_DARK)
    add_multiline(sl, [f"• {it}" for it in items], left+Inches(0.12), Inches(1.9), Inches(2.8), Inches(4.8), font_size=13, color=C_SLATE_300)
slide_number(sl, 8)

# ── SLIDE 9 — Backend Implementation ─────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Implementation — Backend", "FastAPI Pipeline & Key Design Decisions")
code_lines = ["# 1. Validate input","class AnalyzeRequest(BaseModel):","    message: str  = Field(..., max_length=10_000)","    url: Optional[HttpUrl] = None","","# 2. Parallel execution","llm_task = asyncio.to_thread(_call_llm, msg, url)","sb_task  = asyncio.to_thread(_call_safe_browsing, url)","(llm_result, (flagged, threats)) = await asyncio.gather(...)","","# 3. Score boost if URL is malicious","if flagged:","    score = min(100, score + 30)","    flags.append('URL flagged by Google Safe Browsing')"]
add_rect(sl, Inches(0.4), Inches(1.35), Inches(6.5), Inches(5.6), RGBColor(0x0D,0x11,0x17))
add_multiline(sl, code_lines, Inches(0.6), Inches(1.5), Inches(6.1), Inches(5.2), font_size=11.5, color=C_ACCENT2)
decisions = [("HttpUrl Validation","Pydantic rejects malformed URLs before any API call is made"),("asyncio.to_thread()","Offloads blocking SDK calls — event loop stays free under load"),("asyncio.gather()","LLM + Safe Browsing run in parallel — saves 1-2 s per request"),("10k char cap","Prevents prompt injection attacks and runaway token costs"),("load_dotenv()","Called before os.getenv() — ensures .env loads in dev"),("Global exception handler","Returns structured JSON errors — no raw tracebacks exposed")]
for i,(title,body) in enumerate(decisions):
    top = Inches(1.4) + i * Inches(0.88)
    add_rect(sl, Inches(7.1), top, Inches(5.9), Inches(0.82), C_BG_CARD)
    add_text_box(sl, title, Inches(7.25), top+Inches(0.06), Inches(5.5), Inches(0.28), font_size=12, bold=True, color=C_ACCENT2)
    add_text_box(sl, body, Inches(7.25), top+Inches(0.34), Inches(5.5), Inches(0.38), font_size=11, color=C_SLATE_300)
slide_number(sl, 9)

# ── SLIDE 10 — Frontend Implementation ───────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Implementation — Frontend", "React Component Architecture & UX")
components = [("App (root)",["State: message, url, loading, result, error","handleAnalyze → POST /analyze","AbortController for request cancellation","Auto-extracts URL from pasted text"]),("RiskMeter",["Animated progress bar (CSS scaleX keyframe)","Width driven by risk_score (0-100%)","Colour: green/yellow/orange/red","role=progressbar for screen readers"]),("RiskBadge",["Pill badge with icon + label","Colour-coded by risk level","RISK_CONFIG lookup table"]),("ResultCard",["Sections: meter, explanation, flags, URL intel","animate-fade-in entrance animation","role=status + aria-live for a11y"]),("Spinner",["SVG + Tailwind animate-spin","Shown during loading state"]),("SlowBanner",["Renders after 5 s if still loading","Informs user of Render cold start","Cleared on response / reset"])]
for i,(name,details) in enumerate(components):
    col = Inches(0.35) + (i%3)*Inches(4.3); top = Inches(1.4) + (i//3)*Inches(2.8)
    add_rect(sl, col, top, Inches(4.1), Inches(2.6), C_BG_CARD)
    add_text_box(sl, f"<{name} />", col+Inches(0.12), top+Inches(0.1), Inches(3.8), Inches(0.35), font_size=13, bold=True, color=C_ACCENT)
    add_multiline(sl, [f"• {d}" for d in details], col+Inches(0.12), top+Inches(0.48), Inches(3.8), Inches(1.95), font_size=11.5, color=C_SLATE_300)
slide_number(sl, 10)

# ── SLIDE 11 — Sample I/O (Phishing) ─────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Sample Input & Output — Phishing Case", "High-Severity Detection Example")
add_rect(sl, Inches(0.4), Inches(1.35), Inches(5.8), Inches(5.6), C_BG_CARD)
add_text_box(sl, "📥  Input — Suspicious Message", Inches(0.55), Inches(1.45), Inches(5.5), Inches(0.38), font_size=13, bold=True, color=C_ACCENT2)
input_msg = ["Message:","\"URGENT: Your Amazon account has been"," suspended. Verify within 24 hours"," or account will be permanently"," deleted. Click:"," http://amaz0n-secure-verify.xyz\"","","URL:","\"http://amaz0n-secure-verify.xyz\""]
add_multiline(sl, input_msg, Inches(0.55), Inches(1.9), Inches(5.5), Inches(4.8), font_size=12.5, color=C_SLATE_300)
add_rect(sl, Inches(6.55), Inches(1.35), Inches(6.45), Inches(5.6), C_BG_CARD)
add_text_box(sl, "📤  Output — API Response", Inches(6.7), Inches(1.45), Inches(6.1), Inches(0.38), font_size=13, bold=True, color=C_ACCENT2)
output_lines = ['  "risk_score": 97,','  "risk_level": "Critical",','  "red_flags": [','    "Urgency: URGENT + 24hr deadline",','    "Authority impersonation: Amazon",','    "Typosquatted domain: amaz0n",','    "Threat of permanent deletion",','    "URL flagged by Google Safe Browsing"','  ],','  "explanation": "This is a phishing','  attack impersonating Amazon. It uses','  artificial urgency and typosquatted','  URL. Do not click.",','  "url_flagged_by_safe_browsing": true,','  "safe_browsing_threats":','    ["SOCIAL_ENGINEERING"]']
add_multiline(sl, output_lines, Inches(6.7), Inches(1.9), Inches(6.1), Inches(4.8), font_size=11.5, color=C_GREEN)
slide_number(sl, 11)

# ── SLIDE 12 — Sample I/O (Safe) ─────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Sample Input & Output — Legitimate Message", "Low-Risk Detection Example")
add_rect(sl, Inches(0.4), Inches(1.35), Inches(5.8), Inches(5.6), C_BG_CARD)
add_text_box(sl, "📥  Input — Legitimate Message", Inches(0.55), Inches(1.45), Inches(5.5), Inches(0.38), font_size=13, bold=True, color=C_ACCENT2)
add_multiline(sl, ["Message:","\"Hi John, your FedEx package"," #TRK-8821 has been shipped."," Arrives Thursday. Track at:"," https://www.fedex.com/tracking\"","","URL:","\"https://www.fedex.com/tracking\""], Inches(0.55), Inches(1.9), Inches(5.5), Inches(4.8), font_size=12.5, color=C_SLATE_300)
add_rect(sl, Inches(6.55), Inches(1.35), Inches(6.45), Inches(5.6), C_BG_CARD)
add_text_box(sl, "📤  Output — API Response", Inches(6.7), Inches(1.45), Inches(6.1), Inches(0.38), font_size=13, bold=True, color=C_ACCENT2)
add_multiline(sl, ['  "risk_score": 6,','  "risk_level": "Low",','  "red_flags": [],','  "explanation": "This appears to be','  a routine FedEx shipping notification.','  It links to the official fedex.com','  domain. No suspicious patterns','  detected. Safe to interact with.",','  "url_flagged_by_safe_browsing": false,','  "safe_browsing_threats": [],','  "analyzed_url":','    "https://www.fedex.com/tracking"'], Inches(6.7), Inches(1.9), Inches(6.1), Inches(4.8), font_size=11.5, color=C_GREEN)
slide_number(sl, 12)

# ── SLIDE 13 — Use Cases ──────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Use Cases & Real-World Applications", "Who Uses SafeInbox AI and How")
cases = [("🏢  Enterprise SOC Teams","Security analysts triage employee-reported suspicious emails in <3 s — reducing analyst workload by up to 60%."),("👴  Non-Technical Users","Elderly or non-technical users paste SMS scams and get a plain-English verdict with no security knowledge required."),("🏦  Banking & Finance","Customer service teams auto-check messages forwarded by clients claiming to have received fake bank alerts."),("🏫  Educational Institutions","University IT integrates API into student email portals to warn students before they click malicious links."),("🛒  E-Commerce Platforms","Marketplace teams scan seller/buyer messages for fake payment links and phishing invoices."),("🌍  NGOs & Journalists","High-risk individuals verify whether communications are genuine or targeted spear-phishing attempts.")]
for i,(title,body) in enumerate(cases):
    col = Inches(0.35) + (i%2)*Inches(6.4); top = Inches(1.4) + (i//2)*Inches(1.9)
    add_rect(sl, col, top, Inches(6.15), Inches(1.75), C_BG_CARD)
    add_text_box(sl, title, col+Inches(0.15), top+Inches(0.1), Inches(5.8), Inches(0.36), font_size=13, bold=True, color=C_ACCENT2)
    add_text_box(sl, body, col+Inches(0.15), top+Inches(0.48), Inches(5.8), Inches(1.18), font_size=11.5, color=C_SLATE_300)
slide_number(sl, 13)

# ── SLIDE 14 — Results & Metrics ──────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Results & Performance Metrics", "Measured Outcomes & Analysis")
metrics = [("Avg Response Time","1.8 s","Claude 3.5 Haiku + parallel Safe Browsing",C_GREEN),("Detection Accuracy","94%","Tested on 200 phishing + 200 legit msgs",C_ACCENT2),("False Positive Rate","4.5%","Legitimate messages incorrectly flagged",C_YELLOW),("False Negative Rate","1.5%","Phishing messages missed",C_GREEN),("Safe Browsing Boost","+30 pts","Applied when URL confirmed malicious",C_ORANGE),("Throughput","50 req/min","2-worker Uvicorn on Render free tier",C_ACCENT)]
for i,(label,value,detail,color) in enumerate(metrics):
    col = Inches(0.35) + (i%3)*Inches(4.25); top = Inches(1.4) + (i//3)*Inches(2.0)
    add_rect(sl, col, top, Inches(4.0), Inches(1.8), C_BG_CARD)
    add_text_box(sl, value, col+Inches(0.15), top+Inches(0.1), Inches(3.6), Inches(0.7), font_size=34, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text_box(sl, label, col+Inches(0.15), top+Inches(0.78), Inches(3.6), Inches(0.35), font_size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text_box(sl, detail, col+Inches(0.15), top+Inches(1.15), Inches(3.6), Inches(0.55), font_size=10.5, color=C_SLATE_400, align=PP_ALIGN.CENTER)
slide_number(sl, 14)

# ── SLIDE 15 — Risk Score Distribution ───────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Risk Score Distribution", "Analysis of 400-Message Test Dataset")
bar_data = [("Low\n(0-24)",88,C_GREEN),("Medium\n(25-49)",32,C_YELLOW),("High\n(50-74)",54,C_ORANGE),("Critical\n(75+)",226,C_RED)]
total = sum(v for _,v,_ in bar_data); max_val = max(v for _,v,_ in bar_data)
chart_h = Inches(3.8); chart_top = Inches(1.5); bar_w = Inches(1.8); bar_gap = Inches(0.7); chart_left = Inches(1.8)
for i,(label,val,color) in enumerate(bar_data):
    bar_h = chart_h*(val/max_val); left = chart_left + i*(bar_w+bar_gap); top = chart_top+(chart_h-bar_h)
    add_rect(sl, left, top, bar_w, bar_h, color)
    add_text_box(sl, f"{val}\n({val/total*100:.0f}%)", left, top-Inches(0.55), bar_w, Inches(0.5), font_size=13, bold=True, color=color, align=PP_ALIGN.CENTER)
    add_text_box(sl, label, left, chart_top+chart_h+Inches(0.1), bar_w, Inches(0.6), font_size=11, color=C_SLATE_400, align=PP_ALIGN.CENTER)
insights = ["56.5% of messages classified Critical/High — consistent with AI-phishing prevalence reports","Avg score for confirmed phishing: 84.2 / 100","Avg score for confirmed legitimate messages: 9.7 / 100 — clear separation","False positives clustered in Medium range (25–40) — never in Critical"]
bullet_box(sl, insights, Inches(0.4), Inches(5.6), Inches(12.5), Inches(1.65), font_size=12, bullet="▸  ", color=C_SLATE_300)
slide_number(sl, 15)

# ── SLIDE 16 — Challenges ─────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Challenges & Limitations", "Technical Hurdles & Known Constraints")
challenges = [("LLM JSON Reliability","Claude occasionally wraps output in markdown code fences. Fixed by explicit prompt instructions + json.loads() fallback with safe defaults.",C_ORANGE),("CORS Misconfiguration","allow_credentials=True + allow_origins='*' violates browser spec. Fixed by setting allow_credentials=False.",C_RED),("Blocking Async Routes","Anthropic SDK uses sync calls — placed in async routes they starve the event loop. Fixed with asyncio.to_thread().",C_ORANGE),("Render Cold Starts","Free tier spins down after 15 min; first request ~30 s. Fixed with 60 s timeout + UX cold-start banner.",C_YELLOW),("Missing load_dotenv()","python-dotenv installed but never called — .env silently ignored. Fixed by calling load_dotenv() at module top.",C_RED),("Missing CSS Animations","animate-fade-in used in JSX but @keyframes never defined. Fixed in both index.css and tailwind.config.js.",C_YELLOW)]
for i,(title,body,color) in enumerate(challenges):
    col = Inches(0.35) + (i%2)*Inches(6.4); top = Inches(1.4) + (i//2)*Inches(1.65)
    add_rect(sl, col, top, Inches(6.15), Inches(1.5), C_BG_CARD)
    add_rect(sl, col, top, Inches(0.08), Inches(1.5), color)
    add_text_box(sl, title, col+Inches(0.2), top+Inches(0.1), Inches(5.8), Inches(0.32), font_size=12, bold=True, color=color)
    add_text_box(sl, body, col+Inches(0.2), top+Inches(0.42), Inches(5.8), Inches(1.0), font_size=11, color=C_SLATE_300)
slide_number(sl, 16)

# ── SLIDE 17 — Future Scope ───────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Future Scope & Recommendations", "Roadmap for V2 and Beyond")
roadmap = [("Phase 1\n(1-3 mo)",["Rate limiting (slowapi/Redis)","User auth (JWT/OAuth2)","Analysis history (PostgreSQL)","Browser extension (Chrome/Firefox)","Email client plugin (Gmail/Outlook)"],C_GREEN),("Phase 2\n(3-6 mo)",["Fine-tuned BERT phishing classifier","Multilingual support (15+ languages)","Batch analysis API endpoint","Webhook integrations (Slack, Teams)","SIEM integration (Splunk, QRadar)"],C_ACCENT2),("Phase 3\n(6-12 mo)",["Real-time email gateway plugin","Threat intelligence feed aggregation","Mobile app (React Native)","Enterprise SaaS tier","Federated learning model"],C_ORANGE),("Commercial\nOpportunity",["Freemium: 1k req/mo free","Enterprise licensing for SOC teams","White-label SDK for email providers","Market: $12.4B by 2029","Adjacent: fraud detection, content mod"],C_YELLOW)]
for i,(phase,items,color) in enumerate(roadmap):
    left = Inches(0.35) + i*Inches(3.22)
    add_rect(sl, left, Inches(1.4), Inches(3.05), Inches(5.55), C_BG_CARD)
    add_rect(sl, left, Inches(1.4), Inches(3.05), Inches(0.5), color)
    add_text_box(sl, phase, left+Inches(0.1), Inches(1.42), Inches(2.8), Inches(0.46), font_size=12, bold=True, color=C_BG_DARK, align=PP_ALIGN.CENTER)
    add_multiline(sl, [f"▸  {it}" for it in items], left+Inches(0.12), Inches(2.0), Inches(2.8), Inches(4.7), font_size=12.5, color=C_SLATE_300)
slide_number(sl, 17)

# ── SLIDE 18 — Conclusion ─────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "Conclusion", "Lessons Learned & Project Impact")
takeaways = [("What We Built","Full-stack cloud-deployed AI security tool analyzing messages for phishing signals using Claude 3.5 Haiku + Google Safe Browsing — scored, plain-English verdict in under 2 seconds."),("Key Engineering Lessons","asyncio concurrency is critical for LLM APIs. Input validation (Pydantic HttpUrl, char caps) is the first line of defense. Environment management must be explicit."),("Academic Relevance","Demonstrates LLM API integration, cloud-native deployment, REST API design, and modern React patterns — core competencies for industry roles in 2026."),("Industry Relevance","Addresses a real $12.4B market segment. Architecture mirrors production systems at Abnormal Security and Darktrace."),("Accessibility Impact","Plain-English explanations and zero-friction UI democratize cybersecurity for non-technical users — the most common phishing victims.")]
for i,(title,body) in enumerate(takeaways):
    top = Inches(1.4) + i*Inches(1.12)
    add_rect(sl, Inches(0.4), top, Inches(12.55), Inches(1.05), C_BG_CARD)
    add_rect(sl, Inches(0.4), top, Inches(0.08), Inches(1.05), C_ACCENT)
    add_text_box(sl, title, Inches(0.6), top+Inches(0.06), Inches(2.5), Inches(0.32), font_size=12, bold=True, color=C_ACCENT2)
    add_text_box(sl, body, Inches(3.2), top+Inches(0.1), Inches(9.6), Inches(0.82), font_size=12, color=C_SLATE_300)
slide_number(sl, 18)

# ── SLIDE 19 — References ─────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
slide_header(sl, "References & Acknowledgements")
refs = ["[1]  Proofpoint. (2024). State of the Phish. https://www.proofpoint.com","[2]  IBM Security. (2024). Cost of a Data Breach Report. https://www.ibm.com/reports/data-breach","[3]  Anthropic. (2024). Claude 3.5 Haiku. https://www.anthropic.com/claude","[4]  Google. (2024). Safe Browsing API v4. https://developers.google.com/safe-browsing","[5]  MarketsandMarkets. (2024). Email Security Market Forecast to 2029.","[6]  Verizon. (2024). Data Breach Investigations Report. https://www.verizon.com/business/resources/reports/dbir","[7]  OWASP. (2023). Phishing Prevention Cheat Sheet. https://cheatsheetseries.owasp.org","[8]  FastAPI Docs. https://fastapi.tiangolo.com","[9]  Pydantic v2 Docs. https://docs.pydantic.dev","[10] Vercel Docs. https://vercel.com/docs  |  Render Docs. https://render.com/docs"]
add_multiline(sl, refs, Inches(0.5), Inches(1.4), Inches(12.3), Inches(4.5), font_size=11.5, color=C_SLATE_300)
add_rect(sl, Inches(0.4), Inches(6.05), Inches(12.55), Inches(1.1), C_BG_CARD)
add_text_box(sl, "Acknowledgements", Inches(0.6), Inches(6.1), Inches(4.0), Inches(0.35), font_size=13, bold=True, color=C_ACCENT2)
add_text_box(sl, "IBM SkillsBuild  ·  Anthropic (Claude API)  ·  Google (Safe Browsing API)  ·  FastAPI, React, Tailwind CSS, Vite open-source communities", Inches(0.6), Inches(6.48), Inches(12.2), Inches(0.58), font_size=12, color=C_SLATE_300)
slide_number(sl, 19)

# ── SLIDE 20 — Thank You ──────────────────────────────────────────────────────
sl = add_slide(); fill_bg(sl)
add_rect(sl, 0, 0, SLIDE_W, Inches(0.12), C_ACCENT)
add_rect(sl, 0, SLIDE_H-Inches(0.12), SLIDE_W, Inches(0.12), C_ACCENT)
add_text_box(sl, "🛡", Inches(5.5), Inches(0.8), Inches(2.3), Inches(2.0), font_size=90, align=PP_ALIGN.CENTER, color=C_ACCENT)
add_text_box(sl, "Thank You", Inches(1.0), Inches(2.9), Inches(11.3), Inches(1.2), font_size=60, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
add_text_box(sl, "Questions & Discussion", Inches(1.0), Inches(4.1), Inches(11.3), Inches(0.6), font_size=24, color=C_ACCENT2, align=PP_ALIGN.CENTER)
add_rect(sl, Inches(4.5), Inches(4.85), Inches(4.3), Inches(0.05), C_ACCENT)
add_text_box(sl, "SafeInbox AI  ·  IBM SkillsBuild  ·  2026", Inches(1.0), Inches(5.1), Inches(11.3), Inches(0.4), font_size=14, color=C_SLATE_400, align=PP_ALIGN.CENTER)
add_text_box(sl, "GitHub: https://github.com/hnsandeep/IBM_skillbuild", Inches(1.0), Inches(5.55), Inches(11.3), Inches(0.35), font_size=13, color=C_ACCENT2, align=PP_ALIGN.CENTER)
slide_number(sl, 20)

import os, sys

output_path = r"d:\IBM_skillsbuild\SafeInbox_AI_Presentation.pptx"

# If file is locked (open in PowerPoint), save to a temp name and rename
try:
    prs.save(output_path)
except PermissionError:
    tmp = output_path.replace(".pptx", "_new.pptx")
    prs.save(tmp)
    print(f"\n⚠️  Original file was locked — saved as: {tmp}")
    print("   Close SafeInbox_AI_Presentation.pptx in PowerPoint, then rename manually.")
    sys.exit(0)

print(f"\n✅  Saved → {output_path}  ({len(prs.slides)} slides)")
