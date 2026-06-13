# PitchIQ — Affiliate Link Activation Prompt
## For Claude Code · Run when you have approved affiliate URLs

---

## CONTEXT

PitchIQ (https://getpitchiq.net) is a static HTML sports intelligence site.
Every page contains an `AFF` config object and sportsbook comparison cards.
Currently all affiliate URLs are set to `'#'` — clicks fall back to a Coming
Soon modal. This prompt replaces them with your live tracking URLs.

There are also 4 bonus strings to update per book (shown in the odds cards).

---

## YOUR APPROVED AFFILIATE LINKS

Fill these in before running:

```
DRAFTKINGS_URL  = "[PASTE YOUR DRAFTKINGS TRACKING URL HERE]"
FANDUEL_URL     = "[PASTE YOUR FANDUEL TRACKING URL HERE]"
BETMGM_URL      = "[PASTE YOUR BETMGM TRACKING URL HERE — or leave # if pending]"
CAESARS_URL     = "[PASTE YOUR CAESARS TRACKING URL HERE — or leave # if pending]"

DRAFTKINGS_BONUS = "Bet $5, Get $200"
FANDUEL_BONUS    = "$200 Bonus Bets"
BETMGM_BONUS     = "Up to $1,500 Back"
CAESARS_BONUS    = "$1,000 First Bet"
```

> Bonus copy sometimes changes when you get approved — check your affiliate
> dashboard for the current offer string and update above before running.

---

## PHASE 1 — AUDIT (dry run first)

Run these checks before touching any files:

```bash
cd ~/Claude/Projects/PitchIQ

# Count how many AFF entries are still '#' (should be 4 per page × ~20 pages)
grep -rc "draftkings: '#'" . --include="*.html" | grep -v ":0"
grep -rc "fanduel:    '#'" . --include="*.html" | grep -v ":0"

# List every file that has AFF config
grep -rl "var AFF = {" . --include="*.html"

# Confirm total file count
ls *.html | wc -l
```

Expected: ~20 HTML files all showing 1 match each for the AFF pattern.
If any file shows 0, note it — it may need manual review.

---

## PHASE 2 — UPDATE AFF CONFIG (all HTML files)

Use Python to do a precise, safe replacement across every `.html` file.
Do NOT use sed — the URLs may contain characters that break sed patterns.

Write and run this script:

```python
import os, re, glob

# ── FILL THESE IN ──────────────────────────────────────────────────────────
DK  = "[DRAFTKINGS_URL]"
FD  = "[FANDUEL_URL]"
MGM = "[BETMGM_URL]"      # use '#' if not yet approved
CES = "[CAESARS_URL]"     # use '#' if not yet approved

DK_BONUS  = "Bet $5, Get $200"
FD_BONUS  = "$200 Bonus Bets"
MGM_BONUS = "Up to $1,500 Back"
CES_BONUS = "$1,000 First Bet"
# ───────────────────────────────────────────────────────────────────────────

OLD_AFF = """var AFF = {
  draftkings: '#',
  fanduel:    '#',
  betmgm:     '#',
  caesars:    '#',
};"""

NEW_AFF = f"""var AFF = {{
  draftkings: '{DK}',
  fanduel:    '{FD}',
  betmgm:     '{MGM}',
  caesars:    '{CES}',
}};"""

updated = []
skipped = []

for path in glob.glob("*.html"):
    with open(path, "r") as f:
        content = f.read()

    if "var AFF = {" not in content:
        skipped.append(path)
        continue

    new_content = content.replace(OLD_AFF, NEW_AFF)

    if new_content == content:
        skipped.append(f"{path} (no exact match — check manually)")
        continue

    with open(path, "w") as f:
        f.write(new_content)
    updated.append(path)

print(f"\n✅ Updated {len(updated)} files:")
for f in sorted(updated): print(f"   {f}")
if skipped:
    print(f"\n⚠️  Skipped {len(skipped)} files:")
    for f in skipped: print(f"   {f}")
```

Save as `activate_affiliates.py` and run: `python3 activate_affiliates.py`

---

## PHASE 3 — UPDATE BONUS COPY IN SPORTSBOOK CARDS

Each match page has a sportsbook comparison card showing bonus text.
Update if your approved bonuses differ from the defaults:

```python
import glob

# Map: old bonus text → new bonus text per book
# Only add entries where the text actually changed
REPLACEMENTS = {
    # "Bet $5, Get $200":   "Bet $5, Get $200",   # DraftKings — same, skip
    # "$200 Bonus Bets":    "$200 Bonus Bets",    # FanDuel — same, skip
    # "Up to $1,500 Back":  "Up to $1,500 Back",  # BetMGM — same, skip
    # "$1,000 First Bet":   "$1,000 First Bet",   # Caesars — same, skip
}

if not REPLACEMENTS:
    print("No bonus copy changes needed — all match defaults.")
else:
    for path in glob.glob("*.html"):
        with open(path) as f:
            content = f.read()
        changed = False
        for old, new in REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
                changed = True
        if changed:
            with open(path, "w") as f:
                f.write(content)
            print(f"Updated bonus copy: {path}")
```

---

## PHASE 4 — UPDATE href ATTRIBUTES ON SPORTSBOOK ROWS

The sportsbook rows use `href="#" data-aff="draftkings"` — the JS intercepts
the click and opens the correct URL from AFF config. This already works once
Phase 2 is done. No href changes needed.

However — confirm the JS click handler is still intact on a sample page:

```bash
grep -A5 "data-aff" brazil-morocco.html | head -30
grep "AFF\[" brazil-morocco.html | head -5
```

Expected output: JS that reads `AFF[aff]` and opens the URL.

---

## PHASE 5 — VERIFY

```bash
# Confirm '#' is gone from AFF configs
grep -r "draftkings: '#'" . --include="*.html"
# Should return: nothing (0 matches)

# Confirm your real URL is present
grep -c "draftkings:" index.html
# Should return: 1

# Spot-check one file
grep "AFF = {" -A5 brazil-morocco.html
```

---

## PHASE 6 — REMOVE COMING SOON MODAL FOR APPROVED BOOKS (optional)

Once DraftKings and FanDuel are live, users should go directly to the
sportsbook — not see the Coming Soon modal. The modal fires because `AFF[book]`
was `'#'`. After Phase 2 updates AFF with real URLs, the modal will no longer
fire for those books automatically.

Confirm by checking the click handler logic:

```bash
grep -A10 "data-aff" brazil-morocco.html | grep -A8 "addEventListener"
```

If the handler checks `if (!url || url === '#')` before opening — it's already
smart. If it always opens the modal AND the URL, look for the condition and
confirm real URLs bypass it.

---

## PHASE 7 — COMMIT & DEPLOY

```bash
cd ~/Claude/Projects/PitchIQ
git add -A
git commit -m "Activate affiliate links: DraftKings + FanDuel live"
git push origin main
```

Vercel auto-deploys on push. Changes are live in ~60 seconds.

---

## POST-DEPLOY CHECKLIST

- [ ] Visit getpitchiq.net/brazil-morocco → click "DraftKings" → goes to DK (not modal)
- [ ] Visit getpitchiq.net/brazil-morocco → click "FanDuel" → goes to FD (not modal)  
- [ ] Check affiliate dashboards 24h later for click tracking
- [ ] Update BetMGM + Caesars URLs when those approvals arrive (re-run this prompt)

---

## NOTES

- `rel="noopener sponsored"` is already on all affiliate links (correct for SEO)
- If DraftKings/FanDuel send geo-targeted URLs per state, use the generic
  national URL for now — geo-routing is handled on their end
- Keep this file — re-run Phase 2 anytime a book updates their tracking URL
