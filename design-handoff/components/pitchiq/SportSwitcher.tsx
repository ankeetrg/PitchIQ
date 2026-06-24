"use client";

import { useApp } from "@/app/providers";

export function SportSwitcher() {
  const { setCricketOpen } = useApp();
  return (
    <div className="sport-switcher">
      <div className="ss-inner w">
        <div className="ss-tab active">⚽ Soccer</div>
        <div className="ss-tab" onClick={() => setCricketOpen(true)} role="button" tabIndex={0}
          onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") setCricketOpen(true); }}>
          🏏 Cricket <span className="ss-badge">Q4 2026</span>
        </div>
        <div className="ss-right">IPL &amp; International · Coming Soon — click to register interest</div>
      </div>
    </div>
  );
}
