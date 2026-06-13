# PitchIQ — Homepage Design Polish
## Run with: claude --dangerously-skip-permissions

You are a senior frontend engineer working on getpitchiq.net — a premium World Cup 2026 fantasy and betting intelligence site. The homepage (index.html) has dead spots, a static hero showing only one match, and poor scroll rhythm. Fix all of this. Pure HTML/CSS/JS only — no frameworks, no build tools.

Read index.html in full before touching anything.

---

## DESIGN TOKENS (already in :root — do not change)

```
--nav:#071D36  --grn:#00963F  --grn-h:#007A32  --bg:#EEF1F6
--surf:#fff    --t1:#0F1923   --t2:#3C5168     --t3:#7C92A8
--b1:#E2E8F0   --b2:#C8D5E0   --r:6px          --r2:12px
--sans:'Inter'  --cond:'Barlow Condensed'
```

---

## CHANGE 1 — REPLACE HERO WITH TODAY'S MATCH SLIDER

The current hero shows only Brazil vs Morocco in a static card. Replace `.match-hero` + `.side-col` with a full-width 2-column layout:

**Left column (main):** A swipeable/clickable match card carousel showing all today's matches. Auto-advances every 6 seconds. User can click dots or arrow buttons to jump.

Each card shows:
- Group badge + venue
- Teams with flag images (flagcdn.com/w80/[iso].png)
- Kickoff time or LIVE pill + score if in progress  
- 3-column odds strip (Home / Draw / Away) linking to match pages via data-aff
- PitchIQ AI pick badge (green pill, e.g. "Switzerland Win")
- "Full Preview →" CTA linking to the match page

**Today's 4 matches to show (in order, PT times):**

```js
var TODAY_MATCHES = [
  {
    slug: 'qatar-switzerland',
    home: 'Qatar',        home_iso: 'qa',  home_ml: '+340',
    away: 'Switzerland',  away_iso: 'ch',  away_ml: '-145',
    draw_ml: '+280',
    group: 'B', time: '12PM PT', venue: 'BMO Field, Toronto',
    ai_pick: 'Switzerland Win', ai_conf: 74,
    status: 'live', elapsed: 85   // update this — it's late in the match
  },
  {
    slug: 'germany-curacao',
    home: 'Germany',  home_iso: 'de',  home_ml: '-360',
    away: 'Curaçao',  away_iso: 'cw',  away_ml: '+900',
    draw_ml: '+500',
    group: 'E', time: '3PM PT', venue: 'Mercedes-Benz Stadium, Atlanta',
    ai_pick: 'Germany Win to Nil', ai_conf: 81,
    status: 'upcoming'
  },
  {
    slug: 'brazil-morocco',
    home: 'Brazil',   home_iso: 'br',  home_ml: '-138',
    away: 'Morocco',  away_iso: 'ma',  away_ml: '+500',
    draw_ml: '+290',
    group: 'C', time: '6PM PT', venue: 'MetLife Stadium, NJ',
    ai_pick: 'Brazil Win', ai_conf: 68,
    status: 'upcoming'
  },
  {
    slug: 'haiti-scotland',
    home: 'Haiti',    home_iso: 'ht',  home_ml: '+380',
    away: 'Scotland', away_iso: 'gb-sct', away_ml: '-125',
    draw_ml: '+310',
    group: 'C', time: '9PM PT', venue: 'Gillette Stadium, MA',
    ai_pick: 'Under 2.5 Goals', ai_conf: 62,
    status: 'upcoming'
  }
];
```

Carousel CSS: cards are `position:absolute`, transition `transform 0.4s cubic-bezier(.4,0,.2,1)`. The active card slides in from right. Height is fixed at ~340px so layout doesn't jump.

Dot indicators: 4 dots below the card, green when active.

**Right column (sidebar):** Keep the existing Fixtures widget + Best Bets widget. Remove the 300x250 ad slot from here — it breaks the rhythm. Move it below the hero section.

---

## CHANGE 2 — REPLACE STATS STRIP WITH "TODAY'S RESULTS" SCOREBOARD

The stats strip (104 matches, 48 nations, etc.) is decorative filler. Replace it with a **horizontal scrollable scoreboard** of today's FT results + upcoming matches.

Style: dark navy background (`--nav`), single row, scrolls horizontally on mobile. Each result is a pill card.

```js
var SCOREBOARD = [
  // FT results (Jun 12-13)
  { home:'Mexico',       home_iso:'mx', score:'2–0', away:'South Africa', away_iso:'za', status:'FT',  group:'A' },
  { home:'South Korea',  home_iso:'kr', score:'2–1', away:'Czechia',      away_iso:'cz', status:'FT',  group:'A' },
  { home:'Canada',       home_iso:'ca', score:'1–1', away:'Bosnia',       away_iso:'ba', status:'FT',  group:'B' },
  { home:'USA',          home_iso:'us', score:'4–1', away:'Paraguay',     away_iso:'py', status:'FT',  group:'D' },
  // Today upcoming/live
  { home:'Qatar',        home_iso:'qa', score:'',    away:'Switzerland',  away_iso:'ch', status:'LIVE', group:'B', time:'85\''},
  { home:'Germany',      home_iso:'de', score:'',    away:'Curaçao',      away_iso:'cw', status:'3PM',  group:'E' },
  { home:'Brazil',       home_iso:'br', score:'',    away:'Morocco',      away_iso:'ma', status:'6PM',  group:'C' },
  { home:'Haiti',        home_iso:'ht', score:'',    away:'Scotland',     away_iso:'gb-sct', status:'9PM', group:'C' },
];
```

Each pill: flag + team abbrev + score/time + flag. FT pills have muted styling. LIVE pill has a red pulsing dot. Upcoming pills show time in green.

Keep the scroll-ticker that's above the nav separate — this scoreboard replaces the stats strip only.

---

## CHANGE 3 — FIX FANTASY TABLE OPPONENT MATCHUPS

The fantasy picks table has wrong opponents. Fix these rows (update `fp-match` cells and player nations):

```
Mbappé      → FRA vs SEN  (Jun 16, Group I)
Vinicius    → BRA vs MAR  (Jun 13, Group C) ← today
Haaland     → NOR vs IRQ  (Jun 16, Group I)
Bruno F.    → POR vs DRC  (Jun 17, Group K)
Pedri       → ESP vs CPV  (Jun 15, Group H) ← tomorrow
Rúben Dias  → POR vs DRC  (Jun 17, Group K)
Alisson     → BRA vs MAR  (Jun 13, Group C)
```

Also add a "TODAY" badge to Vinicius and Alisson rows (they play today).

---

## CHANGE 4 — ADD GROUP STANDINGS WIDGET

Between the Fantasy Picks section and the Betting Intelligence section, add a compact **Group Standings** widget. Horizontal tab selector: Group A / B / C / D (show A-D for now, others coming).

Table columns: Flag · Team · P · W · D · L · GD · Pts

Use these real standings after today's Jun 12-13 morning results:

```js
var STANDINGS = {
  A: [
    { iso:'mx',  name:'Mexico',       p:1, w:1, d:0, l:0, gd:'+2', pts:3 },
    { iso:'kr',  name:'Korea Rep.',   p:1, w:1, d:0, l:0, gd:'+1', pts:3 },
    { iso:'cz',  name:'Czechia',      p:1, w:0, d:0, l:1, gd:'-1', pts:0 },
    { iso:'za',  name:'South Africa', p:1, w:0, d:0, l:1, gd:'-2', pts:0 }
  ],
  B: [
    { iso:'ca',  name:'Canada',       p:1, w:0, d:1, l:0, gd:'0',  pts:1 },
    { iso:'ba',  name:'Bosnia',       p:1, w:0, d:1, l:0, gd:'0',  pts:1 },
    { iso:'ch',  name:'Switzerland',  p:1, w:0, d:0, l:0, gd:'–',  pts:0, note:'Playing' },
    { iso:'qa',  name:'Qatar',        p:1, w:0, d:0, l:0, gd:'–',  pts:0, note:'Playing' }
  ],
  C: [
    { iso:'br',  name:'Brazil',       p:0, w:0, d:0, l:0, gd:'–',  pts:0, note:'6PM today' },
    { iso:'ma',  name:'Morocco',      p:0, w:0, d:0, l:0, gd:'–',  pts:0, note:'6PM today' },
    { iso:'ht',  name:'Haiti',        p:0, w:0, d:0, l:0, gd:'–',  pts:0, note:'9PM today' },
    { iso:'gb-sct', name:'Scotland',  p:0, w:0, d:0, l:0, gd:'–',  pts:0, note:'9PM today' }
  ],
  D: [
    { iso:'us',  name:'USA',          p:1, w:1, d:0, l:0, gd:'+3', pts:3 },
    { iso:'py',  name:'Paraguay',     p:1, w:0, d:0, l:1, gd:'-3', pts:0 },
    { iso:'au',  name:'Australia',    p:0, w:0, d:0, l:0, gd:'–',  pts:0 },
    { iso:'tr',  name:'Türkiye',      p:0, w:0, d:0, l:0, gd:'–',  pts:0 }
  ]
};
```

Leader row gets a subtle green left border. Widget title: "Group Standings · WC2026". Link: "All Groups →" → /standings

---

## CHANGE 5 — SMOOTH SCROLL + SECTION RHYTHM

The page scrolls in chunks because sections have inconsistent vertical spacing. Fix:

1. Add `scroll-behavior: smooth` to `html` (already there — confirm it's on body too).
2. Replace all `margin-bottom: 28px` / `margin-bottom: 32px` on sections with a consistent `--gap: 32px` variable and use it uniformly.
3. Add `padding: 32px 0` to the Betting Intelligence section — it currently has no top breathing room.
4. Add a thin `1px solid var(--b1)` divider between the scoreboard and Fantasy Picks section so sections visually separate.
5. All `.rv` (reveal-on-scroll) elements already have IntersectionObserver. Make sure the Group Standings widget and scoreboard also get `class="rv"`.
6. Stagger the carousel card entrance: first card fades in at 0ms, each subsequent card 60ms later.

---

## CHANGE 6 — FILL THE NEWS SECTION GAP

The news section (ESPN RSS feed) loads async and leaves a white gap while loading. The skeleton cards exist but are too tall. Fix:

1. Reduce skeleton card height from whatever it is to `200px` (matching the real card image height).
2. Add a subtle `border: 1px solid var(--b1)` to skeleton cards so they don't look like blank holes.
3. If the RSS fetch fails entirely, show 3 hardcoded fallback cards linking to today's match previews:
   - "Brazil vs Morocco Preview" → /brazil-morocco
   - "Germany vs Curaçao Preview" → /germany-curacao  
   - "Spain vs Cape Verde Preview" → /spain-capeverde

---

## WHAT NOT TO TOUCH

- Do not change the top ticker bar
- Do not change the nav
- Do not remove or modify affiliate link structure (data-aff, AFF config, rel="noopener sponsored")
- Do not change the Coming Soon modal logic
- Do not change the disclaimer bar
- Do not change the footer
- Do not add any external JS libraries
- Do not modify any other HTML files

---

## VERIFICATION

After all changes:

```bash
# No broken internal links
grep -o 'href="/[^"]*"' index.html | sort -u

# Confirm carousel JS exists
grep -c "TODAY_MATCHES" index.html

# Confirm standings data exists
grep -c "STANDINGS" index.html

# Confirm scoreboard exists
grep -c "SCOREBOARD" index.html

# No wrong match names in fantasy table
grep -i "FRA vs URU\|BRA vs COL\|NOR vs GHA\|POR vs KOR\|ESP vs MEX" index.html && echo "❌ WRONG MATCHUPS STILL PRESENT" || echo "✅ Matchups clean"
```

## DONE

Report:
```
=== DESIGN POLISH COMPLETE ===
Match carousel: [built / error]
Scoreboard: [built / error]
Fantasy matchups fixed: [Y/N]
Standings widget: [built / error]
Scroll rhythm: [fixed]
News fallback: [added]
Broken links: [N or list]
```
