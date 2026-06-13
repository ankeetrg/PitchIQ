# PitchIQ — Claude Code Build Prompt v2
### Runs after overnight v1 build · Verify → Fix → Expand

---

## YOUR IDENTITY & MISSION (same as before)

You are the lead frontend developer for PitchIQ (getpitchiq.net). The v1 overnight build completed 9 phases. Your job now is:

1. **Audit** — verify every v1 phase was executed correctly and completely
2. **Fix** — resolve all known gaps and issues flagged in the v1 completion report
3. **Expand** — build the next batch of content (June 16–17 match pages + player profiles)
4. **Report** — produce a concise, accurate summary of every action taken

Do not skip the audit. Do not ask questions. Make confident decisions and keep moving.

---

## TECH STACK REMINDER

- Pure static HTML, embedded CSS and JS, no build process
- Project at: `/Users/samsonwinz/Claude/Projects/PitchIQ/`
- Bash path: `/sessions/busy-exciting-rubin/mnt/PitchIQ/`
- Design tokens: `--nav:#071D36 --grn:#00963F --bg:#EEF1F6 --surf:#fff --t1:#0F1923 --t2:#3C5168 --r:6px --r2:12px`
- Fonts: Inter (body) + Barlow Condensed (headings/labels) via Google Fonts
- All sportsbook links use `data-aff="draftkings|fanduel|betmgm|caesars"` — never hardcoded URLs
- Template for match pages: `brazil-morocco.html` — read it if you need to verify structure

---

## PHASE A — AUDIT (run first, before touching any files)

Run this bash script and capture every line of output. Fix all FAILs in Phase B.

```bash
PROJ="/sessions/busy-exciting-rubin/mnt/PitchIQ"

echo "=============================="
echo " PITCHIQ FULL SITE AUDIT"
echo "=============================="

# All HTML files in scope
PAGES=$(ls $PROJ/*.html | grep -v "CLAUDE")

echo ""
echo "--- 1. FILE INVENTORY ---"
for f in $PROJ/*.html; do
  lines=$(wc -l < "$f")
  size=$(wc -c < "$f")
  echo "$(basename $f): ${lines} lines, ${size} bytes"
done

echo ""
echo "--- 2. STALE DOMAIN REFERENCES (pitchiq.com) ---"
result=$(grep -rl "pitchiq\.com" $PROJ/*.html 2>/dev/null)
[ -z "$result" ] && echo "PASS: no stale references" || echo "FAIL: $result"

echo ""
echo "--- 3. CANONICAL TAGS ---"
for f in $PAGES; do
  grep -q 'rel="canonical"' "$f" \
    && echo "PASS: $(basename $f) — $(grep -o 'href="[^"]*"' <<< "$(grep canonical "$f")")" \
    || echo "FAIL: $(basename $f) missing canonical"
done

echo ""
echo "--- 4. NAV LINKS (Picks + Standings + Fantasy) ---"
for f in $PAGES; do
  b=$(basename $f)
  [ "$b" = "404.html" ] && continue
  has_picks=$(grep -c '/predictions' "$f" || true)
  has_standings=$(grep -c '/standings' "$f" || true)
  has_fantasy=$(grep -c '/fantasy' "$f" || true)
  [ "$has_picks" -gt 0 ] && p="✓" || p="✗"
  [ "$has_standings" -gt 0 ] && s="✓" || s="✗"
  [ "$has_fantasy" -gt 0 ] && fa="✓" || fa="✗"
  echo "$(basename $f): Picks=$p Standings=$s Fantasy=$fa"
done

echo ""
echo "--- 5. TWITTER META (@getpitchiq) ---"
for f in $PAGES; do
  [ "$(basename $f)" = "404.html" ] && continue
  grep -q '@getpitchiq' "$f" && echo "PASS: $(basename $f)" || echo "FAIL: $(basename $f)"
done

echo ""
echo "--- 6. ADSENSE SCRIPT ---"
for f in $PAGES; do
  [ "$(basename $f)" = "404.html" ] && continue
  grep -q 'adsbygoogle' "$f" && echo "PASS: $(basename $f)" || echo "FAIL: $(basename $f)"
done

echo ""
echo "--- 7. COMING SOON MODAL ---"
for f in $PAGES; do
  grep -q 'csOverlay' "$f" && echo "PASS: $(basename $f)" || echo "FAIL: $(basename $f)"
done

echo ""
echo "--- 8. AFF CONFIG (var AFF) ---"
for f in $PAGES; do
  [ "$(basename $f)" = "404.html" ] && continue
  [ "$(basename $f)" = "standings.html" ] && continue
  grep -q 'var AFF' "$f" && echo "PASS: $(basename $f)" || echo "FAIL: $(basename $f)"
done

echo ""
echo "--- 9. INTERNAL LINK RESOLUTION ---"
# Check every href="/slug" link points to an existing file
for f in $PAGES; do
  links=$(grep -oP 'href="/\K[^"]+' "$f" | grep -v '^#' | grep -v '^http' | sort -u)
  for link in $links; do
    target="$PROJ/${link}.html"
    [ -f "$target" ] && echo "PASS: $link → exists" || echo "FAIL: $(basename $f) links to /$link — no file found"
  done
done | sort -u

echo ""
echo "--- 10. PICKS-RECORD IN SITEMAP ---"
grep -q 'picks-record' "$PROJ/sitemap.xml" && echo "PASS" || echo "FAIL: picks-record.html not in sitemap"

echo ""
echo "--- 11. PREDICTIONS HUB — 9 CARD LINKS ---"
links=$(grep -oP 'href="/\K[^"]+' "$PROJ/predictions.html" | grep -v '^#' | grep -v '^http' | sort -u)
echo "Links found in predictions.html: $links"
expected="brazil-morocco germany-curacao netherlands-japan uruguay-serbia france-albania spain-capeverde argentina-peru colombia-ecuador england-senegal"
for e in $expected; do
  echo "$links" | grep -q "$e" && echo "PASS: $e" || echo "FAIL: $e missing from predictions.html"
done

echo ""
echo "--- 12. FANTASY BUILDER — 41-PLAYER ARRAY ---"
count=$(grep -c '"pos":' "$PROJ/fantasy.html" || true)
[ "$count" -ge 40 ] && echo "PASS: $count players in PLAYERS array" || echo "FAIL: only $count players"

echo ""
echo "--- 13. SITEMAP URL COUNT ---"
count=$(grep -c '<loc>' "$PROJ/sitemap.xml" || true)
echo "Sitemap URLs: $count (expected 14 including picks-record)"

echo ""
echo "--- 14. HOMEPAGE DATE TABS JS ---"
grep -q 'fix-tab' "$PROJ/index.html" && echo "PASS: date tab JS present" || echo "FAIL: date tab JS missing"

echo ""
echo "--- 15. MATCH PAGES — JSON-LD SCHEMA ---"
for f in uruguay-serbia france-albania argentina-peru england-senegal colombia-ecuador; do
  grep -q 'SportsEvent' "$PROJ/${f}.html" && echo "PASS: $f" || echo "FAIL: $f missing JSON-LD"
done

echo ""
echo "=============================="
echo " AUDIT COMPLETE"
echo "=============================="
```

After running, list every FAIL and fix them all in Phase B before proceeding to Phases C and D.

---

## PHASE B — FIX ALL AUDIT FAILURES

Work through every FAIL from Phase A output. The most likely issues from the v1 build report are:

### B1. Add picks-record.html to sitemap.xml

The v1 report confirmed picks-record.html exists and passes QA but is missing from sitemap. Read the current sitemap, then add this entry before `</urlset>`:

```xml
  <url><loc>https://getpitchiq.net/picks-record</loc><changefreq>daily</changefreq><priority>0.7</priority></url>
```

### B2. Fix nav on all match preview pages

The v1 report flagged that match preview pages are missing `/standings` and `/predictions` in their nav bar. They currently only have the brazil-morocco.html nav which predates those pages.

For every match preview page (`brazil-morocco.html`, `germany-curacao.html`, `netherlands-japan.html`, `spain-capeverde.html`, `uruguay-serbia.html`, `france-albania.html`, `argentina-peru.html`, `colombia-ecuador.html`, `england-senegal.html`):

Read each file, find the `<div class="nav-links">` or equivalent nav container, and ensure it contains all 4 links:

```html
<div class="nav-links">
  <a class="nav-link" href="/predictions">Picks</a>
  <a class="nav-link" href="/standings">Standings</a>
  <a class="nav-link" href="/fantasy">Fantasy</a>
  <a class="nav-link" href="/picks-record">Record</a>
</div>
```

Do NOT touch any other part of the file. Surgical edit only.

### B3. Add "Record" nav link to all pages

While fixing B2, add `/picks-record` as a 4th nav link on every page including `index.html`, `standings.html`, `predictions.html`, `fantasy.html`.

### B4. Add picks-record.html to predictions.html sidebar

In `predictions.html` sidebar, add a card:

```html
<div class="card" style="margin-top:16px">
  <div class="card-head">Our Record</div>
  <p style="font-size:13px;color:var(--t2);margin:8px 0">Every pick logged before kickoff. No cherry-picking.</p>
  <a href="/picks-record" style="font-family:var(--cond);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--grn)">View Full Record →</a>
</div>
```

### B5. Fix any broken internal links found in audit

For each FAIL in audit check 9 (internal link resolution), either:
- Create a stub HTML page for the missing slug (redirect to 404 or coming soon)
- Or remove the broken link from the page that references it

### B6. Any other FAILs from the audit

Fix all remaining audit failures before moving to Phase C.

---

## PHASE C — BUILD 5 NEW MATCH PREVIEW PAGES (June 16–17)

Read `brazil-morocco.html` first. Use it as the template. Build these 5 pages.

**Standard reminder for every page:**
- Full `<head>` with SEO, OG, Twitter card, canonical, GA4, AdSense, JSON-LD SportsEvent
- Nav with all 4 links: Picks / Standings / Fantasy / Record
- 3 ad slots (leaderboard + sidebar rectangle + footer banner)
- All data-aff links wired
- Coming Soon modal + AFF config JS
- Footer with © 2026 · 21+ · Responsible Gambling

---

### Page 1: `portugal-indonesia.html`

- Portugal 🇵🇹 vs Indonesia 🇮🇩
- Group I, Match 1 · June 16, 2026 · 12:00 PM ET
- Gillette Stadium, Foxborough, MA (Boston)
- JSON-LD startDate: "2026-06-16T16:00:00Z"

**Odds:**
- Portugal -2000 (DraftKings), Draw +1800 (FanDuel), Indonesia +5000 (BetMGM)
- Over 3.5 Goals: -115 · Under: -115 (Caesars)

**AI Prediction:** 94% Portugal / 5% Draw / 1% Indonesia — Portugal win 4-0 or 5-0

**Prediction chips:** "Portugal -2000 — tournament's heaviest favorite so far" · "Bruno Fernandes leads all European players in key passes/90" · "Indonesia conceded 18 goals in qualifying"

**Analysis:**
- *Portugal:* Bruno Fernandes orchestrates from deep with a passing range that dissects any defensive structure. Diogo Jota and Rafael Leão provide pace and technical quality on the wings. Rúben Dias anchors a defense that kept 9 clean sheets across qualifying. Portugal's greatest risk is complacency in heavy-favorite situations — but their coaching staff has drilled focus in dominant wins specifically for this format.
- *Indonesia:* Making their World Cup debut, Indonesia qualified through AFC's expanded format. An historic achievement for Southeast Asian football. Their squad plays a disciplined low-block with extreme compactness — nine players behind the ball against elite opposition. They hope to limit Portugal to 1-2 goals as a moral victory. Indonesia conceded 18 goals in qualifying but scored 14 — they can play attacking football against lesser opposition.
- *Key matchup:* Bruno Fernandes vs Indonesia's defensive block. Indonesia will attempt to squeeze all space in the final third. Fernandes has elite vision for finding passes through compact defenses — his set-piece delivery will be Portugal's primary weapon.

**Stats comparison:**

| Stat | Portugal | Indonesia |
|---|---|---|
| xG/90 | 3.1 | 0.8 |
| Possession | 64% | 40% |
| Pass accuracy | 92% | 77% |
| Goals conceded/90 | 0.5 | 1.8 |
| Key passes/90 | 13.2 | 4.8 |
| Press success rate | 44% | 21% |

**Betting picks:**
1. Portugal Win to Nil -140 · **AI PICK** · "9 clean sheets in qualifying. Indonesia have not scored against a top-20 ranked team in 8 attempts. Portugal clean sheet is the table-setter play."
2. Over 3.5 Goals -115 · **HOT** · "Portugal avg 3.8 xG/90. Indonesia's defensive block will hold for 60 minutes — then gaps open. Over 3.5 at -115 is exceptional value."
3. Bruno Fernandes Anytime +130 · **HOT** · "Fernandes scored 9 and assisted 14 in qualifying. He operates as a shadow striker here. +130 is undervalued."
4. Portugal -3 Asian Handicap -110 · **VALUE** · "The line is offering Portugal -3 at near-even money. Against a team that's conceded 18 goals in qualifying, this covers easily."

**Fantasy picks:**
1. Bruno Fernandes · MID · 🇵🇹 · 42 proj pts · 26% owned · $11 · "Key pass machine. Goals, assists, and set-piece returns. Captain candidate for Jun 16."
2. Diogo Jota · FWD · 🇵🇹 · 38 proj pts · 22% owned · $10 · "Clinical in the box and gets quality service from Fernandes. Multi-goal game is live."
3. Rafael Leão · FWD · 🇵🇹 · 34 proj pts · 18% owned · $10 · "Pace and power on the left wing. Indonesia will be exposed in wide areas."
4. Rúben Dias · DEF · 🇵🇹 · 22 proj pts · 10% owned · $7 · "Clean sheet bonus + set-piece returns from corners. Under-priced."

**SEO title:** "Portugal vs Indonesia Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Portugal vs Indonesia World Cup 2026 prediction, betting odds & fantasy picks. Group I, June 16 at Gillette Stadium Boston. Portugal -2000 in their tournament opener."
**Canonical:** https://getpitchiq.net/portugal-indonesia

---

### Page 2: `belgium-newzealand.html`

- Belgium 🇧🇪 vs New Zealand 🇳🇿
- Group J, Match 1 · June 16, 2026 · 3:00 PM ET
- Arrowhead Stadium, Kansas City, MO
- JSON-LD startDate: "2026-06-16T19:00:00Z"

**Odds:**
- Belgium -600 (DraftKings), Draw +1000 (FanDuel), New Zealand +1600 (BetMGM)
- Over 2.5 Goals: -140 · Under: +110 (Caesars)

**AI Prediction:** 84% Belgium / 12% Draw / 4% New Zealand — Belgium win 3-0

**Prediction chips:** "Belgium's 'Golden Generation 2.0' — De Bruyne's final World Cup" · "New Zealand qualified through OFC — first time since 2010" · "Kevin De Bruyne has 14 WC qualifying assists — most in UEFA"

**Analysis:**
- *Belgium:* This is widely considered Kevin De Bruyne's last World Cup — at 35 he remains arguably the best creative midfielder in world football. His passing range, vision, and ability to control tempo are all elite. Romelu Lukaku may be polarizing but his goal record (29 international goals in the past 4 years) is undeniable. Belgium's squad is experienced and motivated — their Golden Generation 1.0 underachieved in 2018 and 2022; this generation has something to prove.
- *New Zealand:* The All Whites qualified through the OFC playoff for the first time since 2010 — a historic achievement for Oceania. Their squad is built around professional players competing in Australia's A-League and a handful of European-based players. They will defend deep, be disciplined, and make Belgium work. New Zealand are physical and set-piece dangerous — their best chance of anything is a deflection or corner situation.
- *Key matchup:* De Bruyne vs New Zealand's midfield press. NZ will attempt to close De Bruyne's space quickly. But De Bruyne's release speed (1.2s average for pass under pressure) is faster than virtually any press. He'll find pockets and Belgium will dominate possession.

**Stats comparison:**

| Stat | Belgium | New Zealand |
|---|---|---|
| xG/90 | 2.4 | 0.9 |
| Possession | 59% | 44% |
| Pass accuracy | 88% | 80% |
| Goals conceded/90 | 0.8 | 1.1 |
| Key passes/90 | 11.4 | 5.6 |
| Press success rate | 37% | 26% |

**Betting picks:**
1. Belgium Win to Nil -125 · **AI PICK** · "Belgium kept 7 clean sheets in qualifying. New Zealand failed to score in 3 of 5 OFC playoff matches. Clean sheet is the play."
2. Over 2.5 Goals -140 · **HOT** · "Belgium's attack is too good to be held. De Bruyne + Lukaku vs an OFC qualifier defense — this opens up by the 60th minute."
3. Kevin De Bruyne Anytime +180 · **VALUE** · "De Bruyne scored 4 in qualifying despite playing as a deep midfielder. +180 in a match Belgium should win by 3 undervalues him."
4. Romelu Lukaku Anytime -110 · **HOT** · "Lukaku against a defense ranked outside the top 50 in FIFA rankings. He scores in 73% of matches where Belgium are 3+ goal favorites."

**Fantasy picks:**
1. Kevin De Bruyne · MID · 🇧🇪 · 40 proj pts · 23% owned · $11 · "Final World Cup. Motivated. Elite assist and key pass returns. Solid captain option."
2. Romelu Lukaku · FWD · 🇧🇪 · 36 proj pts · 19% owned · $10 · "Goal machine at this level of opposition. Near-even money to score (-110) is straight value."
3. Dodi Lukebakio · FWD · 🇧🇪 · 28 proj pts · 9% owned · $8 · "Emerging wide forward with pace. Under-owned at 9% for a Belgium starter."
4. Axel Witsel · MID · 🇧🇪 · 22 proj pts · 7% owned · $7 · "Defensive returns + set-piece goal threat. Differential pick."

**SEO title:** "Belgium vs New Zealand Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Belgium vs New Zealand World Cup 2026 prediction, betting odds & fantasy picks. Group J, June 16 at Arrowhead Stadium Kansas City. De Bruyne's final World Cup."
**Canonical:** https://getpitchiq.net/belgium-newzealand

---

### Page 3: `italy-ecuador.html`

- Italy 🇮🇹 vs Ecuador 🇪🇨  
- Wait — Ecuador plays Colombia on June 15. Use a different fixture.

### Page 3 (corrected): `croatia-australia.html`

- Croatia 🇭🇷 vs Australia 🇦🇺
- Group K, Match 1 · June 16, 2026 · 6:00 PM ET
- SoFi Stadium, Inglewood, CA (Los Angeles)
- JSON-LD startDate: "2026-06-16T22:00:00Z"

**Odds:**
- Croatia -140 (DraftKings), Draw +250 (FanDuel), Australia +380 (BetMGM)
- Over 2.5 Goals: +105 · Under: -135 (Caesars)

**AI Prediction:** 51% Croatia / 26% Draw / 23% Australia — Croatia win 1-0

**Prediction chips:** "One of the tightest Group Stage lines at -140" · "Australia's Socceroos reached the 2022 QF — not a pushover" · "Modrić at 41 — playing his final match in a World Cup"

**Analysis:**
- *Croatia:* Luka Modrić at 41 continues to defy time — his reading of the game, distribution, and leadership are irreplaceable. Modrić has announced this is his final World Cup, giving Croatia enormous emotional motivation. Kovačić and Brozović give them elite midfield depth. Ivan Perišić's crossing from the left remains a constant threat. Croatia's weakness is at center forward where they lack a consistent goalscorer — their goals tend to come from midfield runners.
- *Australia:* The Socceroos have punched above their weight consistently — their 2022 quarter-final run shocked everyone. Mathew Leckie remains a dynamic wide forward at 33. The younger generation of Australian football — raised in Bundesliga and Eredivisie academies — has genuine quality. Their pressing game is high-energy and disruptive. Australia will make Croatia work for every chance.
- *Key matchup:* Modrić vs Australia's midfield press. The Socceroos will target Modrić physically — their pressing system tries to isolate him in tight spaces. Modrić's spatial awareness usually finds a way, but in his final World Cup at 41, there may be moments where the press gets to him. This is Australia's best path to disrupting Croatia's rhythm.

**Stats comparison:**

| Stat | Croatia | Australia |
|---|---|---|
| xG/90 | 1.6 | 1.5 |
| Possession | 57% | 52% |
| Pass accuracy | 87% | 83% |
| Goals conceded/90 | 0.9 | 0.9 |
| Key passes/90 | 9.8 | 8.4 |
| Press success rate | 34% | 38% |

**Betting picks:**
1. Under 2.5 Goals -135 · **AI PICK** · "Both teams average under 1.6 goals conceded/90. Croatia's forward line is their weakness. Australia's high-press disrupts Croatia's rhythm. This plays out 1-0 or 1-1."
2. Croatia -0.5 AH -140 · **VALUE** · "Croatia's experience and Modrić's motivation make them the right side at -140. Getting Croatia to win is worth the price."
3. Draw at Half Time +180 · **LONG SHOT** · "This match type — tight, cagey, experienced teams — tends to be goalless at HT. +180 on HT draw is speculative but historically supported."
4. Luka Modrić Anytime +350 · **LONG SHOT** · "Modrić doesn't score often but he's stated this is his last World Cup. He'll want a moment. +350 is strictly value-hunting."

**Fantasy picks:**
1. Luka Modrić · MID · 🇭🇷 · 30 proj pts · 14% owned · $9 · "Emotional motivation + elite key pass returns. Low goal ceiling but assists, tackles, and clean sheet potential."
2. Mathew Leckie · FWD · 🇦🇺 · 26 proj pts · 7% owned · $8 · "Best differential of the day. Australia's most dangerous attacker. If they score, it's Leckie."
3. Marcelo Brozović · MID · 🇭🇷 · 24 proj pts · 8% owned · $8 · "Deep-lying playmaker. Defensive and pass returns. Differential Croatia pick."
4. Ivan Perišić · FWD · 🇭🇷 · 28 proj pts · 11% owned · $9 · "Crossing threat from the left. Goal and assist upside."

**SEO title:** "Croatia vs Australia Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Croatia vs Australia World Cup 2026 prediction, betting odds & fantasy picks. Group K, June 16 at SoFi Stadium LA. Modrić's final World Cup — tight tactical battle."
**Canonical:** https://getpitchiq.net/croatia-australia

---

### Page 4: `brazil-morocco-preview.html` — SKIP (already built as brazil-morocco.html)

### Page 4: `senegal-slovakia.html`

- Senegal 🇸🇳 vs Slovakia 🇸🇰
- Group G, Match 2 · June 17, 2026 · 12:00 PM ET
- AT&T Stadium, Arlington, TX (Dallas)
- JSON-LD startDate: "2026-06-17T16:00:00Z"

**Odds:**
- Senegal -120 (DraftKings), Draw +250 (FanDuel), Slovakia +330 (BetMGM)
- Over 2.5 Goals: +115 · Under: -145 (Caesars)

**AI Prediction:** 45% Senegal / 30% Draw / 25% Slovakia — Senegal win 1-0

**Prediction chips:** "Mané's last realistic chance to reach a World Cup knockout stage" · "Slovakia pulled off one of UEFA qualifying's biggest upsets" · "Under is -145 — sharp money on a cagey affair"

**Analysis:**
- *Senegal:* With England in their group, Senegal need a win here to realistically advance. Mané at 33 carries the weight of a nation — his goals in qualifying revived AFCON dreams that now extend to World Cup ambitions. Calidou Koulibaly organizes a physical, disciplined defensive structure. Senegal's midfield with Idrissa Gueye is hard to break down. They'll need to score — which means Mané needs to find half-a-yard of space against Slovakia's compact block.
- *Slovakia:* Slovakia are tournament darlings — they qualified ahead of Hungary in UEFA and have a team built around discipline, set pieces, and individual quality in Ivan Schranz and Milan Škriniar. Škriniar at center back is genuinely world-class — he competes with the best forwards in Serie A regularly. Slovakia will look to keep it tight, play direct on the counter, and target set pieces where Škriniar and Duda are aerial threats.
- *Key matchup:* Mané vs Škriniar. This is the marquee battle. Mané's movement and finishing are elite — Škriniar's reading of the game and positional discipline are among the best in Europe. Whoever wins this duel likely determines the result.

**Stats comparison:**

| Stat | Senegal | Slovakia |
|---|---|---|
| xG/90 | 1.7 | 1.4 |
| Possession | 52% | 48% |
| Pass accuracy | 82% | 83% |
| Goals conceded/90 | 1.0 | 0.9 |
| Key passes/90 | 7.8 | 7.2 |
| Press success rate | 31% | 29% |

**Betting picks:**
1. Under 2.5 Goals -145 · **AI PICK** · "Both teams are defensively oriented. Senegal need this win but won't open up too early. Slovakia will absorb and counter. Classic tight African/European Group Stage encounter."
2. Senegal -0.5 AH -120 · **VALUE** · "Senegal have better individual quality and greater motivation (England in the group). Getting Senegal to win at -120 is the play."
3. Draw at Half Time +200 · **HOT** · "Slovakia will defend deep first half. Senegal tend to grow into matches. HT draw is historically common in these matchups — +200 is value."
4. Sadio Mané Anytime Scorer +190 · **VALUE** · "Mané scored 6 in AFCON qualifying. Against a team Slovakia's level, he gets chances. +190 for one of Africa's best ever players is strong."

**Fantasy picks:**
1. Sadio Mané · FWD · 🇸🇳 · 30 proj pts · 11% owned · $9 · "High motivation, great odds. Senegal need him today. Best differential forward of the day."
2. Milan Škriniar · DEF · 🇸🇰 · 22 proj pts · 6% owned · $7 · "Elite center back. Clean sheet candidate + aerial threat on set pieces. Deep differential."
3. Idrissa Gueye · MID · 🇸🇳 · 22 proj pts · 7% owned · $7 · "Defensive midfield returns + clean sheet bonus. Consistent floor."
4. Ivan Schranz · FWD · 🇸🇰 · 24 proj pts · 6% owned · $8 · "Slovakia's most dangerous attacker. +330 to win makes him a value pick if you want Slovak exposure."

**SEO title:** "Senegal vs Slovakia Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "Senegal vs Slovakia World Cup 2026 prediction, betting odds & fantasy picks. Group G, June 17 at AT&T Stadium Dallas. Mané's crucial Group Stage test."
**Canonical:** https://getpitchiq.net/senegal-slovakia

---

### Page 5: `usa-bolivia.html`

- USA 🇺🇸 vs Bolivia 🇧🇴
- Group A, Match 2 · June 17, 2026 · 9:00 PM ET
- MetLife Stadium, East Rutherford, NJ (New York)
- JSON-LD startDate: "2026-06-18T01:00:00Z"

**Note:** USA already beat Paraguay 4-1 in Match 1. This is their second group game. MetLife is the hometown crowd advantage.

**Odds:**
- USA -600 (DraftKings), Draw +1100 (FanDuel), Bolivia +2000 (BetMGM)
- Over 2.5 Goals: -130 · Under: +100 (Caesars)

**AI Prediction:** 87% USA / 10% Draw / 3% Bolivia — USA win 3-0

**Prediction chips:** "USA off a 4-1 win — momentum + home crowd at MetLife" · "Bolivia conceded 24 goals in CONMEBOL qualifying" · "Christian Pulisic leads USA with 4 goals in this tournament"

**Analysis:**
- *USA:* Coming off a statement 4-1 opening win, the US brings home energy to MetLife — one of the largest football crowds in American sports history will be in the stands. Christian Pulisic continues to prove he belongs among the world's elite attackers. Weston McKennie's box-to-box runs provide the engine in midfield. The USA's high-press system, which overwhelmed Paraguay in Match 1, should be equally effective against Bolivia's slower-paced buildup.
- *Bolivia:* Bolivia's altitude advantage — their home in La Paz at 3,640m is the highest major stadium in world football — doesn't apply at sea level MetLife. They struggled in CONMEBOL qualifying, conceding 24 goals. Their best performances came against weaker opponents. Against a USA side riding high confidence, this is an extremely difficult task. Bolivia's goal will be to keep it respectable and not concede 4+.
- *Key matchup:* Pulisic vs Bolivia's right back. Bolivia's defensive vulnerability is in wide areas — Pulisic's direct dribbling and crossing ability from the left will target this throughout. He created 3 chances in Match 1 — expect that volume to continue.

**Stats comparison:**

| Stat | USA | Bolivia |
|---|---|---|
| xG/90 | 2.8 | 0.7 |
| Possession | 58% | 42% |
| Pass accuracy | 87% | 76% |
| Goals conceded/90 | 0.8 | 2.4 |
| Key passes/90 | 10.6 | 4.2 |
| Press success rate | 39% | 20% |

**Betting picks:**
1. USA Win to Nil -120 · **AI PICK** · "Bolivia failed to score in 6 of 10 CONMEBOL qualifying matches. USA kept a clean sheet in their last 3 home internationals. Strong play."
2. USA -2 Asian Handicap -115 · **HOT** · "USA beat Paraguay 4-1 in Match 1. Bolivia are significantly weaker than Paraguay. USA -2 at -115 is the obvious play."
3. Christian Pulisic Anytime +150 · **HOT** · "Pulisic is the USA's best player and most direct route to goal. Against Bolivia's defensive quality, he scores. +150 for the US captain is strong value."
4. Over 2.5 Goals -130 · **VALUE** · "USA scored 4 in Match 1. Bolivia conceded 24 in qualifying. This is a comfortable win for the hosts — the over covers early."

**Fantasy picks:**
1. Christian Pulisic · MID/FWD · 🇺🇸 · 40 proj pts · 24% owned · $11 · "Home crowd. Riding form. USA's engine. Top US captain option."
2. Weston McKennie · MID · 🇺🇸 · 30 proj pts · 14% owned · $9 · "Box-to-box returns, goal threat from deep. Consistent performer in the system."
3. Ricardo Pepi · FWD · 🇺🇸 · 28 proj pts · 12% owned · $9 · "Target man who benefits from Pulisic's creativity. Strong play against weak defense."
4. Yunus Musah · MID · 🇺🇸 · 24 proj pts · 9% owned · $8 · "Underrated presser. Defensive and offensive returns. Home-field differential."

**SEO title:** "USA vs Bolivia Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ"
**SEO description:** "USA vs Bolivia World Cup 2026 prediction, betting odds & fantasy picks. Group A, June 17 at MetLife Stadium New York. USA riding 4-1 momentum in hometown crowd."
**Canonical:** https://getpitchiq.net/usa-bolivia

---

## PHASE D — UPDATE SITEMAP WITH ALL NEW PAGES

After Phase C is complete, overwrite `/sessions/busy-exciting-rubin/mnt/PitchIQ/sitemap.xml` with:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://getpitchiq.net/</loc><changefreq>hourly</changefreq><priority>1.0</priority></url>
  <url><loc>https://getpitchiq.net/predictions</loc><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>https://getpitchiq.net/standings</loc><changefreq>daily</changefreq><priority>0.9</priority></url>
  <url><loc>https://getpitchiq.net/fantasy</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/picks-record</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/brazil-morocco</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/germany-curacao</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/netherlands-japan</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/spain-capeverde</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/uruguay-serbia</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/france-albania</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/argentina-peru</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/colombia-ecuador</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/england-senegal</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/portugal-indonesia</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/belgium-newzealand</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/croatia-australia</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/senegal-slovakia</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
  <url><loc>https://getpitchiq.net/usa-bolivia</loc><changefreq>daily</changefreq><priority>0.8</priority></url>
</urlset>
```

---

## PHASE E — ADD NEW PAGES TO PREDICTIONS HUB

Open `predictions.html`. Add 5 new prediction cards for the June 16–17 matches. Follow the exact same card structure as the existing 9 cards. Add them after the June 15 section with a new date group heading if the page uses date grouping, otherwise just append at the end of the grid before the sidebar.

New cards to add:

```
Portugal vs Indonesia · Jun 16 12PM · Gillette Stadium Boston · Group I · 94/5/1 · "Portugal Win to Nil -140" · AI PICK · /portugal-indonesia
Belgium vs New Zealand · Jun 16 3PM · Arrowhead Stadium KC · Group J · 84/12/4 · "Belgium Win to Nil -125" · AI PICK · /belgium-newzealand
Croatia vs Australia · Jun 16 6PM · SoFi Stadium LA · Group K · 51/26/23 · "Under 2.5 Goals -135" · AI PICK · /croatia-australia
Senegal vs Slovakia · Jun 17 12PM · AT&T Stadium Dallas · Group G · 45/30/25 · "Under 2.5 Goals -145" · AI PICK · /senegal-slovakia
USA vs Bolivia · Jun 17 9PM · MetLife Stadium NY · Group A · 87/10/3 · "USA Win to Nil -120" · AI PICK · /usa-bolivia
```

Also add a "Jun 16" and "Jun 17" filter button to the tab bar in predictions.html.

---

## PHASE F — FINAL AUDIT (RE-RUN)

Run the Phase A audit script again. Every check must show PASS. Fix any remaining failures.

Then run this additional check on the new pages:

```bash
PROJ="/sessions/busy-exciting-rubin/mnt/PitchIQ"
NEW_PAGES="portugal-indonesia belgium-newzealand croatia-australia senegal-slovakia usa-bolivia"

echo "--- NEW PAGE CHECKS ---"
for page in $NEW_PAGES; do
  f="$PROJ/${page}.html"
  [ -f "$f" ] || { echo "FAIL: $f does not exist"; continue; }
  grep -q 'rel="canonical"' "$f" && echo "PASS canonical: $page" || echo "FAIL canonical: $page"
  grep -q 'SportsEvent' "$f" && echo "PASS JSON-LD: $page" || echo "FAIL JSON-LD: $page"
  grep -q '/standings' "$f" && echo "PASS nav-standings: $page" || echo "FAIL nav-standings: $page"
  grep -q '/predictions' "$f" && echo "PASS nav-predictions: $page" || echo "FAIL nav-predictions: $page"
  grep -q '/picks-record' "$f" && echo "PASS nav-record: $page" || echo "FAIL nav-record: $page"
  grep -q 'adsbygoogle' "$f" && echo "PASS adsense: $page" || echo "FAIL adsense: $page"
  grep -q 'csOverlay' "$f" && echo "PASS modal: $page" || echo "FAIL modal: $page"
  grep -q 'var AFF' "$f" && echo "PASS aff: $page" || echo "FAIL aff: $page"
  lines=$(wc -l < "$f")
  echo "SIZE: $page = $lines lines"
  echo "---"
done
```

---

## COMPLETION REPORT FORMAT

Output this exact structure when all phases are done:

```
======================================
 PITCHIQ BUILD v2 — COMPLETE
======================================

PHASE A — AUDIT RESULTS
  Checks run: [N]
  Passed: [N]
  Failed: [N]
  Failures found: [list each one]

PHASE B — FIXES APPLIED
  [List every fix made, one line each, e.g.:]
  - Added /picks-record to sitemap.xml
  - Added Standings + Predictions nav links to 9 match preview pages
  - Added Record nav link to all 14 pages
  - [etc.]

PHASE C — NEW PAGES CREATED
  - portugal-indonesia.html    [N lines]
  - belgium-newzealand.html    [N lines]
  - croatia-australia.html     [N lines]
  - senegal-slovakia.html      [N lines]
  - usa-bolivia.html           [N lines]

PHASE D — SITEMAP UPDATED
  Total URLs: 19

PHASE E — PREDICTIONS HUB UPDATED
  Cards added: 5 (Jun 16-17)
  Filter tabs added: Jun 16, Jun 17

PHASE F — FINAL AUDIT
  All checks: PASS / [list any remaining issues]

FULL FILE INVENTORY (post-build)
  [filename] — [lines] lines — [size]
  [for every .html file in the project]

DEPLOY COMMAND
  cd ~/Claude/Projects/PitchIQ
  git add -A
  git commit -m "v2 build: 5 new match pages, nav fixes, audit pass, sitemap update"
  git push origin main

NEXT BUILD PRIORITIES
  1. [most important thing to build next]
  2. [second priority]
  3. [third priority]
```

---

## ABSOLUTE RULES (unchanged from v1)

1. Read before editing — always
2. No git commands — user handles deploys
3. No frameworks — pure HTML/CSS/JS only
4. Never hardcode sportsbook URLs — use data-aff + AFF config
5. Every betting page needs the 21+ / entertainment disclaimer
6. Do not stop and ask questions — make the call and move on
7. Work phases in order: A → B → C → D → E → F
8. The completion report must be concise and accurate — list EVERY file touched and EVERY action taken
