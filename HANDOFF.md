# PitchIQ — Team Handoff & Progress Log

**Project:** getpitchiq.net  
**Stack:** Static HTML/CSS/JS on Vercel + Python generators  
**Rule:** Never commit `.env.local`. Never push with git commands — Samson pushes manually.

---

## How to Use This File

Both of you add updates at the top of the **Progress Log** section with your name and date.  
Use the **Outstanding Tasks** section as a shared checklist — check things off as they're done.

---

## Outstanding Tasks

### 🔴 Urgent

- [ ] **Fix GA4 ID on 77 match pages** — 77 pages still have placeholder `GA_MEASUREMENT_ID` instead of `G-N9PX9ZKHLR`. Run this from the project root:
  ```bash
  find . -name "*.html" -exec sed -i '' 's/GA_MEASUREMENT_ID/G-N9PX9ZKHLR/g' {} +
  ```
  Then push to Vercel and verify in GA4 Real-Time.

### 🟡 This Week

- [ ] **Run updaters after each match day** — See Automation section below. Samson has scheduled tasks set up in Cowork but someone should confirm they're running correctly after the next match day.
- [ ] **Add BreadcrumbList schema to match pages** — Add to `generate_pages.py` so it outputs automatically. See `COWORKER_TASKS.md` task #6 for the JSON-LD snippet.
- [ ] **Add FAQ schema to match pages** — 3–4 FAQs per page (who wins, what are the odds, best fantasy pick). Wire into `generate_pages.py`. See `COWORKER_TASKS.md` task #7.
- [ ] **Populate result_data.py as matches finish** — Add completed match results to `result_data.py`, then run `python3 generate_result_pages.py` to publish the result page. See format below.

### 🟢 Before Phase 2

- [ ] Add `og:image:width/height` (1200×630) to all pages
- [ ] Add `apple-touch-icon.png` (180×180px) to project root
- [ ] Configure AdSense publisher ID once approved (replace `ca-pub-XXXXXXXXXXXXXXXX`)
- [ ] Add internal "More predictions →" links in match page footers

---

## Automation (New — June 2026)

Four Python scripts now handle all site data updates. Run from the project root.

### Quick reference

| Script | What it does | Source | Cost |
|---|---|---|---|
| `update_standings.py` | Group standings + 12 group pages | ESPN API | Free |
| `update_picks_record.py` | Grades AI picks, updates W/L/ROI | ESPN API | Free |
| `update_odds.py` | Refreshes odds on upcoming match pages | The Odds API | 1 req/run |
| `update_fantasy.py` | Updates player pts + ownership% | ESPN API | Free |
| `update_all.py` | Runs all 4 in sequence | — | — |

### After each match day

```bash
python3 update_all.py              # run everything
python3 update_all.py --skip-odds  # skip odds (save API quota)
python3 update_all.py --dry        # preview only, don't write files
```

### Scheduled (Samson's machine, via Cowork)

- **9:00 AM** — `update_odds.py` (fresh pre-match lines)
- **3:00 PM** — `update_all.py --skip-odds` (after noon kickoffs)
- **11:00 PM** — `update_all.py --skip-odds` (after evening kickoffs)

These run automatically when Cowork is open. If the machine is asleep, they run on next launch.

### Environment variables

The Odds API key lives in `.env.local` (gitignored). Do not commit it.

```
ODDS_API_KEY=...   # get free key at the-odds-api.com (500 req/mo free)
```

---

## Generator Scripts

| Script | What it generates | Data source | Command |
|---|---|---|---|
| `generate_pages.py` | All 72 match preview pages | `match_data.py` | `python3 generate_pages.py` |
| `generate_result_pages.py` | Post-match result pages | `result_data.py` + `match_data.py` | `python3 generate_result_pages.py` |
| `generate_group_pages.py` | 12 group standings pages | `group_data.py` | `python3 generate_group_pages.py` |

**To publish a result after a match:**
1. Add an entry to `result_data.py` (copy the format from existing entries)
2. Run `python3 generate_result_pages.py slug-name`
3. Add the result URL to `sitemap.xml` with `<changefreq>never</changefreq>`
4. Push to Vercel

---

## Progress Log

---

### Claude (Pitch) — 2026-06-23 (v2 SEO layer + workspace recovery)

**Workspace move recovery.** The `Claude` folder was moved from `~/Downloads/Claude` to
`~/Claude` mid-session, while Codex was building the v2 SEO layer. This stranded 30 of
Codex's new files in the old (now-dead) `~/Downloads/Claude/Projects/PitchIQ` shell.
Recovered all 30 into the live workspace; verified nothing else was unique there (only a
`.DS_Store`); deleted the stale shell. **No data lost.** Lesson: don't move the workspace
root while an agent session is running against it.

**v2 SEO content layer (in `design-handoff/`, the Next.js 14 app) — built + verified:**

- **Data layer:** `match_data.py` migrated to typed TS at `design-handoff/data/matches.ts`
  (all 72 matches) via `design-handoff/scripts/generate_matches_ts.py`. Plus `data/teams.ts`
  and `data/firstBatch.ts`. ⚠️ Two sources of truth now exist (`match_data.py` for the static
  site, `matches.ts` for v2) — keep them in sync via the generator, or retire one before launch.
- **Routes:** `/world-cup-2026` hub + `scores`, `schedule`, `fantasy`, match hubs for all 72,
  and `preview`/`odds-picks` only for `brazil-morocco` (intentional — avoids thin AI pages).
  Team guides (USA/Brazil/France), betting explainers, MDX articles under `content/articles/`.
- **SEO:** `app/sitemap.ts` + `app/robots.ts` (auto-generated), `generateMetadata()` on all
  routes via `lib/seo.ts`, Article/Breadcrumb/SportsEvent JSON-LD, canonical base
  `https://getpitchiq.net`. Root `app/layout.tsx` now has `metadataBase`, title template,
  OG/Twitter defaults, publisher, robots.
- **Newsletter:** wired `Newsletter.tsx` to a real `app/api/newsletter/route.ts` — Zod
  validation, in-memory rate-limit (`// TODO` shared store before real traffic), env-gated
  provider (accepts-but-doesn't-store when unconfigured), idempotent, honeypot, no PII logging.
- **Compliance verified:** affiliate links stay `href="#"` with `rel="sponsored"`; odds
  disclaimer + `// LEGAL-REVIEW-REQUIRED` on odds components; "AI Pick" badges throughout.
- **Analytics:** Vercel Analytics + env-gated GA4 (`NEXT_PUBLIC_GA_ID`) in layout.
- **Tooling:** added `.env.example`; set up ESLint (`.eslintrc.json` → `next/core-web-vitals`).
- **Verification:** `npx tsc --noEmit` → clean. `npm run build` → 93 pages. `npm run lint`
  → 0 errors (1 non-blocking `<img>` warning in the team-guide page; needs `next/image` +
  `flagcdn.com` domain allowlist as a follow-up).

**Open items for v2:** choose/wire a newsletter provider (`NEWSLETTER_API_URL/KEY`); set
`NEXT_PUBLIC_GA_ID`; add Google Search Console verification (meta tag/DNS — not code);
reconcile the v2 `sitemap.ts` vs the static `sitemap.xml` at cutover.

---

### Samson — 2026-06-23

**Session with Claude (Pitch):**

Built full automation layer for the site:

- Created `update_standings.py` — fetches live WC standings from ESPN hidden API, patches `group_data.py`, regenerates all 12 group pages
- Created `update_picks_record.py` — grades all pending AI picks (moneyline, AH, totals, BTTS, anytime scorer) against ESPN results, updates badges + W/L/ROI counters
- Created `update_odds.py` — pulls fresh odds from The Odds API, updates all upcoming match pages (5 values: home/draw/away ML + O/U). Needs `ODDS_API_KEY` in `.env.local`
- Created `update_fantasy.py` — aggregates goals/assists from ESPN match summaries, recalculates player DFS pts and ownership%
- Created `update_all.py` — master runner, runs all 4 scripts in sequence
- Set up 3 Cowork scheduled tasks to run automatically daily (9 AM odds / 3 PM results / 11 PM results)
- Created `.env.local` with Odds API key (gitignored)
- Created `.gitignore`

**Also done in prior sessions:**
- Fixed `robots.txt` sitemap URL (was pointing to wrong domain `pitchiq.com`)
- Expanded `sitemap.xml` from 80 → 91 URLs (added group pages + result pages)
- Built `article-template.html` for data-rich content pages
- Built `generate_result_pages.py` + `result_data.py` for post-match result pages
- Built `generate_group_pages.py` + `group_data.py` for group standings pages
- Generated `group-a.html` through `group-l.html`

**Still needed:**
- GA4 fix on 77 match pages (see Outstanding Tasks)
- Manual push to Vercel after each update run

---
