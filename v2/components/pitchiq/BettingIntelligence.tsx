"use client";

import { Activity, Gauge, Target } from "lucide-react";
import { Reveal } from "./Reveal";

const cards = [
  {
    id: "value",
    icon: Target,
    label: "Best value bet",
    title: "France ML still clears fair price",
    body: "Model fair line sits near -215 after live xG, leaving a small but visible edge against consensus.",
    badge: "+5.4%",
  },
  {
    id: "sharp",
    icon: Activity,
    label: "Sharp money alert",
    title: "Spain spread pressure",
    body: "The move from -1.5 to -1.75 came with lower public ticket share, a classic professional signal.",
    badge: "Steam",
  },
  {
    id: "public",
    icon: Gauge,
    label: "Public vs sharp",
    title: "USA total split",
    body: "Tickets prefer over, but larger bets have moved the number down. Treat 2.5 as a key threshold.",
    badge: "Divergence",
  },
];

// LEGAL-REVIEW-REQUIRED: odds intelligence is educational and must not imply guaranteed returns.
export function BettingIntelligence() {
  return (
    <section className="bg-[var(--bg2)] py-10">
      <div className="max-shell">
        <Reveal>
          <div className="mb-5 flex flex-col justify-between gap-3 md:flex-row md:items-end">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.18em] text-gold">Market context</p>
              <h2 className="font-cond text-5xl font-black uppercase leading-none">Betting Intelligence</h2>
            </div>
            <p className="max-w-md text-sm leading-6 text-[var(--t2)]">
              Line movement, public splits, and model price checks labeled for legal review.
            </p>
          </div>
        </Reveal>
        <div className="grid gap-4 md:grid-cols-3">
          {cards.map((card, index) => {
            const Icon = card.icon;
            return (
              <Reveal key={card.id} delay={index * 0.06}>
                <article className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
                  <div className="flex items-center justify-between gap-3">
                    <span className="flex h-10 w-10 items-center justify-center rounded-md bg-gold-dim text-gold">
                      <Icon size={19} />
                    </span>
                    <span className="rounded-sm bg-green-dim px-2 py-1 text-xs font-black uppercase text-green">{card.badge}</span>
                  </div>
                  <p className="mt-5 text-xs font-black uppercase tracking-[0.14em] text-[var(--t4)]">{card.label}</p>
                  <h3 className="mt-2 font-cond text-3xl font-black uppercase leading-none">{card.title}</h3>
                  <p className="mt-3 text-sm leading-6 text-[var(--t2)]">{card.body}</p>
                </article>
              </Reveal>
            );
          })}
        </div>
        <p className="mt-4 text-xs text-[var(--t3)]">LEGAL-REVIEW-REQUIRED: all odds references are dynamic, jurisdiction-dependent, and informational.</p>
      </div>
    </section>
  );
}
