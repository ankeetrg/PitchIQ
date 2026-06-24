"use client";

import { useApp } from "@/app/providers";
import { tickerItems, type TickItem } from "./data";

function Item({ it, liveScore, liveMin }: { it: TickItem; liveScore: string; liveMin: string }) {
  const score = it.liveMatch ? liveScore : it.score;
  const trailing = it.liveMatch ? liveMin : it.trailing;
  return (
    <div className="tick-item">
      <span className={`tick-status ${it.status}`}>{it.statusLabel}</span> {it.home}
      {score ? <span className="score">{score}</span> : null} {it.away}
      {trailing ? <span className={`tick-status ${it.status}`}>{trailing}</span> : null}
    </div>
  );
}

export function LiveTicker() {
  const { match } = useApp();
  const liveScore = `${match.home}–${match.away}`;
  const liveMin = match.live ? `${match.min}'` : "FT";
  // duplicate the set for a seamless marquee loop
  const items = [...tickerItems, ...tickerItems];

  return (
    <div className="ticker">
      <div className="ticker-badge">
        <div className="ticker-dot" /> Live
      </div>
      <div className="ticker-scroll">
        <div className="ticker-track">
          {items.map((it, i) => (
            <Item key={i} it={it} liveScore={liveScore} liveMin={liveMin} />
          ))}
        </div>
      </div>
      <div className="ticker-right">WC 2026 · Group Stage</div>
    </div>
  );
}
