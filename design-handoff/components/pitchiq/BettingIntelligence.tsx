import { Reveal } from "./Reveal";

export function BettingIntelligence() {
  return (
    <Reveal className="betting-section">
      <div className="sec-header">
        <div className="sec-title">
          Betting Intelligence
          <span className="sec-sub">AI-identified value across all markets</span>
        </div>
        <a className="btn-secondary" href="#">
          All Picks →
        </a>
      </div>

      <div className="bet-grid">
        {/* Best Value */}
        <div className="bet-card">
          <div className="bc-head">
            <div className="bc-label">Best Value Bet · Today</div>
            <div className="bc-badge value">AI PICK</div>
          </div>
          <div className="bc-body">
            <div className="bc-bet-name">France to Score First</div>
            <div className="bc-match">FRA vs URU · Group E · MetLife Stadium</div>
            <div className="bc-books">
              <div className="bc-book-row best">
                <span className="bc-book-name">DraftKings</span>
                <span className="bc-book-odds">+120</span>
                <span className="bc-book-best-tag">BEST</span>
              </div>
              <div className="bc-book-row">
                <span className="bc-book-name">FanDuel</span>
                <span className="bc-book-odds">+115</span>
              </div>
              <div className="bc-book-row">
                <span className="bc-book-name">BetMGM</span>
                <span className="bc-book-odds">+110</span>
              </div>
            </div>
            <div className="bc-meta">
              <div className="bc-chip pos">Value 8.4/10</div>
              <div className="bc-chip pos">74% Hit Rate</div>
              <div className="bc-chip">Last 12 WC Games</div>
            </div>
            <a className="bc-cta" href="#">
              Bet at DraftKings +120 →
            </a>
          </div>
        </div>

        {/* Sharp Money */}
        <div className="bet-card">
          <div className="bc-head">
            <div className="bc-label">Sharp Money Alert</div>
            <div className="bc-badge sharp">SHARP</div>
          </div>
          <div className="bc-body">
            <div className="bc-bet-name">Uruguay ML — Line Moving</div>
            <div className="bc-match">FRA vs URU · Group E · Today</div>
            <div className="bc-move-wrap">
              <div className="bc-move-title">Line Movement — Last 6 Hours</div>
              <div className="bc-move-chart">
                <div className="bc-bar" style={{ height: "30%" }} />
                <div className="bc-bar" style={{ height: "38%" }} />
                <div className="bc-bar" style={{ height: "34%" }} />
                <div className="bc-bar high" style={{ height: "62%" }} />
                <div className="bc-bar high" style={{ height: "76%" }} />
                <div className="bc-bar now" style={{ height: "60%" }} />
              </div>
            </div>
            <div className="bc-books">
              <div className="bc-book-row">
                <span className="bc-book-name">Opened</span>
                <span className="bc-book-odds" style={{ color: "var(--t3)" }}>
                  +420
                </span>
              </div>
              <div className="bc-book-row best">
                <span className="bc-book-name">Current Best</span>
                <span className="bc-book-odds">+380</span>
                <span className="bc-book-best-tag">NOW</span>
              </div>
            </div>
            <div className="bc-meta">
              <div className="bc-chip neg">−40 pts moved</div>
              <div className="bc-chip shr">Sharp action</div>
            </div>
            <a className="bc-cta" href="#">
              Track at BetMGM →
            </a>
          </div>
        </div>

        {/* Public vs Sharp */}
        <div className="bet-card">
          <div className="bc-head">
            <div className="bc-label">Public vs Sharp · Over/Under</div>
            <div className="bc-badge move">TRENDING</div>
          </div>
          <div className="bc-body">
            <div className="bc-bet-name">FRA vs URU — Over 2.5</div>
            <div className="bc-match">Total Goals Market · Best: −110 Caesars</div>
            <div className="bc-books" style={{ marginBottom: "10px" }}>
              <div className="bc-book-row best">
                <span className="bc-book-name">Caesars</span>
                <span className="bc-book-odds">−110</span>
                <span className="bc-book-best-tag">BEST</span>
              </div>
              <div className="bc-book-row">
                <span className="bc-book-name">DraftKings</span>
                <span className="bc-book-odds">−115</span>
              </div>
            </div>
            <div className="bc-split-wrap">
              <div className="bc-split-labels">
                <span style={{ color: "var(--blue)" }}>OVER 62%</span>
                <span style={{ color: "var(--red)" }}>UNDER 38%</span>
              </div>
              <div className="bc-split-bar">
                <div className="bc-split-home" style={{ width: "62%" }} />
                <div className="bc-split-away" style={{ width: "38%" }} />
              </div>
            </div>
            <div className="bc-meta">
              <div className="bc-chip pos">62% Tickets → Over</div>
              <div className="bc-chip pos">71% Money → Over</div>
            </div>
            <a className="bc-cta" href="#">
              Bet Over at Caesars →
            </a>
          </div>
        </div>
      </div>
    </Reveal>
  );
}
