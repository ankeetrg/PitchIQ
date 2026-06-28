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

### 🔴 Urgent — PICK UP HERE NEXT SESSION

- [x] **Finish R32 knockout page generation** ✅ DONE (commit fd90a14, 2026-06-29) — 16 pages generated and live. R16/QF/SF/Final pages auto-generate via GitHub Actions once teams are confirmed.

  ~~One blocker remains: `data/live.json` has an unresolved git merge conflict. Steps to finish:~~

  **1. Fix the conflict:**
  ```powershell
  cd C:\Users\mroads\Documents\GitHub\PitchIQ
  git checkout --theirs data/live.json
  git add data/live.json
  # if in a rebase: git rebase --continue
  ```

  **2. Test the generator:**
  ```powershell
  python generate_knockout_pages.py --dry
  ```
  Should print 16 slugs. If 0 pages, team names in live.json don't match `_TEAM_DATA`. Debug:
  ```powershell
  python -c "import json; d=json.load(open('data/live.json')); [print(v.get('home',{}).get('name'), '|', v.get('away',{}).get('name')) for k,v in d.get('knockout',{}).items() if v.get('home',{}).get('code')]"
  ```
  Known possible mismatches: `DR Congo` → needs `Congo DR`; `USA` → needs `United States`; `Bosnia` → needs `Bosnia-Herzegovina`; `Cape Verde` → needs `Cape Verde Islands`. Fix by adding the alias key in `_TEAM_DATA` inside `generate_knockout_pages.py`.

  **3. Generate pages:**
  ```powershell
  python generate_knockout_pages.py
  ```

  **4. Commit and push (DO NOT stage `data/live.json`, `standings.html`, `test_api.py`, `data/results.json`):**
  ```powershell
  git add predictions.html generate_knockout_pages.py HANDOFF.md
  git add .github/workflows/sync-standings.yml .github/workflows/update-odds.yml
  # Stage generated pages (check names with: git status --short):
  git add southafrica-canada.html brazil-japan.html germany-paraguay.html netherlands-morocco.html
  git add ivorycoast-norway.html france-sweden.html mexico-ecuador.html england-congodr.html
  git add belgium-senegal.html unitedstates-bosniaherzegovina.html spain-austria.html portugal-croatia.html
  git add switzerland-algeria.html australia-egypt.html argentina-capeverdeislands.html colombia-ghana.html
  git commit -m "feat: R32 knockout match pages + auto-generator for R16-Final [skip ci]"
  git push
  ```

  **5. Verify live:** Go to https://getpitchiq.net/predictions → click Round of 32 → cards with real teams should now be clickable links.

- [ ] **Fix GA4 ID on 77 match pages** — 77 pages still have placeholder `GA_MEASUREMENT_ID` instead of `G-N9PX9ZKHLR`. Run this from the project root:
  ```bash
  find . -name "*.html" -exec sed -i '' 's/GA_MEASUREMENT_ID/G-N9PX9ZKHLR/g' {} +
  ```
  Then push to Vercel and verify in GA4 Real-Time.

---

## 📅 Date-Triggered Manual Tasks (knockout rounds)

> **How to use this section:** On each date below, open the live site first.
> If the pages already exist (GitHub Actions did it automatically), skip the whole block — you're done.
> Only run the commands if the pages are missing.

---

### 🗓️ July 9 — Round of 16 pages (check after last R32 match)

**First: check if GitHub Actions already built them automatically.**
Go to https://getpitchiq.net/predictions → click **Round of 16** — if the 8 cards are clickable links, you're done. Skip this block entirely.

**If cards are NOT clickable (pages missing), run manually:**

```powershell
cd C:\Users\mroads\Documents\GitHub\PitchIQ
git pull

# Step 1 — See what team names live.json has for R16
python -c "import json; d=json.load(open('data/live.json',encoding='utf-8')); [print(k,'|',v.get('home',{}).get('name'),'vs',v.get('away',{}).get('name')) for k,v in d.get('knockout',{}).items() if v.get('home',{}).get('code') and 'r16' in str(v.get('stage',''))]"

# Step 2 — Dry run (see what pages would be generated)
python generate_knockout_pages.py --dry
```

If Step 2 prints 0 pages, a team name from the API doesn't match `_TEAM_DATA` in `generate_knockout_pages.py`.
Open `generate_knockout_pages.py`, find `_TEAM_DATA = {`, and add the missing name as a new key pointing to the same data. Common mismatches: `DR Congo` vs `Congo DR`, `USA` vs `United States`, `Bosnia` vs `Bosnia-Herzegovina`, `Côte d'Ivoire` vs `Ivory Coast`.

```powershell
# Step 3 — Generate for real
python generate_knockout_pages.py

# Step 4 — Commit generated pages (NOT live.json or standings.html)
git status --short   # identify new .html files
# Stage only the new .html files shown:
git add <list the new .html filenames here>
git commit -m "feat: R16 knockout match pages [skip ci]"
git push
```

- [ ] R16 pages verified live on July 9

---

### 🗓️ July 12 — Quarter-Final pages (check after last R16 match)

**First: check if GitHub Actions already built them.**
Go to https://getpitchiq.net/predictions → click **Quarter-Finals** — if 4 cards are clickable, skip this block.

**If pages missing, run manually:**

```powershell
cd C:\Users\mroads\Documents\GitHub\PitchIQ
git pull
python generate_knockout_pages.py --dry
# If 0 pages: debug team names (see July 9 steps above), fix alias in _TEAM_DATA, then:
python generate_knockout_pages.py
git status --short
git add <new .html filenames>
git commit -m "feat: QF knockout match pages [skip ci]"
git push
```

- [ ] QF pages verified live on July 12

---

### 🗓️ July 15 — Semi-Final pages (check after last QF match)

**First: check if GitHub Actions already built them.**
Go to https://getpitchiq.net/predictions → click **Semi-Finals** — if 2 cards are clickable, skip this block.

**If pages missing, run manually:**

```powershell
cd C:\Users\mroads\Documents\GitHub\PitchIQ
git pull
python generate_knockout_pages.py --dry
python generate_knockout_pages.py
git status --short
git add <new .html filenames>
git commit -m "feat: SF knockout match pages [skip ci]"
git push
```

- [ ] SF pages verified live on July 15

---

### 🗓️ July 18 — Final + Third Place pages (check after last SF match)

**First: check if GitHub Actions already built them.**
Go to https://getpitchiq.net/predictions → click **Final** — if the card is a clickable link, skip this block.

**If pages missing, run manually:**

```powershell
cd C:\Users\mroads\Documents\GitHub\PitchIQ
git pull
python generate_knockout_pages.py --dry
python generate_knockout_pages.py
git status --short
git add <new .html filenames>
git commit -m "feat: Final + 3rd place knockout pages [skip ci]"
git push
```

- [ ] Final + 3rd place pages verified live on July 18

---

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

### Claude — 2026-06-29 (R32 knockout match pages)

**Task: Build HTML match pages for all 16 Round of 32 cards so "Full Preview & Picks →" button links to a real page (same as group stage cards).**

**Files written/changed:**

- **`generate_knockout_pages.py`** _(new)_ — Full knockout page generator. Reads `data/knockout.json` + `data/live.json`, generates one HTML page per knockout slot with real teams using `brazil-morocco.html` as template. Contains `_TEAM_DATA` (all 32 R32 teams with analysis/stats/players), `_H2H` (head-to-head context per match), `_SUPPORTING_PICKS` (2 supporting bets per match). Writes `page_slug` back to `live.json` so predictions.html can wire up the link. Safe to re-run (skips unchanged pages). Imports helpers from `generate_pages.py`. Run: `python generate_knockout_pages.py`

- **`predictions.html`** (line ~1517) — `koCardHTML()` updated to output `<a href="/{page_slug}">` instead of a `<div>` when `live.page_slug` is set. R16/QF/SF/Final cards remain `<div>` until those pages are generated.

- **`.github/workflows/sync-standings.yml`** — Added `python3 generate_knockout_pages.py` step after `sync_knockout.py` (with `continue-on-error: true`).

- **`.github/workflows/update-odds.yml`** — Same addition.

**How it auto-scales to later rounds:** When football-data.org starts reporting R16 teams (after R32 completes ~Jul 9), `sync_knockout.py` populates those slots in `live.json`, the generator runs on the next workflow trigger, and R16 pages are committed by the bot automatically. No manual work needed.

**Blocker — not yet committed:** `data/live.json` has an unresolved merge conflict from a bot push during this session. See Outstanding Tasks above for the exact fix commands.

**Next steps:** See the 🔴 Urgent section in Outstanding Tasks above — fix the conflict, run the generator, commit, and push.

---

### Claude (Pitch) — 2026-06-27 (v2 live scores wired)

**Task: Connect real ESPN scores to the v2 Next.js app (`v2/`).**

The v2 app had a working ESPN client (`v2/lib/espn.ts`) but it was never called from the frontend. `LiveMatchProvider` was running a hardcoded France vs Uruguay simulation with scripted goals. Fixed in three files:

**Files changed:**

- **`v2/app/api/live-scores/route.ts`** _(new)_ — 5-line Next.js route that calls `getLiveScores()` and returns JSON. No API key needed — uses ESPN's free public scoreboard endpoint.
- **`v2/components/pitchiq/LiveMatchProvider.tsx`** — Replaced the fake simulation entirely. Now polls `/api/live-scores` on mount and every 30 seconds. Features the first live/halftime match, falls back to first upcoming match. Odds drift animation kept for feel.
- **`v2/components/pitchiq/FixturesWidget.tsx`** — Removed hardcoded `SCHEDULE`. Now reads all matches from context. Shows live scores in green, formats kickoff times from ISO timestamps.

**How it works:**

```
ESPN scoreboard API (free, no key)
  → GET /api/live-scores (Next.js route, revalidates every 30s server-side)
    → LiveMatchProvider polls every 30s client-side
      → match (featured) + matches (all) exposed via context
        → FeaturedMatch, LiveTicker, FixturesWidget all read from context
```

**To run locally:**

```bash
cd /Users/samsonwinz/Claude/Projects/PitchIQ/v2
npm run dev
# open http://localhost:3000
```

**If ESPN returns no matches** (tournament off-season, etc.), it falls back to hardcoded `SCOREBOARD` from `pitchiq-data.ts` so the UI never breaks.

**Next steps for this coworker:**

The v2 app loads and scores are live, but the **visual design doesn't match the static site or the prototype** (`design-handoff/PitchIQ.html`). That's the main open item. When you pick up v2 next, start by opening `design-handoff/PitchIQ.html` in a browser alongside `http://localhost:3000` and diff the two visually. The design tokens and CSS are all in `design-handoff/pitchiq.css` — the v2 components need to pull from those same tokens.

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
