import { sportsbooks } from "./data";

export function SportsbookPromo() {
  return (
    <div className="promo-bar">
      <div className="promo-inner">
        <span className="promo-label">Sportsbook Offers</span>
        <div className="promo-books">
          {sportsbooks.map((b) => (
            <a key={b.name} className="promo-book" href="#">
              <span className="pb-name">{b.name}</span>
              <span className="pb-offer">{b.offer}</span>
              <span className="pb-arrow">↗</span>
            </a>
          ))}
        </div>
        <span className="promo-legal">21+ · T&amp;Cs apply</span>
      </div>
    </div>
  );
}
