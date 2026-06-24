# PitchIQ — Coworker Task List
**Prepared:** 2026-06-22  
**Reviewer:** Claude (Pitch)  
**Priority:** P1 = do now, P2 = this week, P3 = before Phase 2

---

## 🔴 P1 — Critical Bugs (Breaking SEO / Analytics)

### 1. Fix robots.txt sitemap URL
**File:** `robots.txt`  
**Problem:** Sitemap points to the wrong domain — Google can't find your sitemap.  
**Current:** `Sitemap: https://pitchiq.com/sitemap.xml`  
**Fix:** Change to `Sitemap: https://getpitchiq.net/sitemap.xml`  
One line change. Do this first — every day this is wrong costs crawl budget.

---

### 2. Fix GA4 tracking ID on all match pages
**Files:** 77 out of ~78 HTML match pages  
**Problem:** Match pages have the placeholder `GA_MEASUREMENT_ID` instead of the real `G-N9PX9ZKHLR`. Only `index.html` has the correct ID. You're flying blind on traffic to every match page.  
**Fix:** Run a find-and-replace across all `.html` files:
```bash
find . -name "*.html" -exec sed -i '' 's/GA_MEASUREMENT_ID/G-N9PX9ZKHLR/g' {} +
```
Then push to Vercel. Verify in GA4 Real-Time after deploy.

---

### 3. Update picks-record.html with real results
**File:** `picks-record.html`  
**Problem:** The public W/L tracker shows 0 wins and 0 losses. Group stage is underway — this needs current results or it looks broken.  
**Fix:** Manually update each pick row with `win`/`loss` badge and update the header stat counters. Refer to `STATUS.md` for the update process.

---

## 🟡 P2 — SEO Improvements (This Week)

### 4. Add lastmod dates to sitemap.xml
**File:** `sitemap.xml`  
**Problem:** No `<lastmod>` tags on any URL. Google uses these to prioritize recrawling.  
**Fix:** Add `<lastmod>2026-06-22</lastmod>` to each `<url>` block. Completed match pages can use their match date; hub pages (`predictions`, `standings`) use today's date. Update the sitemap after each match day.

### 5. Change sitemap changefreq for finished matches
**File:** `sitemap.xml`  
**Problem:** All 72 match pages have `<changefreq>daily</changefreq>`, even for matches that are over. This wastes crawl budget.  
**Fix:** Change finished match pages to `<changefreq>never</changefreq>` and `<priority>0.5</priority>`. Only upcoming/live matches stay at `daily`.

### 6. Add BreadcrumbList structured data to match pages
**Files:** All `{home}-{away}.html` pages  
**Problem:** Match pages have `SportsEvent` schema but no breadcrumb trail. Breadcrumbs appear in Google SERPs and improve CTR.  
**Fix:** Add this JSON-LD block to each match page (update names/URLs per match):
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Home","item":"https://getpitchiq.net"},
    {"@type":"ListItem","position":2,"name":"Predictions","item":"https://getpitchiq.net/predictions"},
    {"@type":"ListItem","position":3,"name":"Brazil vs Morocco"}
  ]
}
```
Add to `match_data.py` so `generate_pages.py` outputs it automatically on future pages.

### 7. Add FAQ schema to match pages
**Files:** All `{home}-{away}.html` pages  
**Problem:** FAQ schema can trigger rich results in Google (expandable Q&A in SERPs). Match preview pages are perfect for this.  
**Fix:** Add 3–4 FAQs per match page (Who will win? What are the odds? Best fantasy pick?). Wire it into `generate_pages.py` so it auto-generates from `match_data.py` fields.

### 8. Add `<meta name="author">` and article publish date to match pages
**Problem:** Match pages lack author and date metadata, which signals freshness to Google.  
**Fix:** Add to each match page `<head>`:
```html
<meta name="author" content="PitchIQ"/>
<meta property="article:published_time" content="2026-06-13T00:00:00Z"/>
<meta property="article:modified_time" content="2026-06-13T00:00:00Z"/>
```

---

## 🟢 P3 — Before Phase 2 / Nice to Have

### 9. Configure AdSense publisher ID
**Files:** All HTML pages  
**Problem:** Every page loads AdSense with `ca-pub-XXXXXXXXXXXXXXXX` (placeholder). Ads won't serve until replaced.  
**Fix:** Once your AdSense account is approved, run the same `sed` command pattern as the GA4 fix to replace the placeholder with your real publisher ID across all pages.

### 10. Add apple-touch-icon file
**Problem:** `index.html` references `/apple-touch-icon.png` but the file doesn't exist in the repo. iOS users get a broken icon when bookmarking.  
**Fix:** Generate a 180×180px PNG of the PitchIQ "P" logo and add it to the project root as `apple-touch-icon.png`.

### 11. Add `og:image:width` and `og:image:height` to all pages
**Problem:** OG image tags exist but lack dimensions. Some platforms (Slack, Discord) won't render the preview card without them.  
**Fix:** Add alongside existing OG image tags:
```html
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
```

### 12. Wire match page internal links to predictions hub
**Problem:** Match pages don't link back to `/predictions`. Internal linking helps Google understand site structure and distributes PageRank.  
**Fix:** Add a "More predictions →" link in each match page footer pointing to `https://getpitchiq.net/predictions`.

---

## Summary

| # | Task | Priority | Effort |
|---|------|----------|--------|
| 1 | Fix robots.txt sitemap URL | P1 | 2 min |
| 2 | Fix GA4 ID on 77 match pages | P1 | 10 min |
| 3 | Update picks-record W/L results | P1 | 30 min |
| 4 | Add lastmod to sitemap | P2 | 30 min |
| 5 | Update changefreq for finished matches | P2 | 20 min |
| 6 | Add BreadcrumbList schema | P2 | 1 hr |
| 7 | Add FAQ schema to match pages | P2 | 2 hr |
| 8 | Add author + publish date meta | P2 | 30 min |
| 9 | Configure AdSense publisher ID | P3 | 10 min |
| 10 | Add apple-touch-icon.png | P3 | 15 min |
| 11 | Add og:image dimensions | P3 | 20 min |
| 12 | Add internal links to predictions hub | P3 | 1 hr |
