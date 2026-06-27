"use client";

import Image from "next/image";
import { Check, Plus } from "lucide-react";
import { useMemo, useState } from "react";
import { FANTASY_PICKS } from "@/lib/pitchiq-data";
import type { FantasyPosition } from "@/lib/pitchiq-types";
import { Reveal } from "./Reveal";
import { useToast } from "./Toast";

const filters: Array<"ALL" | FantasyPosition> = ["ALL", "FWD", "MID", "DEF", "GK"];

const positionClasses: Record<FantasyPosition, string> = {
  FWD: "bg-red-dim text-red",
  MID: "bg-green-dim text-green",
  DEF: "bg-blue-dim text-blue",
  GK: "bg-gold-dim text-gold",
};

export function FantasyPicks() {
  const { showToast } = useToast();
  const [filter, setFilter] = useState<"ALL" | FantasyPosition>("ALL");
  const [picked, setPicked] = useState<Set<string>>(new Set());

  const rows = useMemo(
    () => FANTASY_PICKS.filter((pick) => filter === "ALL" || pick.position === filter),
    [filter],
  );

  return (
    <section id="fantasy" className="bg-[var(--bg2)] py-10">
      <div className="max-shell">
        <Reveal>
          <div className="mb-5 flex flex-col justify-between gap-3 md:flex-row md:items-end">
            <div>
              <p className="text-xs font-black uppercase tracking-[0.18em] text-gold">DFS and captain pool</p>
              <h2 className="font-cond text-5xl font-black uppercase leading-none">Fantasy Picks</h2>
            </div>
            <div className="flex flex-wrap gap-2">
              {filters.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setFilter(item)}
                  className={`rounded-md border px-4 py-2 text-sm font-black transition ${
                    filter === item
                      ? "border-green-border bg-green text-white"
                      : "border-[var(--b1)] bg-[var(--surf)] text-[var(--t2)] hover:border-gold-border hover:text-gold"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </Reveal>

        <Reveal delay={0.08}>
          <div className="overflow-hidden rounded-lg border border-[var(--b1)] bg-[var(--surf)] shadow-[var(--shadow-soft)]">
            <div className="overflow-x-auto">
              <table className="w-full min-w-[820px] text-sm">
                <thead className="bg-[var(--bg)] text-[11px] uppercase tracking-[0.14em] text-[var(--t4)]">
                  <tr>
                    <th className="px-4 py-3 text-left">Player</th>
                    <th className="px-3 py-3 text-left">Pos</th>
                    <th className="px-3 py-3 text-right">Salary</th>
                    <th className="px-3 py-3 text-right">Proj</th>
                    <th className="px-3 py-3 text-right">Own</th>
                    <th className="px-3 py-3 text-right">Edge</th>
                    <th className="px-4 py-3 text-right">Pick</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((pick) => {
                    const active = picked.has(pick.id);
                    return (
                      <tr key={pick.id} className={`border-t border-[var(--b1)] transition ${active ? "bg-green-dim" : ""}`}>
                        <td className="px-4 py-4">
                          <div className="flex items-center gap-3">
                            <Image
                              src={`https://flagcdn.com/w40/${pick.flagCode}.png`}
                              alt={`${pick.team} flag`}
                              width={26}
                              height={18}
                              sizes="26px"
                              className="h-[18px] w-[26px] rounded-sm object-cover"
                            />
                            <div>
                              <div className="font-black">{pick.player}</div>
                              <div className="mt-1 text-xs text-[var(--t3)]">{pick.note}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-3 py-4">
                          <span className={`rounded-sm px-2 py-1 text-xs font-black ${positionClasses[pick.position]}`}>{pick.position}</span>
                        </td>
                        <td className="px-3 py-4 text-right font-bold">{pick.salary}</td>
                        <td className="px-3 py-4 text-right font-black">{pick.projection.toFixed(1)}</td>
                        <td className="px-3 py-4 text-right text-[var(--t2)]">{pick.ownership}</td>
                        <td className="px-3 py-4 text-right font-black text-green">{pick.edge}</td>
                        <td className="px-4 py-4 text-right">
                          <button
                            type="button"
                            onClick={() => {
                              setPicked((current) => {
                                const next = new Set(current);
                                if (next.has(pick.id)) {
                                  next.delete(pick.id);
                                } else {
                                  next.add(pick.id);
                                  showToast(`${pick.player} added to fantasy card`, "success");
                                }
                                return next;
                              });
                            }}
                            className={`inline-flex h-9 w-9 items-center justify-center rounded-md border transition ${
                              active
                                ? "border-green-border bg-green text-white"
                                : "border-[var(--b1)] bg-[var(--bg)] text-[var(--t2)] hover:border-green-border hover:text-green"
                            }`}
                            aria-label={`Toggle ${pick.player}`}
                          >
                            {active ? <Check size={16} /> : <Plus size={16} />}
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
