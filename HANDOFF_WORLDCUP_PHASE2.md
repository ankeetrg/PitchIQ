# Handoff — World Cup Homepage Enhancements, Phase 2

**Self-contained brief.** A new chat session (or a new Claude user) can pick up the work from this file alone. Phase 1 is shipped; Phase 2 (live ticker + hero carousel wired to live scores) is the remaining work.

---

## 1. Project & deploy basics

- **Repo (local):** `C:\Users\mroads\Documents\GitHub\PitchIQ`
- **Remote:** `https://github.com/ankeetrg/PitchIQ.git`, branch `main`
- **Hosting:** GitHub Pages serving from `main` **root**. There is **no GitHub Actions build** for the static site — **pushing to `main` auto-deploys** to https://getpitchiq.net.
- **No `gh` CLI** on the machine — use plain `git`.
- **Homepage file:** `index.html` (single file; CSS in a `<style>` block, JS in a `<script>` block near the end).

### SOP for any change (follow in order)
1. **Preview locally first** — open the file in a browser (PowerShell `Start-Process "C:\Users\mroads\Documents\GitHub\PitchIQ\index.html"`) and show the user before pushing. ⚠️ Caveat below.
2. **Push to `main`** with a descriptive commit (this auto-deploys).
3. **After every push, update memory** — append the change (commit hash + before/after) to the change log and refresh the index line.

⚠️ **Local preview limitation:** the homepage uses `fetch('/data/*.json')` with absolute paths. Opened as a local `file://`, those fetches fail, so **live-data behaviour (scores, knockout) cannot be fully verified locally** — only on getpitchiq.net. Preview confirms layout/no-JS-errors; the user verifies data on the live site after push.

---

## 2. Data layer (the source of truth — already in git)

- **`data/live.json`** — written server-side by `generate_live_data.py` (football-data.org + ESPN). `js/pitchiq-live.js` polls it every 5 min (`js/pitchiq-config.js` → `window.PITCHIQ_CONFIG`). Shape:
  - `matches`: object keyed by **group-match slug** (e.g. `"mexico-southafrica"`, `"brazil-morocco"`). Each value:
    ```json
    { "home":"Mexico","away":"South Africa","home_emoji":"🇲🇽","away_emoji":"🇿🇦",
      "date_short":"Jun 11","time_str":"5:00 PM ET","venue_short":"Estadio Azteca",
      "home_ml":"-165","draw_ml":"+280","away_ml":"+490","ou_line":"2.5",
      "home_prob":62,"draw_prob":22,"away_prob":16,
      "status":"upcoming|live|ft","score_home":null,"score_away":null,"clock":null }
    ```
  - `knockout`: object keyed by **bracket id** (`"wc2026-m73"`). Each value:
    ```json
    { "stage":"r32","status":"ft|live|upcoming|tbd","score_home":0,"score_away":1,"clock":null,
      "home":{"name":"South Africa","code":"za","emoji":"🇿🇦"},
      "away":{"name":"Canada","code":"ca","emoji":"🇨🇦"},
      "page_slug":"southafrica-canada" }
    ```
    A knockout side is **decided** only if `home.code`/`away.code` exists; otherwise show **TBD**.
  - `standings`: groups `A`..`L` (used by the standings widget — not part of Phase 2).
  - `_meta`: timestamps.
- **`data/knockout.json`** — base bracket (32 matches, stages `r32,r16,qf,sf,tp,final`). Each match has `slug` (= the `wc2026-mXX` id), `round` ("Round of 32"), `date_short` ("Jun 29"), `time_str`, `home/away` placeholder names ("Runner-up Group A"), `prob`, `pick`, `odds`. **No ISO date field** — derive ISO from `date_short` + year 2026.

**Slug alignment:** `live.json.matches` keys == the homepage `FIXTURES` slugs. So group live data is looked up by `live.json.matches[slug]`. Knockout live data is `live.json.knockout[wc2026-mXX]`, joined to `knockout.json` by `slug`.

---

## 3. What Phase 1 already did (shipped, commit `472eb28`)

In `index.html`, the **Fixtures & Previews** pane:
- Calendar rebuilt to match `predictions.html`: month title + **prev/next arrows**, month nav bounded to months with fixtures, green=has-fixtures / grey=disabled days.
- A `loadKnockoutFixtures()` IIFE fetches `/data/knockout.json` + overlays `/data/live.json`'s `knockout`, and appends **R32→Final** rows to the fixtures list. Undecided teams render `<span class="fix-tbd">TBD</span>`. ISO derived via `isoFromShort()`.
- Date tabs (today/tomorrow) + any calendar day filter across **group + knockout** rows by ISO date.

These helpers now exist inside the fixtures IIFE and are good patterns to reuse: `isoFromShort(date_short)`, `esc()`, `flagImg(code,name)`, `badge(iso)`, `TEAMS` map, `FIXTURES` array.

---

## 4. Phase 2 — the work to do

Wire the two remaining homepage widgets to live data so they show **today's** matches with **live scores** from the API (`data/live.json`).

### Task A — Live ticker (top scrolling bar)
- **Where:** `index.html`, `(function buildTicker(){…})()` (~line 3720, inside the big fixtures IIFE) populating `#tickerTrack` (~line 2482).
- **Current:** shows only today's **group** fixtures from the hardcoded `FIXTURES` array, **no scores**.
- **Wanted:**
  1. Show **only today's** matches (group **and** knockout). "Today" = local date; group rows have ISO in `FIXTURES`, knockout via `isoFromShort(date_short)`.
  2. For each, overlay live data by slug: group → `live.json.matches[slug]`, knockout → `live.json.knockout[wc2026-mXX]`. If `status==="live"` or `"ft"` and scores present, show the **score** (e.g. `2–1`, plus `clock` if live); otherwise show kickoff time.
  3. If no matches today, keep the existing "No matches scheduled today" message.
- **Note:** `pitchiq-live.js` has an `updateTicker(data)` that expects a `data.ticker` array — **live.json has no `ticker` key**, so that path is dormant. Either (a) build the ticker in `index.html` from `matches`/`knockout` + re-render on poll, or (b) add a `ticker` array to `generate_live_data.py` and let `pitchiq-live.js` own it. Recommend (a) for a pure front-end change; mention (b) to the user if they prefer server-side.

### Task B — Hero carousel / pagination cards
- **Where:** `index.html`, `var TODAY_MATCHES` (~line 3151), `buildMatchCard(m)` (~line 3177), `(function initCarousel(){…})()` (~line 3210) rendering into `#mcViewport` (~line 2539). Card classes are `mc-*` (`.mc-card`, `.mc-teams`, `.mc-mid`, `.mc-odds`, `.mc-status`, etc.).
- **Current:** `TODAY_MATCHES` is **hardcoded** (Qatar–Switzerland, etc.) and never reflects the real date or scores.
- **Wanted:**
  1. Build the carousel from **today's** matches (group + knockout), same "today" logic as the ticker.
  2. Add a **live score** at a suitable spot on the card — the `.mc-mid` block currently shows `VS` / kickoff time and the AI pick; for live/ft matches show `score_home–score_away` (+ `clock` for live) there, and keep the `LIVE` status pill (`.mc-status.live`) already supported by `buildMatchCard`.
  3. Be **TBD-aware** for knockout cards (undecided side → "TBD", no flag).
  4. If there are no matches today, render a graceful empty card (don't leave the carousel blank/broken).
- Live scores should refresh with the poll cycle (re-render or update the active card every `PITCHIQ_CONFIG.pollInterval`).

### Cross-cutting
- Reuse Phase 1 helpers; keep one source of "today's matches" (a small function returning the merged group+knockout list with live overlay) shared by ticker + carousel.
- **Graceful fallback:** if `/data/*.json` fails, fall back to current static behaviour — never blank the widgets.
- Don't disturb the already-shipped fixtures calendar, standings, or collapsible sections.

---

## 5. Acceptance criteria (verify on getpitchiq.net)
1. Ticker shows **only today's** matches; live games show a score that updates; pre-match shows kickoff time; "no matches" message when empty.
2. Carousel cards are **today's** matches with a live score visible on live/ft cards; knockout cards show TBD where undecided; arrows/dots still work.
3. No regressions to fixtures calendar, standings, or collapsible sections.
4. No console errors when the JSON is reachable; graceful fallback when it isn't.

---

## 6. Copy-paste prompt for a fresh session

> You're continuing work on the PitchIQ homepage (`index.html`) in the repo `C:\Users\mroads\Documents\GitHub\PitchIQ`. Read `HANDOFF_WORLDCUP_PHASE2.md` in the repo root first — it has the full context, data shapes, file/line anchors, SOP, and acceptance criteria.
>
> Implement **Phase 2**: wire the homepage **live ticker** and the **hero carousel** to `data/live.json` (+ `data/knockout.json`) so both show **only today's matches** (group + knockout) with **live scores** (e.g. `2–1`, with the in-match clock for live games), falling back to kickoff time before a match starts. Make the carousel build from a real "today's matches" derivation (the `TODAY_MATCHES` array is currently hardcoded — replace it), add a live score at a sensible spot on each card, and be TBD-aware for undecided knockout ties. Reuse the Phase-1 helpers (`isoFromShort`, `esc`, `flagImg`, `badge`, `TEAMS`, `FIXTURES`) and keep a single shared "today's matches" function for both widgets. Keep graceful fallbacks so nothing blanks if the JSON can't load.
>
> Follow the SOP: preview locally and show me first (note: `file://` can't fetch `/data/*.json`, so the live-data parts verify only on getpitchiq.net), then push to `main` (auto-deploys), then update memory. Don't touch the already-shipped fixtures calendar, standings, or collapsible sections.

---

*Created during the Phase-1 session. Phase 1 = commit `472eb28`. When Phase 2 ships, record its commit here and in memory (`pitchiq-homepage-changes.md`).*
