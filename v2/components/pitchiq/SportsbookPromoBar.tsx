"use client";

import { ShieldCheck } from "lucide-react";
import { SPORTSBOOK_PROMOS } from "@/lib/pitchiq-data";
import { useToast } from "./Toast";

// LEGAL-REVIEW-REQUIRED: affiliate CTAs intentionally point to # until compliance approval.
export function SportsbookPromoBar() {
  const { showToast } = useToast();

  return (
    <section className="border-y border-[var(--b1)] bg-[var(--surf)] py-5">
      <div className="max-shell">
        <div className="grid gap-3 lg:grid-cols-[220px_1fr] lg:items-center">
          <div className="flex items-center gap-3">
            <ShieldCheck className="text-green" size={22} />
            <div>
              <p className="text-xs font-black uppercase tracking-[0.14em] text-gold">Legal odds context</p>
              <h2 className="font-cond text-2xl font-black uppercase leading-none">Compare Books</h2>
            </div>
          </div>
          <div className="grid gap-3 md:grid-cols-3">
            {SPORTSBOOK_PROMOS.map((promo) => (
              <a
                key={promo.id}
                href="#"
                data-affiliate={promo.id}
                onClick={(event) => {
                  event.preventDefault();
                  showToast(`${promo.name} link pending affiliate activation`, "warning");
                }}
                className="rounded-md border border-[var(--b1)] bg-[var(--bg)] p-4 transition hover:border-gold-border hover:bg-gold-dim"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="font-black">{promo.name}</span>
                  <span className="rounded-sm bg-green-dim px-2 py-1 text-xs font-black text-green">{promo.cta}</span>
                </div>
                <p className="mt-2 text-sm font-bold text-[var(--t1)]">{promo.offer}</p>
                <p className="mt-1 text-xs leading-5 text-[var(--t3)]">{promo.detail}</p>
              </a>
            ))}
          </div>
        </div>
        <p className="mt-3 text-xs text-[var(--t3)]">LEGAL-REVIEW-REQUIRED: availability, promotions, and odds depend on jurisdiction and operator terms.</p>
      </div>
    </section>
  );
}
