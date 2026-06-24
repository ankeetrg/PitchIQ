import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { JsonLd } from "@/components/content/JsonLd";
import { MatchHub } from "@/components/content/MatchContent";
import { MATCHES, getMatchBySlug } from "@/data/matches";
import { sportsEventJsonLd } from "@/lib/jsonld";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

interface MatchPageProps {
  params: { matchSlug: string };
}

export function generateStaticParams() {
  return MATCHES.map((match) => ({ matchSlug: match.slug }));
}

export function generateMetadata({ params }: MatchPageProps): Metadata {
  const match = getMatchBySlug(params.matchSlug);
  if (!match) {
    return buildMetadata({
      title: "World Cup 2026 Match Not Found",
      description: "World Cup 2026 match hub not found.",
      path: "/world-cup-2026/matches",
    });
  }

  return buildMetadata({
    title: `${match.home} vs ${match.away} Prediction, Odds, Fantasy Picks`,
    description: `${match.home} vs ${match.away} World Cup 2026 match hub with AI pick, odds context, fantasy targets, kickoff time, and venue.`,
    path: `/world-cup-2026/matches/${match.slug}`,
    type: "article",
  });
}

export default function MatchPage({ params }: MatchPageProps) {
  const match = getMatchBySlug(params.matchSlug);
  if (!match) notFound();

  const path = `/world-cup-2026/matches/${match.slug}`;

  return (
    <>
      <JsonLd data={sportsEventJsonLd(match, path)} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: "Matches", path: "/world-cup-2026/schedule" },
          { name: `${match.home} vs ${match.away}`, path },
        ])}
      />
      <MatchHub match={match} />
    </>
  );
}
