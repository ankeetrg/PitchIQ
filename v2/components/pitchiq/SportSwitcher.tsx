"use client";

import { Trophy } from "lucide-react";
import { useState } from "react";
import { CricketModal } from "./CricketModal";

const sports = [
  { id: "soccer", label: "World Cup 2026", live: true },
  { id: "cricket", label: "Cricket", live: false },
] as const;

export function SportSwitcher() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <section className="sticky top-[108px] z-[185] border-b border-[var(--b1)] bg-[var(--bg)]/95 backdrop-blur">
        <div className="max-shell sport-switcher flex h-14 items-center gap-3 overflow-x-auto">
          {sports.map((sport) => (
            <button
              key={sport.id}
              type="button"
              onClick={() => {
                if (sport.id === "cricket") {
                  setModalOpen(true);
                }
              }}
              className={`flex shrink-0 items-center gap-2 rounded-md border px-4 py-2 text-sm font-black transition ${
                sport.live
                  ? "border-green-border bg-green-dim text-green"
                  : "border-[var(--b1)] bg-[var(--surf)] text-[var(--t2)] hover:border-gold-border hover:text-gold"
              }`}
            >
              <Trophy size={16} />
              {sport.label}
              {sport.live ? <span className="pulse-dot h-2 w-2 rounded-full bg-green" /> : null}
            </button>
          ))}
        </div>
      </section>
      <CricketModal open={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  );
}
