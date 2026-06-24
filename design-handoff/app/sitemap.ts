import type { MetadataRoute } from "next";
import { FIRST_BATCH_ROUTES, INTENT_MATCH_SLUGS, STATIC_WORLD_CUP_ROUTES } from "@/data/firstBatch";
import { MATCHES } from "@/data/matches";
import { TEAM_GUIDES } from "@/data/teams";
import { getAllArticles } from "@/lib/articles";
import { absoluteUrl } from "@/lib/seo";

function entry(path: string, lastModified = new Date()): MetadataRoute.Sitemap[number] {
  return {
    url: absoluteUrl(path),
    lastModified,
    changeFrequency: "daily",
    priority: path === "/" ? 1 : 0.8,
  };
}

export default function sitemap(): MetadataRoute.Sitemap {
  const articles = getAllArticles();
  const routes = new Set<string>([
    "/",
    ...STATIC_WORLD_CUP_ROUTES,
    ...FIRST_BATCH_ROUTES,
    ...MATCHES.map((match) => `/world-cup-2026/matches/${match.slug}`),
    ...TEAM_GUIDES.map((team) => `/world-cup-2026/teams/${team.slug}`),
    ...INTENT_MATCH_SLUGS.flatMap((slug) => [
      `/world-cup-2026/matches/${slug}/preview`,
      `/world-cup-2026/matches/${slug}/odds-picks`,
    ]),
    ...articles.map((article) => article.slug),
  ]);

  return [...routes].map((route) => {
    const article = articles.find((item) => item.slug === route);
    return entry(route, article ? new Date(article.updatedAt) : new Date());
  });
}
