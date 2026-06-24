import { notFound } from "next/navigation";
import { getArticleByPath } from "@/lib/articles";
import { articleJsonLd } from "@/lib/jsonld";
import { breadcrumbJsonLd } from "@/lib/seo";
import { ArticleView } from "./ArticleView";
import { JsonLd } from "./JsonLd";

interface ArticleRouteProps {
  path: string;
  crumb: string;
  crumbPath?: string;
  showOddsSlot?: boolean;
}

export function ArticleRoute({ path, crumb, crumbPath, showOddsSlot = false }: ArticleRouteProps) {
  const article = getArticleByPath(path);
  if (!article) notFound();

  return (
    <>
      <JsonLd data={articleJsonLd(article)} />
      <JsonLd
        data={breadcrumbJsonLd([
          { name: "Home", path: "/" },
          { name: "World Cup 2026", path: "/world-cup-2026" },
          { name: crumb, path: crumbPath ?? "/world-cup-2026" },
          { name: article.title, path },
        ])}
      />
      <ArticleView article={article} showOddsSlot={showOddsSlot} />
    </>
  );
}
