#!/usr/bin/env python3
"""
PitchIQ — master live-data generator.

Fetches data from all configured providers and writes data/live.json.
This file is read by pitchiq-live.js to update the site in real time.

Run:
    python3 generate_live_data.py            # full fetch
    python3 generate_live_data.py --dry      # print JSON, don't write
    python3 generate_live_data.py --mock     # use match_data.py values only

The GitHub Action runs this after update_odds.py so one push covers both.
"""

import json, sys, os, urllib.request, urllib.error
from datetime import datetime, timezone

# Load env from .env.local if present
def load_dotenv():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env.local')
    if not os.path.exists(path):
        return
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip(); v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v

load_dotenv()

import importlib.util, pathlib

PROJ = pathlib.Path(__file__).parent
DRY  = '--dry'  in sys.argv
MOCK = '--mock' in sys.argv

# ── Import shared config ──────────────────────────────────────────────────────
from config import active_provider, api_key, LIVE_JSON, SCHEMA_VERSION, DATA_SOURCE

# ── Import match data ─────────────────────────────────────────────────────────
spec = importlib.util.spec_from_file_location('match_data', PROJ / 'match_data.py')
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
MATCHES = mod.MATCHES


# ── Utilities ─────────────────────────────────────────────────────────────────

def fmt_ml(val):
    try:
        n = int(val)
        return f'+{n}' if n > 0 else str(n)
    except (TypeError, ValueError):
        return str(val) if val else None


def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


# ── Odds API adapter ──────────────────────────────────────────────────────────

import re as _re
_FLAG_RE = _re.compile(r'[\U0001F1E0-\U0001F1FF]{2}')
_NAME_MAP = {
    'ir iran': 'iran', 'türkiye': 'turkey', "côte d'ivoire": 'ivory coast',
    'korea republic': 'korea republic', 'south korea': 'korea republic',
    'dr congo': 'dr congo', 'congo dr': 'dr congo',
    'bosnia and herzegovina': 'bosnia', 'bosnia & herzegovina': 'bosnia',
    'united states': 'usa', 'curacao': 'curaçao',
    'cape verde islands': 'cape verde', 'czech republic': 'czechia',
}

def _norm(name):
    name = _FLAG_RE.sub('', name).strip().lower()
    return _NAME_MAP.get(name, name)


def fetch_odds_api():
    """Fetch h2h + totals from The Odds API. Returns dict keyed by slug."""
    key = api_key()
    if not key:
        print('  ODDS_API_KEY not set — skipping odds fetch')
        return {}

    cfg = active_provider()
    results = {}

    for sport in cfg['sport_keys']:
        url = (
            f"{cfg['base_url']}/sports/{sport}/odds"
            f"?apiKey={key}&regions={cfg['regions']}"
            f"&markets={cfg['markets']}&oddsFormat={cfg['odds_format']}&dateFormat=iso"
        )
        print(f'  Trying sport key: {sport}')
        try:
            events = fetch_json(url)
            print(f'  ✓ {len(events)} events from The Odds API')
            # Build slug → odds map
            for m in MATCHES:
                ev = _find_event(m['home'], m['away'], events)
                if not ev:
                    continue
                odds = _extract_odds(ev, m['home'], m['away'])
                if odds:
                    results[m['slug']] = odds
            return results
        except urllib.error.HTTPError as e:
            if e.code == 422:
                print(f'  Sport key not found, trying next...')
                continue
            print(f'  HTTP {e.code} — {e.read().decode()[:120]}')
            break
        except Exception as e:
            print(f'  Error: {e}')
            break

    return results


def _find_event(home, away, events):
    h, a = _norm(home), _norm(away)
    for ev in events:
        eh = _norm(ev.get('home_team', ''))
        ea = _norm(ev.get('away_team', ''))
        if (eh == h and ea == a) or (eh == a and ea == h):
            return ev
    return None


def _extract_odds(event, home, away):
    from collections import Counter
    h = _norm(home)
    h2h_home, h2h_draw, h2h_away = [], [], []
    tot_line, tot_over, tot_under = [], [], []

    for bm in event.get('bookmakers', []):
        for mkt in bm.get('markets', []):
            key = mkt.get('key', '')
            if key == 'h2h':
                for oc in mkt.get('outcomes', []):
                    n = _norm(oc.get('name', ''))
                    p = oc.get('price', 0)
                    if n == 'draw':         h2h_draw.append(p)
                    elif n == h:            h2h_home.append(p)
                    else:                   h2h_away.append(p)
            elif key == 'totals':
                for oc in mkt.get('outcomes', []):
                    n     = oc.get('name', '').lower()
                    p     = oc.get('price', 0)
                    point = oc.get('point', 2.5)
                    if n == 'over':   tot_over.append(p); tot_line.append(point)
                    elif n == 'under': tot_under.append(p)

    def avg_ml(prices):
        if not prices:
            return None
        avg = sum(prices) / len(prices)
        return f'+{int(avg)}' if avg >= 0 else str(int(avg))

    home_ml = avg_ml(h2h_home)
    if not home_ml:
        return None

    ou_line = Counter(tot_line).most_common(1)[0][0] if tot_line else 2.5

    return {
        'home_ml':  home_ml,
        'draw_ml':  avg_ml(h2h_draw) or '+280',
        'away_ml':  avg_ml(h2h_away) or '+400',
        'ou_line':  str(ou_line),
        'ou_over':  avg_ml(tot_over)  or '-110',
        'ou_under': avg_ml(tot_under) or '-110',
    }


# ── ESPN adapter (scores + standings) ─────────────────────────────────────────

def fetch_espn_scores():
    """
    Fetch live scores from ESPN free API.
    Returns dict: { slug: { status, score_home, score_away, clock } }

    To migrate to a different scores API, replace this function only.
    The caller expects the same dict shape.
    """
    url = 'https://site.api.espn.com/apis/site/v2/sports/soccer/FIFA.WORLD/scoreboard'
    try:
        data = fetch_json(url)
    except Exception as e:
        print(f'  ESPN fetch failed: {e}')
        return {}

    scores = {}
    for event in data.get('events', []):
        comp = event.get('competitions', [{}])[0]
        competitors = comp.get('competitors', [])
        if len(competitors) < 2:
            continue

        # Map ESPN team names to our slugs
        home_c = next((c for c in competitors if c.get('homeAway') == 'home'), None)
        away_c = next((c for c in competitors if c.get('homeAway') == 'away'), None)
        if not home_c or not away_c:
            continue

        home_name = home_c.get('team', {}).get('displayName', '')
        away_name = away_c.get('team', {}).get('displayName', '')

        # Find matching slug from match_data
        slug = _slug_for_teams(home_name, away_name)
        if not slug:
            continue

        status_type = event.get('status', {}).get('type', {})
        state = status_type.get('state', 'pre')   # pre | in | post
        detail = status_type.get('shortDetail', '')
        clock  = event.get('status', {}).get('displayClock', '')

        scores[slug] = {
            'status':     'live' if state == 'in' else ('ft' if state == 'post' else 'upcoming'),
            'score_home': int(home_c.get('score', 0)) if state != 'pre' else None,
            'score_away': int(away_c.get('score', 0)) if state != 'pre' else None,
            'clock':      clock if state == 'in' else None,
            'detail':     detail,
        }

    return scores


def _slug_for_teams(home_name, away_name):
    h, a = _norm(home_name), _norm(away_name)
    for m in MATCHES:
        mh, ma = _norm(m['home']), _norm(m['away'])
        if (mh == h and ma == a) or (mh == a and ma == h):
            return m['slug']
    return None


# ── Build the live.json payload ───────────────────────────────────────────────

def build_payload(odds_by_slug, scores_by_slug):
    """
    Merge odds + scores + match_data into the canonical live.json shape.

    SCHEMA — data/live.json:
    {
      "_meta": { generated_at, source, schema_version },
      "matches": {
        "<slug>": {
          home_ml, draw_ml, away_ml, ou_line, ou_over, ou_under,
          home_prob, draw_prob, away_prob,
          status, score_home, score_away, clock,
          home, away, home_emoji, away_emoji, time_str, date_short, venue_short
        }
      },
      "ticker": [ { slug, home, away, home_emoji, away_emoji,
                    status, score_home, score_away, time_str, clock } ],
      "standings": {
        "<group>": [ { team, flag, played, won, drawn, lost, gf, ga, pts } ]
      }
    }
    """
    matches_out = {}
    ticker_out  = []

    for m in MATCHES:
        slug = m['slug']

        # Start from match_data values (always present)
        entry = {
            'home':        m['home'],
            'away':        m['away'],
            'home_emoji':  m.get('home_emoji', ''),
            'away_emoji':  m.get('away_emoji', ''),
            'date_short':  m.get('date_short', ''),
            'time_str':    m.get('time_str', ''),
            'venue_short': m.get('venue_short', ''),
            # Odds — from match_data as fallback
            'home_ml':  fmt_ml(m.get('home_ml')),
            'draw_ml':  fmt_ml(m.get('draw_ml')),
            'away_ml':  fmt_ml(m.get('away_ml')),
            'ou_line':  str(m.get('ou_line', '2.5')),
            'ou_over':  fmt_ml(m.get('ou_over')),
            'ou_under': fmt_ml(m.get('ou_under')),
            # Probabilities
            'home_prob': m.get('home_prob', 0),
            'draw_prob': m.get('draw_prob', 0),
            'away_prob': m.get('away_prob', 0),
            # Live scores — default to no data
            'status':     'upcoming',
            'score_home': None,
            'score_away': None,
            'clock':      None,
        }

        # Overlay live odds if available
        if slug in odds_by_slug:
            entry.update(odds_by_slug[slug])

        # Overlay live scores if available
        if slug in scores_by_slug:
            sc = scores_by_slug[slug]
            entry.update({
                'status':     sc['status'],
                'score_home': sc['score_home'],
                'score_away': sc['score_away'],
                'clock':      sc.get('clock'),
            })

        matches_out[slug] = entry

        # Ticker entry
        ticker_out.append({
            'slug':       slug,
            'home':       m['home'],
            'away':       m['away'],
            'home_emoji': m.get('home_emoji', ''),
            'away_emoji': m.get('away_emoji', ''),
            'time_str':   m.get('time_str', ''),
            'date_short': m.get('date_short', ''),
            'status':     entry['status'],
            'score_home': entry['score_home'],
            'score_away': entry['score_away'],
            'clock':      entry['clock'],
        })

    return {
        '_meta': {
            'generated_at':   datetime.now(timezone.utc).isoformat(),
            'source':         DATA_SOURCE,
            'schema_version': SCHEMA_VERSION,
        },
        'matches': matches_out,
        'ticker':  ticker_out,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'\nPitchIQ live-data generator — {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}\n')

    if MOCK:
        print('Running in --mock mode (match_data.py values only)\n')
        odds_by_slug   = {}
        scores_by_slug = {}
    else:
        print('Step 1: Fetch live odds...')
        odds_by_slug = fetch_odds_api()
        print(f'  {len(odds_by_slug)} matches with fresh odds\n')

        print('Step 2: Fetch live scores from ESPN...')
        scores_by_slug = fetch_espn_scores()
        print(f'  {len(scores_by_slug)} matches with live/final scores\n')

    print('Step 3: Build live.json payload...')
    payload = build_payload(odds_by_slug, scores_by_slug)
    print(f'  {len(payload["matches"])} matches, {len(payload["ticker"])} ticker entries\n')

    if DRY:
        print(json.dumps(payload, indent=2))
    else:
        with open(LIVE_JSON, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f'  ✓ Written to {LIVE_JSON}')

    print('\nDone.')


if __name__ == '__main__':
    main()
