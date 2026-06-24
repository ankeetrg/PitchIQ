"use client";

import { useRef, useState } from "react";
import { useApp } from "@/app/providers";

interface NewsletterProps {
  compact?: boolean;
  title?: string;
}

export function Newsletter({ compact = false, title }: NewsletterProps = {}) {
  const { showToast } = useApp();
  const inputRef = useRef<HTMLInputElement>(null);
  const [label, setLabel] = useState("Subscribe");
  const [done, setDone] = useState(false);
  const [error, setError] = useState(false);
  const [busy, setBusy] = useState(false);

  async function submit() {
    if (busy) return;
    const val = (inputRef.current?.value ?? "").trim();
    // Basic client-side gate; the server route is the source of truth.
    if (!val.includes("@")) {
      setError(true);
      inputRef.current?.focus();
      window.setTimeout(() => setError(false), 1600);
      return;
    }

    setBusy(true);
    setLabel("…");
    try {
      const res = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: val }),
      });
      if (!res.ok) throw new Error(`Subscribe failed: ${res.status}`);
      setDone(true);
      setLabel("✓ You're in!");
      if (inputRef.current) inputRef.current.value = "";
      showToast("✓ Welcome to PitchIQ Daily — picks incoming!");
      window.setTimeout(() => {
        setDone(false);
        setLabel("Subscribe");
      }, 3500);
    } catch {
      setError(true);
      setLabel("Try again");
      showToast("Something went wrong — please try again.");
      window.setTimeout(() => {
        setError(false);
        setLabel("Subscribe");
      }, 2400);
    } finally {
      setBusy(false);
    }
  }

  const form = (
    <div className="nl-form">
      <div className="nl-input-row">
        <input
          ref={inputRef}
          className="nl-input"
          type="email"
          placeholder="Enter your email address…"
          style={error ? { borderColor: "var(--red)" } : undefined}
          onKeyDown={(e) => {
            if (e.key === "Enter") submit();
          }}
        />
        <button
          className="nl-btn"
          onClick={submit}
          disabled={busy}
          style={done ? { background: "var(--grn)" } : undefined}
        >
          {label}
        </button>
      </div>
      <div className="nl-note">No spam. Unsubscribe anytime. 18+ only.</div>
    </div>
  );

  if (compact) {
    return (
      <div className="nl-strip nl-strip--compact">
        <div className="nl-copy">
          <div className="nl-eyebrow">✦ PitchIQ Daily</div>
          <div className="nl-title">{title ?? "Get the Edge Before Kickoff"}</div>
        </div>
        {form}
      </div>
    );
  }

  return (
    <div className="nl-strip">
      <div className="w">
        <div className="nl-inner">
          <div className="nl-copy">
            <div className="nl-eyebrow">✦ PitchIQ Daily</div>
            <div className="nl-title">{title ?? "Get the Edge Before Kickoff"}</div>
            <div className="nl-sub">
              AI picks, line movement alerts, and fantasy intel delivered every match day morning.
              Join 1M+ fans already winning.
            </div>
            <div className="nl-perks">
              <div className="nl-perk">Daily AI Picks</div>
              <div className="nl-perk">Line Movement Alerts</div>
              <div className="nl-perk">Fantasy Top Picks</div>
              <div className="nl-perk">Free Forever</div>
            </div>
          </div>
          {form}
        </div>
      </div>
    </div>
  );
}
