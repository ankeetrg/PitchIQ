"use client";

import { BarChart3, Bell, Home, Trophy } from "lucide-react";
import { useState } from "react";
import { CricketModal } from "./CricketModal";

const items = [
  { label: "Home", href: "#", icon: Home },
  { label: "Fantasy", href: "#fantasy", icon: Trophy },
  { label: "Lines", href: "#predictions", icon: BarChart3 },
  { label: "Alerts", href: "#newsletter", icon: Bell },
];

export function MobileBottomNav() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <nav className="fixed inset-x-0 bottom-0 z-[220] border-t border-[var(--b1)] bg-[var(--surf)]/95 backdrop-blur md:hidden" aria-label="Mobile navigation">
        <div className="grid h-[64px] grid-cols-4">
          {items.map((item) => {
            const Icon = item.icon;
            return (
              <a key={item.label} href={item.href} className="flex flex-col items-center justify-center gap-1 text-[11px] font-black text-[var(--t3)] transition hover:text-gold">
                <Icon size={19} />
                {item.label}
              </a>
            );
          })}
        </div>
        <button
          type="button"
          onClick={() => setModalOpen(true)}
          className="absolute right-3 top-[-52px] flex h-11 items-center gap-2 rounded-md bg-gold px-4 text-xs font-black uppercase text-white shadow-[var(--shadow)]"
        >
          Cricket
        </button>
      </nav>
      <CricketModal open={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  );
}
