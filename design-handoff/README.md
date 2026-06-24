# Handoff: PitchIQ — World Cup 2026 Intelligence Platform

## Overview
PitchIQ is an AI-powered soccer fantasy and sports betting intelligence platform, launching for World Cup 2026. This handoff covers the **homepage / dashboard** — the primary landing surface for all users. It is designed to attract new users while giving returning users immediate value (live scores, AI picks, betting intel, fantasy rankings).

The platform is planned to expand to detail pages (match page, player page, betting markets page) in a future phase.

---

## About the Design Files
The files in this bundle — `PitchIQ.html`, `pitchiq.css`, `pitchiq.js` — are **high-fidelity design references built in plain HTML/CSS/JS**. They are prototypes showing the intended look, feel, and interactive behavior of the product. They are **not production code to ship directly**.

Your task is to **recreate these designs in your chosen production stack** (React, Next.js, etc.) using its established patterns, component libraries, and data layer. Use these files as the visual and behavioral specification.

---

## Fidelity
**High-fidelity.** Colors, typography, spacing, shadows, animations, and interactions are all final. Recreate pixel-perfectly. Every CSS variable value in `pitchiq.css` is a finalized design token — use them directly or map them into your design system.

---

## Design System Tokens

### Fonts
```
Body:      Inter (Google Fonts) — 400, 500, 600, 700
Display:   Barlow Condensed (Google Fonts) — 400, 600, 700, 800, 900
Fallbacks: system-ui, sans-serif / Arial Narrow, sans-serif
```
Barlow Condensed is used for ALL headings, labels, stats, scores, badges, nav, and UI chrome. Inter is used for body copy and table cells only.

### Color Palette — Light Mode
```
Background page:    #F8F5EF  (warm off-white)
Background 2:       #F1EBE2  (slightly darker warm)
Surface (cards):    #FFFFFF
Nav background:     #091525  (deep navy)
Nav 2 (sub-nav):    #0C1C2E

Green (positive):   #00963F
Green hover:        #007B33
Green dim bg:       rgba(0,150,63,0.10)
Green dim border:   rgba(0,150,63,0.22)

Gold (primary CTA): #D97706
Gold hover:         #B45309
Gold dim bg:        rgba(217,119,6,0.10)
Gold dim border:    rgba(217,119,6,0.24)

Blue (prob/DEF):    #2563EB
Blue dim:           rgba(37,99,235,0.10)

Red (live/FWD):     #DC2626
Red dim:            rgba(220,38,38,0.10)

Text primary:       #0F1923
Text secondary:     #374151
Text tertiary:      #6B7280
Text muted:         #9CA3AF

Border light:       #E5DDD0
Border medium:      #CEC5B5
```

### Color Palette — Dark Mode
Applied via `[data-theme="dark"]` on `<html>`:
```
Background page:    #0B1420
Background 2:       #101C2C
Surface (cards):    #152030
Border light:       rgba(255,255,255,0.07)
Border medium:      rgba(255,255,255,0.13)
Text primary:       #EDF2F7
Text secondary:     #94A3B8
Text tertiary:      #64748B
Text muted:         #475569
```
Nav colors stay the same in both modes (already dark navy).

### Position Colors
```
GK:  Gold  #D97706
DEF: Blue  #2563EB
MID: Green #00963F
FWD: Red   #DC2626
```

### Spacing & Radii
```
Border radius small:  6px
Border radius large:  12px
```

### Shadows
```
Default:  0 1px 3px rgba(15,10,5,0.05), 0 4px 14px rgba(15,10,5,0.04)
Medium:   0 2px 8px rgba(15,10,5,0.07), 0 10px 28px rgba(15,10,5,0.05)
Hover:    0 6px 20px rgba(15,10,5,0.11), 0 16px 40px rgba(15,10,5,0.07)
Dark mode shadows use rgba(0,0,0,...) at higher opacity (0.25–0.55)
```

---

## Screens / Views

### 1. Homepage Dashboard (`PitchIQ.html`)

#### Layout
Max content width: **1360px**, centered, 24px horizontal padding.  
Page has 5 stacked zones:
1. Live Ticker (sticky, 34px, z-index 200)
2. Primary Navbar (sticky below ticker, 58px, z-index 190)
3. Sport Switcher sub-nav (sticky below nav, 38px, z-index 185)
4. Main content (24px top padding, 48px bottom padding)
5. Footer

#### 1a. Live Ticker
- Full-width bar, height 34px, `background: #091525`, sticky top 0
- Left: red "LIVE" badge (red bg, white uppercase label + pulsing white dot)
- Center: horizontally auto-scrolling ticker track (CSS animation, 34s linear infinite, pauses on hover). Items separated by 22px padding + right border. Each item: status pill + team codes + score (bold white) + minute.
  - Status pills: `LIVE` = red bg; `FT` = semi-transparent white; kick-off times = green tint bg
- Right: "WC 2026 · Group Stage" label, muted, uppercase
- Mask-image fade on left and right edges

#### 1b. Primary Navbar
- Background `#091525`, height 58px, sticky top 34px
- Logo: "Pitch**IQ**" — Barlow Condensed 900, 24px, white + gold span
- Nav links: Barlow Condensed 700, 13px, uppercase, 0.07em spacing, 58px height links; active state = white + gold 2px bottom border underline + subtle white bg; hover = white
- Right side: single circular dark/light toggle button (34px, 50% border-radius, white SVG sun icon in light mode, moon icon in dark mode). Subtle white semi-transparent bg, 1px white border.
- Mobile (≤640px): links hidden, hamburger button shown

#### 1c. Sport Switcher
- Background `#0C1C2E`, height 38px, sticky top 92px
- "⚽ Soccer" active tab (gold 2px bottom underline), "🏏 Cricket" tab with "Q4 2026" gold badge
- Right: small muted label about Cricket
- Opens a bottom-sheet modal on Cricket tab click (see Modal section)

#### 1d. Hero Grid
Two-column grid: `1fr 340px`, 20px gap, aligned to top.  
Collapses to single column at 900px.

**Left: Featured Match Card**  
Full card with `border-radius: 12px`, overflow hidden, medium shadow.

- **Header strip** (`background: linear-gradient(135deg, #091424 0%, #0D2248 55%, #102E60 100%)`): match badge (group/stadium, gold venue), live pill (red bg + pulsing dot + minute counter), match date/time
- **Teams section** (same gradient, darker): 3-column grid (`1fr 140px 1fr`). Each team: 54px flag emoji, 22px/900 uppercase team name, 5-dot form indicator (W=green/D=grey/L=red, each 20×20px)
- **Score** (center column): "vs" label muted, large score `font-size: 60px, font-weight: 900` white, minute label in red below
- **Live Odds Strip** (`background: rgba(255,255,255,0.04)`): 4 equal columns — France Win / Draw / Uruguay Win / O/U 2.5. Each: uppercase label, large odds value (favored = `#86efac` green, dog = white), movement arrow (up=green, down=red), book name
- **AI Win Probability** (white surface): heading + "✦ PitchIQ AI" gold badge. Segmented bar: blue (home) + grey (draw) + red (away). Animates from 0% on load. Labels below with large % + team name
- **Key Stats row**: 4 columns — H2H, xG home, xG away, AI Confidence. Values in 22px/900 Barlow Condensed; blue emphasis on notable values
- **CTA row**: gold primary button "Bet at DraftKings −140 →", ghost secondary button "Full Match Analysis", right-aligned muted legal note

**Right: Side Widgets**  
Two stacked cards, `background: var(--surf)`, `border: 1px solid var(--b1)`, 12px radius, light shadow.

- **Today's Fixtures**: list of 6 fixtures. Each row: status pill (LIVE/FT/kick-off time) + match name/sub-text + score or time. Hover = subtle bg tint
- **Best Bets Today**: 4 bet rows. Each: bet name/match sub-text + colored tag (VALUE/HOT/SHARP) + gold odds pill

#### 1e. Stats Strip
Full-width, `background: var(--bg2)`, top/bottom border. 6 items in a flex row, each centered vertically. Gold large number (30px/900 Barlow), uppercase muted label. Numbers animate up from 0 when scrolled into view (count-up, 1400ms ease-out cubic).
```
64           Matches Covered
1,800        Players Ranked
72%          AI Pick Accuracy
50,000       Daily Simulations
1M+          Active Users
24/7         Live Coverage
```

#### 1f. Fantasy Picks Section
Full-width table card.

- **Section header**: gold 4px left-bar accent + "FANTASY PICKS" uppercase title (20px/900 Barlow) + sub-label date. Right: segmented tab switcher (Proj Pts / Ownership / Value) + "View All 250+ →" dark button
- **Toolbar**: position filter pills (All / FWD / MID / DEF / GK) — active state colored by position. Right: muted update timestamp
- **Table columns**: Rank · Player (flag avatar + name/nation) · Pos pill · Match · Proj Pts · Own % (with mini fill bar) · vs Avg trend · + Pick button
- Row hover = very subtle gold tint bg. Picked rows = green left border + green tint bg
- **Footer bar**: pulsing green dot + "Updated every 15 min" note + "View Full Rankings →" button

#### 1g. Betting Intelligence Section
3-column grid of cards (collapses 2-col at 1100px, 1-col at 900px). Each card:
- Header: label + badge (AI PICK / SHARP / TRENDING)
- Body: large bet name (19px/900), match sub-text
- **Card 1 (Best Value)**: sportsbook comparison list (3 books, "BEST" gold tag on top line), meta chips (Value score, hit rate), gold CTA button
- **Card 2 (Sharp Money)**: line movement mini bar chart (6 bars, height-based, red = high sharp action, green = current), opened vs current odds
- **Card 3 (Public vs Sharp)**: over/under split bar (blue = over %, red = under %), ticket % and money % chips, CTA

#### 1h. News & Analysis
4-column grid (collapses to 2 at 1100px, 1 at 640px). Featured card spans 2 columns.
Each card: colored gradient image placeholder (140px height, 210px for featured) with category badge. Body: headline (Barlow Condensed, 3-line clamp), byline + date + read time. Hover = lift + shadow.

Image gradients:
```
France analysis:  linear-gradient(135deg, #002395 → #ED2939)
Brazil:           linear-gradient(135deg, #009C3B → #FFDF00)
Betting:          linear-gradient(135deg, #1D4ED8 → #7C3AED)
Fantasy:          linear-gradient(135deg, #059669 → #0EA5E9)
```

#### 1i. Newsletter Strip
Full-width, `background: #091525`. Two-column flex (copy left, form right). Copy: eyebrow + title + subtitle + 4 checkmark perks. Form: email input + "Subscribe" gold button side by side. Confirmation toast on submit.

#### 1j. Footer
4-column grid: brand column (logo + tagline + social icons) + 3 link columns (World Cup 2026 / Fantasy / Betting). Bottom bar: copyright + legal disclaimer.

#### 1k. Mobile Bottom Nav (≤640px)
Fixed bottom bar, `background: #091525`, 60px height. 5 tabs: Home / Scores / Fantasy / Betting / Account. Active tab = gold. Icons (18px) + labels (9px uppercase).

#### 1l. Cricket Modal (bottom sheet)
Triggered by clicking the Cricket sport tab. Full-screen overlay (dark + blur), bottom sheet slides up. Contains: phase label, IPL/International/AI feature grid, early access email form.

---

## Interactions & Behavior

### Dark / Light Mode Toggle
- Persisted in `localStorage` key `pitchiq-theme`
- Applied as `data-theme="dark"` attribute on `<html>`
- On toggle: add class `theme-switching` to `<html>`, which enables 250ms CSS transitions on background-color, border-color, color, box-shadow for all elements — then remove class after 400ms
- Sun SVG icon shows in light mode, moon SVG in dark mode — controlled purely by CSS `[data-theme="dark"] .icon-sun { display: none }`

### Live Match Simulation
The homepage simulates a live France vs Uruguay match in progress (67'). Tick interval: **1500ms = 1 game minute**.

Scripted events:
- **73'**: Goal → home score increments, score flashes (scale up + green color, 700ms), toast notification, probabilities update to 80/13/7, odds drift
- **84'**: Yellow card toast
- **90'**: Injury time toast  
- **94'**: Full time → live pill changes to static white, dot animation stops, fixture status changes to FT, final toast

Score sync: hero card, side fixture widget, and ticker all update together.

### Odds Drift
- On goal: manual drift applied (France more favored)
- Every 20 seconds: random ±5/10 point drift on all odds. Triggers a scale-up flash animation (0.55s) on changed elements.

### Probability Bar
Animated with CSS `transition: width 1.4s cubic-bezier(0.4,0,0.2,1)`. Triggered 700ms after page load.

### Scroll Reveal
All sections (`.rv`) and stat items animate in: `opacity: 0 → 1`, `translateY(20px → 0)`, 550ms ease-out. Triggered by IntersectionObserver at 8% threshold. Stat numbers count up from 0 when revealed.

### Ownership Bars
IntersectionObserver triggers CSS width transition from 0 to final value when fantasy table enters viewport.

### Fantasy Position Filter
Clicking a position pill (FWD/MID/DEF/GK) filters table rows by matching `.pos-pill` text. "All" shows all rows.

### Pick System
"+ Pick" button toggles gold → green, updates text to "✓ Picked", adds green left-border to row, fires toast notification.

### Newsletter Submit
Email validation (must contain `@`). On success: button turns green "✓ You're in!", input clears, toast fires. Resets after 3.5s. On failure: input border turns red briefly.

### Toast System
Global `showToast(msg)` function. Bottom-centered fixed pill (above mobile nav). Auto-dismisses after 2800ms. Replaces any in-flight toast.

---

## State Management Needed
```
pitchiq-theme         localStorage — "light" | "dark"
liveMatchMinute       In-memory — current match minute (starts at 67)
homeGoals / awayGoals In-memory — goal counts
oddsState             In-memory — { fra, draw, uru, ou } current odds values
pickedPlayers         In-memory (or localStorage) — Set of picked player names
activePositionFilter  In-memory — current position filter tab
activeFantasyTab      In-memory — Proj Pts / Ownership / Value
cricketModalOpen      In-memory — boolean
```

In production, the live match state and odds would come from a WebSocket or polling API.

---

## Future Detail Pages (Phase 2)
The following pages are planned and will be designed next:
- **Match Detail Page** — full timeline, lineups, advanced stats, all markets
- **Player Profile Page** — career stats, form chart, fantasy history, ownership trends
- **Fantasy Rankings Page** — full sortable table, filters, lineup builder
- **Betting Markets Page** — full odds comparison across books, line movement history

---

## Assets
- **Fonts**: Google Fonts — Inter + Barlow Condensed. Load via `<link>` in `<head>`.
- **Icons**: Theme toggle uses inline SVG (sun/moon paths, standard Feather icon shapes — no external dependency)
- **Images**: All "images" in this prototype are emoji flags + colored CSS gradient placeholders. Replace with real photography/team assets in production.
- **No icon library required** — all status badges, tabs, and indicators are pure CSS + text

---

## Files in This Bundle
```
PitchIQ.html    — Complete homepage markup (single file, fully annotated)
pitchiq.css     — Full design system: tokens, components, layout, responsive, animations
pitchiq.js      — Live simulation, theme toggle, scroll reveal, all interactions
README.md       — This document
```

---

## Responsive Breakpoints
```
≤1100px: Hero side col narrows to 300px; betting grid 2-col; news grid 2-col
≤900px:  Hero goes single column; side widgets go horizontal row; betting 1-col; footer 2-col
≤640px:  Mobile bottom nav appears; desktop nav links hidden; news 1-col; footer 1-col;
         fantasy table hides ownership% and vs avg columns
```

---

## Notes for the Developer
1. **Sticky layering**: Ticker (z:200) → Navbar (z:190) → Sport Switcher (z:185). Navbar is `top: 34px` (ticker height), sport switcher is `top: 92px` (ticker + navbar).
2. **Body bottom padding**: `60px` to clear the mobile bottom nav on small screens.
3. **`font-variant-numeric: tabular-nums`** is applied to all scores, odds, and stats to prevent layout shift as numbers update.
4. **The `theme-switching` class** on `<html>` is the key to smooth transitions — it must be removed after 400ms or transitions will affect page-load.
5. **Ticker loop**: The ticker items are duplicated in the DOM to create a seamless loop. `translateX(-50%)` brings it back to start.
6. **All card hover states** use `transform: translateY(-1px)` or `translateY(-2px)` + elevated shadow — keep this consistent.
7. **Gold is the primary action color** — all primary CTAs, active states, and highlights use `#D97706`.
