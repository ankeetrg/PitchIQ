import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { JsonLd } from "@/components/content/JsonLd";
import {
  MatchAnalysisSection,
  MatchFantasySection,
  MatchHero,
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

interface PreviewPageProps {
  params: { matchSlug: string };
}

export const dynamicParams = false;

export function generateStaticParams() {
  return INTENT_MATCH_SLUGS.map((matchSlug) => ({ matchSlug }));
}

export function generateMetadata({ params }: PreviewPageProps): Metadata {
  const match = getMatchBySlug(params.matchSlug);
  if (!match) {
    return buildMetadata({
      title: "World Cup 2026 Preview Not Found",
      description: "World Cup 2026 match preview not found.",
      path: "/world-cup-2026",
    });
  }

  return buildMetadata({
    title: `${match.home} vs ${match.away} Preview: World Cup 2026`,
    description: `${match.home} vs ${match.away} preview with AI-labeled match read, key stats, fantasy targets, and kickoff context.`,
    path: `/world-cup-2026/matches/${match.slug}/preview`,
    type: "article",
  });
}

export default function MatchPreviewPage({ params }: PreviewPageProps) {
  const match = getMatchBySlug(params.matchSlug);
  if (!match) notFound();

  const path = `/world-cup-2026/matches/${match.slug}/preview`;

  return (
    <main className="content-page">
      <JsonLd data={sportsEventJsonLd(match, path)} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: `${match.home} vs ${match.away}`, path: `/world-cup-2026/matches/${match.slug}` },
          { name: "Preview", path },
        ])}
      />
      <div className="content-wrap">
        <StickyLiveScoresLink />
        <MatchHero match={match} />
        <MatchAnalysisSection match={match} />
        <MidArticleSignup />
        <MatchFantasySection match={match} />
        <BottomArticleSignup />
      </div>
    </main>
  );
}
