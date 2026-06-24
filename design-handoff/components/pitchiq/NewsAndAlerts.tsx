import { Reveal } from "./Reveal";
import { news, alerts } from "./data";

export function NewsAndAlerts() {
  return (
    <Reveal className="news-section">
      <div className="sec-header">
        <div className="sec-title">Latest Analysis &amp; News</div>
        <a className="btn-secondary" href="/world-cup-2026">
          All Articles →
        </a>
      </div>

      <div className="news-alerts-grid">
        <div className="news-grid">
          {news.map((n, i) => (
            <div className={`news-card${n.featured ? " featured" : ""}`} key={i}>
              <div className="nc-img">
                <div className={`nc-img-inner ${n.variant}`}>{n.icon}</div>
                <div className="nc-cat">{n.cat}</div>
              </div>
              <div className="nc-body">
                <div className="nc-headline">{n.headline}</div>
                <div className="nc-meta">
                  <span className="by">{n.by}</span>
                  <span className="nc-meta-dot">·</span>
                  <span>{n.date}</span>
                  <span className="nc-meta-dot">·</span>
                  <span>{n.read}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="alert-card">
          <div className="alert-head">
            <div className="alert-title">Live Alerts</div>
            <a className="alert-link" href="/world-cup-2026/scores">
              All →
            </a>
          </div>
          {alerts.map((a, i) => (
            <div className="alert-row" key={i}>
              <div className={`alert-icon ${a.kind}`}>{a.icon}</div>
              <div className="alert-body">
                <div className="alert-player">{a.player}</div>
                <div className="alert-msg">{a.msg}</div>
                <div className="alert-time">{a.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Reveal>
  );
}
