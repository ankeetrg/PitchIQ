import { Newsletter } from "@/components/pitchiq/Newsletter";

export function StickyLiveScoresLink() {
  return (
    <div className="sticky-score-link">
      <a href="/world-cup-2026/scores">Live scores</a>
      <span>Updated match center, odds movement, and AI picks.</span>
    </div>
  );
}

export function FantasyToolCta() {
  return (
    <div className="fantasy-tool-cta">
      <div>
        <strong>Build the lineup before kickoff.</strong>
        <span>Projected points, ownership, and AI-ranked value plays for World Cup 2026.</span>
      </div>
      <a href="/world-cup-2026/fantasy">Open Fantasy Tool</a>
    </div>
  );
}

export function MidArticleSignup() {
  return <Newsletter compact />;
}

export function BottomArticleSignup() {
  return <Newsletter compact title="Get PitchIQ Daily" />;
}
