"use client";

import { useApp } from "@/app/providers";
import { Reveal } from "./Reveal";
import { groups, schedule } from "./data";

export function StandingsSchedule() {
  const { match } = useApp();
  const liveScore = `${match.home}–${match.away}`;

  return (
    <Reveal className="standings-section">
      <div className="sec-header">
        <div className="sec-title">
          Group Standings
          <span className="sec-sub">Live tables · World Cup 2026</span>
        </div>
        <a className="btn-secondary" href="#">
          All Groups →
        </a>
      </div>

      <div className="std-grid">
        <div className="groups-grid">
          {groups.map((g) => (
            <div className="group-card" key={g.letter}>
              <div className="gc-head">
                <div className="gc-title">{g.letter}</div>
                <div className="gc-sub">{g.sub}</div>
              </div>
              <table className="std-table">
                <thead>
                  <tr>
                    <th>Team</th>
                    <th>P</th>
                    <th>W</th>
                    <th>D</th>
                    <th>GD</th>
                    <th>Pts</th>
                  </tr>
                </thead>
                <tbody>
                  {g.rows.map((r, i) => (
                    <tr key={r.name} className={i === 0 ? "pos-1" : i === 1 ? "pos-2" : undefined}>
                      <td>
                        <div className="std-team">
                          <span className="std-flag">{r.flag}</span>
                          <span className="std-name">{r.name}</span>
                        </div>
                      </td>
                      <td>{r.p}</td>
                      <td>{r.w}</td>
                      <td>{r.d}</td>
                      <td>{r.gd}</td>
                      <td>
                        <span className="std-pts">{r.pts}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>

        <div className="sched-card">
          <div className="sched-head">
            <div className="sched-title">Today&apos;s Schedule</div>
            <div className="sched-date">Jun 12, 2026</div>
          </div>
          {schedule.map((row, i) => {
            const isLive = row.liveMatch;
            const status = isLive && !match.live ? "ft" : row.status;
            const statusLabel = isLive && !match.live ? "FT" : row.statusLabel;
            const score = isLive ? liveScore : row.score;
            const scoreClass =
              status === "ko" ? "is-ko" : status === "live" ? "is-live" : "";
            return (
              <div className="sched-row" key={i}>
                <div className={`sched-status ${status}`}>{statusLabel}</div>
                <div className={`sched-match${status === "ft" ? " is-ft" : ""}`}>{row.match}</div>
                <div className={`sched-score ${scoreClass}`}>{score}</div>
              </div>
            );
          })}
        </div>
      </div>
    </Reveal>
  );
}
