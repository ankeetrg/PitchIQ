export function OddsDisclaimer() {
  return (
    <p className="content-disclaimer">
      Odds shown are for informational purposes only. Gambling may be illegal in your
      jurisdiction. AI picks are estimates, not guarantees.
    </p>
  );
}

// LEGAL-REVIEW-REQUIRED
export function AffiliateOddsSlot() {
  const books = ["DraftKings", "FanDuel", "BetMGM", "Caesars"];

  return (
    <div className="affiliate-slot" aria-label="Sportsbook offers">
      <div className="affiliate-copy">
        <strong>Sportsbook offers</strong>
        <span>Affiliate links are pending approval. Signup opens a coming-soon flow.</span>
      </div>
      <div className="affiliate-books">
        {books.map((book) => (
          <a key={book} href="#" rel="sponsored noopener" target="_blank">
            {book}
          </a>
        ))}
      </div>
      <OddsDisclaimer />
    </div>
  );
}
