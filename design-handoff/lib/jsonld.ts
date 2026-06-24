import type { Article } from "./articles";
import type { Match } from "@/data/matches";
import { absoluteUrl } from "./seo";

export function articleJsonLd(article: Article) {
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: article.title,
    description: article.description,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt,
    author: {
      "@type": "Organization",
      name: article.author,
      url: absoluteUrl("/"),
    },
    publisher: {
      "@type": "Organization",
      name: "PitchIQ",
      url: absoluteUrl("/"),
      logo: {
        "@type": "ImageObject",
        url: absoluteUrl("/pitchiq-banner.png"),
      },
    },
    image: absoluteUrl(article.ogImage),
    mainEntityOfPage: absoluteUrl(article.slug),
  };
}

export function sportsEventJsonLd(match: Match, path: string) {
  return {
    "@context": "https://schema.org",
    "@type": "SportsEvent",
    name: `${match.home} vs ${match.away} - World Cup 2026`,
    startDate: match.jsonDt,
    eventStatus: "https://schema.org/EventScheduled",
    sport: "Soccer",
    url: absoluteUrl(path),
    location: {
      "@type": "Place",
      name: match.venueName,
      address: match.venueAddr,
    },
    homeTeam: {
      "@type": "SportsTeam",
      name: match.home,
    },
    awayTeam: {
      "@type": "SportsTeam",
      name: match.away,
    },
  };
}
