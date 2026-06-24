import type { Metadata } from "next";
import { ArticleRoute } from "@/components/content/ArticleRoute";
import { getArticleByPath } from "@/lib/articles";
import { buildMetadata } from "@/lib/seo";

const ARTICLE_PATH = "/world-cup-2026/fantasy/best-players";

export function generateMetadata(): Metadata {
  const article = getArticleByPath(ARTICLE_PATH);
  return buildMetadata({
    title: article?.title ?? "Best World Cup 2026 Fantasy Players",
    description: article?.description ?? "World Cup 2026 fantasy player picks and projections.",
    path: ARTICLE_PATH,
    image: article?.ogImage,
    type: "article",
  });
}

export default function BestPlayersPage() {
  return <ArticleRoute path={ARTICLE_PATH} crumb="Fantasy" crumbPath="/world-cup-2026/fantasy" />;
}
