import type { Metadata } from "next";
import { ArticleRoute } from "@/components/content/ArticleRoute";
import { getAllArticles, getNewsArticleBySlug } from "@/lib/articles";
import { buildMetadata } from "@/lib/seo";

interface NewsPageProps {
  params: { slug: string };
}

export function generateStaticParams() {
  return getAllArticles()
    .filter((article) => article.category === "News")
    .map((article) => ({ slug: article.slug.split("/").at(-1) ?? "" }));
}

export function generateMetadata({ params }: NewsPageProps): Metadata {
  const article = getNewsArticleBySlug(params.slug);
  return buildMetadata({
    title: article?.title ?? "World Cup 2026 News",
    description: article?.description ?? "World Cup 2026 news and analysis from PitchIQ.",
    path: article?.slug ?? `/world-cup-2026/news/${params.slug}`,
    image: article?.ogImage,
    type: "article",
  });
}

export default function NewsArticlePage({ params }: NewsPageProps) {
  return (
    <ArticleRoute
      path={`/world-cup-2026/news/${params.slug}`}
      crumb="News"
      crumbPath="/world-cup-2026"
    />
  );
}
