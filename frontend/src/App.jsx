/**
 * SafeInbox AI — App.jsx
 *
 * Improvements over v1:
 * - animate-fade-in / animate-grow-x now defined (were missing → broken animation)
 * - Character counter on textarea with warning colour near limit
 * - URL auto-extracted from message text as a convenience hint
 * - AbortController cancels in-flight request on Reset
 * - Accessible: role="status" live region for results, aria-live for errors
 * - key prop uses stable value instead of pure array index
 * - Render cold-start banner when backend takes > 5 s (free tier warning)
 * - Analysed URL displayed in results so user can verify what was checked
 */

import { useState, useRef, useEffect, useCallback } from "react";
import axios from "axios";

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const API_URL     = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const MAX_CHARS   = 10_000;
const SLOW_MS     = 5_000;   // show "waking up…" banner after this many ms

// ---------------------------------------------------------------------------
// Risk-level display config
// ---------------------------------------------------------------------------
const RISK_CONFIG = {
  Low:      { bar: "bg-green-500",  text: "text-green-400",  badge: "bg-green-500/15 text-green-400 ring-green-500/30",  icon: "✅", label: "Low Risk"      },
  Medium:   { bar: "bg-yellow-500", text: "text-yellow-400", badge: "bg-yellow-500/15 text-yellow-400 ring-yellow-500/30", icon: "⚠️", label: "Medium Risk"   },
  High:     { bar: "bg-orange-500", text: "text-orange-400", badge: "bg-orange-500/15 text-orange-400 ring-orange-500/30", icon: "🚨", label: "High Risk"     },
  Critical: { bar: "bg-red-500",    text: "text-red-400",    badge: "bg-red-500/15 text-red-400 ring-red-500/30",          icon: "☠️", label: "Critical Risk" },
};

// Simple URL extractor — grabs first http(s) URL from raw text
const URL_RE = /https?:\/\/[^\s"'<>)]+/i;
function extractUrl(text) {
  const m = text.match(URL_RE);
  return m ? m[0] : "";
}

// ---------------------------------------------------------------------------
// Small presentational components
// ---------------------------------------------------------------------------

function Spinner({ size = 5 }) {
  return (
    <svg
      className={`animate-spin h-${size} w-${size} text-indigo-400`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
    </svg>
  );
}

function RiskMeter({ score, level }) {
  const cfg = RISK_CONFIG[level] ?? RISK_CONFIG.Medium;
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-slate-400">Risk Score</span>
        <span className={`text-2xl font-extrabold tabular-nums ${cfg.text}`}>
          {score}
          <span className="text-sm font-normal text-slate-500"> / 100</span>
        </span>
      </div>
      {/* Track */}
      <div className="w-full h-3 rounded-full bg-slate-700 overflow-hidden">
        <div
          className={`h-full rounded-full origin-left animate-grow-x ${cfg.bar}`}
          style={{ width: `${score}%` }}
          role="progressbar"
          aria-valuenow={score}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={`Risk score ${score} out of 100`}
        />
      </div>
      <div className="flex justify-between text-xs text-slate-600 select-none" aria-hidden="true">
        {["Safe", "Low", "Medium", "High", "Critical"].map((l) => (
          <span key={l}>{l}</span>
        ))}
      </div>
    </div>
  );
}

function RiskBadge({ level }) {
  const cfg = RISK_CONFIG[level] ?? RISK_CONFIG.Medium;
  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-semibold ring-1 ${cfg.badge}`}>
      <span aria-hidden="true">{cfg.icon}</span>
      {cfg.label}
    </span>
  );
}

function SectionHeading({ children }) {
  return (
    <h3 className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-2">
      {children}
    </h3>
  );
}

// ---------------------------------------------------------------------------
// Result card
// ---------------------------------------------------------------------------
function ResultCard({ data }) {
  const {
    risk_score,
    risk_level,
    red_flags,
    explanation,
    url_flagged_by_safe_browsing,
    safe_browsing_threats,
    analyzed_url,
  } = data;

  return (
    <section
      aria-label="Analysis results"
      role="status"
      aria-live="polite"
      className="mt-8 rounded-2xl border border-slate-700 bg-slate-800/60 backdrop-blur-sm
                 shadow-2xl divide-y divide-slate-700/60 animate-fade-in"
    >
      {/* ── Header ── */}
      <div className="flex flex-wrap items-center justify-between gap-4 px-6 py-5">
        <h2 className="text-base font-semibold text-white">Analysis Result</h2>
        <RiskBadge level={risk_level} />
      </div>

      {/* ── Risk meter ── */}
      <div className="px-6 py-5">
        <RiskMeter score={risk_score} level={risk_level} />
      </div>

      {/* ── Explanation ── */}
      <div className="px-6 py-5">
        <SectionHeading>What this means</SectionHeading>
        <p className="text-slate-200 text-sm leading-relaxed">{explanation}</p>
      </div>

      {/* ── Red flags ── */}
      {red_flags.length > 0 && (
        <div className="px-6 py-5">
          <SectionHeading>Red Flags Detected ({red_flags.length})</SectionHeading>
          <ul className="space-y-2" aria-label="List of red flags">
            {red_flags.map((flag, i) => (
              <li key={`${flag.slice(0, 20)}-${i}`} className="flex items-start gap-2 text-sm text-slate-200">
                <span className="mt-0.5 text-red-400 shrink-0 select-none" aria-hidden="true">⚑</span>
                {flag}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ── URL / Safe Browsing ── */}
      {analyzed_url && (
        <div className="px-6 py-5 space-y-3">
          <SectionHeading>URL Intelligence</SectionHeading>
          {/* Show the URL that was checked */}
          <p className="text-xs text-slate-500 font-mono break-all truncate" title={analyzed_url}>
            Checked: {analyzed_url}
          </p>
          {url_flagged_by_safe_browsing ? (
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-semibold bg-red-500/15 text-red-400 ring-1 ring-red-500/30">
                🚫 Flagged as malicious by Google Safe Browsing
              </span>
              {safe_browsing_threats?.map((t) => (
                <span key={t} className="px-2 py-0.5 rounded text-xs bg-slate-700 text-slate-300 font-mono">
                  {t}
                </span>
              ))}
            </div>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-semibold bg-green-500/15 text-green-400 ring-1 ring-green-500/30">
              ✅ Not flagged by Google Safe Browsing
            </span>
          )}
        </div>
      )}
    </section>
  );
}

// ---------------------------------------------------------------------------
// Main App
// ---------------------------------------------------------------------------
export default function App() {
  const [message, setMessage] = useState("");
  const [url, setUrl]         = useState("");
  const [loading, setLoading] = useState(false);
  const [slow, setSlow]       = useState(false);   // true after SLOW_MS while loading
  const [result, setResult]   = useState(null);
  const [error, setError]     = useState("");

  // AbortController ref so we can cancel in-flight requests on Reset
  const abortRef = useRef(null);
  // Timer ref for the slow-request banner
  const slowTimerRef = useRef(null);

  // Auto-extract URL from pasted message as a user convenience
  useEffect(() => {
    if (!url) {
      const found = extractUrl(message);
      if (found) setUrl(found);
    }
    // Only run when message changes; intentionally omit `url` from deps
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [message]);

  const charsLeft      = MAX_CHARS - message.length;
  const charsNearLimit = charsLeft <= 500;

  const handleAnalyze = useCallback(async (e) => {
    e.preventDefault();
    if (!message.trim()) {
      setError("Please paste a message to analyze.");
      return;
    }

    // Cancel any previous in-flight request
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setLoading(true);
    setResult(null);
    setError("");
    setSlow(false);

    // Show "waking up" banner if the backend is slow (Render free tier cold start)
    slowTimerRef.current = setTimeout(() => setSlow(true), SLOW_MS);

    try {
      const payload = { message: message.trim() };
      if (url.trim()) payload.url = url.trim();

      const { data } = await axios.post(`${API_URL}/analyze`, payload, {
        headers: { "Content-Type": "application/json" },
        timeout: 60_000,                          // 60 s for cold-start tolerance
        signal: controller.signal,
      });

      setResult(data);
    } catch (err) {
      if (axios.isCancel(err)) return;            // user reset mid-flight — ignore
      const detail =
        err.response?.data?.detail ??
        (err.code === "ECONNABORTED" ? "Request timed out. The backend may be starting up — try again." : null) ??
        err.message ??
        "Something went wrong. Please try again.";
      setError(String(detail));
    } finally {
      clearTimeout(slowTimerRef.current);
      setSlow(false);
      setLoading(false);
    }
  }, [message, url]);

  const handleReset = useCallback(() => {
    abortRef.current?.abort();
    clearTimeout(slowTimerRef.current);
    setMessage("");
    setUrl("");
    setResult(null);
    setError("");
    setLoading(false);
    setSlow(false);
  }, []);

  // ── Render ──
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-2xl w-full">

        {/* ── Header ── */}
        <header className="flex flex-col items-center text-center mb-10 gap-4">
          <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-indigo-600/20 ring-1 ring-indigo-500/30">
            <svg className="w-8 h-8 text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z" />
            </svg>
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white">
              SafeInbox <span className="text-indigo-400">AI</span>
            </h1>
            <p className="mt-1.5 text-slate-400 text-sm max-w-sm">
              Paste any suspicious email, SMS, or WhatsApp message — our AI tells you if it's a scam.
            </p>
          </div>
        </header>

        {/* ── Form ── */}
        <form
          onSubmit={handleAnalyze}
          className="rounded-2xl border border-slate-700 bg-slate-800/60 backdrop-blur-sm shadow-xl p-6 space-y-5"
          noValidate
        >

          {/* Message textarea */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label htmlFor="message" className="block text-sm font-medium text-slate-300">
                Suspicious Message <span className="text-red-400" aria-label="required">*</span>
              </label>
              <span
                className={`text-xs tabular-nums ${charsNearLimit ? "text-orange-400" : "text-slate-500"}`}
                aria-live="polite"
                aria-label={`${charsLeft} characters remaining`}
              >
                {charsLeft.toLocaleString()} / {MAX_CHARS.toLocaleString()}
              </span>
            </div>
            <textarea
              id="message"
              rows={6}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              maxLength={MAX_CHARS}
              placeholder="Paste the email, SMS, or WhatsApp message here…"
              required
              aria-required="true"
              aria-describedby={error ? "form-error" : undefined}
              className={`
                w-full rounded-xl bg-slate-900 text-slate-100 placeholder-slate-500
                px-4 py-3 text-sm leading-relaxed resize-y
                border transition-colors
                focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                ${charsNearLimit ? "border-orange-500/50" : "border-slate-600"}
              `}
            />
          </div>

          {/* URL input */}
          <div className="space-y-1.5">
            <label htmlFor="url" className="block text-sm font-medium text-slate-300">
              Suspicious URL{" "}
              <span className="text-slate-500 font-normal">(optional — checked against Google Safe Browsing)</span>
            </label>
            <input
              id="url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://suspicious-link.example.com"
              className="w-full rounded-xl bg-slate-900 border border-slate-600 text-slate-100 placeholder-slate-500
                         px-4 py-2.5 text-sm
                         focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
                         transition-colors"
            />
          </div>

          {/* Slow-start banner */}
          {slow && loading && (
            <div className="flex items-center gap-2 rounded-xl bg-indigo-500/10 border border-indigo-500/20 px-4 py-3 text-sm text-indigo-300" role="status">
              <Spinner size={4} />
              Backend is waking up (free tier cold start) — this may take ~30 s…
            </div>
          )}

          {/* Error banner */}
          {error && (
            <div
              id="form-error"
              role="alert"
              aria-live="assertive"
              className="flex items-start gap-2 rounded-xl bg-red-500/10 border border-red-500/25 px-4 py-3 text-sm text-red-400"
            >
              <span className="shrink-0 mt-0.5" aria-hidden="true">⚠️</span>
              {error}
            </div>
          )}

          {/* Buttons */}
          <div className="flex gap-3 pt-1">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 flex items-center justify-center gap-2 rounded-xl
                         bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700
                         disabled:opacity-50 disabled:cursor-not-allowed
                         text-white font-semibold text-sm py-3 px-6
                         transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
            >
              {loading ? (
                <><Spinner /> Analyzing…</>
              ) : (
                <>
                  <svg className="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1 0 6.5 6.5a7.5 7.5 0 0 0 10.15 10.15z" />
                  </svg>
                  Analyze Message
                </>
              )}
            </button>

            {(message || url || result || loading) && (
              <button
                type="button"
                onClick={handleReset}
                className="rounded-xl border border-slate-600 text-slate-400
                           hover:text-slate-100 hover:border-slate-500
                           text-sm font-medium py-3 px-4
                           transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400"
              >
                Reset
              </button>
            )}
          </div>
        </form>

        {/* ── Results ── */}
        {result && <ResultCard data={result} />}

        {/* ── Footer ── */}
        <footer className="mt-10 text-center text-xs text-slate-600 space-y-1">
          <p>SafeInbox AI · Powered by Claude &amp; Google Safe Browsing</p>
          <p>This tool assists detection — always verify with your IT/security team for sensitive matters.</p>
        </footer>

      </div>
    </div>
  );
}
