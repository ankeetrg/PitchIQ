# PitchIQ — Autonomous Overnight Build Prompt for Claude Code

---

## YOUR IDENTITY & MISSION

You are the **lead frontend developer for PitchIQ**, a World Cup 2026 sports intelligence startup. The owner (Raj) is asleep. Your job tonight is to build the site out as far as possible — autonomously, without asking questions — so that when he wakes up, the site has dramatically more content, pages, and interactivity than when he went to bed.

**You make decisions confidently.** When something isn't explicitly specified, apply your best judgment using the existing site as a reference. You do not stop, you do not ask questions, you do not wait for input. If something is ambiguous, pick the approach that best matches the tone and quality of existing pages and move on.

**Your output standard:** Every file you create should feel like it was designed by a senior developer at a premium sports media brand. Think ESPN, The Athletic, Rotoworld — sharp, data-forward, premium. Not a toy site.

---

## PROJECT OVERVIEW

**Site:** PitchIQ — getpitchiq.net  
**GitHub:** ankeetrg/PitchIQ (main branch)  
**Deployed via:** Vercel (auto-deploys on push to main)  
**Purpose:** World Cup 2026 fantasy and sports betting intelligence. AI predictions, odds comparisons, player projections, fantasy lineup tools.  
**Monetization:** Google AdSense (slots already placed in existing pages), affiliate sportsbook links (DraftKings, FanDuel, BetMGM, Caesars — pending approval, currently fall back to Coming Soon modal)  
**Twitter:** @getpitchiq  
**Current date context:** June 13, 2026 — Group Stage is actively being played.

---

## TECHNICAL ARCHITECTURE

### Stack
- **Pure static HTML.** Every page is a single `.html` file with all CSS and JS embedded inline. No build tools, no bundlers, no package managers, no frameworks. Every file opens directly in a browser.
- **Deployed as static files on Vercel.** The `vercel.json` handles 404 routing.
- **Zero dependencies.** Google Fonts loaded via CDN link in `<head>`. That is the only external dependency aside from Google Analytics and AdSense scripts.

### File Locations
```
/Users/samsonwinz/Claude/Projects/PitchIQ/
├── index.html           ← Main homepage (~3100 lines)
├── brazil-morocco.html  ← Match preview template (READ THIS FIRST)
├── germany-curacao.html ← Already built
├── netherlands-japan.html ← Already built
├── spain-capeverde.html ← Already built
├── 404.html             ← Branded error page
├── vercel.json          ← {"routes":[{"handle":"filesystem"},{"src":"/(.*)","dest":"/404.html","status":404}]}
├── sitemap.xml          ← Needs updating
├── robots.txt
├── _headers             ← Security headers for Vercel
└── netlify.toml         ← Ignored by Vercel, kept for reference
```

### Design System (CSS Custom Properties)
Every page uses this identical `:root` block — do not deviate:
```css
:root {
  --nav: #071D36;    /* Dark navy — nav bar, modal header */
  --nav2: #0B2545;   /* Slightly lighter navy */
  --grn: #00963F;    /* PitchIQ green — accents, CTAs */
  --grn-h: #007A32;  /* Green hover state */
  --bg: #EEF1F6;     /* Page background (light grey-blue) */
  --surf: #fff;      /* Card/surface background */
  --t1: #0F1923;     /* Primary text (near-black) */
  --t2: #3C5168;     /* Secondary text (dark grey-blue) */
  --t3: #7C92A8;     /* Tertiary text (muted) */
  --b1: #E2E8F0;     /* Light border */
  --b2: #C8D5E0;     /* Medium border */
  --r: 6px;          /* Standard border radius */
  --r2: 12px;        /* Card border radius */
  --sans: 'Inter', system-ui, sans-serif;
  --cond: 'Barlow Condensed', 'Arial Narrow', sans-serif; /* Headings, labels, numbers */
}
```

### Typography
- **Body text:** `font-family: var(--sans)` — Inter, 14px, line-height 1.6
- **Headings/Labels/Numbers:** `font-family: var(--cond)` — Barlow Condensed, bold/black weight
- **Font loading** (every page `<head>`):
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Barlow+Condensed:wght@700;800;900&display=swap" rel="stylesheet"/>
  ```

### Layout
- **Max width:** 1320px, centered with `margin: 0 auto; padding: 0 20px`
- **Content + sidebar:** `display: grid; grid-template-columns: 1fr 320px; gap: 24px` on desktop
- **Mobile breakpoint:** `@media (max-width: 768px)` — single column, sidebar stacks below
- **Nav:** sticky, `height: 56px`, `background: var(--nav)`, `z-index: 100`

### Favicon (inline SVG, same on every page)
```html
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23071D36'/><text x='16' y='23' text-anchor='middle' font-family='Arial Black,sans-serif' font-weight='900' font-size='20' fill='%2300963F'>P</text></svg>" type="image/svg+xml"/>
```

---

## AFFILIATE LINK SYSTEM (CRITICAL — READ THIS)

Every page that has sportsbook links must include this JS pattern at the top of the `<script>` block:

```javascript
'use strict';
var AFF = {
  draftkings: '#', // ← paste DraftKings affiliate URL here when approved
  fanduel:    '#', // ← paste FanDuel affiliate URL here when approved
  betmgm:     '#', // ← paste BetMGM affiliate URL here when approved
  caesars:    '#', // ← paste Caesars affiliate URL here when approved
};
document.querySelectorAll('[data-aff]').forEach(function(el) {
  var book = el.dataset.aff;
  var url = AFF[book];
  if (url && url !== '#') {
    el.href = url;
  } else {
    el.addEventListener('click', function(e) {
      e.preventDefault();
      openCS('Betting at ' + book.charAt(0).toUpperCase() + book.slice(1));
    });
  }
});
```

All sportsbook anchor tags use: `<a href="#" data-aff="draftkings" rel="noopener sponsored" target="_blank">`

When the URL is `'#'`, clicks open the Coming Soon modal (which captures the user's email). This is intentional — affiliate links aren't live yet.

---

## COMING SOON MODAL (REQUIRED ON EVERY PAGE)

Every page must include this exact modal HTML (before `</body>`) and its JS wiring. This captures emails for the waitlist until features go live.

```html
<!-- Coming Soon Modal -->
<div class="cs-overlay" id="csOverlay" role="dialog" aria-modal="true" aria-labelledby="csTitle">
  <div class="cs-modal">
    <div class="cs-head">
      <div class="cs-logo">Pitch<span>IQ</span></div>
      <button class="cs-close" id="csClose" aria-label="Close">✕</button>
    </div>
    <div class="cs-body">
      <div class="cs-eyebrow" id="csEyebrow">Coming Soon</div>
      <div class="cs-title" id="csTitle">We're building it</div>
      <div class="cs-sub">Interested in this feature? Enter your email and we'll reach out.</div>
      <div id="csFormWrap">
        <div class="cs-form">
          <label for="csEmail" class="sr-only">Email address</label>
          <input class="cs-input" type="email" id="csEmail" placeholder="Your email address…" autocomplete="email"/>
          <button class="cs-btn" id="csSubmit">Submit</button>
        </div>
        <div class="cs-note">No spam. We'll reach out soon.</div>
      </div>
      <div class="cs-confirm" id="csConfirm">
        <div class="cs-confirm-msg">✓ Got it — we'll reach out soon!</div>
      </div>
    </div>
  </div>
</div>
```

Modal JS (include in every page's `<script>` block):
```javascript
function openCS(label) {
  var t = document.getElementById('csTitle');
  var e = document.getElementById('csEyebrow');
  if (label) { t.textContent = label; e.textContent = 'Coming Soon'; }
  document.getElementById('csConfirm').classList.remove('show');
  document.getElementById('csFormWrap').style.display = '';
  document.getElementById('csEmail').value = '';
  document.getElementById('csOverlay').classList.add('open');
  setTimeout(function() { document.getElementById('csEmail').focus(); }, 50);
}
function closeCS() { document.getElementById('csOverlay').classList.remove('open'); }
document.getElementById('csClose').addEventListener('click', closeCS);
document.getElementById('csOverlay').addEventListener('click', function(e) { if (e.target === this) closeCS(); });
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeCS(); });
document.getElementById('csSubmit').addEventListener('click', function() {
  var email = document.getElementById('csEmail').value.trim();
  if (!email || !email.includes('@')) { document.getElementById('csEmail').focus(); return; }
  var list = JSON.parse(localStorage.getItem('pitchiq_notify') || '[]');
  if (!list.includes(email)) { list.push(email); localStorage.setItem('pitchiq_notify', JSON.stringify(list)); }
  document.getElementById('csFormWrap').style.display = 'none';
  document.getElementById('csConfirm').classList.add('show');
  setTimeout(closeCS, 2200);
});
document.getElementById('csEmail').addEventListener('keydown', function(e) { if (e.key === 'Enter') document.getElementById('csSubmit').click(); });
```

Modal CSS (include in every page's `<style>` block):
```css
.cs-overlay { display:none; position:fixed; inset:0; z-index:2000; background:rgba(7,29,54,.75); backdrop-filter:blur(3px); -webkit-backdrop-filter:blur(3px); align-items:center; justify-content:center; padding:20px; }
.cs-overlay.open { display:flex; }
.cs-modal { background:#fff; border-radius:var(--r2); border:1px solid var(--b1); box-shadow:0 24px 64px rgba(0,0,0,.25); max-width:440px; width:100%; overflow:hidden; animation:csIn .22s ease-out; }
@keyframes csIn { from{opacity:0;transform:scale(.96) translateY(8px)} to{opacity:1;transform:none} }
.cs-head { background:var(--nav); padding:20px 24px 18px; display:flex; align-items:flex-start; justify-content:space-between; }
.cs-logo { font-family:var(--cond); font-size:18px; font-weight:900; color:#fff; }
.cs-logo span { color:var(--grn); }
.cs-close { background:rgba(255,255,255,.12); border:none; color:rgba(255,255,255,.7); width:28px; height:28px; border-radius:50%; font-size:16px; cursor:pointer; display:flex; align-items:center; justify-content:center; }
.cs-close:hover { background:rgba(255,255,255,.22); }
.cs-body { padding:24px; }
.cs-eyebrow { font-family:var(--cond); font-size:10px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color:var(--grn); margin-bottom:6px; }
.cs-title { font-family:var(--cond); font-size:22px; font-weight:900; color:var(--t1); margin-bottom:6px; }
.cs-sub { font-size:13px; color:var(--t2); line-height:1.5; margin-bottom:18px; }
.cs-form { display:flex; gap:0; margin-bottom:8px; }
.cs-input { flex:1; padding:10px 14px; border:1.5px solid var(--b2); border-right:none; border-radius:var(--r) 0 0 var(--r); font-family:var(--sans); font-size:13px; color:var(--t1); background:#f8fafc; outline:none; }
.cs-input:focus { border-color:var(--grn); }
.cs-btn { padding:10px 18px; background:var(--grn); color:#fff; font-family:var(--cond); font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; border-radius:0 var(--r) var(--r) 0; cursor:pointer; border:none; }
.cs-btn:hover { background:var(--grn-h); }
.cs-note { font-size:11px; color:var(--t3); text-align:center; }
.cs-confirm { display:none; text-align:center; padding:8px 0 4px; }
.cs-confirm.show { display:block; }
.cs-confirm-msg { font-family:var(--cond); font-size:14px; font-weight:700; color:var(--grn); }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
```

---

## STANDARD PAGE HEAD TEMPLATE

Every new page must start with this `<head>` structure (fill in page-specific values):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="theme-color" content="#071D36"/>
  <title>PAGE TITLE HERE | PitchIQ</title>
  <meta name="description" content="PAGE DESCRIPTION HERE"/>
  <link rel="canonical" href="https://getpitchiq.net/PAGE-SLUG"/>
  <!-- Favicon -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23071D36'/><text x='16' y='23' text-anchor='middle' font-family='Arial Black,sans-serif' font-weight='900' font-size='20' fill='%2300963F'>P</text></svg>" type="image/svg+xml"/>
  <!-- Open Graph -->
  <meta property="og:type" content="website"/>
  <meta property="og:site_name" content="PitchIQ"/>
  <meta property="og:title" content="PAGE TITLE HERE | PitchIQ"/>
  <meta property="og:description" content="PAGE DESCRIPTION HERE"/>
  <meta property="og:url" content="https://getpitchiq.net/PAGE-SLUG"/>
  <meta property="og:image" content="https://getpitchiq.net/pitchiq-banner.png"/>
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:site" content="@getpitchiq"/>
  <meta name="twitter:title" content="PAGE TITLE HERE | PitchIQ"/>
  <meta name="twitter:description" content="PAGE DESCRIPTION HERE"/>
  <meta name="twitter:image" content="https://getpitchiq.net/pitchiq-banner.png"/>
  <!-- Google Analytics GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','GA_MEASUREMENT_ID');</script>
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Barlow+Condensed:wght@700;800;900&display=swap" rel="stylesheet"/>
  <style>
    /* ... page CSS here ... */
  </style>
</head>
```

---

## STANDARD NAV COMPONENT

Every page (new and existing) must use this exact nav. The active page link gets `aria-current="page"`:

```html
<nav class="nav" aria-label="Primary navigation">
  <div class="nav-inner">
    <a class="nav-logo" href="/">Pitch<span>IQ</span></a>
    <div class="nav-links">
      <a class="nav-link" href="/predictions">Picks</a>
      <a class="nav-link" href="/standings">Standings</a>
      <a class="nav-link" href="/fantasy">Fantasy</a>
    </div>
  </div>
</nav>
```

Nav CSS:
```css
.nav { background:var(--nav); height:56px; display:flex; align-items:center; box-shadow:0 2px 12px rgba(0,0,0,.25); position:sticky; top:0; z-index:100; }
.nav-inner { max-width:1320px; margin:0 auto; padding:0 20px; width:100%; display:flex; align-items:center; justify-content:space-between; }
.nav-logo { font-family:var(--cond); font-size:22px; font-weight:900; color:#fff; text-decoration:none; }
.nav-logo span { color:var(--grn); }
.nav-links { display:flex; align-items:center; gap:2px; }
.nav-link { font-family:var(--cond); font-size:12px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:rgba(255,255,255,.65); padding:7px 12px; border-radius:var(--r); transition:color .15s,background .15s; text-decoration:none; }
.nav-link:hover, .nav-link[aria-current="page"] { color:#fff; background:rgba(255,255,255,.10); }
@media (max-width:640px) { .nav-link { padding:6px 8px; font-size:11px; } }
```

---

## STANDARD FOOTER COMPONENT

Every page uses this footer:

```html
<footer class="ft">
  <div class="ft-inner">
    <div class="ft-logo">Pitch<span>IQ</span></div>
    <div class="ft-links">
      <a href="/predictions">Picks</a>
      <a href="/standings">Standings</a>
      <a href="/fantasy">Fantasy</a>
    </div>
    <div class="ft-social">
      <a href="https://twitter.com/getpitchiq" target="_blank" rel="noopener" aria-label="Follow PitchIQ on X/Twitter">𝕏 @getpitchiq</a>
    </div>
    <p class="ft-legal">© 2026 PitchIQ · For entertainment purposes only · Must be 21+ to bet · <a href="https://www.ncpgambling.org" target="_blank" rel="noopener">Responsible Gambling</a></p>
  </div>
</footer>
```

Footer CSS:
```css
.ft { background:var(--nav); padding:32px 20px; margin-top:40px; }
.ft-inner { max-width:1320px; margin:0 auto; display:flex; flex-direction:column; align-items:center; gap:12px; text-align:center; }
.ft-logo { font-family:var(--cond); font-size:20px; font-weight:900; color:#fff; }
.ft-logo span { color:var(--grn); }
.ft-links { display:flex; gap:16px; }
.ft-links a { font-family:var(--cond); font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:rgba(255,255,255,.5); text-decoration:none; transition:color .15s; }
.ft-links a:hover { color:#fff; }
.ft-social a { font-family:var(--cond); font-size:12px; font-weight:700; color:var(--grn); text-decoration:none; }
.ft-legal { font-size:11px; color:rgba(255,255,255,.3); line-height:1.5; }
.ft-legal a { color:rgba(255,255,255,.4); }
```

---

## AD SLOT STANDARD (3 PLACEMENTS PER PAGE)

Include these 3 placements on every page. The publisher ID and slot IDs are placeholders — do not change them, they will be filled in later by the user.

**Placement 1 — Leaderboard (below nav, full width):**
```html
<div class="ad-leaderboard" aria-hidden="true">
  <ins class="adsbygoogle" style="display:block;width:728px;height:90px;margin:0 auto" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="1111111111"></ins>
</div>
```

**Placement 2 — Rectangle (in sidebar, 300×250):**
```html
<div aria-hidden="true">
  <ins class="adsbygoogle" style="display:block;width:300px;height:250px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="2222222222"></ins>
</div>
```

**Placement 3 — Banner (above footer, full width):**
```html
<div class="ad-footer-banner" aria-hidden="true">
  <ins class="adsbygoogle" style="display:block;width:728px;height:90px;margin:0 auto" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="3333333333"></ins>
</div>
```

---

## BEST PRACTICES — APPLY TO EVERY FILE

### Accessibility
- All images/icons need `alt` text or `aria-label`
- Interactive elements (buttons, links) need `:focus-visible` outlines
- Color contrast: text on `--nav` (dark navy) background must use white or `--grn` — never `--t2` or `--t3`
- `role="dialog"` and `aria-modal="true"` on modal overlays
- Skip navigation isn't required but nav landmark must use `<nav aria-label="Primary navigation">`
- Add `aria-current="page"` to the active nav link on each page

### Mobile Responsiveness (required)
Every page must be fully usable on a 375px screen. Required breakpoints:
```css
@media (max-width: 1024px) {
  /* Sidebar stacks below main content */
  .layout { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  /* Cards go full width, font sizes adjust */
  .match-header { flex-direction: column; text-align: center; }
}
@media (max-width: 480px) {
  /* Nav link text may truncate, ad leaderboard hides (too wide for mobile) */
  .ad-leaderboard, .ad-footer-banner { display: none; }
}
```

### Performance
- No JavaScript libraries. Vanilla JS only.
- Inline all CSS — no external stylesheets (except Google Fonts which is already async)
- Use `loading="lazy"` if any `<img>` tags are added
- Font display is handled by Google Fonts URL — no extra `font-display` needed
- IntersectionObserver for `.rv` (reveal) animation class where used

### SEO
- Every page needs: `<title>`, `<meta name="description">`, `<link rel="canonical">`, OG tags, Twitter card tags
- Title format: `"[Match/Feature] — World Cup 2026 | PitchIQ"` (under 60 chars preferred)
- Description: 140–160 chars, includes key terms
- JSON-LD structured data on match preview pages (SportsEvent schema)
- Internal linking: pages link to related match pages, predictions hub, standings

### Code Quality
- Use `'use strict';` at top of every `<script>` block
- No inline event handlers (`onclick="..."`) — use `addEventListener`
- No `var` in new code — use `const` and `let` (existing files use `var` for IE compat, new pages can use modern JS)
- CSS reset at top of every `<style>` block: `*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }`
- Use CSS custom properties (`var(--grn)`) not hardcoded hex values
- Smooth scroll: `html { scroll-behavior: smooth; }`

### Content Quality
- Write match analysis that sounds like a sharp sports analyst, not a stats dump
- Betting picks should include a label: `AI PICK`, `HOT`, `VALUE`, or `LONG SHOT`
- Fantasy picks must include projected points AND ownership percentage
- Never make any guarantee about betting outcomes — add "entertainment purposes only" framing
- Odds format is American (+/-) throughout

---

## PHASE 1 — Build 5 New Match Preview Pages

**Before you start:** Read `brazil-morocco.html` fully (it is at `/Users/samsonwinz/Claude/Projects/PitchIQ/brazil-morocco.html`). Extract the full HTML structure as your template. You only need to read it ONCE — then adapt it for each match below. Change all match-specific content (teams, flags, times, venues, odds, analysis, picks) while keeping the page structure identical.

**What every match preview page must contain:**
1. Standard `<head>` with SEO tags and JSON-LD SportsEvent schema
2. Standard nav (with active `aria-current="page"` removed — none of the nav links is "active" on a match page)
3. Leaderboard ad slot
4. Match header: team flags (emoji), team names, group, match date/time (ET), venue name & city
5. Live odds strip: Moneyline (home / draw / away) + Over/Under — all as `data-aff` links
6. AI prediction probability bar (3-way: Home Win % / Draw % / Away Win %)
7. Prediction summary chips (key stat callouts supporting the prediction)
8. Match analysis: 2–3 paragraphs each team, 1 paragraph on key matchup
9. Key stats grid (xG, clean sheets, recent form, relevant numbers)
10. Stats comparison table (6 rows: xG/90, possession, pass accuracy, goals conceded/90, key passes/90, press success rate)
11. 4 betting picks with labels (AI PICK / HOT / VALUE / LONG SHOT), each with data-aff link to relevant book
12. Top 4 fantasy picks with: name, position, flag, projected points, ownership%, price, short reasoning
13. Sidebar: sportsbook odds comparison card, trending searches card, rectangle ad slot, next group matches card
14. Twitter CTA: "Follow @getpitchiq for live picks and updates"
15. Footer banner ad slot
16. Standard footer
17. Coming Soon modal
18. AFF config + data-aff wiring JS

---

### Match 1: `uruguay-serbia.html`

**Match info:**
- Uruguay 🇺🇾 vs Serbia 🇷🇸
- Group E, Match 2 · June 14, 2026 · 7:00 PM ET
- SoFi Stadium, Inglewood, CA
- JSON-LD: name "Uruguay vs Serbia — FIFA World Cup 2026", startDate "2026-06-14T23:00:00Z", location "SoFi Stadium, Inglewood, California"

**Odds:**
- Moneyline: Uruguay +230 (FanDuel), Draw +230 (DraftKings), Serbia +115 (BetMGM)
- Over 2.5 Goals: -105 (Caesars) · Under 2.5: -125 (DraftKings)

**AI Prediction:** 28% Uruguay / 28% Draw / 44% Serbia — Serbia win 1-0

**Prediction chips:** "Serbia +115 — best value in Group E" · "Uruguay kept 6 clean sheets in qualifying" · "Both teams average under 1.4 goals conceded/90"

**Analysis:**
- *Serbia:* Vlahović and Mitrović give Serbia two elite striker options — one of the few teams in the tournament with genuine depth at center forward. Milinković-Savić controls midfield tempo with passing range and physicality that can dominate most opponents. Serbia qualified impressively from UEFA, conceding just 8 goals across 10 qualifying matches. Their biggest question is whether they can unlock a disciplined defensive block — they've struggled against low-block teams in recent form.
- *Uruguay:* Darwin Núñez is one of the most dangerous strikers in the world in transition — his pace and finishing are elite when he gets service. But Uruguay's midfield will need Federico Valverde and Rodrigo Bentancur to win the physical battle against Serbia's engine room. Defensive solidity is their trademark: 6 clean sheets in CONMEBOL qualifying is the best record in the confederation. They'll look to absorb pressure and punish Serbia on the counter.
- *Key matchup:* Vlahović vs. Uruguayan CB pairing. Uruguay's central defenders are disciplined but were challenged by aerial threats in qualifying. Vlahović at 6'2" is a constant aerial threat on set pieces — Uruguay must stop Serbia from winning corners.

**Stats comparison:**
| Stat | Serbia | Uruguay |
|---|---|---|
| xG/90 | 1.6 | 1.4 |
| Possession | 54% | 51% |
| Pass accuracy | 86% | 84% |
| Goals conceded/90 | 0.8 | 0.7 |
| Key passes/90 | 8.2 | 7.6 |
| Press success rate | 32% | 29% |

**Betting picks:**
1. Serbia -0.5 Asian Handicap -110 · **VALUE** · "Serbia -0.5 AH is the sharpest line on this match. Backing Serbia to do anything but lose at -110 is strong value given Uruguay's defensive setup."
2. Under 2.5 Goals -125 · **AI PICK** · "Both teams average under 1.5 goals conceded/90. This sets up as a tight, low-scoring encounter. Under is our model's top play."
3. Dušan Vlahović Anytime Scorer +210 · **HOT** · "Vlahović has scored in 3 straight Serbia competitive matches. At +210, this is underpriced."
4. Darwin Núñez Anytime Scorer +240 · **LONG SHOT** · "If Uruguay get a counterattack opportunity, Núñez finishes. High risk but strong upside at +240."

**Fantasy picks:**
1. Dušan Vlahović · FWD · 🇷🇸 · 34 proj pts · 14% owned · $9 · "Two striker system means Vlahović gets more touches in the box than usual. Best midfielder for Group E."
2. Darwin Núñez · FWD · 🇺🇾 · 32 proj pts · 13% owned · $9 · "Explosive upside if Uruguay get space to run in behind Serbia's high defensive line."
3. Federico Valverde · MID · 🇺🇾 · 28 proj pts · 10% owned · $9 · "Engine room of Uruguay's press. Scores, assists, and racks up defensive bonus points."
4. Sergej Milinković-Savić · MID · 🇷🇸 · 26 proj pts · 9% owned · $8 · "Differential pick. SMS controls matches — if Serbia win 1-0, he's the reason."

**SEO title:** "Uruguay vs Serbia Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Uruguay vs Serbia World Cup 2026 prediction, betting odds & fantasy picks. Group E, June 14 at SoFi Stadium. Serbia +115 favorites in a tight tactical battle."
**Canonical:** https://getpitchiq.net/uruguay-serbia

---

### Match 2: `france-albania.html`

**Match info:**
- France 🇫🇷 vs Albania 🇦🇱
- Group H, Match 1 · June 14, 2026 · 10:00 PM ET
- Rose Bowl, Pasadena, CA
- JSON-LD: name "France vs Albania — FIFA World Cup 2026", startDate "2026-06-15T02:00:00Z", location "Rose Bowl, Pasadena, California"

**Odds:**
- Moneyline: France -800 (DraftKings), Draw +1400 (FanDuel), Albania +3000 (BetMGM)
- Over 2.5 Goals: -150 (Caesars) · Under 2.5: +120 (DraftKings)

**AI Prediction:** 88% France / 9% Draw / 3% Albania — France win 3-0 or 4-0

**Prediction chips:** "France -800 — one of the safest tournament openers" · "Mbappé scored 12 in UEFA qualifying" · "Albania conceded 14 goals in qualifying"

**Analysis:**
- *France:* One of three genuine tournament favorites at +650. Mbappé at 27 is arguably the best player on the planet right now — his combination of pace, dribbling, and clinical finishing is unmatched at this tournament. Griezmann at 35 is still a creative hub, winning balls and threading passes in tight spaces. The back line with Theo Hernández at left back gives France an attacking threat from deep. N'Golo Kanté's return from injury is the story of France's qualification — his energy and ball-winning re-energized the team in the final 6 qualifiers.
- *Albania:* Albania's World Cup debut is historic — they qualified through a competitive UEFA group, beating several established nations. Their head coach has built a disciplined low-block system that frustrated opponents in qualifying. But this is a different level. Albania conceded 14 goals in qualifying despite their defensive setup, and France's attacking firepower is several tiers above any team Albania have faced. Their best realistic outcome is limiting France to 1-2 goals with a set-piece moment of their own.
- *Key matchup:* Mbappé vs. Albania's right back. Albania's defensive shape is organized, but Mbappé's ability to receive behind the defensive line will create constant problems. Expect France to use him in central areas rather than wide, where Albania's two defensive blocks close passing lanes.

**Stats comparison:**
| Stat | France | Albania |
|---|---|---|
| xG/90 | 2.9 | 0.9 |
| Possession | 61% | 43% |
| Pass accuracy | 91% | 79% |
| Goals conceded/90 | 0.6 | 1.4 |
| Key passes/90 | 12.1 | 5.4 |
| Press success rate | 41% | 24% |

**Betting picks:**
1. France Win to Nil -130 · **AI PICK** · "France have kept 8 clean sheets in their last 10. Albania have not scored in 3 of their last 5 international matches. This is a layup."
2. France -2 Asian Handicap -115 · **HOT** · "France's goal difference in qualifying was +22. Albania gave up 3+ in two qualifying matches. Back France to cover -2."
3. Kylian Mbappé Anytime Scorer -120 · **HOT** · "Mbappé scored in 8 of 10 qualifying matches. -120 is nearly even money for a player who scores in 80% of matches."
4. Mbappé 2+ Goals +200 · **LONG SHOT** · "If France are flying and Mbappé gets into rhythm early, this is live. He had 4 multi-goal qualifying matches."

**Fantasy picks:**
1. Kylian Mbappé · FWD · 🇫🇷 · 45 proj pts · 32% owned · $12 · "Captain candidate. Near-certain scorer, likely assist, possible 2-goal game. Highest ceiling at the tournament."
2. Antoine Griezmann · MID/FWD · 🇫🇷 · 36 proj pts · 21% owned · $10 · "Creative hub. Expect 1-2 assists and goal involvement. Consistent fantasy producer."
3. Ousmane Dembélé · FWD · 🇫🇷 · 30 proj pts · 14% owned · $9 · "Value play. Dembélé's direct dribbling will terrorize Albania's wide defenders. Likely 1 goal or assist."
4. N'Golo Kanté · MID · 🇫🇷 · 24 proj pts · 9% owned · $8 · "Clean sheet bonus + defensive returns. Under-owned for a France starter."

**SEO title:** "France vs Albania Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "France vs Albania World Cup 2026 prediction, betting odds & fantasy picks. Group H, June 14 at Rose Bowl Pasadena. France -800 — Mbappé chasing a monster opening night."
**Canonical:** https://getpitchiq.net/france-albania

---

### Match 3: `argentina-peru.html`

**Match info:**
- Argentina 🇦🇷 vs Peru 🇵🇪
- Group C, Match 2 · June 15, 2026 · 4:00 PM ET
- Hard Rock Stadium, Miami, FL
- JSON-LD: name "Argentina vs Peru — FIFA World Cup 2026", startDate "2026-06-15T20:00:00Z", location "Hard Rock Stadium, Miami, Florida"

**Odds:**
- Moneyline: Argentina -700 (DraftKings), Draw +1100 (FanDuel), Peru +3000 (BetMGM)
- Over 2.5 Goals: -130 (Caesars) · Under 2.5: +100 (DraftKings)

**AI Prediction:** 86% Argentina / 10% Draw / 4% Peru — Argentina win 3-0

**Prediction chips:** "Defending champions at +500 to lift the trophy" · "Messi scored 10 in qualifying — leads all CONMEBOL" · "Peru conceded 22 goals in qualifying"

**Analysis:**
- *Argentina:* The defending champions arrive at their title defense with arguably a stronger squad than 2022. Messi at 38 has defied time — his decision-making and vision are still elite, even as his role has shifted to more of a false 9 / #10. Julián Álvarez has emerged as one of the best strikers in Europe — his work rate, movement, and finishing give Argentina a dimension they lacked before his rise. Enzo Fernández has become the complete central midfielder. The question for Argentina is not whether they'll win, but when they'll turn it on.
- *Peru:* Peru qualified via the intercontinental playoff — an achievement in itself. Their squad is built around heart and defensive discipline rather than individual brilliance. Guerrero at 40 is a legendary figure but a symbolic captain rather than a threat to Argentina's defense. Peru's game plan will be to absorb pressure, stay organized, and hope for a set-piece moment. Against this Argentina side, that will require a near-perfect performance across 90 minutes.
- *Key matchup:* Enzo Fernández vs. Peru's midfield press. If Peru attempt any press — which their coach has hinted at — Fernández's passing range will destroy them. If they sit deep, Argentina's wide players (Dembélé was linked, but in this squad, Di María and/or others) will create overloads.

**Stats comparison:**
| Stat | Argentina | Peru |
|---|---|---|
| xG/90 | 2.7 | 0.9 |
| Possession | 60% | 44% |
| Pass accuracy | 89% | 78% |
| Goals conceded/90 | 0.7 | 2.2 |
| Key passes/90 | 11.3 | 5.1 |
| Press success rate | 38% | 22% |

**Betting picks:**
1. Argentina Win to Nil -115 · **AI PICK** · "Argentina's backline is elite. Peru have failed to score in 4 of their last 8 internationals. Argentina clean sheet is the play."
2. Argentina -2 Asian Handicap -120 · **HOT** · "Argentina cover -2 in this matchup. Peru simply do not have the quality to stay within 2 goals of the defending champs."
3. Lionel Messi Anytime Scorer +140 · **HOT** · "Messi scored in 8 of 10 qualifying matches, including hat-tricks vs Bolivia and Venezuela. +140 undervalues him here."
4. Julián Álvarez Anytime Scorer +155 · **VALUE** · "Álvarez is one of the most clinical finishers in world football and plays alongside Messi. +155 with this much supply is value."

**Fantasy picks:**
1. Lionel Messi · FWD/MID · 🇦🇷 · 48 proj pts · 38% owned · $12 · "Elite captain candidate. Goal, assist, and creative returns. The most complete fantasy player in the tournament."
2. Julián Álvarez · FWD · 🇦🇷 · 40 proj pts · 28% owned · $10 · "Álvarez runs more than anyone and plays next to Messi. He'll get his chances."
3. Enzo Fernández · MID · 🇦🇷 · 30 proj pts · 16% owned · $9 · "Pass accuracy, key passes, and potential for a goal from deep. Consistent midfield producer."
4. Rodrigo De Paul · MID · 🇦🇷 · 26 proj pts · 12% owned · $9 · "Workhorse. Defensive and offensive contributions. Cheap for the price."

**SEO title:** "Argentina vs Peru Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Argentina vs Peru World Cup 2026 prediction, betting odds & fantasy picks. Group C, June 15 at Hard Rock Stadium Miami. Defending champions -700 in their opener."
**Canonical:** https://getpitchiq.net/argentina-peru

---

### Match 4: `england-senegal.html`

**Match info:**
- England 🏴󠁧󠁢󠁥󠁮󠁧󠁿 vs Senegal 🇸🇳
- Group G, Match 1 · June 15, 2026 · 10:00 PM ET
- Levi's Stadium, Santa Clara, CA
- JSON-LD: name "England vs Senegal — FIFA World Cup 2026", startDate "2026-06-16T02:00:00Z", location "Levi's Stadium, Santa Clara, California"

**Odds:**
- Moneyline: England -400 (DraftKings), Draw +700 (FanDuel), Senegal +1100 (BetMGM)
- Over 2.5 Goals: -115 (Caesars) · Under 2.5: -115 (DraftKings)

**AI Prediction:** 72% England / 18% Draw / 10% Senegal — England win 2-1

**Prediction chips:** "England +1400 tournament odds — top 5 favorites" · "Kane scored 15 goals in qualifying" · "Senegal beat Belgium 2-0 in their last competitive fixture"

**Analysis:**
- *England:* England enter WC2026 with genuine belief they can go all the way — and the squad depth to back it up. Harry Kane is the best pure center forward in the tournament — his movement, hold-up play, and clinical finishing are world-class. Jude Bellingham at 22 is already a generational midfielder: box-to-box engine, goals from deep, leadership beyond his years. Phil Foden's creativity in tight spaces is elite. England's vulnerability is in big tournament knockouts — the mentality question still looms. But this group stage fixture is about business.
- *Senegal:* Senegal are no pushovers. They beat Belgium in their final qualifier to advance and have a squad built around Premier League quality. Mané at 33 has quietened slightly from his Liverpool peak but is still dangerous in transition. Idrissa Gueye is a tireless defensive midfielder who will try to disrupt England's rhythm. Koulibaly leads a physical defensive unit that could frustrate England if the Three Lions get sloppy in the final third.
- *Key matchup:* Bellingham vs. Gueye. This midfield battle defines the match. If Bellingham gets past Gueye's press and drives into space, England will create. If Gueye neutralizes him, England become more predictable and Senegal stay in the game.

**Stats comparison:**
| Stat | England | Senegal |
|---|---|---|
| xG/90 | 2.4 | 1.6 |
| Possession | 58% | 52% |
| Pass accuracy | 88% | 82% |
| Goals conceded/90 | 0.9 | 1.0 |
| Key passes/90 | 10.2 | 7.8 |
| Press success rate | 36% | 31% |

**Betting picks:**
1. England -0.5 Asian Handicap -110 · **AI PICK** · "England's squad quality is significantly superior. Back them to win rather than draw with -0.5 AH at near-even money."
2. Both Teams to Score Yes +145 · **HOT** · "Senegal have scored in 7 of their last 8 internationals. England's set-piece vulnerability gives Senegal a route to goal. BTTS is live."
3. Harry Kane Anytime Scorer -110 · **HOT** · "15 goals in qualifying. Near-even money on the tournament's second-highest projected scorer. Take it."
4. Jude Bellingham Anytime Scorer +160 · **VALUE** · "Bellingham scored 5 in qualifying with a further 8 assists. His runs from deep make him a consistent scorer threat. +160 is value."

**Fantasy picks:**
1. Jude Bellingham · MID · 🏴󠁧󠁢󠁥󠁮󠁧󠁿 · 38 proj pts · 19% owned · $11 · "Highest upside English player. Goals, assists, and key pass returns. Under-owned relative to his ceiling."
2. Harry Kane · FWD · 🏴󠁧󠁢󠁥󠁮󠁧󠁿 · 36 proj pts · 22% owned · $10 · "Reliable captain candidate. Tournament's second-best scoring striker after Mbappé."
3. Phil Foden · MID · 🏴󠁧󠁢󠁥󠁮󠁧󠁿 · 34 proj pts · 17% owned · $10 · "Creative returns, key passes, and the occasional goal. Consistent midfielder."
4. Sadio Mané · FWD · 🇸🇳 · 26 proj pts · 7% owned · $8 · "Differential pick. If Senegal grab a goal — which BTTS suggests — Mané is the most likely scorer."

**SEO title:** "England vs Senegal Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "England vs Senegal World Cup 2026 prediction, betting odds & fantasy picks. Group G, June 15 at Levi's Stadium San Francisco. England -400 favorites in a tricky opener."
**Canonical:** https://getpitchiq.net/england-senegal

---

### Match 5: `colombia-ecuador.html`

**Match info:**
- Colombia 🇨🇴 vs Ecuador 🇪🇨
- Group F, Match 2 · June 15, 2026 · 7:00 PM ET
- State Farm Stadium, Glendale, AZ
- JSON-LD: name "Colombia vs Ecuador — FIFA World Cup 2026", startDate "2026-06-15T23:00:00Z", location "State Farm Stadium, Glendale, Arizona"

**Odds:**
- Moneyline: Colombia -140 (DraftKings), Draw +260 (FanDuel), Ecuador +400 (BetMGM)
- Over 2.5 Goals: -110 (Caesars) · Under 2.5: -120 (DraftKings)

**AI Prediction:** 48% Colombia / 26% Draw / 26% Ecuador — Colombia win 2-1

**Prediction chips:** "Colombia Copa América runners-up 2024" · "Caicedo — Chelsea's $115M midfielder controls the tempo" · "CONMEBOL's most entertaining qualifying group"

**Analysis:**
- *Colombia:* Colombia arrive at WC2026 with genuine belief after finishing Copa América runners-up in 2024. James Rodríguez at 34 is the creative heartbeat — his vision and set-piece delivery from the left create constant danger. Luis Díaz has developed into one of Liverpool's most exciting players — his direct running and ability to cut inside will test Ecuador's right side. Jhon Duran at center forward has emerged as a powerful, physical finisher. Colombia's weakness is defensive transitions when James plays high.
- *Ecuador:* Ecuador punched above their weight in qualifying and are built around Moisés Caicedo — the $115M Chelsea midfielder who is one of the best young players in the world. His engine, press resistance, and passing range make Ecuador genuinely competitive against anyone. Enner Valencia at 35 is still capable of a moment, and Estupiñán provides quality from left back. Ecuador's best path to a result is controlling midfield through Caicedo and denying Colombia space in behind.
- *Key matchup:* James Rodríguez vs. Moisés Caicedo. James needs time and space — Caicedo will try to deny him both. If Caicedo wins this battle, Ecuador stay in the match. If James gets freedom, Colombia's creativity is overwhelming.

**Stats comparison:**
| Stat | Colombia | Ecuador |
|---|---|---|
| xG/90 | 1.9 | 1.6 |
| Possession | 56% | 54% |
| Pass accuracy | 86% | 84% |
| Goals conceded/90 | 1.1 | 1.0 |
| Key passes/90 | 9.4 | 8.7 |
| Press success rate | 33% | 35% |

**Betting picks:**
1. Colombia -0.5 Asian Handicap +105 · **VALUE** · "Colombia to win at +105 is the best value line on the board today. James Rodríguez at his best gives Colombia a quality edge."
2. Over 2.5 Goals -110 · **AI PICK** · "Both teams scored in 8 of their last 10 internationals combined. This CONMEBOL derby has goal-fest written all over it."
3. Luis Díaz Anytime Scorer +200 · **HOT** · "Díaz scored 8 in qualifying and 11 for Liverpool last season. +200 on one of the tournament's best wide forwards is undervalued."
4. Moisés Caicedo Anytime Scorer +280 · **LONG SHOT** · "Caicedo has started driving forward more under Ecuador's new coach. If he scores, Ecuador take a point. +280 is speculative but alive."

**Fantasy picks:**
1. Luis Díaz · FWD · 🇨🇴 · 34 proj pts · 12% owned · $9 · "Best value forward in Group F. Goals, assists, and direct play. Under-owned at 12%."
2. James Rodríguez · MID · 🇨🇴 · 30 proj pts · 10% owned · $9 · "If Colombia win, James is the reason. Assists and set-piece returns."
3. Enner Valencia · FWD · 🇪🇨 · 28 proj pts · 9% owned · $8 · "Ecuador's most dangerous threat. Differential if Ecuador cause an upset."
4. Moisés Caicedo · MID · 🇪🇨 · 28 proj pts · 8% owned · $8 · "Best under-owned midfielder in the group. Controls matches. Defensive and offensive returns."

**SEO title:** "Colombia vs Ecuador Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Colombia vs Ecuador World Cup 2026 prediction, betting odds & fantasy picks. Group F, June 15 at State Farm Stadium Phoenix. Caicedo vs James Rodríguez — CONMEBOL's best rivalry."
**Canonical:** https://getpitchiq.net/colombia-ecuador

---

## PHASE 2 — Build `standings.html`

Create `/Users/samsonwinz/Claude/Projects/PitchIQ/standings.html`

**Purpose:** Live group standings hub. Shows all group tables for WC2026 Group Stage.

**Key context:** WC2026 uses a new 48-team format — 16 groups of 3 teams. Top 2 from each group advance automatically. The 8 best 3rd-place finishers also advance (32 teams total enter Round of 32).

**Layout:**
```
Nav
Leaderboard Ad
Hero Section — title + format explainer
Tab Bar: [All Groups] [Americas] [Europe] [Africa/Asia]
Groups Grid (2-column desktop, 1-column mobile) — 16 group cards
Sportsbook bonus bar
Footer ad + Footer
Coming Soon Modal
```

**Each group card structure:**
```html
<div class="group-card" data-region="americas">
  <div class="group-head">
    <span class="group-label">GROUP A</span>
    <span class="group-status live">● LIVE</span>
  </div>
  <table class="standings-table">
    <thead>
      <tr><th>Team</th><th title="Games Played">GP</th><th title="Wins">W</th><th title="Draws">D</th><th title="Losses">L</th><th title="Goals For">GF</th><th title="Goals Against">GA</th><th title="Goal Difference">GD</th><th title="Points">Pts</th></tr>
    </thead>
    <tbody>
      <!-- 3 rows, top 2 get class="qualify" which adds green left border -->
    </tbody>
  </table>
</div>
```

**Known results to display as real data (June 13, 2026):**

Group A (Americas):
- USA 🇺🇸: 1GP 1W 0D 0L 4GF 1GA +3GD **3pts** `qualify`
- Canada 🇨🇦: 1GP 0W 1D 0L 1GF 1GA 0GD **1pt**
- Bolivia 🇧🇴: 0GP — — — — — — **0pts** *(plays next)*

Group B (Americas):
- Mexico 🇲🇽: 1GP 1W 0D 0L 2GF 0GA +2GD **3pts** `qualify`
- South Africa 🇿🇦: 1GP 0W 0D 1L 0GF 2GA -2GD **0pts**
- *(3rd team TBD — fixture upcoming)* — fill with "TBD" row

Group C (Africa/Asia):
- South Korea 🇰🇷: 1GP 1W 0D 0L 2GF 1GA +1GD **3pts** `qualify`
- Czech Republic 🇨🇿: 1GP 0W 0D 1L 1GF 2GA -1GD **0pts**
- *(3rd team TBD)* — fill "TBD"

Group D (Europe):
- Canada 🇨🇦... wait — use this data:
  Canada 1pt from 1-1 draw with Bosnia. So Group D is:
- Canada 🇨🇦: 1GP 0W 1D 0L 1GF 1GA 0GD **1pt**
- Bosnia & Herzegovina 🇧🇦: 1GP 0W 1D 0L 1GF 1GA 0GD **1pt**
- *(3rd team TBD)*

Groups E through P: All teams at 0pts 0GP (fixtures from June 14 onward). Build placeholder rows with flags and team names at 0/0/0/0/0/0/0/0 and mark status as "UPCOMING".

**For groups E through P, use these team assignments** (approximate — based on known WC2026 draw context):
- Group E: Germany 🇩🇪, Uruguay 🇺🇾, Curacao 🇨🇼
- Group F: Netherlands 🇳🇱, Colombia 🇨🇴, Ecuador 🇪🇨, Japan 🇯🇵 *(note: 3-team format — pick most likely 3)*
- Group G: England 🏴󠁧󠁢󠁥󠁮󠁧󠁿, Senegal 🇸🇳, Slovakia 🇸🇰
- Group H: Spain 🇪🇸, France 🇫🇷, Albania 🇦🇱, Cape Verde 🇨🇻 *(pick 3)*
- Groups I–P: Use placeholder teams "Team TBD" with note "Fixture data loading..."

**Important note in the page hero:** "WC2026 standings are updated manually during the Group Stage. Refresh for latest results."

**Interactive features:**
1. Tab filter: clicking "Americas" shows only groups tagged `data-region="americas"` — hide others
2. "Qualify" rows (top 2) have green left border: `border-left: 3px solid var(--grn)`
3. Sortable table columns on click (pure JS sort by Pts, GD, GF descending)
4. Groups with live/completed matches get `● LIVE` or `✓ FT` badge; groups with upcoming matches get `UPCOMING` badge

**SEO:**
- Title: "World Cup 2026 Group Stage Standings — All 16 Groups | PitchIQ"
- Description: "Live World Cup 2026 group standings. All 16 groups, updated results, and qualification tracker for the 48-team tournament."
- Canonical: https://getpitchiq.net/standings

---

## PHASE 3 — Build `predictions.html` (AI Picks Hub)

Create `/Users/samsonwinz/Claude/Projects/PitchIQ/predictions.html`

**Purpose:** Central hub for all AI match predictions — the site's most SEO-valuable page for queries like "World Cup 2026 predictions today" and "best bets World Cup 2026."

**Layout:**
```
Nav (aria-current="page" on "Picks" link)
Leaderboard Ad
Hero: "AI Match Predictions" + subtitle "Model-driven picks for every World Cup 2026 fixture"
Filter tabs: [All] [Jun 13] [Jun 14] [Jun 15]
Predictions grid (3-column desktop, 2-column tablet, 1-column mobile)
Sportsbook bonus bar
Rectangle ad
Footer banner ad + Footer
Coming Soon Modal
```

**Each prediction card (link to full preview page):**
```html
<a href="/brazil-morocco" class="pred-card" data-date="2026-06-13">
  <div class="pred-header">
    <span class="pred-group">GROUP C · Jun 13 6PM ET</span>
    <span class="pred-venue">MetLife Stadium</span>
  </div>
  <div class="pred-teams">
    <div class="pred-team">
      <span class="pred-flag">🇧🇷</span>
      <span class="pred-name">Brazil</span>
    </div>
    <div class="pred-vs">VS</div>
    <div class="pred-team">
      <span class="pred-flag">🇲🇦</span>
      <span class="pred-name">Morocco</span>
    </div>
  </div>
  <div class="pred-bar-wrap">
    <div class="pred-bar-home" style="width:58%">58%</div>
    <div class="pred-bar-draw" style="width:22%">22%</div>
    <div class="pred-bar-away" style="width:20%">20%</div>
  </div>
  <div class="pred-pick">
    <span class="pred-pick-badge ai">AI PICK</span>
    Brazil -0.5 AH &nbsp;·&nbsp; <strong>-130</strong>
  </div>
  <div class="pred-cta">Full Preview & Picks →</div>
</a>
```

**All 9 prediction cards:**
1. Brazil vs Morocco · Jun 13 6PM · MetLife · Group C · 58/22/20 · "Brazil -0.5 AH -130" · AI PICK · `/brazil-morocco`
2. Germany vs Curacao · Jun 14 1PM · NRG Stadium Houston · Group E · 92/5/3 · "Germany Win to Nil" · AI PICK · `/germany-curacao`
3. Netherlands vs Japan · Jun 14 4PM · AT&T Stadium Dallas · Group F · 52/24/24 · "Netherlands -0.5 +105" · VALUE · `/netherlands-japan`
4. Uruguay vs Serbia · Jun 14 7PM · SoFi Stadium · Group E · 28/28/44 · "Under 2.5 Goals -125" · AI PICK · `/uruguay-serbia`
5. France vs Albania · Jun 14 10PM · Rose Bowl Pasadena · Group H · 88/9/3 · "France Win to Nil -130" · HOT · `/france-albania`
6. Spain vs Cape Verde · Jun 15 1PM · Mercedes-Benz Stadium Atlanta · Group H · 89/8/3 · "Spain Win to Nil -110" · AI PICK · `/spain-capeverde`
7. Argentina vs Peru · Jun 15 4PM · Hard Rock Stadium Miami · Group C · 86/10/4 · "Argentina Win to Nil -115" · HOT · `/argentina-peru`
8. Colombia vs Ecuador · Jun 15 7PM · State Farm Stadium Glendale · Group F · 48/26/26 · "Over 2.5 Goals -110" · VALUE · `/colombia-ecuador`
9. England vs Senegal · Jun 15 10PM · Levi's Stadium Santa Clara · Group G · 72/18/10 · "England -0.5 AH -110" · AI PICK · `/england-senegal`

**Probability bar colors:**
- Home win bar: `var(--grn)`
- Draw bar: `#7C92A8` (muted grey-blue)
- Away win bar: `var(--nav)` (dark navy)

**Pick badge colors:**
- AI PICK: green background `var(--grn)`, white text
- HOT: orange background `#E8590C`, white text
- VALUE: blue background `#1971C2`, white text
- LONG SHOT: grey background `var(--t3)`, white text

**Filter JS:** clicking a date tab filters `.pred-card` elements by `data-date` attribute. "All" tab shows everything.

**SEO:**
- Title: "AI World Cup 2026 Predictions — Best Bets & Picks Today | PitchIQ"
- Description: "AI-powered World Cup 2026 match predictions for every fixture. Best bets, odds, and expert picks — updated daily through the Group Stage."
- Canonical: https://getpitchiq.net/predictions

---

## PHASE 4 — Build `fantasy.html` (Fantasy Lineup Builder)

Create `/Users/samsonwinz/Claude/Projects/PitchIQ/fantasy.html`

**Purpose:** Interactive tool that lets users build a World Cup fantasy lineup, see projected points, and get player recommendations. High engagement + return visit driver.

**Layout:**
```
Nav (aria-current="page" on "Fantasy" link)
Leaderboard Ad
Hero: "Fantasy Lineup Builder" + subtitle "Build your WC2026 squad · 40 players · AI projections"
Two-panel layout (desktop: pitch left, player list right | mobile: stacked)
  Left: Formation picker + Visual pitch with slots
  Right: Player selection panel (filterable by position)
Score card: Total projected points + Budget used/remaining
Action buttons: [Auto Best XI] [Clear Lineup] [Share Lineup]
Top Differentials section (3 cards for under-owned value picks)
Sportsbook sidebar
Rectangle ad in sidebar
Footer banner + Footer
Coming Soon modal
```

**Formation options:** 4-3-3 (default), 4-4-2, 3-4-3. Selecting changes the number of slots rendered on the pitch for each position row.

**Pitch visualization (CSS):**
```css
.pitch {
  background: linear-gradient(to bottom, #2d6a1f 0%, #2d6a1f 48%, #1f5214 48%, #1f5214 52%, #2d6a1f 52%, #2d6a1f 100%);
  border-radius: var(--r2);
  position: relative;
  min-height: 480px;
  border: 2px solid rgba(255,255,255,.15);
  padding: 16px 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
/* White pitch markings as pseudo-elements or SVG overlay */
/* Center circle, halfway line, penalty areas */
```

**Player slot (empty state):**
```html
<div class="p-slot empty" data-pos="FWD" data-slot="0">
  <div class="p-slot-icon">+</div>
  <div class="p-slot-label">FWD</div>
</div>
```

**Player slot (filled state):**
```html
<div class="p-slot filled" data-pos="FWD" data-slot="0">
  <div class="p-slot-flag">🇫🇷</div>
  <div class="p-slot-name">Mbappé</div>
  <div class="p-slot-pts">45 pts</div>
  <button class="p-slot-remove" aria-label="Remove player">×</button>
</div>
```

**Player pool (use EXACTLY this data array in your JS):**
```javascript
const PLAYERS = [
  // FORWARDS
  {id:1,  name:"Kylian Mbappé",       team:"FRA", flag:"🇫🇷", pos:"FWD", pts:45, own:"32%", price:12},
  {id:2,  name:"Lionel Messi",        team:"ARG", flag:"🇦🇷", pos:"FWD", pts:48, own:"38%", price:12},
  {id:3,  name:"Erling Haaland",      team:"NOR", flag:"🇳🇴", pos:"FWD", pts:44, own:"29%", price:12},
  {id:4,  name:"Vinicius Jr.",         team:"BRA", flag:"🇧🇷", pos:"FWD", pts:42, own:"26%", price:11},
  {id:5,  name:"Lamine Yamal",        team:"ESP", flag:"🇪🇸", pos:"FWD", pts:40, own:"24%", price:11},
  {id:6,  name:"Julián Álvarez",      team:"ARG", flag:"🇦🇷", pos:"FWD", pts:40, own:"28%", price:10},
  {id:7,  name:"Harry Kane",          team:"ENG", flag:"🏴󠁧󠁢󠁥󠁮󠁧󠁿", pos:"FWD", pts:36, own:"22%", price:10},
  {id:8,  name:"Jamal Musiala",       team:"GER", flag:"🇩🇪", pos:"FWD", pts:38, own:"22%", price:10},
  {id:9,  name:"Cody Gakpo",          team:"NED", flag:"🇳🇱", pos:"FWD", pts:36, own:"16%", price:10},
  {id:10, name:"Dušan Vlahović",      team:"SRB", flag:"🇷🇸", pos:"FWD", pts:34, own:"14%", price:9},
  {id:11, name:"Luis Díaz",           team:"COL", flag:"🇨🇴", pos:"FWD", pts:34, own:"12%", price:9},
  {id:12, name:"Rodrygo",             team:"BRA", flag:"🇧🇷", pos:"FWD", pts:34, own:"13%", price:9},
  {id:13, name:"Mikel Oyarzabal",     team:"ESP", flag:"🇪🇸", pos:"FWD", pts:32, own:"16%", price:9},
  {id:14, name:"Darwin Núñez",        team:"URU", flag:"🇺🇾", pos:"FWD", pts:32, own:"13%", price:9},
  {id:15, name:"Kai Havertz",         team:"GER", flag:"🇩🇪", pos:"FWD", pts:31, own:"14%", price:9},
  // MIDFIELDERS
  {id:16, name:"Jude Bellingham",     team:"ENG", flag:"🏴󠁧󠁢󠁥󠁮󠁧󠁿", pos:"MID", pts:38, own:"19%", price:11},
  {id:17, name:"Phil Foden",          team:"ENG", flag:"🏴󠁧󠁢󠁥󠁮󠁧󠁿", pos:"MID", pts:34, own:"17%", price:10},
  {id:18, name:"Pedri",               team:"ESP", flag:"🇪🇸", pos:"MID", pts:34, own:"19%", price:10},
  {id:19, name:"Florian Wirtz",       team:"GER", flag:"🇩🇪", pos:"MID", pts:34, own:"18%", price:10},
  {id:20, name:"James Rodríguez",     team:"COL", flag:"🇨🇴", pos:"MID", pts:30, own:"10%", price:9},
  {id:21, name:"Hakim Ziyech",        team:"MAR", flag:"🇲🇦", pos:"MID", pts:29, own:"11%", price:9},
  {id:22, name:"Enzo Fernández",      team:"ARG", flag:"🇦🇷", pos:"MID", pts:30, own:"16%", price:9},
  {id:23, name:"Takefusa Kubo",       team:"JPN", flag:"🇯🇵", pos:"MID", pts:30, own:"8%",  price:8},
  {id:24, name:"Federico Valverde",   team:"URU", flag:"🇺🇾", pos:"MID", pts:28, own:"10%", price:9},
  {id:25, name:"Rodri",               team:"ESP", flag:"🇪🇸", pos:"MID", pts:28, own:"12%", price:9},
  {id:26, name:"Moisés Caicedo",      team:"ECU", flag:"🇪🇨", pos:"MID", pts:28, own:"8%",  price:8},
  {id:27, name:"Tijjani Reijnders",   team:"NED", flag:"🇳🇱", pos:"MID", pts:26, own:"9%",  price:8},
  {id:28, name:"Sergej M-Savić",      team:"SRB", flag:"🇷🇸", pos:"MID", pts:26, own:"9%",  price:8},
  {id:29, name:"Sadio Mané",          team:"SEN", flag:"🇸🇳", pos:"MID", pts:26, own:"7%",  price:8},
  {id:30, name:"N'Golo Kanté",        team:"FRA", flag:"🇫🇷", pos:"MID", pts:24, own:"9%",  price:8},
  // DEFENDERS
  {id:31, name:"Bukayo Saka",         team:"ENG", flag:"🏴󠁧󠁢󠁥󠁮󠁧󠁿", pos:"DEF", pts:34, own:"21%", price:10},
  {id:32, name:"Achraf Hakimi",       team:"MAR", flag:"🇲🇦", pos:"DEF", pts:22, own:"8%",  price:7},
  {id:33, name:"Marquinhos",          team:"BRA", flag:"🇧🇷", pos:"DEF", pts:24, own:"9%",  price:7},
  {id:34, name:"Virgil van Dijk",     team:"NED", flag:"🇳🇱", pos:"DEF", pts:22, own:"11%", price:7},
  {id:35, name:"Kalidou Koulibaly",   team:"SEN", flag:"🇸🇳", pos:"DEF", pts:20, own:"6%",  price:7},
  {id:36, name:"Pervis Estupiñán",    team:"ECU", flag:"🇪🇨", pos:"DEF", pts:20, own:"6%",  price:6},
  // GOALKEEPERS
  {id:37, name:"Emiliano Martínez",   team:"ARG", flag:"🇦🇷", pos:"GK",  pts:22, own:"11%", price:6},
  {id:38, name:"Yassine Bounou",      team:"MAR", flag:"🇲🇦", pos:"GK",  pts:21, own:"8%",  price:6},
  {id:39, name:"Unai Simón",          team:"ESP", flag:"🇪🇸", pos:"GK",  pts:20, own:"10%", price:6},
  {id:40, name:"Jordan Pickford",     team:"ENG", flag:"🏴󠁧󠁢󠁥󠁮󠁧󠁿", pos:"GK",  pts:18, own:"9%",  price:6},
  {id:41, name:"Manuel Neuer",        team:"GER", flag:"🇩🇪", pos:"GK",  pts:18, own:"7%",  price:6},
];
```

**Budget system:** Total budget = 100 credits. Each player has a price (6–12). The score card shows remaining budget and warns (red) if over budget.

**Auto Best XI logic:** Picks highest `pts` per position slot. 4-3-3 = 1 GK, 4 DEF, 3 MID, 3 FWD. Fill each position with the highest-pts available player for that slot, not already selected.

**"Share Lineup" button:** Opens the Coming Soon modal with label "Share Your Lineup" — this is a placeholder for a future share feature.

**Top Differentials section** (below the builder): 3 hardcoded cards for under-owned picks:
1. Takefusa Kubo · MID · 🇯🇵 · 30 proj pts · 8% owned · "Kubo is the most dangerous player in Group F that nobody is picking. Elite dribbler in tight spaces."
2. Moisés Caicedo · MID · 🇪🇨 · 28 proj pts · 8% owned · "Chelsea's $115M man controls midfield. Under-owned relative to his floor."
3. Luis Díaz · FWD · 🇨🇴 · 34 proj pts · 12% owned · "One of the most explosive wide forwards in the tournament. Criminally under-owned."

**SEO:**
- Title: "World Cup 2026 Fantasy Lineup Builder — Best Picks & Projections | PitchIQ"
- Description: "Build your World Cup 2026 fantasy lineup with AI projections. 40 top players, formation selector, auto Best XI, and differential recommendations."
- Canonical: https://getpitchiq.net/fantasy

---

## PHASE 5 — Update `index.html`

Read the full file before making any edits. Make surgical edits only — do not rewrite sections unnecessarily.

### 5a. Update Nav
Find the `<nav>` element. Add the `.nav-links` div with Picks / Standings / Fantasy links if not already present. Add the nav CSS if not already in the `<style>` block.

### 5b. Link Fixture Cards to Preview Pages
Find the fixtures/upcoming matches section. Wrap each match fixture in an `<a href="/[slug]">` tag (or update existing href="#" to the correct path). Map:
- Brazil vs Morocco → `/brazil-morocco`
- Germany vs Curacao → `/germany-curacao`
- Netherlands vs Japan → `/netherlands-japan`
- Uruguay vs Serbia → `/uruguay-serbia`
- France vs Albania → `/france-albania`
- Spain vs Cape Verde → `/spain-capeverde`
- Argentina vs Peru → `/argentina-peru`
- Colombia vs Ecuador → `/colombia-ecuador`
- England vs Senegal → `/england-senegal`

### 5c. Add CTA to Featured Match Section
In the featured match hero (Brazil vs Morocco), add a green button: `<a href="/brazil-morocco" class="btn-preview">Full Preview & Picks →</a>`

### 5d. Add "View All AI Picks" CTA
After the fixtures section header or at the end of the fixtures section, add:
```html
<a href="/predictions" class="btn-all-picks">View All AI Picks →</a>
```
Style: same as `.btn-preview` — green background, white text, Barlow Condensed, uppercase.

### 5e. Update Footer
Ensure the footer includes links to Picks, Standings, Fantasy, and the Twitter link to @getpitchiq.

---

## PHASE 6 — Add Interactive Date Tabs to Homepage Fixtures

In `index.html`, find the fixtures/scores section. Add a tab bar above the fixtures:

```html
<div class="fix-tabs" role="tablist">
  <button class="fix-tab active" data-filter="all" role="tab" aria-selected="true">All</button>
  <button class="fix-tab" data-filter="2026-06-13" role="tab" aria-selected="false">Jun 13</button>
  <button class="fix-tab" data-filter="2026-06-14" role="tab" aria-selected="false">Jun 14</button>
  <button class="fix-tab" data-filter="2026-06-15" role="tab" aria-selected="false">Jun 15</button>
</div>
```

Add `data-date="2026-06-13"` (or appropriate date) to each fixture card element.

Tab filter JS (add to existing script block):
```javascript
document.querySelectorAll('.fix-tab').forEach(function(tab) {
  tab.addEventListener('click', function() {
    const filter = this.dataset.filter;
    document.querySelectorAll('.fix-tab').forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
    this.classList.add('active');
    this.setAttribute('aria-selected', 'true');
    document.querySelectorAll('[data-date]').forEach(function(card) {
      card.style.display = (filter === 'all' || card.dataset.date === filter) ? '' : 'none';
    });
  });
});
```

Tab CSS:
```css
.fix-tabs { display:flex; gap:6px; margin-bottom:16px; flex-wrap:wrap; }
.fix-tab { font-family:var(--cond); font-size:12px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; padding:6px 14px; border-radius:20px; border:1.5px solid var(--b2); background:transparent; color:var(--t2); cursor:pointer; transition:all .15s; }
.fix-tab:hover { border-color:var(--grn); color:var(--grn); }
.fix-tab.active { background:var(--grn); border-color:var(--grn); color:#fff; }
```

---

## PHASE 7 — Update `sitemap.xml`

Overwrite `/Users/samsonwinz/Claude/Projects/PitchIQ/sitemap.xml` with:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://getpitchiq.net/</loc><changefreq>hourly</changefreq><priority>1.0</priority></url>
  <url><loc>https://getpitchiq.net/predictions</loc><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>https://getpitchiq.net/standings</loc><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>https://getpitchiq.net/fantasy</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/brazil-morocco</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/germany-curacao</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/netherlands-japan</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/spain-capeverde</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/uruguay-serbia</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/france-albania</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/argentina-peru</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/colombia-ecuador</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/england-senegal</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
</urlset>
```

---

## PHASE 8 — Apply Ad Slots Across All New Pages

Use the 3-placement ad structure defined in the "AD SLOT STANDARD" section above. Apply to:
- `uruguay-serbia.html`
- `france-albania.html`
- `argentina-peru.html`
- `england-senegal.html`
- `colombia-ecuador.html`
- `standings.html`
- `predictions.html`
- `fantasy.html`

Confirm they are also present in (already built):
- `brazil-morocco.html`
- `germany-curacao.html`
- `netherlands-japan.html`
- `spain-capeverde.html`

---

## PHASE 9 — Quality Assurance

Run these bash checks and fix any issues found:

```bash
# Set the project path
PROJ="/sessions/busy-exciting-rubin/mnt/PitchIQ"

# 1. Check no page references the old domain pitchiq.com
echo "=== Stale domain references ==="
grep -rl "pitchiq.com" $PROJ/*.html && echo "FAIL: Found pitchiq.com references" || echo "PASS"

# 2. Check every HTML file has a canonical URL
echo "=== Canonical tags ==="
for f in $PROJ/*.html; do
  grep -q 'rel="canonical"' "$f" && echo "PASS: $f" || echo "FAIL: $f missing canonical"
done

# 3. Check every page has Twitter site meta
echo "=== Twitter meta ==="
for f in $PROJ/*.html; do
  grep -q '@getpitchiq' "$f" && echo "PASS: $f" || echo "FAIL: $f missing Twitter meta"
done

# 4. Check every page has AdSense script
echo "=== AdSense script ==="
for f in $PROJ/*.html; do
  [ "$f" = "$PROJ/404.html" ] && continue  # 404 page doesn't need AdSense
  grep -q 'adsbygoogle' "$f" && echo "PASS: $f" || echo "FAIL: $f missing AdSense"
done

# 5. Check every page has Coming Soon modal
echo "=== Coming Soon modal ==="
for f in $PROJ/*.html; do
  grep -q 'csOverlay' "$f" && echo "PASS: $f" || echo "FAIL: $f missing modal"
done

# 6. Check every page has AFF config
echo "=== AFF config ==="
for f in $PROJ/*.html; do
  [ "$f" = "$PROJ/404.html" ] && continue
  [ "$f" = "$PROJ/standings.html" ] && continue  # standings may not have betting links
  grep -q 'var AFF' "$f" && echo "PASS: $f" || echo "WARN: $f missing AFF config"
done

# 7. List all files and sizes
echo "=== File inventory ==="
ls -lh $PROJ/*.html $PROJ/sitemap.xml
```

Fix any FAILs before declaring the build complete.

**Manual review checklist:**
- [ ] `predictions.html` — prediction cards link to correct preview pages
- [ ] `standings.html` — known results (USA 4-1, Mexico 2-0, Korea 2-1, Canada 1-1) display correctly
- [ ] `fantasy.html` — "Auto Best XI" button fills all 11 slots correctly
- [ ] `index.html` — nav has Picks / Standings / Fantasy links
- [ ] `index.html` — fixture cards have date tabs working (clicking Jun 14 hides Jun 13 matches)
- [ ] `sitemap.xml` — all 13 pages are listed
- [ ] No broken internal links (every `href="/page-name"` has a corresponding `.html` file)

---

## COMPLETION REPORT

When all 9 phases are done, output a completion report in this format:

```
=== PITCHIQ OVERNIGHT BUILD — COMPLETE ===

FILES CREATED:
- uruguay-serbia.html      (XXX lines)
- france-albania.html      (XXX lines)
- argentina-peru.html      (XXX lines)
- england-senegal.html     (XXX lines)
- colombia-ecuador.html    (XXX lines)
- standings.html           (XXX lines)
- predictions.html         (XXX lines)
- fantasy.html             (XXX lines)

FILES MODIFIED:
- index.html       — Added nav links, fixture links, date tabs, CTAs
- sitemap.xml      — Updated with 13 pages

TOTAL NEW PAGES: 8
TOTAL PAGES ON SITE: 13 (+ 404 page)
QA CHECKS: X/X passed

ISSUES ENCOUNTERED (if any):
- [list any issues, workarounds applied]

READY TO DEPLOY:
Run in your terminal:
cd ~/Claude/Projects/PitchIQ
git add -A
git commit -m "Overnight build: 8 new pages, standings, predictions hub, fantasy builder, interactive homepage"
git push origin main

Vercel will auto-deploy within ~60 seconds of push.
```

---

## ABSOLUTE RULES (do not break these)

1. **Read before editing.** Use the Read tool on any file before modifying it. Never edit blindly.
2. **No git commands.** User handles all git operations. Do not run git add, commit, or push.
3. **No framework code.** No React, no Vue, no npm install, no build steps. HTML + CSS + vanilla JS only.
4. **No external URLs changed.** Keep all `getpitchiq.net` references as-is. Do not change domains, CDN links, or analytics IDs.
5. **Do not delete existing content.** Only add to or surgically edit existing files. Do not rewrite pages from scratch unless they don't exist yet.
6. **Work in phase order.** Complete Phase 1 fully → Phase 2 → ... → Phase 9. Do not skip phases.
7. **Affiliate links always use data-aff.** Never hardcode a sportsbook URL. Always use `href="#" data-aff="[book]"` and let the AFF config handle the rest.
8. **Entertainment disclaimer on every betting-related page.** Footer must say "Entertainment purposes only · Must be 21+ to bet."
9. **Do not stop and ask questions.** If something is ambiguous, make a reasonable judgment call based on existing pages and keep moving.
