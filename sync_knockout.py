#!/usr/bin/env python3
"""
PitchIQ — knockout bracket sync (Round of 32 → Final).

Pulls live knockout fixtures from football-data.org (free; teams, flags, scores,
status) and overlays live odds from The Odds API (paid; moneylines + derived
win probabilities) when a key is available. Merges a "knockout" section into
data/live.json, which predictions.html reads to render the knockout cards.

Design:
  * data/knockout.json is the static bracket (slug, round, date, venue, match_no),
    already in chronological order within each stage.
  * football-data.org returns the same 32 knockout matches with real teams as each
    round is decided. We pair them to knockout.json by per-stage kickoff order
    (both chronological), so no fragile name/venue matching is needed.
  * The Odds API events are matched to known team names for moneylines.

Run:
    FOOTBALL_DATA_API_KEY=... [ODDS_API_KEY=...] python3 sync_knockout.py
    python3 sync_knockout.py --no-odds      # skip the paid Odds API entirely
    python3 sync_knockout.py --dry          # print the knockout section, don't write

Env:
    FOOTBALL_DATA_API_KEY   required (same key as sync_standings.py)
    ODDS_API_KEY            optional (same key as generate_live_data.py)

Safe by design: on any fetch/parse error the existing live.json is left untouched.
"""

import json, os, sys, re, pathlib, urllib.request, urllib.error
from datetime import datetime, timezone

PROJ          = pathlib.Path(__file__).parent
KNOCKOUT_JSON = PROJ / 'data' / 'knockout.json'
LIVE_JSON     = PROJ / 'data' / 'live.json'
FD_MATCHES    = 'https://api.football-data.org/v4/competitions/WC/matches'

DRY      = '--dry' in sys.argv
NO_ODDS  = '--no-odds' in sys.argv

# football-data stage code -> our stage code (matches data-stage in predictions.html)
STAGE_MAP = {
    'LAST_32':        'r32',
    'LAST_16':        'r16',
    'QUARTER_FINALS': 'qf',
    'SEMI_FINALS':    'sf',
    'THIRD_PLACE':    'tp',
    'FINAL':          'final',
}

# ── Team name -> (flagcdn code, emoji). Shared with sync_standings.py, plus a few
#    football-data spellings (United States, Bosnia-Herzegovina, Cape Verde Islands…).
_TEAM_META = {
    'Mexico': ('mx', '🇲🇽'), 'South Africa': ('za', '🇿🇦'),
    'South Korea': ('kr', '🇰🇷'), 'Korea Republic': ('kr', '🇰🇷'),
    'Czechia': ('cz', '🇨🇿'), 'Canada': ('ca', '🇨🇦'),
    'Bosnia': ('ba', '🇧🇦'), 'Bosnia and Herzegovina': ('ba', '🇧🇦'),
    'Bosnia-Herzegovina': ('ba', '🇧🇦'),
    'Qatar': ('qa', '🇶🇦'), 'Switzerland': ('ch', '🇨🇭'),
    'Brazil': ('br', '🇧🇷'), 'Morocco': ('ma', '🇲🇦'), 'Haiti': ('ht', '🇭🇹'),
    'Scotland': ('gb-sct', '🏴󠁧󠁢󠁳󠁣󠁴󠁿'),
    'USA': ('us', '🇺🇸'), 'United States': ('us', '🇺🇸'),
    'Paraguay': ('py', '🇵🇾'), 'Australia': ('au', '🇦🇺'),
    'Türkiye': ('tr', '🇹🇷'), 'Turkey': ('tr', '🇹🇷'),
    'Germany': ('de', '🇩🇪'), 'Ivory Coast': ('ci', '🇨🇮'), "Côte d'Ivoire": ('ci', '🇨🇮'),
    'Ecuador': ('ec', '🇪🇨'), 'Curaçao': ('cw', '🇨🇼'), 'Curacao': ('cw', '🇨🇼'),
    'Netherlands': ('nl', '🇳🇱'), 'Sweden': ('se', '🇸🇪'), 'Japan': ('jp', '🇯🇵'),
    'Tunisia': ('tn', '🇹🇳'), 'Belgium': ('be', '🇧🇪'), 'Iran': ('ir', '🇮🇷'),
    'Egypt': ('eg', '🇪🇬'), 'New Zealand': ('nz', '🇳🇿'), 'Spain': ('es', '🇪🇸'),
    'Cape Verde': ('cv', '🇨🇻'), 'Cape Verde Islands': ('cv', '🇨🇻'),
    'Saudi Arabia': ('sa', '🇸🇦'), 'Uruguay': ('uy', '🇺🇾'), 'France': ('fr', '🇫🇷'),
    'Norway': ('no', '🇳🇴'), 'Senegal': ('sn', '🇸🇳'), 'Iraq': ('iq', '🇮🇶'),
    'Argentina': ('ar', '🇦🇷'), 'Austria': ('at', '🇦🇹'), 'Algeria': ('dz', '🇩🇿'),
    'Jordan': ('jo', '🇯🇴'), 'Portugal': ('pt', '🇵🇹'), 'Colombia': ('co', '🇨🇴'),
    'DR Congo': ('cd', '🇨🇩'), 'Congo DR': ('cd', '🇨🇩'),
    'Uzbekistan': ('uz', '🇺🇿'), 'England': ('gb-eng', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
    'Croatia': ('hr', '🇭🇷'), 'Panama': ('pa', '🇵🇦'), 'Ghana': ('gh', '🇬🇭'),
}

def team_obj(name):
    if not name:
        return None
    code, emoji = _TEAM_META.get(name, ('xx', '🌍'))
    return {'name': name, 'code': code, 'emoji': emoji}


# ── HTTP ───────────────────────────────────────────────────────────────────────

def fetch_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


# ── The Odds API (optional moneylines + win probabilities) ──────────────────────

_FLAG_RE = re.compile(r'[\U0001F1E0-\U0001F1FF]{2}')
_NAME_MAP = {
    'ir iran': 'iran', 'türkiye': 'turkey', "côte d'ivoire": 'ivory coast',
    'south korea': 'korea republic', 'dr congo': 'dr congo', 'congo dr': 'dr congo',
    'bosnia and herzegovina': 'bosnia', 'bosnia & herzegovina': 'bosnia',
    'bosnia-herzegovina': 'bosnia', 'united states': 'usa', 'curacao': 'curaçao',
    'cape verde islands': 'cape verde', 'czech republic': 'czechia',
}

def _norm(name):
    return _NAME_MAP.get(_FLAG_RE.sub('', name or '').strip().lower(),
                         _FLAG_RE.sub('', name or '').strip().lower())

def _ml_to_prob(ml):
    try:
        n = int(str(ml).replace('+', ''))
    except (TypeError, ValueError):
        return None
    return (100.0 / (n + 100.0)) if n > 0 else ((-n) / ((-n) + 100.0))

def fetch_odds_events():
    """Return raw Odds API events list, or [] if no key / fetch fails."""
    key = os.environ.get('ODDS_API_KEY', '').strip()
    if NO_ODDS or not key:
        return []
    for sport in ('soccer_fifa_world_cup_2026', 'soccer_world_cup', 'soccer_fifa_world_cup'):
        url = (f'https://api.the-odds-api.com/v4/sports/{sport}/odds'
               f'?apiKey={key}&regions=us&markets=h2h&oddsFormat=american&dateFormat=iso')
        try:
            events = fetch_json(url)
            print(f'  Odds API: {len(events)} events from {sport}')
            return events
        except urllib.error.HTTPError as e:
            if e.code == 422:
                continue
            print(f'  Odds API HTTP {e.code}'); return []
        except Exception as e:
            print(f'  Odds API error: {e}'); return []
    return []

def odds_for(home, away, events):
    """Average h2h moneylines for a fixture -> dict with ml + probabilities."""
    if not home or not away:
        return {}
    h, a = _norm(home), _norm(away)
    ev = next((e for e in events
               if {_norm(e.get('home_team')), _norm(e.get('away_team'))} == {h, a}), None)
    if not ev:
        return {}
    hm, dr, aw = [], [], []
    for bm in ev.get('bookmakers', []):
        for mkt in bm.get('markets', []):
            if mkt.get('key') != 'h2h':
                continue
            for oc in mkt.get('outcomes', []):
                n, p = _norm(oc.get('name')), oc.get('price')
                if   n == 'draw': dr.append(p)
                elif n == h:      hm.append(p)
                elif n == a:      aw.append(p)
    def avg_ml(xs):
        if not xs: return None
        v = sum(xs) / len(xs)
        return f'+{int(v)}' if v >= 0 else str(int(v))
    home_ml, draw_ml, away_ml = avg_ml(hm), avg_ml(dr), avg_ml(aw)
    if not home_ml:
        return {}
    out = {'home_ml': home_ml, 'draw_ml': draw_ml, 'away_ml': away_ml}
    ph, pd, pa = _ml_to_prob(home_ml), _ml_to_prob(draw_ml), _ml_to_prob(away_ml)
    if ph and pa:
        pd = pd or 0.0
        tot = ph + pd + pa
        out.update(home_prob=round(ph / tot * 100),
                   draw_prob=round(pd / tot * 100),
                   away_prob=round(pa / tot * 100))
    return out


# ── football-data status / score ────────────────────────────────────────────────

def _status(fd_status):
    s = (fd_status or '').upper()
    if s in ('IN_PLAY', 'PAUSED', 'LIVE'):
        return 'live'
    if s in ('FINISHED', 'AWARDED'):
        return 'ft'
    return 'upcoming'


# ── Build the knockout section ───────────────────────────────────────────────────

def build_knockout(fd_matches, odds_events):
    base = json.loads(KNOCKOUT_JSON.read_text(encoding='utf-8'))['matches']

    # Group our static slots by stage, preserving their (chronological) order.
    base_by_stage = {}
    for m in base:
        base_by_stage.setdefault(m['stage'], []).append(m)

    # Group football-data knockout matches by stage, sorted by kickoff.
    fd_by_stage = {}
    for fm in fd_matches:
        st = STAGE_MAP.get(fm.get('stage'))
        if st:
            fd_by_stage.setdefault(st, []).append(fm)
    for st in fd_by_stage:
        fd_by_stage[st].sort(key=lambda x: x.get('utcDate', ''))

    out = {}
    for stage, slots in base_by_stage.items():
        fd_list = fd_by_stage.get(stage, [])
        for i, slot in enumerate(slots):
            fm = fd_list[i] if i < len(fd_list) else None
            entry = {'stage': stage, 'status': 'upcoming',
                     'score_home': None, 'score_away': None, 'clock': None}
            if fm:
                home = team_obj((fm.get('homeTeam') or {}).get('name'))
                away = team_obj((fm.get('awayTeam') or {}).get('name'))
                if home: entry['home'] = home
                if away: entry['away'] = away
                entry['status'] = _status(fm.get('status'))
                ft = (fm.get('score') or {}).get('fullTime') or {}
                entry['score_home'] = ft.get('home')
                entry['score_away'] = ft.get('away')
                if home and away:
                    entry.update(odds_for(home['name'], away['name'], odds_events))
            out[slot['slug']] = entry
    return out


def merge_into_live(knockout):
    """Read-modify-write: set live.json['knockout'] without disturbing the rest."""
    try:
        existing = json.loads(LIVE_JSON.read_text(encoding='utf-8')) if LIVE_JSON.exists() else {}
    except Exception:
        existing = {}
    existing['knockout'] = knockout
    meta = existing.get('_meta', {})
    meta['knockout_generated_at'] = datetime.now(timezone.utc).isoformat()
    existing['_meta'] = meta
    LIVE_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding='utf-8')


def main():
    key = os.environ.get('FOOTBALL_DATA_API_KEY', '').strip()
    if not key:
        print('ERROR: FOOTBALL_DATA_API_KEY not set.'); sys.exit(1)

    print('Step 1: Fetch WC matches from football-data.org...')
    try:
        data = fetch_json(FD_MATCHES, headers={'X-Auth-Token': key})
    except Exception as e:
        print(f'  Fetch failed: {e} — leaving live.json untouched.'); sys.exit(1)
    fd_matches = data.get('matches', [])
    print(f'  {len(fd_matches)} total matches')

    print('Step 2: Fetch knockout odds (The Odds API)...')
    odds_events = fetch_odds_events()

    print('Step 3: Build knockout section...')
    knockout = build_knockout(fd_matches, odds_events)
    decided = sum(1 for v in knockout.values() if v.get('home'))
    withodds = sum(1 for v in knockout.values() if v.get('home_ml'))
    print(f'  {len(knockout)} fixtures · {decided} with teams · {withodds} with odds')

    if DRY:
        print(json.dumps(knockout, indent=2, ensure_ascii=False)); return
    merge_into_live(knockout)
    print(f'  ✓ Wrote knockout section to {LIVE_JSON}')


if __name__ == '__main__':
    main()
