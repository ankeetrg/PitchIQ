"use client";

import { useApp } from "@/app/providers";
import { Reveal } from "./Reveal";
import { parlay } from "./data";

export function ParlayCard() {
  const { showToast } = useApp();
  return (
    <Reveal className="parlay-section">
      <div className="parlay-card">
        <div className="parlay-head">
          <div>
            <div className="parlay-eyebrow">✦ AI Parlay of the Day</div>
            <div className="parlay-title">
              Three-Leg Value Builder
              <br />
              Modeled at 18.4% Edge
            </div>
          </div>
          <div className="parlay-odds">
            <div className="parlay-odds-val">{parlay.odds}</div>
            <div className="parlay-odds-lbl">Combined Odds</div>
          </div>
        </div>

        <div className="parlay-legs">
          {parlay.legs.map((leg, i) => (
            <div className="parlay-leg" key={i}>
              <div className="parlay-leg-num">{i + 1}</div>
              <div className="parlay-leg-body">
                <div className="parlay-leg-name">{leg.name}</div>
                <div className="parlay-leg-match">{leg.match}</div>
              </div>
              <div className="parlay-leg-odds">{leg.odds}</div>
              <div className="parlay-leg-conf">{leg.conf}% conf.</div>
            </div>
          ))}
        </div>

        <button
          className="parlay-cta"
          onClick={() => showToast("✓ Parlay added to your DraftKings bet slip!")}
        >
          Add Parlay at DraftKings {parlay.odds} →
        </button>
      </div>
    </Reveal>
  );
}
