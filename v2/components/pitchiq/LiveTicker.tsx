"use client";

import { TICKER_ITEMS } from "@/lib/pitchiq-data";
import { americanOdds } from "@/lib/pitchiq-hooks";
import { useLiveMatch } from "./LiveMatchProvider";

const accentClasses = {
  red: "bg-red text-white",
  green: "bg-green text-white",
  gold: "bg-gold text-white",
  blue: "bg-blue text-white",
} as const;

export function LiveTicker() {
  const { match } = useLiveMatch();
  const liveItem = {
    id: "ticker-live-match",
    label: match.status === "fulltime" ? "Final" : "Live",
    value: `${match.home.shortName} ${match.score.home} - ${match.score.away} ${match.away.shortName}`,
    status: match.clock,
    accent: "red" as const,
  };
  const items = [liveItem, ...TICKER_ITEMS.slice(1)];
  const doubled = [...items, ...items];

  return (
    <section className="sticky top-0 z-[200] border-b border-[rgba(255,255,255,0.08)] bg-navy text-white">
      <div className="max-shell flex h-11 items-center gap-4">
        <div className="flex shrink-0 items-center gap-2 rounded-md bg-red px-3 py-1.5 text-xs font-black uppercase tracking-[0.14em]">
          <span className="live-dot h-2 w-2 rounded-full bg-white" />
          Live IQ
        </div>
        <div className="ticker-mask min-w-0 flex-1 overflow-hidden">
          <div className="ticker-track flex w-max gap-4">
            {doubled.map((item, index) => (
              <div key={`${item.id}-${index}`} className="flex items-center gap-2 text-sm">
                <span className={`rounded-sm px-2 py-0.5 text-[10px] font-black uppercase tracking-[0.12em] ${accentClasses[item.accent]}`}>
                  {item.label}
                </span>
                <span className="font-semibold text-white/95">{item.value}</span>
                <span className="text-white/55">{item.status}</span>
                {index === 0 ? (
                  <span className="rounded-sm border border-white/10 px-2 py-0.5 text-white/75">
                    France {americanOdds(match.odds.home)}
                  </span>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
