"use client";

import { Clock3 } from "lucide-react";
import { useLiveMatch } from "./LiveMatchProvider";

export function FixturesWidget() {
  const { match, matches } = useLiveMatch();

  // All matches except the featured one, capped at 5 for the sidebar
  const otherMatches = matches.filter((m) => m.id !== match.id).slice(0, 5);

  function formatKickoff(m: typeof match) {
    if (m.status === "live" || m.status === "halftime") return m.clock;
    if (m.startTime) {
      const d = new Date(m.startTime);
      if (!Number.isNaN(d.getTime())) {
        return d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", timeZoneName: "short" });
      }
    }
    return m.clock;
  }

  return (
    <aside className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.14em] text-gold">Today Schedule</p>
          <h2 className="mt-1 font-cond text-3xl font-black uppercase leading-none">Fixtures</h2>
        </div>
        <Clock3 className="text-[var(--t3)]" size={20} />
      </div>

      <div className="mt-5 space-y-3">
        {/* Featured / live match */}
        <div className="rounded-md border border-green-border bg-green-dim p-3">
          <div className="flex items-center justify-between gap-3">
            <span className="flex items-center gap-2 text-xs font-black uppercase tracking-[0.12em] text-green">
              <span className="pulse-dot h-2 w-2 rounded-full bg-green" />
              {match.clock}
            </span>
            <span className="text-xs font-bold text-[var(--t3)]">{match.group}</span>
          </div>
          <div className="mt-2 flex items-center justify-between gap-3 font-cond text-2xl font-black uppercase leading-none">
            <span>{match.home.shortName}</span>
            <span>{match.score.home}-{match.score.away}</span>
            <span>{match.away.shortName}</span>
          </div>
        </div>

        {/* Remaining matches from ESPN */}
        {otherMatches.map((item) => {
          const isLive = item.status === "live" || item.status === "halftime";
          return (
            <div key={item.id} className="rounded-md border border-[var(--b1)] bg-[var(--bg)] p-3">
              <div className="flex items-center justify-between gap-3 text-xs font-bold text-[var(--t3)]">
                <span className={isLive ? "text-green" : ""}>{formatKickoff(item)}</span>
                <span>{item.group}</span>
              </div>
              <div className="mt-2 flex items-center justify-between gap-3 font-cond text-xl font-black uppercase leading-none">
                <span>{item.home.shortName}</span>
                {isLive ? (
                  <span className="text-green">{item.score.home}-{item.score.away}</span>
                ) : (
                  <span className="text-[var(--t3)]">vs</span>
                )}
                <span>{item.away.shortName}</span>
              </div>
              <div className="mt-2 text-xs text-[var(--t3)]">{item.venue}</div>
            </div>
          );
        })}
      </div>
    </aside>
  );
}
