"""
SafeInbox AI — Real-Time AI-Powered Phishing & Social Engineering Detector
FastAPI backend: single-file, production-ready.

LLM provider: CometAPI (https://api.cometapi.com) — a cost-effective Claude
proxy that accepts the standard Anthropic SDK with a custom base_url.
Set COMETAPI_KEY in your environment (or .env file).

Other features:
- load_dotenv() called at startup so local .env is respected
- url validated as a proper URL via Pydantic HttpUrl
- message capped at 10 000 chars (prompt-injection / abuse guard)
- Blocking LLM + Safe Browsing calls moved off the async event loop
  via asyncio.to_thread — no more request starvation under load
- CORS allow_credentials=False when allow_origins="*" (browser spec fix)
- Startup check logs a clear warning when keys are missing
- /health includes process uptime
"""

import asyncio
import json
import logging
import os
import time
from typing import Optional

import httpx
from dotenv import load_dotenv

# Load .env before anything else reads os.getenv()
load_dotenv()

import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
MAX_MESSAGE_LEN   = 10_000          # chars — prevent prompt-injection / runaway costs
SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
COMET_BASE_URL    = "https://api.cometapi.com"   # CometAPI Claude proxy
LLM_MODEL         = "claude-fable-5-1"           # CometAPI model name
START_TIME        = time.time()

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
COMETAPI_KEY      = os.getenv("COMETAPI_KEY", "")
SAFE_BROWSING_KEY = os.getenv("SAFE_BROWSING_KEY", "")

if not COMETAPI_KEY:
    logger.warning("COMETAPI_KEY is not set — /analyze will return 502")
if not SAFE_BROWSING_KEY:
    logger.warning("SAFE_BROWSING_KEY is not set — URL threat-intel checks disabled")

# Anthropic SDK pointed at CometAPI base URL (thread-safe, reuse across requests)
anthropic_client = (
    anthropic.Anthropic(
        base_url=COMET_BASE_URL,
        api_key=COMETAPI_KEY,
        max_retries=0,          # fail fast — let FastAPI handle retries/errors
    )
    if COMETAPI_KEY else None
)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="SafeInbox AI",
    description="Real-Time AI-Powered Phishing & Social Engineering Detector",
    version="1.1.0",
)

# CORS — credentials must be False when origins is wildcard (browser spec)
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
    analyzed_url: Optional[str] = Field(None, description="The URL that was checked, if any")


# ---------------------------------------------------------------------------
# Prompts
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
    parts = [f"Analyze the following message for phishing/social-engineering signals.\n\nMESSAGE:\n{message}"]
    if url:
        parts.append(f"\nURL FOUND IN MESSAGE:\n{url}")
    parts.append("\nReturn ONLY the JSON object.")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Helpers (synchronous — called via asyncio.to_thread)
# ---------------------------------------------------------------------------
def _call_llm(message: str, url: Optional[str]) -> dict:
    """Synchronous Claude call via CometAPI. Run in a thread pool — never call directly from async."""
    if not anthropic_client:
        raise RuntimeError("COMETAPI_KEY is not configured.")

    response = anthropic_client.messages.create(
        model=LLM_MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(message, url)}],
    )

    raw = response.content[0].text.strip()
    logger.info("LLM response: %s", raw)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("LLM returned non-JSON.") from exc

    score = max(0, min(100, int(parsed.get("risk_score", 50))))
    return {
        "risk_score": score,
        "risk_level": parsed.get("risk_level", _score_to_level(score)),
        "red_flags":  parsed.get("red_flags", []) if isinstance(parsed.get("red_flags"), list) else [],
        "explanation": parsed.get("explanation", "No explanation available."),
    }


def _call_safe_browsing(url: str) -> tuple[bool, list[str]]:
    """Synchronous Safe Browsing call. Run in a thread pool. Never raises."""
    if not SAFE_BROWSING_KEY:
        return False, []

    payload = {
        "client": {"clientId": "safeinbox-ai", "clientVersion": "1.1.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(SAFE_BROWSING_URL, params={"key": SAFE_BROWSING_KEY}, json=payload)
            resp.raise_for_status()
            matches = resp.json().get("matches", [])

        if matches:
            threats = list({m.get("threatType", "UNKNOWN") for m in matches})
            logger.info("Safe Browsing flagged %s — threats: %s", url, threats)
            return True, threats

        return False, []

    except Exception as exc:  # noqa: BLE001
        logger.error("Safe Browsing error: %s", exc)
        return False, []


def _score_to_level(score: int) -> str:
    if score < 25:  return "Low"
    if score < 50:  return "Medium"
    if score < 75:  return "High"
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
@app.get("/health", tags=["ops"])
async def health():
    """Liveness probe — returns 200 with service metadata."""
    return {
        "status": "ok",
        "service": "SafeInbox AI",
        "version": "1.1.0",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "llm_provider": "CometAPI",
        "llm_model": LLM_MODEL,
        "cometapi_configured": bool(COMETAPI_KEY),
        "safe_browsing_configured": bool(SAFE_BROWSING_KEY),
    }


@app.post("/analyze", response_model=AnalyzeResponse, tags=["analysis"])
async def analyze(req: AnalyzeRequest):
    """
    Analyze a suspicious message (and optional URL) for phishing signals.

    Pipeline:
    1. Claude LLM scores the message text for social-engineering patterns.
    2. If a URL is provided, Google Safe Browsing is queried in parallel.
    3. A Safe Browsing hit adds +30 to the score (capped at 100).
    """
    url_str = str(req.url).rstrip("/") if req.url else None

    logger.info("analyze — msg_len=%d url=%s", len(req.message), url_str)

    # Run LLM (and optionally Safe Browsing) concurrently in thread pool
    # so neither blocks the event loop.
    if url_str:
        llm_task = asyncio.to_thread(_call_llm, req.message, url_str)
        sb_task  = asyncio.to_thread(_call_safe_browsing, url_str)
        (llm_result, (url_flagged, sb_threats)) = await asyncio.gather(
            llm_task, sb_task, return_exceptions=False
        )
    else:
        try:
            llm_result = await asyncio.to_thread(_call_llm, req.message, None)
        except RuntimeError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        url_flagged, sb_threats = False, []

    # Unpack LLM result (may raise if _call_llm failed inside gather)
    if isinstance(llm_result, Exception):
        raise HTTPException(status_code=502, detail=str(llm_result))

    score: int      = llm_result["risk_score"]
    level: str      = llm_result["risk_level"]
    flags: list     = llm_result["red_flags"]
    explanation     = llm_result["explanation"]

    # Apply Safe Browsing boost
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
