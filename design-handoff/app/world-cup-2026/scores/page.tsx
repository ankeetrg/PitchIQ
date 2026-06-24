import type { Metadata } from "next";
import { JsonLd } from "@/components/content/JsonLd";
import { MATCHES, getTodaysMatches } from "@/data/matches";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

export const metadata: Metadata = buildMetadata({
  title: "World Cup 2026 Live Scores: Match Hubs, Odds, and AI Picks",
  description:
    "World Cup 2026 live scores hub with match links, group context, odds movement, and AI-labeled picks.",
  path: "/world-cup-2026/scores",
});

export default function ScoresPage() {
  const today = getTodaysMatches();
  const visible = today.length ? today : MATCHES.slice(0, 8);

  return (
    <main className="content-page">
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: "Live Scores", path: "/world-cup-2026/scores" },
        ])}
      />
      <div className="content-wrap">
        <section className="wc-hero compact">
          <h1>World Cup 2026 Live Scores</h1>
          <p>Follow every match hub from kickoff through full time. Odds are informational only.</p>
        </section>
        <section className="content-card">
          <div className="section-heading">
            <h2>{today.length ? "Today's Matches" : "Next Match Hubs"}</h2>
          </div>
          <div className="live-score-list">
            {visible.map((match) => (
              <a className="live-score-row" href={`/world-cup-2026/matches/${match.slug}`} key={match.slug}>
                <span>Group {match.group}</span>
                <strong>{match.home} vs {match.away}</strong>
                <em>{match.dateShort} · {match.timeStr}</em>
                <b>Open hub</b>
              </a>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
