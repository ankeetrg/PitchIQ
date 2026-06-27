#!/usr/bin/env python3
"""
PitchIQ — Live odds updater
Source: The Odds API (https://the-odds-api.com)
API key: set ODDS_API_KEY in .env.local or as environment variable

# LEGAL-REVIEW-REQUIRED
# Odds displayed for informational purposes only.
# Gambling may be illegal in your jurisdiction.

Usage:
    python3 update_odds.py                    # update all upcoming match pages
    python3 update_odds.py --dry              # print new odds, don't write
    python3 update_odds.py brazil-morocco     # update one match only

Cost: 1 API request per run (fetches all events at once).
Free tier: 500 requests/month. Use sparingly — once or twice per match day is plenty.

Requires:
    ODDS_API_KEY environment variable (get free key at the-odds-api.com)
"""

import json, sys, re, os, urllib.request, urllib.error, subprocess
from datetime import datetime, timezone

PROJ      = os.path.dirname(os.path.abspath(__file__))
DRY       = '--dry' in sys.argv
TARGET    = next((a for a in sys.argv[1:] if not a.startswith('--')), None)


def load_dotenv():
    path = os.path.join(PROJ, '.env.local')
    if not os.path.exists(path):
        return
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_dotenv()

# ── API config — loaded from config.py (one place to change when migrating) ───
from config import active_provider, api_key as _get_api_key

_cfg = active_provider()
API_KEY       = _get_api_key()
SPORT_KEYS    = _cfg.get('sport_keys', ['soccer_fifa_world_cup_2026'])
ODDS_BASE     = _cfg['base_url'] + '/sports/{sport}/odds'
PREFERRED_BOOKS = _cfg.get('preferred_books', ['draftkings', 'fanduel', 'betmgm'])

# ── Name normalization ────────────────────────────────────────────────────────

NAME_MAP = {
    'ir iran':           'iran',
    'türkiye':           'turkey',
    "côte d'ivoire":     'ivory coast',
    'korea republic':    'korea republic',
    'south korea':       'korea republic',
    'dr congo':          'dr congo',
    'congo dr':          'dr congo',
    'bosnia and herzegovina': 'bosnia',
    'bosnia & herzegovina':   'bosnia',
    'united states':     'usa',
    'curacao':           'curaçao',
    'cape verde islands':'cape verde',
    'new zealand':       'new zealand',
    'czech republic':    'czechia',
}

FLAG_RE = re.compile(r'[\U0001F1E0-\U0001F1FF]{2}')

def normalize(name):
    name = FLAG_RE.sub('', name).strip().lower()
    return NAME_MAP.get(name, name)


# ── Odds API fetch ────────────────────────────────────────────────────────────

def fetch_odds():
    """Fetch h2h + totals odds for all WC events. Returns list of event dicts."""
    if not API_KEY:
        print('\n  ERROR: ODDS_API_KEY not set.')
        print('  Get a free key at https://the-odds-api.com and set it in your environment:')
        print('    export ODDS_API_KEY=your_key_here')
        print('  Or add it to .env.local: ODDS_API_KEY=your_key_here\n')
        sys.exit(1)

    last_error = None
    for sport in SPORT_KEYS:
        url = (
            f'{ODDS_BASE.format(sport=sport)}'
            f'?apiKey={API_KEY}'
            f'&regions=us'
            f'&markets=h2h,totals'
            f'&oddsFormat=american'
            f'&dateFormat=iso'
        )
        print(f'  Trying sport key: {sport}')
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                remaining = r.headers.get('x-requests-remaining', '?')
                print(f'  ✓ Success — {remaining} requests remaining this month')
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            if e.code == 401:
                print(f'\n  ERROR: Invalid API key. Check ODDS_API_KEY.')
                sys.exit(1)
            elif e.code == 422:
                print(f'  Sport key not found, trying next...')
                last_error = f'HTTP {e.code}: {body}'
                continue
            elif e.code == 429:
                print(f'\n  ERROR: Monthly request quota exceeded (free tier = 500 req/mo).')
                sys.exit(1)
            else:
                last_error = f'HTTP {e.code}: {body}'
                print(f'  HTTP {e.code} — trying next')
        except urllib.error.URLError as e:
            last_error = str(e.reason)
            print(f'  Connection error: {e.reason}')

    print(f'\n  ERROR: All sport keys failed. Last error: {last_error}')
    sys.exit(1)


def find_odds_event(home_name, away_name, events):
    """Find a matching event from the Odds API response."""
    h = normalize(home_name)
    a = normalize(away_name)
    for ev in events:
        eh = normalize(ev.get('home_team', ''))
        ea = normalize(ev.get('away_team', ''))
        if (eh == h and ea == a) or (eh == a and ea == h):
            return ev
    return None


def extract_odds(event, home_name, away_name):
    """
    Extract consensus h2h and totals odds from an Odds API event.
    Returns dict with home_ml, draw_ml, away_ml, ou_line, ou_over, ou_under (all strings).
    Averages across all available bookmakers for consensus lines.
    """
    h = normalize(home_name)

    h2h_home, h2h_draw, h2h_away = [], [], []
    tot_line, tot_over, tot_under = [], [], []

    for bm in event.get('bookmakers', []):
        for mkt in bm.get('markets', []):
            key = mkt.get('key', '')

            if key == 'h2h':
                for oc in mkt.get('outcomes', []):
                    n = normalize(oc.get('name', ''))
                    p = oc.get('price', 0)
                    if n == 'draw':
                        h2h_draw.append(p)
                    elif n == h:
                        h2h_home.append(p)
                    else:
                        h2h_away.append(p)

            elif key == 'totals':
                for oc in mkt.get('outcomes', []):
                    n     = oc.get('name', '').lower()
                    p     = oc.get('price', 0)
                    point = oc.get('point', 2.5)
                    if n == 'over':
                        tot_over.append(p)
                        tot_line.append(point)
                    elif n == 'under':
                        tot_under.append(p)

    def avg_to_ml(prices):
        if not prices:
            return None
        avg = sum(prices) / len(prices)
        return f'+{int(avg)}' if avg >= 0 else str(int(avg))

    def avg_line(lines):
        if not lines:
            return 2.5
        # Use most common line
        from collections import Counter
        return Counter(lines).most_common(1)[0][0]

    home_ml = avg_to_ml(h2h_home)
    draw_ml = avg_to_ml(h2h_draw)
    away_ml = avg_to_ml(h2h_away)
    ou_over = avg_to_ml(tot_over)
    ou_under= avg_to_ml(tot_under)
    ou_line = avg_line(tot_line)

    if not all([home_ml, draw_ml, away_ml]):
        return None

    return {
        'home_ml':  home_ml,
        'draw_ml':  draw_ml,
        'away_ml':  away_ml,
        'ou_line':  str(ou_line),
        'ou_over':  ou_over  or '-110',
        'ou_under': ou_under or '-110',
    }


# ── HTML update ───────────────────────────────────────────────────────────────

def fmt_ml(ml_str):
    """Ensure moneyline string has explicit +/- prefix."""
    if not ml_str:
        return ml_str
    try:
        val = int(ml_str)
        return f'+{val}' if val > 0 else str(val)
    except ValueError:
        return ml_str


def update_match_html(slug, home, away, odds):
    """Update a single match page with new odds. Returns True if file was modified."""
    path = os.path.join(PROJ, f'{slug}.html')
    if not os.path.exists(path):
        print(f'    ⚠ File not found: {slug}.html — skipping')
        return False

    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Determine favorite (most negative / smallest positive ML)
    def ml_val(s):
        try:
            return int(s)
        except (TypeError, ValueError):
            return 0

    home_v = ml_val(odds['home_ml'])
    away_v = ml_val(odds['away_ml'])
    fav_name = home if home_v < away_v else away
    fav_ml   = odds['home_ml'] if home_v < away_v else odds['away_ml']

    home_cls = 'fav' if home_v <= 0 and (away_v > 0 or home_v < away_v) else 'dog'
    away_cls = 'fav' if away_v <= 0 and (home_v > 0 or away_v < home_v) else 'dog'

    updated = html

    # ── Main odds strip ───────────────────────────────────────────────────────
    # Pattern: <div class="odd-label">X Win</div>\n<div class="odd-val ...">VAL</div>
    def replace_odds_val(html_in, label_content, new_val, new_cls=None):
        """Find the odd-val div immediately after a given odd-label div and replace it."""
        pattern = (
            r'(<div class="odd-label">' + re.escape(label_content) + r'</div>\s*)'
            r'<div class="odd-val (?:fav|dog)">[-+]?\d+</div>'
        )
        cls = f' {new_cls}' if new_cls else ''
        repl = rf'\g<1><div class="odd-val{cls}">{new_val}</div>'
        return re.sub(pattern, repl, html_in, count=1)

    updated = replace_odds_val(updated, f'{home} Win', fmt_ml(odds['home_ml']), home_cls)
    updated = replace_odds_val(updated, 'Draw',        fmt_ml(odds['draw_ml']), 'dog')
    updated = replace_odds_val(updated, f'{away} Win', fmt_ml(odds['away_ml']), away_cls)
    updated = replace_odds_val(updated, f'Over {odds["ou_line"]} Goals',  fmt_ml(odds['ou_over']),  'dog')
    updated = replace_odds_val(updated, f'Under {odds["ou_line"]} Goals', fmt_ml(odds['ou_under']), 'dog')

    # Also try generic "Over X.X Goals" patterns if the line differs from stored
    # (handles case where ou_line changed)
    for direction, key in [('Over', 'ou_over'), ('Under', 'ou_under')]:
        pattern = (
            rf'(<div class="odd-label">{direction} \d+\.?\d* Goals</div>\s*)'
            r'<div class="odd-val (?:fav|dog)">[-+]?\d+</div>'
        )
        repl = rf'\g<1><div class="odd-val dog">{fmt_ml(odds[key])}</div>'
        updated = re.sub(pattern, repl, updated, count=1)

    # ── Sidebar: Best Odds header ─────────────────────────────────────────────
    updated = re.sub(
        r'(<div class="sc-head">Best Odds: )[^<]+(</div>)',
        rf'\g<1>{fav_name} Win\g<2>',
        updated
    )

    # ── Sidebar: sb-book-odds divs (all 4 show same fav_ml) ──────────────────
    sb_section_pattern = re.compile(
        r'(<!-- Sportsbook comparison -->.*?</div>\s*</div>\s*</div>)',
        re.DOTALL
    )
    def update_sb_odds(sb_html):
        return re.sub(
            r'(<div class="sb-book-odds">)[-+]?\d+(</div>)',
            rf'\g<1>{fmt_ml(fav_ml)}\g<2>',
            sb_html
        )
    updated = sb_section_pattern.sub(
        lambda m: update_sb_odds(m.group(0)),
        updated
    )

    if updated == html:
        print(f'    ~ {slug}.html — no changes (odds may already match or labels not found)')
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated)

    print(f'    ✓ {slug}.html — {home} {fmt_ml(odds["home_ml"])} / Draw {fmt_ml(odds["draw_ml"])} / {away} {fmt_ml(odds["away_ml"])}  |  O/U {odds["ou_line"]}')
    return True


# ── Load match slugs from match_data ─────────────────────────────────────────

def load_matches():
    """Import MATCHES list from match_data.py."""
    import importlib.util
    spec   = importlib.util.spec_from_file_location('match_data', os.path.join(PROJ, 'match_data.py'))
    mod    = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MATCHES


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'\nPitchIQ odds updater — {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}\n')
    print('⚠ LEGAL-REVIEW-REQUIRED: Odds displayed for informational purposes only.\n')

    print('Step 1: Fetch current odds from The Odds API...')
    events = fetch_odds()
    print(f'  {len(events)} events returned\n')

    print('Step 2: Load match list from match_data.py...')
    try:
        matches = load_matches()
    except Exception as e:
        print(f'  ERROR loading match_data.py: {e}')
        sys.exit(1)
    print(f'  {len(matches)} matches in database\n')

    # Filter to target if specified
    if TARGET:
        matches = [m for m in matches if m['slug'] == TARGET]
        if not matches:
            print(f'  ERROR: slug "{TARGET}" not found in match_data.py')
            sys.exit(1)

    # Filter to upcoming matches only (skip completed)
    now = datetime.now(timezone.utc)
    # We'll try to update all matches that still have an odds listing in the API
    # (API only returns future events, so any match found there is upcoming)

    event_home_away = {(normalize(e['home_team']), normalize(e['away_team'])): e for e in events}
    event_home_away.update({(normalize(e['away_team']), normalize(e['home_team'])): e for e in events})

    print('Step 3: Update match pages...\n')
    updated_count = 0
    skipped_count = 0

    for m in matches:
        slug = m['slug']
        home = m['home']
        away = m['away']

        ev = find_odds_event(home, away, events)
        if not ev:
            if TARGET:
                print(f'    ⚠ No odds found for {slug} — match may be completed or not yet listed')
            skipped_count += 1
            continue

        new_odds = extract_odds(ev, home, away)
        if not new_odds:
            print(f'    ⚠ {slug} — could not parse odds from API response')
            skipped_count += 1
            continue

        if DRY:
            h = fmt_ml(new_odds['home_ml'])
            d = fmt_ml(new_odds['draw_ml'])
            a = fmt_ml(new_odds['away_ml'])
            o = fmt_ml(new_odds['ou_over'])
            u = fmt_ml(new_odds['ou_under'])
            ln= new_odds['ou_line']
            print(f'  [DRY] {slug}: {home} {h} / Draw {d} / {away} {a}  |  O{ln} {o} / U{ln} {u}')
            updated_count += 1
        else:
            changed = update_match_html(slug, home, away, new_odds)
            if changed:
                updated_count += 1

    print(f'\n  {updated_count} pages {"would be " if DRY else ""}updated, {skipped_count} skipped (completed or not listed)')

    if not DRY and updated_count > 0:
        print('\nDone. Push when ready:')
        print('  git add *.html && git commit -m "odds update" && git push')


if __name__ == '__main__':
    main()
