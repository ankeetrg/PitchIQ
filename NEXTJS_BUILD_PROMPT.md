# PitchIQ — Next.js 14 Homepage Build
## Run with: claude --dangerously-skip-permissions

You are a senior full-stack engineer rebuilding **getpitchiq.net** — a premium AI-powered soccer fantasy and sports betting intelligence platform for World Cup 2026 — in a production Next.js codebase.

The site is currently a static HTML/CSS/JS prototype. Your job is to port the homepage faithfully into Next.js 14 (App Router) + TypeScript + Tailwind CSS, preserving every design detail, interaction, and data point exactly.

---

## IDENTITY & CONTEXT

**Product:** PitchIQ — World Cup 2026 AI Fantasy & Betting Intelligence Platform  
**URL:** getpitchiq.net  
**Tagline:** AI-powered soccer intelligence for fantasy players and sports bettors  
**Audience:** Fantasy managers and recreational sports bettors, 21+, US-focused  
**Tone:** Premium, sharp, data-forward. Like The Athletic meets ESPN BET — not a sportsbook, not a blog.

**Business model:**
- Affiliate revenue from DraftKings, FanDuel, BetMGM, Caesars (all links currently `'#'` — use `href="#"` with `rel="noopener sponsored"`)
- Email newsletter (no endpoint yet — show success state, store nothing server-side)
- Future: paid fantasy tiers, cricket coverage (Q4 2026)

**Design philosophy:** Dark navy primary palette, gold accents for CTAs and active states, green for AI picks and positive movement, red for live/alerts. Every pixel earns its place — no decorative filler.

**Current tech (reference only, do not port these):**
- Static HTML (`index.html`) + `pitchiq.css` + `pitchiq.js`
- Deployed on Vercel via GitHub (`ankeetrg/PitchIQ`, main branch)
- GA4: `G-N9PX9ZKHLR` (wire this up in the Next.js layout)
- Vercel Analytics: `@vercel/analytics` package

---

## REFERENCE FILES — READ THESE FIRST

Before writing a single line of component code, read:

1. `PitchIQ v2.html` — complete page markup, every section, every data point
2. `pitchiq.css` — full design system: tokens, components, animations, responsive rules
3. `pitchiq.js` — all interactions: live simulation, theme toggle, scroll reveal, toast system, pick system

These are your specification. If something is in the reference files, match it exactly. If something is ambiguous, use your judgment but stay within the design system.

---

## STACK

- **Next.js 14** (App Router) — `app/` directory, `page.tsx` for homepage
- **TypeScript** — strict mode, no `any`
- **Tailwind CSS** — extend config with custom tokens (see below); no arbitrary values where a token exists
- **Framer Motion** — scroll reveal animations and probability bar width transitions
- **next/font/google** — Inter (400/500/600/700) + Barlow Condensed (400/600/700/800/900)
- **@vercel/analytics** — import `Analytics` in root layout
- Keep all PitchIQ components in `/components/pitchiq/`
- Data in `/lib/pitchiq-data.ts` — typed constants, no API calls

---

## TAILWIND CONFIG — extend tailwind.config.ts

```ts
import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: ['selector', '[data-theme="dark"]'],
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: '#091525',
          2: '#0C1C2E',
        },
        gold: {
          DEFAULT: '#D97706',
          hover:   '#B45309',
          dim:     'rgba(217,119,6,0.10)',
          border:  'rgba(217,119,6,0.24)',
        },
        green: {
          DEFAULT: '#00963F',
          hover:   '#007B33',
          dim:     'rgba(0,150,63,0.10)',
          border:  'rgba(0,150,63,0.22)',
        },
        red: {
          DEFAULT: '#DC2626',
          dim:     'rgba(220,38,38,0.10)',
        },
        blue: {
          DEFAULT: '#2563EB',
          dim:     'rgba(37,99,235,0.10)',
        },
      },
      fontFamily: {
        cond: ['"Barlow Condensed"', 'Arial Narrow', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
export default config
```

---

## CSS VARIABLES — globals.css

Set on `:root` (light mode):
```css
:root {
  --bg:   #F8F5EF;
  --bg2:  #F1EBE2;
  --surf: #FFFFFF;
  --b1:   #E5DDD0;
  --b2:   #CEC5B5;
  --t1:   #0F1923;
  --t2:   #374151;
  --t3:   #6B7280;
  --t4:   #9CA3AF;
}

[data-theme="dark"] {
  --bg:   #0B1420;
  --bg2:  #101C2C;
  --surf: #152030;
  --b1:   rgba(255,255,255,0.07);
  --b2:   rgba(255,255,255,0.13);
  --t1:   #EDF2F7;
  --t2:   #94A3B8;
  --t3:   #64748B;
  --t4:   #475569;
}

html {
  scroll-behavior: smooth;
  font-variant-numeric: tabular-nums;
}

body {
  background: var(--bg);
  color: var(--t1);
  padding-bottom: 60px; /* clear mobile bottom nav */
}

.theme-switching * {
  transition: background-color 250ms ease, border-color 250ms ease, color 250ms ease !important;
}
```

---

## PAGE LAYOUT — exact section order

Max content width: **1360px**, centered, **24px horizontal gutter** (`px-6 mx-auto max-w-[1360px]`).

1. Legal Disclaimer Bar
2. Live Ticker (sticky)
3. Primary Navbar (sticky)
4. Sport Switcher (sticky)
5. Hero Grid
6. Sportsbook Promo Bar
7. Stats Strip
8. Group Standings + Today's Schedule
9. Fantasy Picks
10. AI Parlay of the Day
11. Betting Intelligence (3-card grid)
12. Line Movement Feed
13. News & Analysis + Alert Feed
14. Newsletter Strip
15. Footer
16. Mobile Bottom Nav (fixed)

---

## COMPONENT ARCHITECTURE

```
app/
  layout.tsx          ← root layout: fonts, theme provider, Analytics, GA4
  page.tsx            ← homepage: imports all sections in order
  globals.css

components/pitchiq/
  DisclaimerBar.tsx
  LiveTicker.tsx
  Navbar.tsx
  SportSwitcher.tsx
  HeroGrid.tsx
    FeaturedMatchCard.tsx
    FixturesWidget.tsx
    BestBetsWidget.tsx
  SportsbookPromoBar.tsx
  StatsStrip.tsx
  GroupStandings.tsx
  TodaySchedule.tsx
  FantasyPicks.tsx
  AIParlayCard.tsx
  BettingIntelligence.tsx
  LineMovementFeed.tsx
  NewsAndAlerts.tsx
  NewsletterStrip.tsx
  Footer.tsx
  MobileBottomNav.tsx
  Toast.tsx
  CricketModal.tsx
  ThemeProvider.tsx   ← context + localStorage sync

lib/
  pitchiq-data.ts     ← all hardcoded data, fully typed
  pitchiq-types.ts    ← shared TypeScript interfaces
```

---

## DATA — hardcode all of this in lib/pitchiq-data.ts

### Live Match
```ts
export const LIVE_MATCH = {
  home: 'France',     homeIso: 'fr', homeScore: 1,
  away: 'Uruguay',    awayIso: 'uy', awayScore: 0,
  minute: 67,
  group: 'E',
  status: 'LIVE' as const,
  homePct: 72, drawPct: 18, awayPct: 10,
  homeOdds: '-185', drawOdds: '+290', awayOdds: '+480', ouOdds: '2.5',
  homeXg: 1.8, awayXg: 0.4,
  h2h: '3W–2D–1L',
  aiConfidence: 81,
  homeForm: ['W','W','D','W','L'] as const,
  awayForm: ['W','D','L','W','D'] as const,
}
```

### Ticker
```ts
export const TICKER_ITEMS = [
  { label: 'FT',   home: 'Mexico',      hs: 2, away: 'South Africa', as: 0, group: 'A' },
  { label: 'FT',   home: 'South Korea', hs: 2, away: 'Czechia',      as: 1, group: 'A' },
  { label: 'FT',   home: 'Canada',      hs: 1, away: 'Bosnia',       as: 1, group: 'B' },
  { label: 'FT',   home: 'USA',         hs: 4, away: 'Paraguay',     as: 1, group: 'D' },
  { label: '3PM PT', home: 'Qatar',     hs: null, away: 'Switzerland', as: null, group: 'B' },
  { label: '6PM PT', home: 'Brazil',    hs: null, away: 'Morocco',     as: null, group: 'C' },
  { label: '9PM PT', home: 'Haiti',     hs: null, away: 'Scotland',    as: null, group: 'C' },
]
```

### Group Standings (Groups A–D)
```ts
export const STANDINGS = {
  A: [
    { iso: 'mx', name: 'Mexico',       p:1, w:1, d:0, l:0, gd:'+2', pts:3 },
    { iso: 'kr', name: 'Korea Rep.',   p:1, w:1, d:0, l:0, gd:'+1', pts:3 },
    { iso: 'cz', name: 'Czechia',      p:1, w:0, d:0, l:1, gd:'-1', pts:0 },
    { iso: 'za', name: 'South Africa', p:1, w:0, d:0, l:1, gd:'-2', pts:0 },
  ],
  B: [
    { iso: 'ca', name: 'Canada',       p:1, w:0, d:1, l:0, gd:'0',  pts:1 },
    { iso: 'ba', name: 'Bosnia',       p:1, w:0, d:1, l:0, gd:'0',  pts:1 },
    { iso: 'ch', name: 'Switzerland',  p:0, w:0, d:0, l:0, gd:'–',  pts:0 },
    { iso: 'qa', name: 'Qatar',        p:0, w:0, d:0, l:0, gd:'–',  pts:0 },
  ],
  C: [
    { iso: 'br', name: 'Brazil',   p:0, w:0, d:0, l:0, gd:'–', pts:0 },
    { iso: 'ma', name: 'Morocco',  p:0, w:0, d:0, l:0, gd:'–', pts:0 },
    { iso: 'ht', name: 'Haiti',    p:0, w:0, d:0, l:0, gd:'–', pts:0 },
    { iso: 'gb-sct', name: 'Scotland', p:0, w:0, d:0, l:0, gd:'–', pts:0 },
  ],
  D: [
    { iso: 'us', name: 'USA',       p:1, w:1, d:0, l:0, gd:'+3', pts:3 },
    { iso: 'py', name: 'Paraguay',  p:1, w:0, d:0, l:1, gd:'-3', pts:0 },
    { iso: 'au', name: 'Australia', p:0, w:0, d:0, l:0, gd:'–',  pts:0 },
    { iso: 'tr', name: 'Türkiye',   p:0, w:0, d:0, l:0, gd:'–',  pts:0 },
  ],
}
```

### Today's Schedule
```ts
export const SCHEDULE = [
  { home:'Mexico',      hs:2, away:'South Africa', as:0, group:'A', status:'FT' },
  { home:'South Korea', hs:2, away:'Czechia',      as:1, group:'A', status:'FT' },
  { home:'Canada',      hs:1, away:'Bosnia',       as:1, group:'B', status:'FT' },
  { home:'USA',         hs:4, away:'Paraguay',     as:1, group:'D', status:'FT' },
  { home:'Qatar',       hs:null, away:'Switzerland', as:null, group:'B', status:'LIVE', time:'67\'' },
  { home:'Germany',     hs:null, away:'Curaçao',    as:null, group:'E', status:'3PM PT' },
  { home:'Brazil',      hs:null, away:'Morocco',    as:null, group:'C', status:'6PM PT' },
  { home:'Haiti',       hs:null, away:'Scotland',   as:null, group:'C', status:'9PM PT' },
]
```

### Fantasy Picks
```ts
export const FANTASY_PICKS = [
  { rank:1, name:'K. Mbappé',   iso:'fr', pos:'FWD', match:'FRA vs SEN', projPts:18.4, own:34.2, trend:'up',   picked:false },
  { rank:2, name:'Vinicius Jr', iso:'br', pos:'FWD', match:'BRA vs MAR', projPts:16.8, own:28.7, trend:'up',   picked:false, today:true },
  { rank:3, name:'E. Haaland',  iso:'no', pos:'FWD', match:'NOR vs IRQ', projPts:15.2, own:19.4, trend:'flat', picked:false },
  { rank:4, name:'B. Fernandes',iso:'pt', pos:'MID', match:'POR vs DRC', projPts:14.1, own:15.8, trend:'up',   picked:false },
  { rank:5, name:'Pedri',       iso:'es', pos:'MID', match:'ESP vs CPV', projPts:13.7, own:22.3, trend:'down', picked:false },
  { rank:6, name:'R. Dias',     iso:'pt', pos:'DEF', match:'POR vs DRC', projPts:10.2, own:8.1,  trend:'up',   picked:false },
  { rank:7, name:'Alisson',     iso:'br', pos:'GK',  match:'BRA vs MAR', projPts:9.8,  own:11.4, trend:'flat', picked:false, today:true },
]
```

### AI Parlay
```ts
export const PARLAY = {
  odds: '+485',
  legs: [
    { bet:'Brazil Win',         match:'BRA vs MAR', odds:'-138', conf:68 },
    { bet:'Germany Over 3.5',   match:'GER vs CUW', odds:'+110', conf:74 },
    { bet:'Spain Win to Nil',   match:'ESP vs CPV', odds:'-110', conf:71 },
  ],
}
```

### Line Movement
```ts
export const LINE_MOVEMENT = [
  { tag:'SHARP',  bet:'Germany -1.5',       match:'GER vs CUW', open:'-155', current:'-185', dir:'up'   },
  { tag:'HOT',    bet:'Brazil Over 2.5',    match:'BRA vs MAR', open:'-108', current:'-130', dir:'up'   },
  { tag:'VALUE',  bet:'Scotland +0.5 AH',   match:'HTI vs SCO', open:'+105', current:'+120', dir:'up'   },
  { tag:'PUBLIC', bet:'France -1.5 AH',     match:'FRA vs URU', open:'-142', current:'-125', dir:'down' },
]
```

### Alerts
```ts
export const ALERTS = [
  { type:'goal',   player:'Balogun',  detail:'Goal — 23\' (USA vs PAR)',    time:'23m ago' },
  { type:'yellow', player:'Mbappé',   detail:'Yellow card — 41\'',          time:'41m ago' },
  { type:'doubt',  player:'Vinicius', detail:'Minor knock — listed doubtful',time:'1h ago'  },
  { type:'fit',    player:'Haaland',  detail:'Confirmed starter vs IRQ',    time:'2h ago'  },
  { type:'goal',   player:'Son',      detail:'Brace vs Czechia (KOR 2-1)',   time:'FT'      },
  { type:'news',   player:'Messi',    detail:'Captain confirmed, full fitness','time':'3h ago' },
]
```

### Stats Strip
```ts
export const STATS = [
  { value: 64,      label: 'Matches',     suffix: '' },
  { value: 1800,    label: 'Players',     suffix: '' },
  { value: 72,      label: 'AI Accuracy', suffix: '%' },
  { value: 50000,   label: 'Sims Run',    suffix: '' },
  { value: 1000000, label: 'Users',       suffix: '+' },
  { value: 24,      label: 'Coverage',    suffix: '/7' },
]
```

---

## FEATURED MATCH CARD — complete spec

Dark gradient header: `background: linear-gradient(135deg, #091424 0%, #0D2248 50%, #102E60 100%)`

**Header section:**
- Group badge (e.g. "GROUP E") + LIVE pill: red bg `#DC2626`, pulsing white dot (CSS `@keyframes pulse`), minute counter (`67'`)
- Match time text

**Teams section (same gradient bg):**
- 3-column grid: `1fr 140px 1fr`
- Each team: 54px flag emoji, team name (Barlow Condensed 900 22px uppercase), 5-dot form row (W=`#00963F` / D=`#6B7280` / L=`#DC2626`, 20×20px dots)
- Center col: "vs" label, score `1–0` (Barlow 900 60px white), live minute `67'` in red

**Live Odds Strip:** `background: rgba(255,255,255,0.04)`, 4 columns:
- France Win / Draw / Uruguay Win / O/U 2.5
- Favorite odds in `#86efac`, underdog in white
- Movement arrows: ▲ green / ▼ red
- Book name below in muted text

**AI Probability Bar:** white surface card
- Segmented bar: blue home % + grey draw % + red away %
- Widths animate `0% → final` on load: `transition: width 1.4s cubic-bezier(0.4,0,0.2,1)`
- Use Framer Motion `motion.div` with `initial={{ width: 0 }}` and `animate={{ width: '72%' }}` etc.
- Labels: large % + team name below each segment

**Key Stats row:** 4 columns, Barlow 900 22px
- H2H: `3W–2D–1L` / xG Home: `1.8` / xG Away: `0.4` / AI Confidence: `81%`

**CTA row:** Gold primary button "Bet France -185" + ghost secondary "Full Preview" + right-aligned "Must be 21+. T&Cs apply."

---

## INTERACTIONS

### Theme Toggle (ThemeProvider.tsx)
```ts
// On mount: read localStorage 'pitchiq-theme', apply data-theme to <html>
// On toggle:
//   1. Add class 'theme-switching' to <html>
//   2. Flip data-theme between 'dark' / 'light'
//   3. Write to localStorage
//   4. Remove 'theme-switching' after 400ms
// CSS [data-theme="dark"] controls sun/moon icon visibility — no JS class swap needed
```

### Live Match Simulation (useLiveMatch hook)
```ts
// useInterval at 1500ms = 1 game minute, starting at minute 67
// Timeline:
//   minute 73: homeScore+1, flash score (scale+green 700ms), update probs → 80/13/7, toast("⚽ GOAL — Mbappé 73'")
//   minute 84: toast("🟨 Yellow Card — Valverde 84'")
//   minute 90: toast("⏱ Injury Time: +4 minutes")
//   minute 94: match ends → status='FT', LIVE pill → static white pill, dot stops
// All instances update: hero score, side fixtures widget, ticker
```

### Odds Drift
```ts
// On goal at 73': recalculate France odds to reflect 80% win probability
// Every 20s: random ±5–10pt drift on each odds value
// Flash animation on changed value: scale(1.05) → scale(1), background flash, 0.55s
```

### Scroll Reveal
```ts
// Use Framer Motion's useInView or IntersectionObserver at 8% threshold
// Each section: opacity 0→1 + translateY(20px→0), 550ms ease-out
// Stagger children by 60ms per item in grids/tables
```

### Count-up Stats
```ts
// Trigger on scroll into view
// Animate 0 → final value, 1400ms cubic-bezier(0.25,0,0.1,1)
// Use requestAnimationFrame loop inside useEffect
```

### Fantasy Picks Filter
```ts
// Position pills: All / FWD / MID / DEF / GK
// Filter FANTASY_PICKS by pos field on click
// Active pill: gold bg, white text
```

### Pick System
```ts
// "＋ Pick" button: on click → green "✓ Picked", green left border on row
// Toggle-able (click again to unpick)
// On pick: showToast(`${player.name} added to your picks`)
// State: local useState in FantasyPicks component — no persistence needed
```

### Toast (Toast.tsx)
```ts
// Global singleton, renders fixed bottom-center
// showToast(msg: string) — auto-dismiss after 2800ms
// Replaces in-flight toast (reset timer)
// Pill style: navy bg, white text, subtle shadow, slide-up entrance
```

### Cricket Modal (CricketModal.tsx)
```ts
// Triggered by Sport Switcher "Cricket" tab click
// Bottom-sheet: slides up from bottom, backdrop blur overlay
// Contains: "Cricket — Coming Q4 2026" headline + email capture form
// Close: click backdrop or ✕ button
// Body scroll locked while open
```

### Newsletter
```ts
// Email validation: must contain '@' and '.'
// On valid submit: button text → "✓ You're in!", green bg, reset after 3500ms
// On invalid: red border on input for 1200ms
// No API call needed — demo mode only
```

---

## VISUAL DETAILS

```
Border radius sm: 6px  (rounded)
Border radius lg: 12px (rounded-xl)

Shadows (light mode):
  default: 0 1px 3px rgba(15,10,5,0.05), 0 4px 14px rgba(15,10,5,0.04)
  hover:   0 6px 20px rgba(15,10,5,0.11), 0 16px 40px rgba(15,10,5,0.07)

Card hover: translateY(-1px) + elevated shadow

Gold = primary action color (CTAs, active states, highlights)
Green = AI picks, positive movement, success states
Red = live/alerts/loss
Blue = defensive position accent

Position pill colors:
  GK  → gold  #D97706
  DEF → blue  #2563EB
  MID → green #00963F
  FWD → red   #DC2626

Sticky z-index layering:
  Ticker: z-[200]
  Navbar: z-[190]
  Sport Switcher: z-[185]

font-variant-numeric: tabular-nums  ← on all scores, odds, stats
text-wrap: pretty  ← on all headlines
```

---

## RESPONSIVE BREAKPOINTS

| Breakpoint | Changes |
|---|---|
| ≤1100px | Betting grid 2-col; news grid 2-col; line movement 2-col |
| ≤900px | Hero single-col; side widgets row; standings single-col; news+alerts single-col |
| ≤640px | Mobile bottom nav appears; desktop nav links hidden; promo bar 2 books only; groups grid 1-col |

---

## GA4 + ANALYTICS — app/layout.tsx

```tsx
import Script from 'next/script'
import { Analytics } from '@vercel/analytics/react'

// In <head>:
<Script
  src="https://www.googletagmanager.com/gtag/js?id=G-N9PX9ZKHLR"
  strategy="afterInteractive"
/>
<Script id="ga4-init" strategy="afterInteractive">{`
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-N9PX9ZKHLR');
`}</Script>

// In <body> (end):
<Analytics />
```

---

## AFFILIATE LINKS

All sportsbook links use `href="#"` for now. Structure:
```tsx
<a
  href="#"
  rel="noopener sponsored"
  data-aff="draftkings"
  onClick={() => showToast('Redirecting to DraftKings…')}
>
```

When user provides real URLs, replace `href="#"` per book.

---

## DO NOT

- Do not use placeholder lorem ipsum — use exact copy from reference HTML
- Do not add sections not in the reference HTML
- Do not use a UI component library (Chakra, shadcn, Radix UI, etc.) — build from tokens
- Do not use arbitrary Tailwind values where a token exists (`text-[#D97706]` → `text-gold`)
- Do not use `scrollIntoView`
- Do not clear localStorage
- Do not add `console.log` statements
- Do not use `any` type in TypeScript

---

## VERIFICATION

After building all components, run:

```bash
# TypeScript — zero errors
npx tsc --noEmit

# No lorem ipsum
grep -ri "lorem ipsum" app/ components/ && echo "❌ Lorem found" || echo "✅ Clean"

# No arbitrary color values (spot-check)
grep -c "text-\[#" components/ -r

# All sections present
grep -l "DisclaimerBar\|LiveTicker\|Navbar\|SportSwitcher\|HeroGrid\|StatsStrip\|GroupStandings\|FantasyPicks\|AIParlayCard\|BettingIntelligence\|LineMovementFeed\|NewsAndAlerts\|NewsletterStrip\|Footer\|MobileBottomNav" app/page.tsx

# Dev server clean start
npm run dev
```

---

## DONE — Report this when complete:

```
=== PITCHIQ NEXT.JS BUILD COMPLETE ===
TypeScript errors: [0 / N]
Components built: [N/18]
Live simulation: [working / error]
Theme toggle: [working / error]
Scroll reveal: [working / error]
Fantasy filters: [working / error]
Toast system: [working / error]
Responsive: [verified / issues]
GA4 wired: [Y/N]
Dev server: [clean / errors]
```
