"use client";

import { Bell, Newspaper } from "lucide-react";
import { ALERTS, NEWS_ITEMS } from "@/lib/pitchiq-data";
import { Reveal } from "./Reveal";

const toneClasses = {
  info: "bg-blue-dim text-blue",
  warning: "bg-gold-dim text-gold",
  success: "bg-green-dim text-green",
} as const;

export function NewsAndAlerts() {
  return (
    <section id="news" className="bg-[var(--bg2)] py-10">
      <div className="max-shell grid gap-5 lg:grid-cols-[1fr_420px]">
        <Reveal>
          <div className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
            <div className="mb-5 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-black uppercase tracking-[0.14em] text-gold">Analysis desk</p>
                <h2 className="mt-1 font-cond text-4xl font-black uppercase leading-none">News and Analysis</h2>
              </div>
              <Newspaper className="text-[var(--t3)]" size={22} />
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {NEWS_ITEMS.map((item) => (
                <article key={item.id} className="rounded-md border border-[var(--b1)] bg-[var(--bg)] p-4">
                  <div className="flex items-center justify-between gap-3">
                    <span className="rounded-sm bg-gold-dim px-2 py-1 text-xs font-black uppercase text-gold">{item.category}</span>
                    <span className="text-xs font-bold text-[var(--t3)]">{item.readTime}</span>
                  </div>
                  <h3 className="headline-pretty mt-4 font-cond text-2xl font-black uppercase leading-none">{item.title}</h3>
                  <p className="mt-3 text-sm leading-6 text-[var(--t2)]">{item.summary}</p>
                </article>
              ))}
            </div>
          </div>
        </Reveal>

        <Reveal delay={0.08}>
          <aside className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
            <div className="mb-5 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-black uppercase tracking-[0.14em] text-green">Live alerts</p>
                <h2 className="mt-1 font-cond text-4xl font-black uppercase leading-none">Alert Feed</h2>
              </div>
              <Bell className="text-[var(--t3)]" size={22} />
            </div>
            <div className="space-y-3">
              {ALERTS.map((alert) => (
                <div key={alert.id} className="rounded-md border border-[var(--b1)] bg-[var(--bg)] p-4">
                  <div className="flex items-center justify-between gap-3">
                    <span className={`rounded-sm px-2 py-1 text-xs font-black uppercase ${toneClasses[alert.tone]}`}>{alert.time}</span>
                    <span className="text-xs font-bold text-[var(--t3)]">PitchIQ</span>
                  </div>
                  <h3 className="mt-3 font-black">{alert.title}</h3>
                  <p className="mt-2 text-sm leading-6 text-[var(--t2)]">{alert.body}</p>
                </div>
              ))}
            </div>
          </aside>
        </Reveal>
      </div>
    </section>
  );
}
