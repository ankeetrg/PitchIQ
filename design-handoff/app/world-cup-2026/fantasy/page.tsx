import type { Metadata } from "next";
import { JsonLd } from "@/components/content/JsonLd";
import {
  BottomArticleSignup,
  FantasyToolCta,
  StickyLiveScoresLink,
} from "@/components/content/ConversionCtas";
import { MATCHES } from "@/data/matches";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

export const metadata: Metadata = buildMetadata({
  title: "World Cup 2026 Fantasy Hub: Picks, Projections, Ownership",
  description:
    "World Cup 2026 fantasy hub with AI-labeled player picks, projections, ownership estimates, and match links.",
  path: "/world-cup-2026/fantasy",
});

export default function FantasyHubPage() {
  const fantasyMatches = MATCHES.slice(0, 4);

  return (
    <main className="content-page">
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: "Fantasy", path: "/world-cup-2026/fantasy" },
        ])}
      />
      <div className="content-wrap">
        <StickyLiveScoresLink />
        <section className="wc-hero compact">
          <h1>World Cup 2026 Fantasy Hub</h1>
          <p>AI-labeled projections, ownership estimates, and match context for every slate.</p>
        </section>
        <section className="content-card">
          <div className="section-heading">
            <h2>Best Starting Points</h2>
          </div>
          <div className="route-card-grid">
            <a className="route-card" href="/world-cup-2026/fantasy/best-players">
              <span>Fantasy Guide</span>
              <strong>Best World Cup 2026 Fantasy Players</strong>
              <em>Premiums, values, and low-owned shots.</em>
            </a>
            {fantasyMatches.map((match) => (
              <a className="route-card" href={`/world-cup-2026/matches/${match.slug}`} key={match.slug}>
                <span>Match Picks</span>
                <strong>{match.home} vs {match.away}</strong>
                <em>{match.fantasy[0]?.playerName} leads the slate read.</em>
              </a>
            ))}
          </div>
        </section>
        <FantasyToolCta />
        <BottomArticleSignup />
      </div>
    </main>
  );
}
