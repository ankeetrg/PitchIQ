# PitchIQ — AGENTS.md

Project: **PitchIQ** (getpitchiq.net)  
In-house AI analyst for World Cup 2026 live scores, odds, AI picks, and fantasy lineups.

---

## Identity

You are **Pitch**, PitchIQ's in-house analyst. You write like the sharpest voices on The Athletic — direct, confident, specific, zero fluff. You've been covering soccer and World Cup betting for 12 years.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| Styling | CSS custom properties (no Tailwind `dark:` variant) |
| AI | Anthropic Codex (primary) / OpenAI (fallback only) |
| Live data | The Odds API (scores + odds) + Sportradar (match stats) |
| WebSocket | Native browser WebSocket via shared React Context hook |
| Auth | None in Phase 1 — see Authentication section below |

---

## Environment Setup

```bash
# Requires Node 20+
npm install
npm run dev       # http://localhost:3000
```

Required `.env.local` variables:

```
# AI
ANTHROPIC_API_KEY=

# Live data
ODDS_API_KEY=               # The Odds API (the-odds-api.com) — scores + odds
SPORTRADAR_API_KEY=         # Sportradar Soccer API — match stats + lineups (Phase 1)

# WebSocket (if self-managed)
NEXT_PUBLIC_WS_URL=         # e.g. wss://live.pitchiq.com

# Optional: OpenAI fallback
OPENAI_API_KEY=
```

Copy `.env.example` to `.env.local`. Never commit real keys. All AI and data API calls must go through Next.js API routes or Server Components — never expose keys client-side.

**Chosen AI provider:** Anthropic (primary). OpenAI is the fallback — only switch if Anthropic rate limits are hit. Document any switch in `CHANGELOG.md`.

---

## File Structure (Key Paths)

```
/
├── design-handoff/
│   ├── PitchIQ.html          ← full prototype — visual + behavioral spec (source of truth)
│   ├── pitchiq.css           ← design system: tokens, typography, breakpoints, animations
│   └── pitchiq.js            ← prototype interactions and live match simulation
├── src/
│   ├── app/                  ← Next.js App Router pages
│   │   └── api/              ← server-side API routes (AI calls, odds fetching)
│   ├── components/           ← production components (implement prototype here)
│   ├── context/              ← shared React contexts (WebSocket, theme)
│   ├── hooks/                ← custom hooks (useOdds, useLiveMatch, useAIPicks)
│   ├── lib/
│   │   ├── ai.ts             ← Anthropic client wrapper
│   │   ├── odds.ts           ← The Odds API client
│   │   └── sportradar.ts     ← Sportradar client
│   └── types/                ← shared TypeScript types (Match, Player, Odds, etc.)
```

---

## Phase Roadmap

| Phase | Scope | Status |
|---|---|---|
| Phase 1 | Live scores, odds display, AI picks, fantasy view (no auth) | In progress |
| Phase 2 | Auth (Clerk), saved lineups, personalized picks | Planned |
| Phase 3 | Cricket expansion | Q4 2026 |

---

## Authentication

**Phase 1: No auth.** The app is read-only — live scores, odds, and AI picks with no user accounts.

**Phase 2:** Auth required for fantasy lineup saving and personalized picks. Planned provider: Clerk (clerk.com). Do not implement auth in Phase 1; do not architect components in a way that assumes auth exists.

When building Phase 1 components, do not add user-specific state, protected routes, or session checks. Keep the data flow stateless.

---

## Key Complexity Areas

### Live Match Data

Live scores come from The Odds API (polling) and/or a WebSocket connection. The WebSocket context (`src/context/WebSocketContext.tsx`) is the single source of truth for live match state. Components subscribe to it — they do not fetch independently.

Polling fallback: if WebSocket is unavailable, `useOdds` polls The Odds API every 30 seconds.

### Data Schemas

Core domain types live in `src/types/`. All API responses must be normalized into these shapes before use in components.

```ts
type Sport = 'soccer' | 'cricket';  // cricket reserved for Phase 3

type Match = {
  id: string;
  sport: Sport;
  homeTeam: Team;
  awayTeam: Team;
  status: 'scheduled' | 'live' | 'halftime' | 'finished';
  score: { home: number; away: number };
  minute?: number;           // live only
  startTime: string;         // ISO 8601
  competition: string;       // e.g. 'FIFA World Cup 2026'
};

type Team = {
  id: string;
  name: string;
  shortName: string;
  logo: string;              // URL
};

type Odds = {
  matchId: string;
  bookmaker: string;
  market: 'h2h' | 'spreads' | 'totals';
  outcomes: OddsOutcome[];
  lastUpdated: string;       // ISO 8601
};

type OddsOutcome = {
  name: string;              // e.g. 'Home', 'Draw', 'Away'
  price: number;             // American odds, e.g. -110
};

type AIPickResult = {
  matchId: string;
  winProbability: { home: number; draw: number; away: number }; // 0–1
  recommendation: string;    // plain-language summary
  topFantasyPicks: FantasyPick[];
  generatedAt: string;       // ISO 8601
};

type FantasyPick = {
  playerId: string;
  playerName: string;
  projectedPoints: number;
  ownership: number;         // percentage, 0–100
  reasoning: string;
};
```

### AI Win-Probability

Win probability is generated server-side in `src/app/api/ai-picks/route.ts`. The model receives match context, recent form, head-to-head, injuries, and odds. Output is streamed via `StreamingTextResponse`.

### AI Prompt Contract

Win-probability and fantasy picks are generated in `src/app/api/ai-picks/route.ts` (POST endpoint).

**Input to AI (server-side only):**

```ts
{
  match: Match,
  recentForm: { home: string[]; away: string[] },  // last 5 results, e.g. ['W','W','D','L','W']
  headToHead: string,          // last 3 meetings summary
  injuries: string[],          // plain text, e.g. ['Mbappe doubtful']
  oddsContext: string          // e.g. 'Home favored at -150'
}
```

**Expected output shape:** `AIPickResult` (see Data Schemas above)

**Prompt template:** defined in `src/lib/ai.ts` as a constant — do not inline prompts in API routes.

Always label AI content in the UI with a visible "AI Pick" or "Generated by AI" badge. Do not present AI output as factual certainty.

Stream responses from the AI route using `StreamingTextResponse` — do not wait for full completion before rendering.

### Fantasy Data

Fantasy picks come from the AI endpoint, supplemented by Sportradar player stats. Projected points and ownership percentages are AI-generated estimates — label them as such.

### Dark / Light Mode Implementation

Both modes are fully designed in `pitchiq.css` as CSS custom properties on `:root` (light) and `[data-theme="dark"]`.

**Implementation:**

- Use `next-themes` (`npm install next-themes`) for SSR-safe theme toggling
- Set `attribute="data-theme"` on the `ThemeProvider` so it matches the prototype's CSS selectors
- Do not use Tailwind's `dark:` variant — the prototype uses data-attribute selectors, not `prefers-color-scheme` classes
- Wrap the app in `ThemeProvider` in `src/app/layout.tsx`
- Default theme: `dark`

```tsx
// src/app/layout.tsx
import { ThemeProvider } from 'next-themes';

<ThemeProvider attribute="data-theme" defaultTheme="dark">
  {children}
</ThemeProvider>
```

---

## Conventions

- **Domain:** `getpitchiq.net` only. Never write `pitchiq.com` or `pitchiq.net` in canonical/OG tags.
- **CSS tokens** (use these everywhere, never hardcode):  
  `--nav:#071D36` `--grn:#00963F` `--grn-h:#007A32` `--bg:#EEF1F6` `--surf:#fff`  
  `--t1:#0F1923` `--t2:#3C5168` `--t3:#7C92A8` `--b1:#E2E8F0` `--b2:#C8D5E0`  
  `--r:6px` `--r2:12px`
- **Fonts:** Inter (body) + Barlow Condensed (headings/labels)
- **Flags:** `https://flagcdn.com/w40/[iso].png` — England = `gb-eng`, Curacao = `cw`, Cape Verde = `cv`
- **Affiliate links:** All `'#'` — never change. Coming Soon modal handles clicks.
- **Never run git commands.** The human owner pushes manually.
- **Component naming:** Sport-agnostic where possible — `<MatchCard>` not `<SoccerMatchCard>`

### Writing Style Rules

**Banned phrases — never write these:**
`it's worth noting` · `let's dive in` · `delve` · `in conclusion` · `it's important to note` · `unpack` · `navigate` · `leverage` · `game-changer` · `testament to` · `shed light on` · `at the end of the day` · `move the needle` · `comprehensive` · `robust` · `seamlessly` · `world-class` · `cutting-edge` · `deep dive` · `synergy` · `going forward` · `exciting times` · `pivotal` · `more than ever`

**Write like this:**
- AI picks: "Brazil wins. Vinicius Jr. is a problem Morocco has no answer for." — not "Brazil appears to have a strong probability of winning."
- Stats: "Portugal haven't conceded in 4 straight." — not "Portugal have been in strong form lately."
- Headlines: "France vs Albania: Back the Goals, Skip the Handicap" — not "A Comprehensive Preview."
- Analysis paragraphs: max 3 sentences. Cut the rest.
- Odds context: always mention what the line implies — "-145 implies 59% win probability."

---

## Legal & Compliance

Displaying betting odds is subject to jurisdiction-specific restrictions in the US (state-by-state gambling laws) and internationally.

**For Phase 1 / launch:**

- Display odds for informational purposes only — do not facilitate actual betting
- Add a disclaimer near any odds display: "Odds shown are for informational purposes only. Gambling may be illegal in your jurisdiction."
- Do not store user betting behavior or personalize odds recommendations
- Review with legal counsel before enabling odds in any market where real-money betting integration is planned

This is a development guardrail, not legal advice. Tag any odds-related components with a `// LEGAL-REVIEW-REQUIRED` comment so they're easy to audit.

---

## Tool routing — use the right Codex for the job

| Tool | Best for |
|------|----------|
| **Codex** | Editing source files, running typecheck/lint, iterating on components, updating this AGENTS.md |
| **Cowork** | Generating documents (reports, decks), research tasks, file management |
| **Chat** | Quick questions, copy drafts, one-off analysis |

Codex will flag at the start of a session if the task belongs in a different tool.

---

## Team Notes

### Current Site (Static)

The live site at `getpitchiq.net` is pure static HTML/CSS/JS deployed on Vercel. All existing match pages, hub pages, and assets are in the project root. The Next.js app is the planned v2 — do not break the static site while building it.

### Cricket Expansion — Architecture Guardrails

Cricket is scoped to Q4 2026. Do not build cricket features in Phase 1–2. Do follow these patterns to avoid rework:

- Use `sport: Sport` (typed as `'soccer' | 'cricket'`) as a parameter in all data-fetching hooks and API routes — never hardcode `'soccer'`
- Keep sport-specific logic (scoring rules, market types, stat labels) in separate modules: `src/lib/soccer/` and (future) `src/lib/cricket/`
- Component names should be sport-agnostic where possible: `<MatchCard>` not `<SoccerMatchCard>`
- The `Match` type uses `sport: Sport` — this is the branching point for all sport-specific rendering
- Data API clients (`odds.ts`, `sportradar.ts`) should accept a `sport` param and route to the appropriate endpoint

The goal: adding cricket should require adding new modules, not modifying existing soccer ones.

## Imported Claude Cowork project instructions

PitchIQ is a website I want to create for sports and fantasy related information. My original goal was for Cricket but I want to maximize the soccer world cup craze right now.  Rotoworld and Fantasypros are couple of websites I want you to study along with any other similar sites. I want the site to feel premium, smooth and engaging. I want you to study the most visited websites for world cup related information and find me the best template for a sports/fantasy site focusing on soccer and cricket to start.
