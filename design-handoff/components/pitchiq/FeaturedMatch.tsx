"use client";

import { motion } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { useApp } from "@/app/providers";

function fmtOdds(v: number) {
  return v > 0 ? `+${v}` : `${v}`;
}

function OddValue({ value, kind }: { value: number; kind: "fav" | "dog" }) {
  const [flash, setFlash] = useState(false);
  const prev = useRef(value);
  useEffect(() => {
    if (prev.current !== value) {
      prev.current = value;
      setFlash(true);
      const t = window.setTimeout(() => setFlash(false), 600);
      return () => window.clearTimeout(t);
    }
  }, [value]);
  return (
    <div className={`mh-odd-val ${kind}${flash ? " flash-odds" : ""}`}>{fmtOdds(value)}</div>
  );
}

export function FeaturedMatch() {
  const { match, odds, prob, scoreFlashId } = useApp();
  const [scoreFlash, setScoreFlash] = useState(false);

  useEffect(() => {
    if (scoreFlashId === 0) return;
    setScoreFlash(true);
    const t = window.setTimeout(() => setScoreFlash(false), 800);
    return () => window.clearTimeout(t);
  }, [scoreFlashId]);

  const score = `${match.home}–${match.away}`;
  const minLabel = match.live ? `${match.min}'` : "FT";

  return (
    <div className="match-hero">
      <div className="mh-header">
        <div className="mh-badge">
          Group E · Match 1 · <span>MetLife Stadium, NJ</span>
        </div>
        <div className={`mh-live-pill${match.live ? "" : " ended"}`}>
          <div className="dot" />
          <span>{minLabel}</span>
        </div>
        <div className="mh-time">Jun 12, 2026 · 3:00 PM ET</div>
      </div>

      <div className="mh-teams">
        <div className="mh-team">
          <div className="mh-team-flag">🇫🇷</div>
          <div className="mh-team-name">France</div>
          <div className="mh-team-form">
            <div className="mh-fp w">W</div>
            <div className="mh-fp w">W</div>
            <div className="mh-fp w">W</div>
            <div className="mh-fp d">D</div>
            <div className="mh-fp w">W</div>
          </div>
        </div>
        <div className="mh-vs">
          <div className="mh-vs-text">vs</div>
          <div className={`mh-score${scoreFlash ? " flash" : ""}`}>{score}</div>
          <div className="mh-score-min">● {minLabel}</div>
        </div>
        <div className="mh-team">
          <div className="mh-team-flag">🇺🇾</div>
          <div className="mh-team-name">Uruguay</div>
          <div className="mh-team-form">
            <div className="mh-fp w">W</div>
            <div className="mh-fp w">W</div>
            <div className="mh-fp d">D</div>
            <div className="mh-fp l">L</div>
            <div className="mh-fp w">W</div>
          </div>
        </div>
      </div>

      {/* Live odds strip */}
      <div className="mh-odds">
        <div className="mh-odd">
          <div className="mh-odd-label">France Win</div>
          <OddValue value={odds.fra} kind="fav" />
          <div className="mh-odd-move up">▲ moved</div>
          <div className="mh-odd-book">DraftKings</div>
        </div>
        <div className="mh-odd">
          <div className="mh-odd-label">Draw</div>
          <OddValue value={odds.draw} kind="dog" />
          <div className="mh-odd-move down">▼ moved</div>
          <div className="mh-odd-book">FanDuel</div>
        </div>
        <div className="mh-odd">
          <div className="mh-odd-label">Uruguay Win</div>
          <OddValue value={odds.uru} kind="dog" />
          <div className="mh-odd-move up">▲ moved</div>
          <div className="mh-odd-book">BetMGM</div>
        </div>
        <div className="mh-odd">
          <div className="mh-odd-label">O/U 2.5 Goals</div>
          <OddValue value={odds.ou} kind="dog" />
          <div className="mh-odd-move" style={{ color: "var(--t4)" }}>
            — even
          </div>
          <div className="mh-odd-book">Caesars</div>
        </div>
      </div>

      {/* AI probability */}
      <div className="mh-prob">
        <div className="mh-prob-head">
          <div className="mh-prob-title">AI Win Probability — 50,000 Simulations</div>
          <div className="mh-prob-ai-badge">✦ PitchIQ AI</div>
        </div>
        <div className="prob-bar-wrap">
          <motion.div
            className="prob-seg home"
            initial={{ width: "0%" }}
            animate={{ width: `${prob.h}%` }}
            transition={{ duration: 1.4, ease: [0.4, 0, 0.2, 1] }}
          />
          <motion.div
            className="prob-seg draw"
            initial={{ width: "0%" }}
            animate={{ width: `${prob.d}%` }}
            transition={{ duration: 1.4, ease: [0.4, 0, 0.2, 1] }}
          />
          <motion.div
            className="prob-seg away"
            initial={{ width: "0%" }}
            animate={{ width: `${prob.a}%` }}
            transition={{ duration: 1.4, ease: [0.4, 0, 0.2, 1] }}
          />
        </div>
        <div className="prob-labels">
          <div className="prob-lbl">
            <span className="pct">{prob.h}%</span>
            <span className="team">France Win</span>
          </div>
          <div className="prob-lbl c">
            <span className="pct">{prob.d}%</span>
            <span className="team">Draw</span>
          </div>
          <div className="prob-lbl">
            <span className="pct">{prob.a}%</span>
            <span className="team">Uruguay Win</span>
          </div>
        </div>
      </div>

      {/* Key stats */}
      <div className="mh-stats">
        <div className="mh-stat">
          <div className="mh-stat-val">3–1–1</div>
          <div className="mh-stat-lbl">H2H Last 5</div>
        </div>
        <div className="mh-stat">
          <div className="mh-stat-val">
            <em>2.8</em>
          </div>
          <div className="mh-stat-lbl">France xG/Game</div>
        </div>
        <div className="mh-stat">
          <div className="mh-stat-val">1.4</div>
          <div className="mh-stat-lbl">Uruguay xG/Game</div>
        </div>
        <div className="mh-stat">
          <div className="mh-stat-val">
            <em>High</em>
          </div>
          <div className="mh-stat-lbl">AI Confidence</div>
        </div>
      </div>

      {/* CTA row */}
      <div className="mh-cta">
        <a className="btn-primary" href="#">
          Bet at DraftKings {fmtOdds(odds.fra)} →
        </a>
        <a className="btn-secondary" href="#">
          Full Match Analysis
        </a>
        <div className="mh-cta-note">Odds live · Updated 2 min ago · 18+ only</div>
      </div>
    </div>
  );
}
