import type { Article } from "@/lib/articles";
import { articleToBlocks } from "@/lib/articles";
import { AffiliateOddsSlot } from "./OddsCompliance";
import {
  BottomArticleSignup,
  FantasyToolCta,
  MidArticleSignup,
  StickyLiveScoresLink,
} from "./ConversionCtas";

interface ArticleViewProps {
  article: Article;
  showOddsSlot?: boolean;
}

export function ArticleView({ article, showOddsSlot = false }: ArticleViewProps) {
  const blocks = articleToBlocks(article.body);
  const midpoint = Math.max(2, Math.floor(blocks.length / 2));

  return (
    <main className="content-page">
      <div className="content-wrap">
        <StickyLiveScoresLink />
        <article className="article-shell">
          <div className="article-kicker">{article.category}</div>
          <h1>{article.title}</h1>
          <p className="article-dek">{article.description}</p>
          <div className="article-meta">
            <span>By {article.author}</span>
            <span>{new Date(article.publishedAt).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric",
            })}</span>
            <span>{article.readingTime}</span>
          </div>

          <div className="article-body">
            {blocks.map((block, index) => (
              <div key={`${block.type}-${index}`}>
                {index === midpoint ? <MidArticleSignup /> : null}
                {block.type === "h2" ? <h2>{block.content}</h2> : null}
                {block.type === "p" ? <p>{block.content}</p> : null}
                {block.type === "ul" ? (
                  <ul>
                    {(block.content as string[]).map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                ) : null}
              </div>
            ))}
          </div>

          {showOddsSlot ? <AffiliateOddsSlot /> : null}
          <FantasyToolCta />
          <BottomArticleSignup />
        </article>
      </div>
    </main>
  );
}
