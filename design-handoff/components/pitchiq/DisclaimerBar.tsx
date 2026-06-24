"use client";

import { useState } from "react";

export function DisclaimerBar() {
  const [dismissed, setDismissed] = useState(false);
  if (dismissed) return null;

  return (
    <div className="disclaimer-bar" role="region" aria-label="Legal disclaimer">
      <div className="db-inner">
        <span className="db-warn">⚠ 18+</span>
        <span className="db-text">
          Gambling involves risk. PitchIQ is an entertainment &amp; information service — not a
          licensed sportsbook. If you or someone you know has a gambling problem, call{" "}
          <a href="tel:1-800-522-4700">1-800-522-4700</a>.
        </span>
        <button
          className="db-close"
          aria-label="Dismiss disclaimer"
          onClick={() => setDismissed(true)}
        >
          ✕
        </button>
      </div>
    </div>
  );
}
