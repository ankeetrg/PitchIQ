"use client";

import { Brain, CheckCircle2 } from "lucide-react";
import { PARLAY } from "@/lib/pitchiq-data";
import { Reveal } from "./Reveal";
import { useToast } from "./Toast";

// LEGAL-REVIEW-REQUIRED: AI picks and odds must remain labeled as educational, not financial advice.
export function AIParlayCard() {
  const { showToast } = useToast();

  return (
    <section className="bg-[var(--bg)] py-10">
      <div className="max-shell">
        <Reveal>
          <article className="overflow-hidden rounded-lg border border-[var(--b1)] bg-[var(--surf)] shadow-[var(--shadow)]">
            <div className="grid gap-0 lg:grid-cols-[0.9fr_1.1fr]">
              <div className="bg-[linear-gradient(135deg,#091424_0%,#0D2248_54%,#102E60_100%)] p-6 text-white">
                <div className="flex items-center gap-3">
                  <span className="flex h-11 w-11 items-center justify-center rounded-md bg-gold">
                    <Brain size={22} />
                  </span>
                  <div>
                    <p className="text-xs font-black uppercase tracking-[0.16em] text-white/55">AI-generated analysis</p>
                    <h2 className="font-cond text-4xl font-black uppercase leading-none">{PARLAY.title}</h2>
                  </div>
                </div>
                <div className="mt-7 font-cond text-7xl font-black leading-none text-gold">{PARLAY.payout}</div>
                <p className="mt-2 text-sm font-bold text-white/70">Composite confidence: {PARLAY.confidence}%</p>
                <p className="mt-5 max-w-md text-sm leading-6 text-white/68">{PARLAY.rationale}</p>
              </div>

              <div className="p-6">
                <div className="space-y-3">
                  {PARLAY.legs.map((leg) => (
                    <div key={leg.id} className="rounded-md border border-[var(--b1)] bg-[var(--bg)] p-4">
                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-3">
                          <CheckCircle2 className="text-green" size={20} />
                          <span className="font-black">{leg.label}</span>
                        </div>
                        <span className="font-cond text-2xl font-black text-gold">{leg.odds}</span>
                      </div>
                      <div className="mt-3 h-2 overflow-hidden rounded-full bg-[var(--b1)]">
                        <div className="h-full rounded-full bg-green" style={{ width: `${leg.confidence}%` }} />
                      </div>
                      <div className="mt-1 text-right text-xs font-bold text-[var(--t3)]">{leg.confidence}% confidence</div>
                    </div>
                  ))}
                </div>
                <button
                  type="button"
                  onClick={() => showToast("AI parlay saved to watchlist", "success")}
                  className="mt-5 min-h-11 w-full rounded-md bg-green px-5 text-sm font-black text-white transition hover:bg-green-hover"
                >
                  Save AI Card
                </button>
                <p className="mt-3 text-xs leading-5 text-[var(--t3)]">LEGAL-REVIEW-REQUIRED: AI content is informational. Check books, laws, and bankroll rules before any wager.</p>
              </div>
            </div>
          </article>
        </Reveal>
      </div>
    </section>
  );
}
