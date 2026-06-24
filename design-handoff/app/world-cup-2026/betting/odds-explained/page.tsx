import type { Metadata } from "next";
import { ArticleRoute } from "@/components/content/ArticleRoute";
import { getArticleByPath } from "@/lib/articles";
import { buildMetadata } from "@/lib/seo";

const ARTICLE_PATH = "/world-cup-2026/betting/odds-explained";

export function generateMetadata(): Metadata {
  const article = getArticleByPath(ARTICLE_PATH);
  return buildMetadata({
    title: article?.title ?? "World Cup 2026 Odds Explained",
    description: article?.description ?? "World Cup 2026 betting odds explained.",
    path: ARTICLE_PATH,
    image: article?.ogImage,
    type: "article",
  });
}

export default function OddsExplainedPage() {
  return <ArticleRoute path={ARTICLE_PATH} crumb="Betting" crumbPath="/world-cup-2026/betting/odds-explained" showOddsSlot />;
}
