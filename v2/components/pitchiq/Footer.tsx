const columns = [
  {
    title: "Coverage",
    links: ["Predictions", "Fantasy Picks", "Standings", "News"],
  },
  {
    title: "Tools",
    links: ["Live Odds", "Line Movement", "AI Parlay", "Alerts"],
  },
  {
    title: "Company",
    links: ["About", "Contact", "Privacy", "Responsible Gaming"],
  },
];

export function Footer() {
  return (
    <footer className="border-t border-[var(--b1)] bg-[var(--surf)] py-10">
      <div className="max-shell grid gap-8 md:grid-cols-[1.1fr_1fr]">
        <div>
          <a href="#" className="inline-flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-md bg-gold text-lg font-black text-white">
              IQ
            </span>
            <span className="font-cond text-3xl font-black uppercase leading-none">
              Pitch<span className="text-gold">IQ</span>
            </span>
          </a>
          <p className="mt-4 max-w-lg text-sm leading-6 text-[var(--t2)]">
            Live World Cup 2026 predictions, fantasy intelligence, and AI-labeled market context for getpitchiq.net.
          </p>
          <p className="mt-4 text-xs leading-5 text-[var(--t3)]">
            18+. Gamble responsibly. Odds are informational and subject to change. LEGAL-REVIEW-REQUIRED before affiliate activation.
          </p>
        </div>

        <div className="grid gap-5 sm:grid-cols-3">
          {columns.map((column) => (
            <div key={column.title}>
              <h3 className="text-xs font-black uppercase tracking-[0.14em] text-[var(--t4)]">{column.title}</h3>
              <div className="mt-3 space-y-2">
                {column.links.map((link) => (
                  <a key={link} href="#" className="block text-sm font-semibold text-[var(--t2)] transition hover:text-gold">
                    {link}
                  </a>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </footer>
  );
}
