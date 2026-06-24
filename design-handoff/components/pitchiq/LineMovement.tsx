import { Reveal } from "./Reveal";
import { lineMoves } from "./data";

export function LineMovement() {
  return (
    <Reveal className="lm-section">
      <div className="sec-header">
        <div className="sec-title">
          Line Movement
          <span className="sec-sub">Where the money is moving right now</span>
        </div>
        <a className="btn-secondary" href="#">
          Full Tracker →
        </a>
      </div>

      <div className="lm-grid">
        {lineMoves.map((m, i) => (
          <div className="lm-card" key={i}>
            <span className={`lm-tag ${m.tagKind}`}>{m.tag}</span>
            <div className="lm-name">{m.name}</div>
            <div className="lm-match">{m.match}</div>
            <div className="lm-line">
              <span className="lm-open">{m.open}</span>
              <span className="lm-arrow-sep">→</span>
              <span className="lm-now">{m.now}</span>
              <span className={`lm-move ${m.moveKind}`}>{m.move}</span>
            </div>
          </div>
        ))}
      </div>
    </Reveal>
  );
}
