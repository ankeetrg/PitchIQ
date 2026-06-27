"use client";

import { ArrowDownRight, ArrowRight, ArrowUpRight } from "lucide-react";
import { LINE_MOVEMENT } from "@/lib/pitchiq-data";
import { Reveal } from "./Reveal";

// LEGAL-REVIEW-REQUIRED: line movement is displayed for market education only.
export function LineMovementFeed() {
  return (
    <section className="bg-[var(--bg)] py-10">
      <div className="max-shell">
        <Reveal>
          <div className="mb-5 flex flex-col justify-between gap-3 md:flex-row md:items-end">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.18em] text-gold">Market feed</p>
              <h2 className="font-cond text-5xl font-black uppercase leading-none">Line Movement</h2>
            </div>
            <p className="max-w-md text-sm leading-6 text-[var(--t2)]">Opening numbers, current numbers, and signal labels update from API fallback data.</p>
          </div>
        </Reveal>
        <div className="grid gap-3">
          {LINE_MOVEMENT.map((item, index) => {
            const Icon = item.movement === "up" ? ArrowUpRight : item.movement === "down" ? ArrowDownRight : ArrowRight;
            return (
              <Reveal key={item.id} delay={index * 0.05}>
                <div className="grid gap-3 rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-4 shadow-[var(--shadow-soft)] md:grid-cols-[1fr_130px_130px_160px] md:items-center">
                  <div>
                    <div className="text-xs font-black uppercase tracking-[0.14em] text-[var(--t4)]">{item.market}</div>
                    <div className="mt-1 font-cond text-3xl font-black uppercase leading-none">{item.match}</div>
                  </div>
                  <div>
                    <div className="text-xs text-[var(--t4)]">Open</div>
                    <div className="font-bold">{item.open}</div>
                  </div>
                  <div>
                    <div className="text-xs text-[var(--t4)]">Current</div>
                    <div className="font-bold text-gold">{item.current}</div>
                  </div>
                  <div className="flex items-center gap-2 rounded-md bg-[var(--bg)] px-3 py-2">
                    <Icon className={item.movement === "down" ? "text-red" : item.movement === "up" ? "text-green" : "text-[var(--t3)]"} size={18} />
                    <div>
                      <div className="text-xs font-black text-[var(--t1)]">{item.move}</div>
                      <div className="text-xs text-[var(--t3)]">{item.signal}</div>
                    </div>
                  </div>
                </div>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
