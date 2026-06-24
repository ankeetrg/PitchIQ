import { footerCols } from "./data";

export function Footer() {
  return (
    <footer className="footer">
      <div className="w">
        <div className="ft-grid">
          <div>
            <div className="ft-logo">
              Pitch<span>IQ</span>
            </div>
            <div className="ft-tagline">
              AI-powered soccer intelligence for fantasy players and sports bettors. World Cup 2026
              and beyond.
            </div>
            <div className="ft-socials">
              <a className="ft-social" href="#" aria-label="X">𝕏</a>
              <a className="ft-social" href="#" aria-label="LinkedIn">in</a>
              <a className="ft-social" href="#" aria-label="YouTube">▶</a>
              <a className="ft-social" href="#" aria-label="Instagram">📸</a>
            </div>
          </div>
          {footerCols.map((col) => (
            <div className="ft-col" key={col.title}>
              <div className="ft-col-title">{col.title}</div>
              <ul>
                {col.links.map((l) => (
                  <li key={l}>
                    <a href="#">{l}</a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="ft-bot">
          <div className="ft-legal">
            © 2026 PitchIQ · <a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="#">About</a>
          </div>
          <div className="ft-disclaimer">
            Gambling involves risk. Must be of legal age in your jurisdiction. PitchIQ is an
            entertainment &amp; information service — not a licensed sportsbook.
          </div>
        </div>
      </div>
    </footer>
  );
}
