"use client";

import { useRef, useState } from "react";
import { useApp } from "@/app/providers";

const features = [
  { icon: "🏏", title: "IPL 2027", sub: "Fantasy picks + betting intel" },
  { icon: "🌍", title: "International", sub: "Test, ODI & T20I coverage" },
  { icon: "🤖", title: "PitchIQ AI", sub: "Same engine, new sport" },
];

export function CricketModal() {
  const { cricketOpen, setCricketOpen, showToast } = useApp();
  const inputRef = useRef<HTMLInputElement>(null);
  const [label, setLabel] = useState("Notify Me");
  const [done, setDone] = useState(false);

  function submit() {
    const val = inputRef.current?.value ?? "";
    if (val.includes("@")) {
      setDone(true);
      setLabel("✓ Registered!");
      if (inputRef.current) inputRef.current.value = "";
      showToast("✓ You're on the Cricket early access list!");
      window.setTimeout(() => {
        setCricketOpen(false);
        setDone(false);
        setLabel("Notify Me");
      }, 2000);
    } else {
      inputRef.current?.focus();
    }
  }

  return (
    <div
      className={`modal-overlay${cricketOpen ? " open" : ""}`}
      onClick={(e) => {
        if (e.target === e.currentTarget) setCricketOpen(false);
      }}
      role="dialog"
      aria-modal="true"
      aria-label="PitchIQ Cricket — coming soon"
    >
      <div className="modal-sheet">
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 24 }}>
          <div>
            <div className="modal-eyebrow">🏏 Phase 2 · Coming Q4 2026</div>
            <div className="modal-title">
              PitchIQ Cricket
              <br />
              IPL &amp; International Coverage
            </div>
          </div>
          <button className="modal-close" aria-label="Close" onClick={() => setCricketOpen(false)}>
            ✕
          </button>
        </div>

        <div className="modal-features">
          {features.map((f) => (
            <div className="modal-feature" key={f.title}>
              <div className="modal-feature-icon">{f.icon}</div>
              <div className="modal-feature-title">{f.title}</div>
              <div className="modal-feature-sub">{f.sub}</div>
            </div>
          ))}
        </div>

        <p className="modal-text">
          Be the first to access PitchIQ Cricket. We&apos;ll send you early access plus our opening
          IPL picks when we launch.
        </p>

        <div className="modal-form">
          <input
            ref={inputRef}
            className="modal-input"
            type="email"
            placeholder="Enter your email for early access…"
            onKeyDown={(e) => {
              if (e.key === "Enter") submit();
            }}
          />
          <button
            className="modal-submit"
            onClick={submit}
            style={done ? { background: "var(--grn)" } : undefined}
          >
            {label}
          </button>
        </div>
        <p className="modal-fine">No spam. Cricket launch alerts only. Unsubscribe anytime.</p>
      </div>
    </div>
  );
}
