import type { Metadata } from "next";
import { JsonLd } from "@/components/content/JsonLd";
import { StickyLiveScoresLink } from "@/components/content/ConversionCtas";
import { MATCHES } from "@/data/matches";
import { TEAM_GUIDES } from "@/data/teams";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

export const metadata: Metadata = buildMetadata({
  title: "World Cup 2026 Hub: Live Scores, Schedule, Picks, Fantasy",
  description:
    "World Cup 2026 live scores, match hubs, schedule, AI picks, fantasy targets, and team guides from PitchIQ.",
  path: "/world-cup-2026",
});

export default function WorldCupHubPage() {
  const featured = MATCHES.slice(0, 6);

  return (
    <main className="content-page">
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
        ])}
      />
      <div className="content-wrap">
        <StickyLiveScoresLink />
        <section className="wc-hero">
          <h1>World Cup 2026 Live Scores, Picks, Fantasy, and Team Guides</h1>
          <p>
            One match hub for every group-stage game. Live scores, AI-labeled picks, odds context,
            and fantasy reads stay tied to the schedule.
          </p>
          <div className="hero-actions">
            <a href="/world-cup-2026/scores">Live Scores</a>
            <a href="/world-cup-2026/schedule">Full Schedule</a>
          </div>
        </section>

        <section className="content-card">
          <div className="section-heading">
            <h2>Featured Match Hubs</h2>
            <a href="/world-cup-2026/schedule">See all 72</a>
          </div>
          <div className="route-card-grid">
            {featured.map((match) => (
              <a href={`/world-cup-2026/matches/${match.slug}`} className="route-card" key={match.slug}>
                <span>Group {match.group} · {match.dateShort}</span>
                <strong>{match.home} vs {match.away}</strong>
                <em>{match.timeStr} · {match.venueShort}</em>
              </a>
            ))}
          </div>
        </section>

        <section className="content-card">
          <div className="section-heading">
            <h2>First Team Guides</h2>
          </div>
          <div className="route-card-grid three">
            {TEAM_GUIDES.map((team) => (
              <a href={`/world-cup-2026/teams/${team.slug}`} className="route-card" key={team.slug}>
                <span>Team Guide</span>
                <strong>{team.name}</strong>
                <em>{team.description}</em>
              </a>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
