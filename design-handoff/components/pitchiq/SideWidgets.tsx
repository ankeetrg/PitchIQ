"use client";

import { useApp } from "@/app/providers";
import { fixtures, bestBets } from "./data";

export function SideWidgets() {
  const { match } = useApp();
  const liveScore = `${match.home}–${match.away}`;
  const liveMin = match.live ? `${match.min}'` : "FT";

  return (
    <div className="side-col">
      {/* Today's Fixtures */}
      <div className="widget">
        <div className="w-head">
          <div className="w-title">Today&apos;s Fixtures</div>
          <a className="w-link" href="#">
            Full Schedule →
          </a>
        </div>
        {fixtures.map((f, i) => {
          const isLive = f.liveMatch;
          const status = isLive && !match.live ? "ft" : f.status;
          const statusLabel = isLive && !match.live ? "FT" : f.statusLabel;
          return (
            <div className="fixture-row" key={i}>
              <div className={`fix-status ${status}`}>{statusLabel}</div>
              <div className="fix-match">
                {f.match}
                <em>
                  {f.meta}
                  {isLive ? (match.live ? liveMin : "Full Time") : ""}
                </em>
              </div>
              <div className={`fix-score${f.scoreUpcoming ? " upcoming" : ""}`}>
                {isLive ? liveScore : f.score}
              </div>
            </div>
          );
        })}
      </div>

      {/* Best Bets */}
      <div className="widget">
        <div className="w-head">
          <div className="w-title">⚡ Best Bets Today</div>
          <a className="w-link" href="#">
            All Picks →
          </a>
        </div>
        {bestBets.map((b, i) => {
          const tagStyle =
            b.tagKind === "hot"
              ? { background: "var(--red-d)", color: "var(--red)" }
              : b.tagKind === "sharp"
              ? { background: "var(--blue-d)", color: "var(--blue)" }
              : undefined;
          return (
            <div className="bet-row" key={i}>
              <div className="bet-match-info">
                {b.name}
                <em>{b.meta}</em>
              </div>
              <div className="bet-value-tag" style={tagStyle}>
                {b.tag}
              </div>
              <div className="bet-odds-pill">{b.odds}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
