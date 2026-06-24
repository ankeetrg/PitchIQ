import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { JsonLd } from "@/components/content/JsonLd";
import {
  MatchFantasySection,
  MatchHero,
  MatchOddsSection,
  MatchPicksSection,
} from "@/components/content/MatchContent";
import {
  BottomArticleSignup,
  MidArticleSignup,
  StickyLiveScoresLink,
} from "@/components/content/ConversionCtas";
import { INTENT_MATCH_SLUGS } from "@/data/firstBatch";
import { getMatchBySlug } from "@/data/matches";
import { sportsEventJsonLd } from "@/lib/jsonld";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

interface OddsPicksPageProps {
  params: { matchSlug: string };
}

export const dynamicParams = false;

export function generateStaticParams() {
  return INTENT_MATCH_SLUGS.map((matchSlug) => ({ matchSlug }));
}

export function generateMetadata({ params }: OddsPicksPageProps): Metadata {
  const match = getMatchBySlug(params.matchSlug);
  if (!match) {
    return buildMetadata({
      title: "World Cup 2026 Odds Picks Not Found",
      description: "World Cup 2026 odds picks page not found.",
      path: "/world-cup-2026",
    });
  }

  return buildMetadata({
    title: `${match.home} vs ${match.away} Odds and AI Picks`,
    description: `${match.home} vs ${match.away} odds, implied probability, AI-labeled picks, fantasy targets, and market read.`,
    path: `/world-cup-2026/matches/${match.slug}/odds-picks`,
    type: "article",
  });
}

export default function MatchOddsPicksPage({ params }: OddsPicksPageProps) {
  const match = getMatchBySlug(params.matchSlug);
  if (!match) notFound();

  const path = `/world-cup-2026/matches/${match.slug}/odds-picks`;

  return (
    <main className="content-page">
      <JsonLd data={sportsEventJsonLd(match, path)} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: `${match.home} vs ${match.away}`, path: `/world-cup-2026/matches/${match.slug}` },
          { name: "Odds and Picks", path },
        ])}
      />
      <div className="content-wrap">
        <StickyLiveScoresLink />
        <MatchHero match={match} />
        <MatchOddsSection match={match} />
        <MidArticleSignup />
        <MatchPicksSection match={match} />
        <MatchFantasySection match={match} />
        <BottomArticleSignup />
      </div>
    </main>
  );
}
