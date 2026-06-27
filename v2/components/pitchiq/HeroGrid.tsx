"use client";

import { FeaturedMatch } from "./FeaturedMatch";
import { FixturesWidget } from "./FixturesWidget";
import { BestBetsWidget } from "./BestBetsWidget";
import { useLiveMatch } from "./LiveMatchProvider";
import { Reveal } from "./Reveal";

export function HeroGrid() {
  const { match, oddsFlashKey, scoreFlashKey } = useLiveMatch();

  return (
    <section id="predictions" className="bg-[var(--bg)] py-8 md:py-10">
      <div className="max-shell">
        <Reveal>
          <div className="mb-5 flex flex-col justify-between gap-3 md:flex-row md:items-end">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.18em] text-gold">World Cup 2026 Live Center</p>
              <h1 className="headline-pretty mt-2 max-w-4xl font-cond text-5xl font-black uppercase leading-[0.92] tracking-normal md:text-7xl">
                Live predictions, fantasy edges, and odds intelligence.
              </h1>
            </div>
            <p className="max-w-md text-sm leading-6 text-[var(--t2)]">
              AI-labeled match context, simulated live movement, standings, schedule, and fantasy picks for getpitchiq.net.
            </p>
          </div>
        </Reveal>

        <div className="grid gap-5 lg:grid-cols-[minmax(0,1.55fr)_minmax(320px,0.9fr)]">
          <Reveal>
            <FeaturedMatch match={match} oddsFlashKey={oddsFlashKey} scoreFlashKey={scoreFlashKey} />
          </Reveal>
          <div className="grid gap-5">
            <Reveal delay={0.08}>
              <FixturesWidget />
            </Reveal>
            <Reveal delay={0.14}>
              <BestBetsWidget />
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
