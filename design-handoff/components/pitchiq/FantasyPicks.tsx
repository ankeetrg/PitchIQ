"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { useApp } from "@/app/providers";
import { Reveal } from "./Reveal";
import { players, type Pos } from "./data";

type Filter = "all" | Pos;
const filters: Filter[] = ["all", "FWD", "MID", "DEF", "GK"];
const sortTabs = ["Proj Pts", "Ownership", "Value"];

export function FantasyPicks() {
  const { showToast } = useApp();
  const [filter, setFilter] = useState<Filter>("all");
  const [sort, setSort] = useState("Proj Pts");
  const [picked, setPicked] = useState<Set<string>>(new Set());
  const [bump, setBump] = useState<string | null>(null);

  function togglePick(name: string) {
    setPicked((prev) => {
      const next = new Set(prev);
      const isPicked = next.has(name);
      if (isPicked) {
        next.delete(name);
        showToast(`${name} removed`);
      } else {
        next.add(name);
        showToast(`✓ ${name} added to lineup!`);
        setBump(name);
        window.setTimeout(() => setBump((b) => (b === name ? null : b)), 180);
      }
      return next;
    });
  }

  return (
    <Reveal className="fantasy-section">
      <div className="sec-header">
        <div className="sec-title">
          Fantasy Picks
          <span className="sec-sub">World Cup 2026 · Matchday 1 · Jun 12</span>
        </div>
        <div className="sec-right">
          <div className="sec-tabs">
            {sortTabs.map((t) => (
              <div
                key={t}
                className={`sec-tab${sort === t ? " active" : ""}`}
                onClick={() => setSort(t)}
              >
                {t}
              </div>
            ))}
          </div>
          <a className="btn-view-all" href="#">
            View All 250+ →
          </a>
        </div>
      </div>

      <div className="fp-card">
        <div className="fp-toolbar">
          <div className="fp-filters">
            {filters.map((f) => (
              <div
                key={f}
                className={`fp-filter${filter === f ? " active" : ""}`}
                data-pos={f === "all" ? undefined : f}
                onClick={() => setFilter(f)}
              >
                {f === "all" ? "All" : f}
              </div>
            ))}
          </div>
          <div className="fp-info">
            Projections updated 12 min ago · AI model + form + matchup data
          </div>
        </div>

        <table className="fp-table">
          <thead>
            <tr>
              <th>Rk</th>
              <th>Player</th>
              <th>Pos</th>
              <th>Match</th>
              <th className="num">Proj Pts ▼</th>
              <th className="num">Own %</th>
              <th className="num">vs Avg</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {players.map((p) => {
              const hidden = filter !== "all" && p.pos !== filter;
              const isPicked = picked.has(p.name);
              return (
                <tr
                  key={p.name}
                  className={isPicked ? "picked" : undefined}
                  style={hidden ? { display: "none" } : undefined}
                >
                  <td className="fp-rank">{p.rank}</td>
                  <td>
                    <div className="fp-player">
                      <div className="fp-avatar">{p.flag}</div>
                      <div>
                        <div className="fp-name">{p.name}</div>
                        <div className="fp-nation">{p.nation}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className={`pos-pill ${p.pos}`}>{p.pos}</span>
                  </td>
                  <td>
                    <div className="fp-match">
                      {p.matchTeam} <span className="opp">{p.opp}</span>
                    </div>
                  </td>
                  <td className="num fp-proj">
                    {p.proj} <span className="pts-lbl">pts</span>
                  </td>
                  <td className="num">
                    <div className="fp-own-wrap">
                      <div className="fp-own-pct">{p.own}</div>
                      <div className="fp-own-bar">
                        <motion.div
                          className="fp-own-fill"
                          initial={{ width: "0%" }}
                          whileInView={{ width: p.own }}
                          viewport={{ once: true, amount: 0.1 }}
                          transition={{ duration: 1, ease: "easeOut" }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="num">
                    <div className={`fp-trend ${p.trendKind}`}>{p.trend}</div>
                  </td>
                  <td>
                    <button
                      className={`btn-pick${isPicked ? " picked" : ""}`}
                      onClick={() => togglePick(p.name)}
                      style={bump === p.name ? { transform: "scale(1.12)" } : undefined}
                    >
                      {isPicked ? "✓ Picked" : "+ Pick"}
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        <div className="fp-footer">
          <div className="fp-footer-note">
            Projections powered by PitchIQ AI · Updated every 15 min during live matches
          </div>
          <a className="btn-view-all" href="#">
            View Full Rankings →
          </a>
        </div>
      </div>
    </Reveal>
  );
}
