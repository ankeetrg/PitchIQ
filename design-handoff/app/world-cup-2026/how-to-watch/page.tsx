import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ArticleView } from "@/components/content/ArticleView";
import { JsonLd } from "@/components/content/JsonLd";
import { getArticleByPath } from "@/lib/articles";
import { articleJsonLd } from "@/lib/jsonld";
import { breadcrumbJsonLd, buildMetadata } from "@/lib/seo";

const ARTICLE_PATH = "/world-cup-2026/how-to-watch";

export function generateMetadata(): Metadata {
  const article = getArticleByPath(ARTICLE_PATH);
  if (!article) {
    return buildMetadata({ title: "How to Watch World Cup 2026", description: "", path: ARTICLE_PATH });
  }
  return buildMetadata({
    title: article.title,
    description: article.description,
    path: article.slug,
    image: article.ogImage,
    type: "article",
  });
}

export default function HowToWatchPage() {
  const article = getArticleByPath(ARTICLE_PATH);
  if (!article) notFound();

  return (
    <>
      <JsonLd data={articleJsonLd(article)} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: "How to Watch", path: ARTICLE_PATH },
        ])}
      />
      <ArticleView article={article} />
    </>
  );
}
