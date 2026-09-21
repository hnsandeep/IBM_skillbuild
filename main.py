"""
SafeInbox AI — Real-Time AI-Powered Phishing & Social Engineering Detector
FastAPI backend: single-file, production-ready.

LLM provider: OpenRouter (https://openrouter.ai)
  - Uses the OpenAI-compatible REST API via httpx (no extra SDK needed)
  - Set OPENROUTER_KEY in your .env file
  - Model: anthropic/claude-3.5-haiku  (fast, cost-efficient)

Other features:
- load_dotenv() called at startup so local .env is respected
- url validated as a proper URL via Pydantic HttpUrl
- message capped at 10 000 chars (prompt-injection / abuse guard)
- Blocking LLM + Safe Browsing calls run via asyncio.to_thread
- CORS allow_credentials=False (browser spec compliant)
- Global error handler — never exposes tracebacks
- /health includes uptime + provider info
- GET / redirects to /docs
"""

import asyncio
import json
import logging
import os
import time
from typing import Optional

import httpx
from dotenv import load_dotenv

# Load .env before anything reads os.getenv()
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field, HttpUrl, field_validator

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger("safeinbox")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAX_MESSAGE_LEN    = 10_000
START_TIME         = time.time()

# OpenRouter config
OPENROUTER_BASE    = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL          = "anthropic/claude-3-haiku"      # OpenRouter model ID
APP_NAME           = "SafeInbox AI"
APP_URL            = "https://github.com/hnsandeep/IBM_skillbuild"

# Google Safe Browsing
SAFE_BROWSING_URL  = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
OPENROUTER_KEY    = os.getenv("OPENROUTER_KEY", "")
SAFE_BROWSING_KEY = os.getenv("SAFE_BROWSING_KEY", "")

if not OPENROUTER_KEY:
    logger.warning("OPENROUTER_KEY is not set — /analyze will return 502")
if not SAFE_BROWSING_KEY:
    logger.warning("SAFE_BROWSING_KEY is not set — URL threat-intel checks disabled")

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SafeInbox AI",
    description="Real-Time AI-Powered Phishing & Social Engineering Detector",
    version="1.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=MAX_MESSAGE_LEN,
        description="Suspicious message text (max 10 000 chars)",
    )
    url: Optional[HttpUrl] = Field(
        None,
        description="Optional URL to cross-check against Google Safe Browsing",
    )

    @field_validator("message")
    @classmethod
    def strip_message(cls, v: str) -> str:
        return v.strip()


class AnalyzeResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str = Field(..., description="Low | Medium | High | Critical")
    red_flags: list[str]
    explanation: str
    url_flagged_by_safe_browsing: bool = False
    safe_browsing_threats: list[str] = []
    analyzed_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are SafeInbox AI, an expert cybersecurity analyst specialising in
phishing, smishing, vishing, and social-engineering attacks.

You MUST respond with ONLY valid JSON — no markdown, no prose, no code fences.
Required keys:
  "risk_score"  : integer 0-100
  "risk_level"  : exactly one of "Low", "Medium", "High", "Critical"
  "red_flags"   : array of short strings (each ≤ 80 chars)
  "explanation" : 2-3 sentence plain-English summary for a non-technical user

Risk level thresholds: 0-24 Low · 25-49 Medium · 50-74 High · 75-100 Critical

Signals to detect (non-exhaustive):
- Urgency/fear language ("act now", "account suspended", "final warning")
- Authority impersonation (bank, IRS, Apple, Google, Amazon, PayPal, etc.)
- Requests for sensitive data (OTP, password, card number, SSN, wire transfer)
- Grammar/spelling errors or unnatural machine-translated phrasing
- Suspicious URLs, shortened links, typosquatted/lookalike domains
- Unsolicited prize, lottery, inheritance, or job offers
- Threats of legal action or account termination
- Mismatched or spoofed sender information"""


def _build_user_prompt(message: str, url: Optional[str]) -> str:
    parts = [
        f"Analyze the following message for phishing/social-engineering signals.\n\nMESSAGE:\n{message}"
    ]
    if url:
        parts.append(f"\nURL FOUND IN MESSAGE:\n{url}")
    parts.append("\nReturn ONLY the JSON object.")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Helper: call OpenRouter (synchronous — run via asyncio.to_thread)
# ---------------------------------------------------------------------------
def _call_llm(message: str, url: Optional[str]) -> dict:
    """
    Call OpenRouter's OpenAI-compatible endpoint using httpx.
    Runs in a thread pool — never call directly from async context.
    """
    if not OPENROUTER_KEY:
        raise RuntimeError("OPENROUTER_KEY is not configured.")

    headers = {
        "Authorization":  f"Bearer {OPENROUTER_KEY}",
        "Content-Type":   "application/json",
        "HTTP-Referer":   APP_URL,      # required by OpenRouter
        "X-Title":        APP_NAME,     # shown in OpenRouter dashboard
    }

    payload = {
        "model": LLM_MODEL,
        "max_tokens": 600,
        "temperature": 0.1,             # low temp for consistent JSON output
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": _build_user_prompt(message, url)},
        ],
    }

    try:
        with httpx.Client(timeout=45.0) as client:
            resp = client.post(OPENROUTER_BASE, headers=headers, json=payload)
            resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error("OpenRouter HTTP error %s: %s", exc.response.status_code, exc.response.text)
        raise RuntimeError(f"OpenRouter API error: {exc.response.status_code} — {exc.response.text}") from exc
    except httpx.RequestError as exc:
        logger.error("OpenRouter request error: %s", exc)
        raise RuntimeError(f"Could not reach OpenRouter: {exc}") from exc

    data = resp.json()
    raw  = data["choices"][0]["message"]["content"].strip()
    logger.info("LLM raw response: %s", raw)

    # Strip accidental code fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("LLM non-JSON response: %s", raw)
        raise RuntimeError("LLM returned non-JSON output.") from exc

    score = max(0, min(100, int(parsed.get("risk_score", 50))))
    return {
        "risk_score":   score,
        "risk_level":   parsed.get("risk_level", _score_to_level(score)),
        "red_flags":    parsed.get("red_flags", []) if isinstance(parsed.get("red_flags"), list) else [],
        "explanation":  parsed.get("explanation", "No explanation available."),
    }


# ---------------------------------------------------------------------------
# Helper: Google Safe Browsing (synchronous — run via asyncio.to_thread)
# ---------------------------------------------------------------------------
def _call_safe_browsing(url: str) -> tuple[bool, list[str]]:
    """Never raises — returns (False, []) on any failure."""
    if not SAFE_BROWSING_KEY:
        return False, []

    payload = {
        "client": {"clientId": "safeinbox-ai", "clientVersion": "1.2.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE", "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes":    ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries":    [{"url": url}],
        },
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(
                SAFE_BROWSING_URL,
                params={"key": SAFE_BROWSING_KEY},
                json=payload,
            )
            resp.raise_for_status()
            matches = resp.json().get("matches", [])
        if matches:
            threats = list({m.get("threatType", "UNKNOWN") for m in matches})
            logger.info("Safe Browsing flagged %s — %s", url, threats)
            return True, threats
        return False, []
    except Exception as exc:  # noqa: BLE001
        logger.error("Safe Browsing error: %s", exc)
        return False, []


# ---------------------------------------------------------------------------
# Helper: score → risk level string
# ---------------------------------------------------------------------------
def _score_to_level(score: int) -> str:
    if score < 25: return "Low"
    if score < 50: return "Medium"
    if score < 75: return "High"
    return "Critical"


# ---------------------------------------------------------------------------
# Global error handler
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def _global_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again."},
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def root():
    """Redirect bare root to the interactive API docs."""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["ops"])
async def health():
    """Liveness probe — returns 200 with service metadata."""
    return {
        "status":                   "ok",
        "service":                  "SafeInbox AI",
        "version":                  "1.2.0",
        "uptime_seconds":           round(time.time() - START_TIME, 1),
        "llm_provider":             "OpenRouter",
        "llm_model":                LLM_MODEL,
        "openrouter_configured":    bool(OPENROUTER_KEY),
        "safe_browsing_configured": bool(SAFE_BROWSING_KEY),
    }


@app.post("/analyze", response_model=AnalyzeResponse, tags=["analysis"])
async def analyze(req: AnalyzeRequest):
    """
    Analyze a suspicious message (and optional URL) for phishing signals.

    Pipeline:
    1. OpenRouter / Claude 3.5 Haiku scores the message for social-engineering patterns.
    2. If a URL is provided, Google Safe Browsing is queried in parallel.
    3. A Safe Browsing hit adds +30 to the score (capped at 100).
    """
    url_str = str(req.url).rstrip("/") if req.url else None
    logger.info("analyze — msg_len=%d url=%s", len(req.message), url_str)

    # Run LLM + Safe Browsing concurrently (both blocking → thread pool)
    if url_str:
        try:
            llm_result, (url_flagged, sb_threats) = await asyncio.gather(
                asyncio.to_thread(_call_llm, req.message, url_str),
                asyncio.to_thread(_call_safe_browsing, url_str),
            )
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
    else:
        try:
            llm_result = await asyncio.to_thread(_call_llm, req.message, None)
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        url_flagged, sb_threats = False, []

    score: int  = llm_result["risk_score"]
    level: str  = llm_result["risk_level"]
    flags: list = llm_result["red_flags"]
    explanation = llm_result["explanation"]

    # Safe Browsing score boost
    if url_flagged:
        score = min(100, score + 30)
        level = _score_to_level(score)
        flags.append("URL confirmed malicious by Google Safe Browsing")

    return AnalyzeResponse(
        risk_score=score,
        risk_level=level,
        red_flags=flags,
        explanation=explanation,
        url_flagged_by_safe_browsing=url_flagged,
        safe_browsing_threats=sb_threats,
        analyzed_url=url_str,
    )
