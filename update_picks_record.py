#!/usr/bin/env python3
"""
PitchIQ — Picks record updater
Source: ESPN hidden JSON API (no key required)

Usage:
    python3 update_picks_record.py          # fetch results + update picks-record.html
    python3 update_picks_record.py --dry    # show grades only, don't write

Automatically grades completed picks and updates W/L/P/ROI stats.
Player anytime scorer picks require scorer data from ESPN match summaries.
If scorer data is unavailable, those picks stay pending with a warning.

Run after each match day.
"""

import json, sys, re, os, urllib.request, urllib.error
from datetime import datetime

PROJ      = os.path.dirname(os.path.abspath(__file__))
DRY       = '--dry' in sys.argv
HTML_PATH = os.path.join(PROJ, 'picks-record.html')

SCOREBOARD_BASE = 'https://site.api.espn.com/apis/site/v2/sports/soccer/FIFA.WORLD/scoreboard'
SUMMARY_BASE    = 'https://site.api.espn.com/apis/site/v2/sports/soccer/FIFA.WORLD/summary?event={eid}'

# ESPN name → PitchIQ name (and vice-versa normalization target)
NAME_MAP = {
    'ir iran':           'iran',
    'türkiye':           'turkey',
    'turkey':            'turkey',
    "côte d'ivoire":     'ivory coast',
    'korea republic':    'korea',
    'south korea':       'korea',
    'dr congo':          'dr congo',
    'congo dr':          'dr congo',
    'bosnia and herzegovina': 'bosnia',
    'bosnia & herzegovina':   'bosnia',
    'united states':     'usa',
    'curacao':           'curaçao',
    'cape verde islands':'cape verde',
    'new zealand':       'new zealand',
    'saudi arabia':      'saudi arabia',
    'czech republic':    'czechia',
}

FLAG_RE = re.compile(r'[\U0001F1E0-\U0001F1FF]{2}|[\U0001F3F4](?:\uDB40[\uDC00-\uDCFF]+󠁿)?')

def normalize(name):
    name = FLAG_RE.sub('', name)
    name = re.sub(r'\s+', ' ', name).strip().lower()
    return NAME_MAP.get(name, name)

def _fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


# ── ESPN data ─────────────────────────────────────────────────────────────────

def fetch_all_events():
    """Fetch all WC2026 match results from ESPN across all group stage dates."""
    events = []
    seen   = set()

    # Group stage: June 11 – July 2. Query in weekly chunks.
    for date in ['20260611', '20260618', '20260625', '20260702']:
        try:
            data = _fetch(f'{SCOREBOARD_BASE}?dates={date}&limit=64')
        except Exception as e:
            print(f'  Warning: scoreboard {date} failed: {e}')
            continue

        for ev in data.get('events', []):
            eid = ev.get('id')
            if eid in seen:
                continue
            seen.add(eid)

            comp        = (ev.get('competitions') or [{}])[0]
            competitors = comp.get('competitors', [])
            status_type = (ev.get('status') or {}).get('type', {})
            completed   = status_type.get('completed', False)

            if len(competitors) < 2:
                continue

            home = next((c for c in competitors if c.get('homeAway') == 'home'), competitors[0])
            away = next((c for c in competitors if c.get('homeAway') == 'away'), competitors[1])

            events.append({
                'id':         eid,
                'home':       home.get('team', {}).get('displayName', ''),
                'away':       away.get('team', {}).get('displayName', ''),
                'home_score': int(home.get('score', -1)) if completed else -1,
                'away_score': int(away.get('score', -1)) if completed else -1,
                'completed':  completed,
            })

    return events


def fetch_scorers(event_id):
    """Return a set of goal scorer display names (lowercased) for a match."""
    try:
        data = _fetch(SUMMARY_BASE.format(eid=event_id))
    except Exception as e:
        print(f'    Warning: summary fetch failed for event {event_id}: {e}')
        return set()

    scorers = set()
    # Try header → competitions → details (ESPN summary shape)
    comps = (data.get('header') or {}).get('competitions') or data.get('competitions') or []
    for comp in comps:
        for detail in comp.get('details', []):
            is_goal = (
                detail.get('scoringPlay', False) or
                str(detail.get('type', {}).get('id', '')) in ('101', '102', '200', '201', '130')
            )
            if is_goal:
                for athlete in detail.get('athletesInvolved', []):
                    name = athlete.get('displayName', '').lower()
                    if name:
                        scorers.add(name)

    return scorers


def find_event(home_name, away_name, events):
    h = normalize(home_name)
    a = normalize(away_name)
    for ev in events:
        eh = normalize(ev['home'])
        ea = normalize(ev['away'])
        if (eh == h and ea == a) or (eh == a and ea == h):
            return ev
    return None


# ── HTML parsing ──────────────────────────────────────────────────────────────

PENDING_ROW_RE = re.compile(
    r'(<tr\s+data-status="pending"[^>]*>)(.*?)(</tr>)',
    re.DOTALL | re.IGNORECASE
)
MATCH_TD_RE = re.compile(r'<td class="match">([^<]+)</td>', re.IGNORECASE)
PICK_TD_RE  = re.compile(r'<td class="pick">([^<]+)</td>',  re.IGNORECASE)
ODDS_TD_RE  = re.compile(r'<td class="odds[^"]*">([-+]?\d+)</td>', re.IGNORECASE)
BADGE_RE    = re.compile(r'<span class="badge [^"]+">.*?</span>', re.IGNORECASE)
PNL_RE      = re.compile(r'<td class="pnl[^"]*">[^<]*</td>', re.IGNORECASE)


def parse_pending_rows(html):
    rows = []
    for m in PENDING_ROW_RE.finditer(html):
        inner   = m.group(2)
        match_m = MATCH_TD_RE.search(inner)
        pick_m  = PICK_TD_RE.search(inner)
        odds_m  = ODDS_TD_RE.search(inner)
        if not (match_m and pick_m and odds_m):
            continue

        match_text = match_m.group(1)
        teams = [t.strip() for t in re.split(r'\s+vs\s+', FLAG_RE.sub('', match_text), flags=re.IGNORECASE)]
        if len(teams) != 2:
            continue

        rows.append({
            'full_match': m.group(0),
            'open_tag':   m.group(1),
            'inner':      inner,
            'close_tag':  m.group(3),
            'home':       teams[0].strip(),
            'away':       teams[1].strip(),
            'pick':       pick_m.group(1).strip(),
            'odds':       int(odds_m.group(1)),
        })
    return rows


# ── Pick grading ──────────────────────────────────────────────────────────────

def pnl_str(outcome, odds):
    """P&L string for a $100 unit bet in American odds."""
    if outcome == 'win':
        profit = odds if odds > 0 else round(10000 / abs(odds), 0)
        return f'+{profit:.0f}'
    if outcome == 'loss':
        return '-100'
    if outcome == 'push':
        return '+0'
    return '--'


def grade_pick(pick_text, ev, scorers):
    """
    Returns (outcome, reason) where outcome is 'win'|'loss'|'push'|'pending'.
    """
    if not ev or not ev['completed'] or ev['home_score'] < 0:
        return ('pending', 'Match not yet complete')

    hs    = ev['home_score']
    as_   = ev['away_score']
    total = hs + as_
    pick  = pick_text.lower().strip()
    hn    = normalize(ev['home'])
    an    = normalize(ev['away'])

    def team_margin(team_str):
        """Return (margin, found) where margin = team_score - opp_score."""
        tn = normalize(team_str)
        if tn == hn:
            return hs - as_, True
        if tn == an:
            return as_ - hs, True
        return 0, False

    # ── Moneyline win ─────────────────────────────────────────────────────────
    m = re.match(r'^(.+?)\s+win$', pick)
    if m:
        margin, found = team_margin(m.group(1))
        if not found:
            return ('pending', f'Team not matched: "{m.group(1)}"')
        return ('win' if margin > 0 else 'loss', f'{hs}-{as_}')

    # ── AH -0.5 (moneyline win) ───────────────────────────────────────────────
    m = re.match(r'^(.+?)\s+-0\.5\s+ah$', pick)
    if m:
        margin, found = team_margin(m.group(1))
        if not found:
            return ('pending', f'Team not matched: "{m.group(1)}"')
        if margin > 0:
            return ('win', f'{hs}-{as_}')
        if margin < 0:
            return ('loss', f'{hs}-{as_}')
        return ('push', 'draw')

    # ── Spread handicap e.g. Argentina -1.5 ──────────────────────────────────
    m = re.match(r'^(.+?)\s+(-\d+\.5)$', pick)
    if m:
        hdp = float(m.group(2))
        margin, found = team_margin(m.group(1))
        if not found:
            return ('pending', f'Team not matched: "{m.group(1)}"')
        adjusted = margin + hdp
        if adjusted > 0:
            return ('win', f'margin {margin:+d}')
        if adjusted < 0:
            return ('loss', f'margin {margin:+d}')
        return ('push', 'exact cover')

    # ── Win to Nil (clean sheet win) ──────────────────────────────────────────
    m = re.match(r'^(.+?)\s+win to nil$', pick)
    if m:
        margin, found = team_margin(m.group(1))
        if not found:
            return ('pending', f'Team not matched: "{m.group(1)}"')
        tn   = normalize(m.group(1))
        conc = as_ if tn == hn else hs
        won  = margin > 0 and conc == 0
        return ('win' if won else 'loss', f'{hs}-{as_}')

    # ── Win or Draw (double chance) ───────────────────────────────────────────
    m = re.match(r'^(.+?)\s+win or draw$', pick)
    if m:
        margin, found = team_margin(m.group(1))
        if not found:
            return ('pending', f'Team not matched: "{m.group(1)}"')
        return ('win' if margin >= 0 else 'loss', f'{hs}-{as_}')

    # ── Over totals ───────────────────────────────────────────────────────────
    m = re.match(r'^over\s+(\d+\.?\d*)\s+goals?$', pick)
    if m:
        line = float(m.group(1))
        return ('win' if total > line else 'loss', f'total {total}')

    # ── Under totals ──────────────────────────────────────────────────────────
    m = re.match(r'^under\s+(\d+\.?\d*)\s+goals?$', pick)
    if m:
        line = float(m.group(1))
        return ('win' if total < line else 'loss', f'total {total}')

    # ── Both Teams to Score ───────────────────────────────────────────────────
    if 'both teams to score' in pick:
        return ('win' if hs > 0 and as_ > 0 else 'loss', f'{hs}-{as_}')

    # ── Player Anytime Scorer ─────────────────────────────────────────────────
    m = re.match(r'^(.+?)\s+anytime(?:\s+scorer)?$', pick)
    if m:
        player = m.group(1).strip().lower()
        if not scorers:
            return ('pending', 'Scorer data unavailable — resolve manually')
        # Partial name match: "vinicius jr." matches "vinicius jr. santos"
        hit = any(player in s or s in player for s in scorers)
        return ('win' if hit else 'loss', 'scored' if hit else 'did not score')

    return ('pending', f'Unrecognized pick format — resolve manually')


# ── HTML update helpers ───────────────────────────────────────────────────────

def badge_html(outcome):
    MAP = {
        'win':     ('badge-win',     'WIN ✓'),
        'loss':    ('badge-loss',    'LOSS ✗'),
        'push':    ('badge-push',    'PUSH'),
        'pending': ('badge-pending', 'Pending'),
    }
    cls, label = MAP.get(outcome, ('badge-pending', 'Pending'))
    return f'<span class="badge {cls}">{label}</span>'


def pnl_class(outcome):
    return {'win': 'pos', 'loss': 'neg', 'push': 'neutral', 'pending': 'neutral'}.get(outcome, 'neutral')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'\nPitchIQ picks updater — {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')

    print('Step 1: Fetch match results from ESPN...')
    events    = fetch_all_events()
    completed = [e for e in events if e['completed']]
    print(f'  {len(completed)} completed matches found\n')

    print('Step 2: Parse pending picks from picks-record.html...')
    with open(HTML_PATH, encoding='utf-8') as f:
        html = f.read()

    pending = parse_pending_rows(html)
    print(f'  {len(pending)} pending picks\n')

    if not pending:
        print('  Nothing to update.')
        return

    print('Step 3: Grade picks...\n')
    scorer_cache = {}
    graded = []

    for row in pending:
        ev = find_event(row['home'], row['away'], events)
        if ev and ev['completed']:
            # Fetch scorers on demand for anytime-scorer picks
            if 'anytime' in row['pick'].lower():
                eid = ev['id']
                if eid not in scorer_cache:
                    print(f'    Fetching scorers: {ev["home"]} vs {ev["away"]}...')
                    scorer_cache[eid] = fetch_scorers(eid)
                scorers = scorer_cache[eid]
            else:
                scorers = set()

            outcome, reason = grade_pick(row['pick'], ev, scorers)
        else:
            outcome, reason = 'pending', 'Match not yet played'

        icon = {'win': '✓', 'loss': '✗', 'push': '~', 'pending': '?'}.get(outcome, '?')
        print(f'  [{icon}] {row["home"]} vs {row["away"]}  |  {row["pick"]}  →  {outcome.upper()}  ({reason})')
        graded.append({**row, 'outcome': outcome, 'pnl': pnl_str(outcome, row['odds'])})

    print()

    if DRY:
        print('[DRY RUN] No files written.\n')
        return

    print('Step 4: Update picks-record.html...')
    updated_html = html

    for g in graded:
        if g['outcome'] == 'pending':
            continue

        new_open  = re.sub(r'data-status="pending"', f'data-status="{g["outcome"]}"', g['open_tag'])
        new_inner = g['inner']
        new_inner = BADGE_RE.sub(badge_html(g['outcome']), new_inner)

        pnl_cls     = pnl_class(g['outcome'])
        pnl_replace = f'<td class="pnl {pnl_cls}">{g["pnl"]}</td>'
        new_inner   = PNL_RE.sub(pnl_replace, new_inner)

        new_row      = new_open + new_inner + g['close_tag']
        updated_html = updated_html.replace(g['full_match'], new_row, 1)

    # Recount W / L / P from the full updated HTML
    wins   = len(re.findall(r'data-status="win"',  updated_html))
    losses = len(re.findall(r'data-status="loss"', updated_html))
    pushes = len(re.findall(r'data-status="push"', updated_html))

    # ROI from P&L cells
    net, staked = 0.0, 0
    for v in re.findall(r'<td class="pnl (?:pos|neg|neutral)">([^<]+)</td>', updated_html):
        v = v.strip()
        if v == '--':
            continue
        try:
            net   += float(v.replace('+', ''))
            staked += 100
        except ValueError:
            pass

    roi = f'{net / staked * 100:+.1f}%' if staked > 0 else '--'

    updated_html = re.sub(r'(<div[^>]+id="stat-w"[^>]*>)\d+(</div>)',   f'\\g<1>{wins}\\g<2>',   updated_html)
    updated_html = re.sub(r'(<div[^>]+id="stat-l"[^>]*>)\d+(</div>)',   f'\\g<1>{losses}\\g<2>', updated_html)
    updated_html = re.sub(r'(<div[^>]+id="stat-p"[^>]*>)\d+(</div>)',   f'\\g<1>{pushes}\\g<2>', updated_html)
    updated_html = re.sub(r'(<div[^>]+id="stat-roi"[^>]*>)[^<]*(</div>)', f'\\g<1>{roi}\\g<2>',  updated_html)

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    resolved = len([g for g in graded if g['outcome'] != 'pending'])
    print(f'  Resolved {resolved} picks — W:{wins} L:{losses} P:{pushes} ROI:{roi}')
    print(f'\nDone. Push when ready:')
    print('  git add picks-record.html && git commit -m "picks record update" && git push')


if __name__ == '__main__':
    main()
