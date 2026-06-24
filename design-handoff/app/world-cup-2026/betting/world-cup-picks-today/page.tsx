import type { Metadata } from "next";
import { ArticleRoute } from "@/components/content/ArticleRoute";
import { getArticleByPath } from "@/lib/articles";
import { buildMetadata } from "@/lib/seo";

const ARTICLE_PATH = "/world-cup-2026/betting/world-cup-picks-today";

export function generateMetadata(): Metadata {
  const article = getArticleByPath(ARTICLE_PATH);
  return buildMetadata({
    title: article?.title ?? "World Cup Picks Today",
    description: article?.description ?? "World Cup 2026 picks today with AI-labeled value angles.",
    path: ARTICLE_PATH,
    image: article?.ogImage,
    type: "article",
  });
}

export default function PicksTodayPage() {
  return <ArticleRoute path={ARTICLE_PATH} crumb="Betting" crumbPath="/world-cup-2026/betting/world-cup-picks-today" showOddsSlot />;
}
