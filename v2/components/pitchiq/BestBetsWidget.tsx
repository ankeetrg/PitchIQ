"use client";

import { Check, Plus } from "lucide-react";
import { useState } from "react";
import { BEST_BETS } from "@/lib/pitchiq-data";
import { useToast } from "./Toast";

// LEGAL-REVIEW-REQUIRED: betting line display must remain informational and include responsible-gaming disclaimers.
export function BestBetsWidget() {
  const { showToast } = useToast();
  const [picked, setPicked] = useState<Set<string>>(new Set());

  return (
    <aside className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.14em] text-green">Best Bets</p>
          <h2 className="mt-1 font-cond text-3xl font-black uppercase leading-none">Edge Board</h2>
        </div>
        <span className="rounded-sm bg-gold-dim px-2 py-1 text-xs font-black uppercase tracking-[0.12em] text-gold">AI-ranked</span>
      </div>

      <div className="mt-5 space-y-3">
        {BEST_BETS.map((bet) => {
          const active = picked.has(bet.id);
          return (
            <button
              type="button"
              key={bet.id}
              onClick={() => {
                setPicked((current) => {
                  const next = new Set(current);
                  if (next.has(bet.id)) {
                    next.delete(bet.id);
                  } else {
                    next.add(bet.id);
                    showToast(`${bet.label} added to picks`, "success");
                  }
                  return next;
                });
              }}
              className={`w-full rounded-md border p-3 text-left transition ${
                active ? "border-green-border bg-green-dim" : "border-[var(--b1)] bg-[var(--bg)] hover:border-gold-border"
              }`}
            >
              <div className="flex items-center justify-between gap-3">
                <span className="font-bold">{bet.label}</span>
                <span className="flex h-8 w-8 items-center justify-center rounded-sm bg-[var(--surf)] text-green">
                  {active ? <Check size={16} /> : <Plus size={16} />}
                </span>
              </div>
              <div className="mt-2 grid grid-cols-3 gap-2 text-xs font-bold text-[var(--t3)]">
                <span>{bet.odds}</span>
                <span>{bet.edge}</span>
                <span>{bet.confidence}%</span>
              </div>
            </button>
          );
        })}
      </div>
      <p className="mt-4 text-xs leading-5 text-[var(--t3)]">LEGAL-REVIEW-REQUIRED: odds vary by state and sportsbook. Affiliate links stay inactive until activation.</p>
    </aside>
  );
}
