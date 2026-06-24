import fs from "fs";
import path from "path";

const ARTICLES_DIR = path.join(process.cwd(), "content", "articles");

export interface ArticleFrontmatter {
  title: string;
  description: string;
  slug: string;
  publishedAt: string;
  updatedAt: string;
  author: string;
  ogImage: string;
  category: string;
}

export interface Article extends ArticleFrontmatter {
  body: string;
  readingTime: string;
}

function parseFrontmatter(raw: string): Article {
  const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) {
    throw new Error("Article is missing frontmatter");
  }

  const fields = Object.fromEntries(
    match[1]
      .split("\n")
      .filter(Boolean)
      .map((line) => {
        const index = line.indexOf(":");
        const key = line.slice(0, index).trim();
        const value = line.slice(index + 1).trim().replace(/^"|"$/g, "");
        return [key, value];
      })
  ) as unknown as ArticleFrontmatter;

  const wordCount = match[2].split(/\s+/).filter(Boolean).length;
  return {
    ...fields,
    body: match[2].trim(),
    readingTime: `${Math.max(2, Math.ceil(wordCount / 220))} min read`,
  };
}

export function getAllArticles(): Article[] {
  if (!fs.existsSync(ARTICLES_DIR)) return [];
  return fs
    .readdirSync(ARTICLES_DIR)
    .filter((file) => file.endsWith(".mdx"))
    .map((file) => parseFrontmatter(fs.readFileSync(path.join(ARTICLES_DIR, file), "utf-8")))
    .sort((a, b) => b.publishedAt.localeCompare(a.publishedAt));
}

export function getArticleByPath(articlePath: string): Article | undefined {
  const normalized = articlePath.startsWith("/") ? articlePath : `/${articlePath}`;
  return getAllArticles().find((article) => article.slug === normalized);
}

export function getNewsArticleBySlug(slug: string): Article | undefined {
  return getAllArticles().find((article) => {
    return article.category === "News" && article.slug.endsWith(`/${slug}`);
  });
}

export function articleToBlocks(body: string) {
  const blocks: Array<{ type: "h2" | "p" | "ul"; content: string | string[] }> = [];
  const lines = body.split("\n");
  let paragraph: string[] = [];
  let list: string[] = [];

  function flushParagraph() {
    if (!paragraph.length) return;
    blocks.push({ type: "p", content: paragraph.join(" ") });
    paragraph = [];
  }

  function flushList() {
    if (!list.length) return;
    blocks.push({ type: "ul", content: list });
    list = [];
  }

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) {
      flushParagraph();
      flushList();
      continue;
    }
    if (trimmed.startsWith("## ")) {
      flushParagraph();
      flushList();
      blocks.push({ type: "h2", content: trimmed.replace(/^##\s+/, "") });
      continue;
    }
    if (trimmed.startsWith("- ")) {
      flushParagraph();
      list.push(trimmed.replace(/^-\s+/, ""));
      continue;
    }
    flushList();
    paragraph.push(trimmed);
  }

  flushParagraph();
  flushList();
  return blocks;
}
