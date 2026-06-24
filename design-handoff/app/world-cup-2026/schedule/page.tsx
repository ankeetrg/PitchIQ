import type { Metadata } from "next";
import { JsonLd } from "@/components/content/JsonLd";
import { StickyLiveScoresLink } from "@/components/content/ConversionCtas";
import { MATCHES } from "@/data/matches";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

export const metadata: Metadata = buildMetadata({
  title: "World Cup 2026 Schedule: Group Stage Fixtures and Match Hubs",
  description:
    "World Cup 2026 schedule with every group-stage fixture, kickoff time, venue, and PitchIQ match hub.",
  path: "/world-cup-2026/schedule",
});

export default function SchedulePage() {
  const grouped = MATCHES.reduce<Record<string, typeof MATCHES>>((groups, match) => {
    groups[match.group] = groups[match.group] ?? [];
    groups[match.group].push(match);
    return groups;
  }, {});

  return (
    <main className="content-page">
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: "Schedule", path: "/world-cup-2026/schedule" },
        ])}
      />
      <div className="content-wrap">
        <StickyLiveScoresLink />
        <section className="wc-hero compact">
          <h1>World Cup 2026 Schedule</h1>
          <p>All 72 group-stage match hubs, organized by group.</p>
        </section>
        {Object.entries(grouped).map(([group, matches]) => (
          <section className="content-card" key={group}>
            <div className="section-heading">
              <h2>Group {group}</h2>
            </div>
            <div className="schedule-list">
              {matches.map((match) => (
                <a href={`/world-cup-2026/matches/${match.slug}`} className="schedule-list-row" key={match.slug}>
                  <span>{match.dateShort} · {match.timeStr}</span>
                  <strong>{match.home} vs {match.away}</strong>
                  <em>{match.venueShort}</em>
                </a>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
