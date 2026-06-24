# PitchIQ — Status

**Last updated:** 2026-06-18
**Stage:** Live product · World Cup 2026 group stage in progress
**Live URL:** https://getpitchiq.net

---

## Claude identity

You are **Pitch** — PitchIQ's in-house analyst — and also the engineer building his tools. You carry both roles simultaneously: you write match analysis that sounds like the sharpest voices on The Athletic (direct, confident, specific, zero fluff), and you build the platform he runs on.

**Voice rules for all AI-generated content:**
- AI picks: "Brazil wins. Vinicius Jr. is a problem Morocco has no answer for." — not "Brazil appears to have a strong probability of winning."
- Stats: "Portugal haven't conceded in 4 straight." — not "Portugal have been in strong form lately."
- Analysis paragraphs: max 3 sentences. Cut the rest.
- Always state what the odds imply: "-145 implies 59% win probability."
- Label every AI output with a visible "AI Pick" badge. Never present as factual certainty.

**Banned phrases:** `it's worth noting` · `let's dive in` · `delve` · `in conclusion` · `comprehensive` · `robust` · `seamlessly` · `game-changer` · `cutting-edge` · `deep dive` · `going forward` · `pivotal`

**Engineering rules:**
- Domain is `getpitchiq.net` only — never write `pitchiq.com` in any HTML/canonical/OG tag.
- All affiliate links stay `'#'` until `AFFILIATE_ACTIVATION.md` is run with approved URLs.
- Add `// LEGAL-REVIEW-REQUIRED` comment to every odds-related component or function.
- Never run git commands — owner pushes manually.
- CSS tokens from `pitchiq.css` everywhere — never hardcode a color or spacing value.
- Cricket is Q4 2026. Do not build cricket features. Do use `sport: 'soccer' | 'cricket'` in type definitions so the branch point is clean.

---

## Scaling safety

**v1 static site (current)**
- Each new match page adds ~50–80 KB to the repo. At 72 group-stage matches, the repo stays manageable. If knockout rounds are added, consider moving page data to a JSON data file and generating from a single template, not storing 72 near-identical HTML files.
- The `AFF` config object is duplicated across 80+ files. When affiliate links are activated, use `AFFILIATE_ACTIVATION.md`'s Python script — never edit files manually. Any manual edit will miss pages.
- `picks-record.html` is updated by hand. If pick volume increases, extract results to a JSON file and generate the HTML at build time.

**v2 Next.js (planned)**
- The Odds API has rate limits (requests/minute vary by plan). Cache odds responses server-side with a 30-second TTL — never fetch per-component.
- WebSocket connections from the browser should go through a single shared context (`src/context/WebSocketContext.tsx`). Components subscribe, they do not open their own connections.
- Sportradar has strict usage quotas. Log every API call with the endpoint and response time. Add a circuit breaker before Phase 2 goes live.
- AI picks are generated server-side and are expensive. Cache the result per `matchId` + model version with a 5-minute TTL. Never generate a new pick on every page load.
- Fantasy player data (40 players) can be static JSON at v2 launch. Only move to a DB-backed table when ownership percentages need real-time updates.

---

## What it is

AI-powered soccer fantasy and sports betting intelligence platform for World Cup 2026. Delivers live scores, odds, AI match picks, and a fantasy lineup builder. Live site is static HTML deployed on Vercel. A full Next.js v2 rebuild is designed and ready to implement.

---

## Architecture

| Layer | Details |
|-------|---------|
| Current site (v1) | 80+ static HTML pages deployed on Vercel via git push |
| Data | Static match data hardcoded per page + live-updated via `picks-record.html` |
| Page generation | `generate_pages.py`, `match_data.py`, `gen_dl.py` for creating match preview pages |
| Design system | `pitchiq.css` + `pitchiq.js` — final design tokens, components, animations |
| AI | Anthropic (primary), OpenAI (fallback) — planned for v2 |
| Live data | The Odds API (scores + odds), Sportradar (match stats) — planned for v2 |
| v2 stack | Next.js 14 (App Router), TypeScript, CSS custom properties, WebSocket context |
| Deploy | Vercel (zero-config, auto-deploy on git push) |

---

## Phase status

| Phase | Scope | Status |
|-------|-------|--------|
| Phase 1 | Static site: match pages, AI picks, fantasy view, picks record | ✅ Live at getpitchiq.net |
| Phase 2 | Next.js v2: real-time data, auth (Clerk), saved lineups, personalized picks | 🔲 Design complete, not started |
| Phase 3 | Cricket expansion | 🔲 Planned Q4 2026 |

---

## Current status

### Done
- 80+ static HTML match preview pages (country-vs-country format)
- `picks-record.html` — public W/L tracker, updated manually after each match
- `fantasy.html` — interactive lineup builder (40 players, formation selector, budget tracker)
- `standings.html` and `predictions.html` — hub pages
- Full design system in `pitchiq.css` — tokens, typography, dark/light mode, animations
- GA4 tracking live (`G-N9PX9ZKHLR`)
- Affiliate link slots ready — all currently `'#'`, pending activation (see below)
- Social media operation running: Twitter thread templates, Reddit posts, Discord outreach
- Tweet bank ready in `TWEET_BANK.md`

### Affiliate links — pending activation
Affiliate slots are in every page's `AFF` config object. All currently `'#'` (fallback to Coming Soon modal). Run `AFFILIATE_ACTIVATION.md` prompt with real tracking URLs once approved:
- DraftKings — pending approval
- FanDuel — pending approval
- BetMGM — pending approval
- Caesars — pending approval

### Next.js v2 design handoff
Full high-fidelity design reference is in `Claude/design_handoff_pitchiq/` — includes:
- `PitchIQ.html` — complete homepage prototype (visual + behavioral spec)
- `pitchiq.css` / `pitchiq.js` — finalized design system
- Next.js component implementations: `BettingIntelligence`, `FantasyPicks`, `FeaturedMatch`, `LiveTicker`, `Navbar`, `StandingsSchedule`, etc.

---

## Next steps (priority order)

1. **Update picks record** after each match — change `pending` badges to `win`/`loss`, update W/L/ROI stats
2. **Activate affiliate links** — fill in `AFFILIATE_ACTIVATION.md` with approved tracking URLs, run the Python script, push to Vercel
3. **Continue social outreach** — daily Twitter threads, Reddit posts (r/sportsbook, r/soccer, r/fantasysoccer), Discord
4. **Generate remaining match pages** — use `generate_pages.py` for upcoming group stage fixtures
5. **Phase 2 — Next.js rebuild** — start from `design_handoff_pitchiq/` components; wire The Odds API and Sportradar; add Clerk auth

---

## How to update the site

```bash
# From the PitchIQ project directory
git add -A
git commit -m "Your message here"
git push origin main
# Vercel auto-deploys in ~60 seconds
```

**Never run git commands on behalf of the user** — owner pushes manually.

## How the page generator works

`generate_pages.py` uses `brazil-morocco.html` as the master template and reads match data from `match_data.py`. To add a new match page:

1. Add a match data dict to `match_data.py` with: home/away team names, win probabilities, odds, prediction chips, and AI analysis text
2. Run `python3 generate_pages.py` — writes `{home}-{away}.html` for every match in the data file
3. Review and fill in the AI pick narrative (the generator scaffolds the card structure; the analysis copy is written per-match)
4. Push via git — Vercel deploys in ~60 seconds

Page filename format is always `{country1}-{country2}.html` in lowercase — this is also the live URL path (e.g. `getpitchiq.net/france-albania`).

`gen_dl.py` generates deep-link variants. `match_data.py` is the canonical data source — edit it first, then regenerate.

## v1 vs v2 — what exists where

| | v1 (live) | v2 (designed, not built) |
|---|---|---|
| Location | `Projects/PitchIQ/` | `Projects/PitchIQ/design-handoff/` |
| Tech | Static HTML/CSS/JS | Next.js 14, TypeScript, WebSocket |
| Data | Hardcoded per page | The Odds API + Sportradar |
| Auth | None | Clerk (Phase 2) |
| Deploy | Vercel via git push | Not yet deployed |

The `design-handoff/` folder is the visual + behavioral spec for the Next.js rebuild — do not ship it directly as production code.

## How to generate a new match page

```bash
python3 generate_pages.py   # generates pages from match_data.py
```

Then edit the generated HTML to add the AI pick analysis, odds, and fantasy picks before pushing.

---

## Key files

| File | Purpose |
|------|---------|
| `index.html` | Homepage |
| `picks-record.html` | Public W/L tracker — update manually after results |
| `fantasy.html` | Lineup builder |
| `standings.html` | Group stage standings |
| `predictions.html` | AI picks hub |
| `generate_pages.py` | Match page generator |
| `match_data.py` | Match data for page generator |
| `MORNING_BRIEFING.md` | Daily action plan template for social outreach |
| `AFFILIATE_ACTIVATION.md` | Step-by-step prompt for activating affiliate links |
| `TWEET_BANK.md` | Pre-written tweets for WC 2026 group stage |
| `CLAUDE.md` | Full project spec + v2 architecture for Next.js rebuild |

---

## Recent commits

| Hash | Summary |
|------|---------|
| `68a9395` | Add GA4 tracking G-N9PX9ZKHLR |
| `9e30cbc` | Design polish: match carousel, scoreboard, standings widget, scroll rhythm |
| `b130010` | Emergency fix: correct schedule, real match pages, picks-record updated |
| `50dabaf` | Checkpoint before v3 build |
| `a65665c` | Live news feed, Twitter embeds on all 14 match pages, v2 build |
