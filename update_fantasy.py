#!/usr/bin/env python3
"""
PitchIQ — Fantasy player stats updater
Source: ESPN hidden JSON API (no key required, free)

Scoring system used (matches typical WC DFS):
  Goal:          +6 pts
  Assist:        +3 pts
  Clean sheet:   +4 pts (GK/DEF only, full match)
  Yellow card:   -1 pt
  Red card:      -3 pts
  Bonus (saves): +1 pt per 3 saves (GK)

Ownership% is estimated from tournament performance:
  Base ownership is kept from the PLAYERS array.
  A player who scores 1+ goals gets ownership boosted by ~(goals * 4)%.
  Ownership is clamped to [1, 80].

Usage:
    python3 update_fantasy.py          # fetch stats + update fantasy.html
    python3 update_fantasy.py --dry    # print updated table, don't write

Run after each match day.
"""

import json, sys, re, os, urllib.request, urllib.error
from datetime import datetime
from collections import defaultdict

PROJ      = os.path.dirname(os.path.abspath(__file__))
DRY       = '--dry' in sys.argv
HTML_PATH = os.path.join(PROJ, 'fantasy.html')

SCOREBOARD_BASE = 'https://site.api.espn.com/apis/site/v2/sports/soccer/FIFA.WORLD/scoreboard'
SUMMARY_BASE    = 'https://site.api.espn.com/apis/site/v2/sports/soccer/FIFA.WORLD/summary?event={eid}'

# ESPN team code → PitchIQ team code (3-letter)
TEAM_CODE_MAP = {
    'Brazil':         'BRA', 'Morocco':        'MAR', 'France':         'FRA',
    'Argentina':      'ARG', 'Spain':          'ESP', 'Germany':        'GER',
    'England':        'ENG', 'Netherlands':    'NED', 'Portugal':       'POR',
    'Colombia':       'COL', 'Uruguay':        'URU', 'Mexico':         'MEX',
    'Korea Republic': 'KOR', 'Japan':          'JPN', 'Senegal':        'SEN',
    'Ecuador':        'ECU', 'Belgium':        'BEL', 'Serbia':         'SRB',
    'Norway':         'NOR', 'Croatia':        'CRO', 'Denmark':        'DEN',
    'Switzerland':    'SUI', 'Poland':         'POL', 'Sweden':         'SWE',
    'Australia':      'AUS', 'Tunisia':        'TUN', 'Ghana':          'GHA',
    'Cameroon':       'CMR', 'Iran':           'IRN', 'Saudi Arabia':   'KSA',
    'Qatar':          'QAT', 'Canada':         'CAN', 'USA':            'USA',
    'Scotland':       'SCO', 'Haiti':          'HAI', 'Scotland':       'SCO',
    'Türkiye':        'TUR', 'Turkey':         'TUR', 'Paraguay':       'PAR',
    'Cape Verde':     'CPV', 'South Africa':   'RSA', 'Jordan':         'JOR',
    'Algeria':        'ALG', 'DR Congo':       'COD', 'Uzbekistan':     'UZB',
    'Iraq':           'IRQ', 'Bosnia':         'BIH', 'Panama':         'PAN',
    'New Zealand':    'NZL', 'Egypt':          'EGY', 'Ivory Coast':    'CIV',
    "Côte d'Ivoire":  'CIV', 'Curaçao':        'CUW',
}

# DFS scoring weights
POINTS = {
    'goal':          6,
    'assist':        3,
    'clean_sheet':   4,   # GK / DEF only
    'yellow':       -1,
    'red':          -3,
    'save_bonus':    1,   # +1 for every 3 saves by GK
}


def _fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Accept': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


# ── Fetch all completed match event IDs ───────────────────────────────────────

def fetch_completed_event_ids():
    """Return list of ESPN event IDs for completed WC2026 matches."""
    ids = []
    seen = set()
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
            status = (ev.get('status') or {}).get('type', {})
            if status.get('completed', False):
                comp   = (ev.get('competitions') or [{}])[0]
                comps_ = comp.get('competitors', [])
                teams  = [c.get('team', {}).get('displayName', '') for c in comps_]
                home_s = int(comps_[0].get('score', 0)) if comps_ else 0
                away_s = int(comps_[1].get('score', 0)) if len(comps_) > 1 else 0
                ids.append({
                    'id':    eid,
                    'teams': teams,
                    'score': (home_s, away_s),
                })
    return ids


# ── Parse match summary for player events ────────────────────────────────────

def parse_match_summary(event_id, team_scores):
    """
    Return dict: player_name → {goals, assists, yellow, red, played_full, is_gk, saves}
    Also returns list of teams that kept a clean sheet.
    """
    try:
        data = _fetch(SUMMARY_BASE.format(eid=event_id))
    except Exception as e:
        print(f'    Warning: summary {event_id} failed: {e}')
        return {}, []

    player_stats = defaultdict(lambda: {
        'goals': 0, 'assists': 0, 'yellow': 0, 'red': 0,
        'played_full': False, 'is_gk': False, 'saves': 0, 'team': '',
    })

    # ESPN event type IDs (approximate)
    GOAL_IDS    = {'101', '102', '200', '201', '130'}
    ASSIST_IDS  = {'301'}
    YELLOW_IDS  = {'400', '401'}
    RED_IDS     = {'500', '501'}

    comps = (data.get('header') or {}).get('competitions') or data.get('competitions') or []
    for comp in comps:
        for detail in comp.get('details', []):
            type_id = str(detail.get('type', {}).get('id', ''))
            athletes = detail.get('athletesInvolved', [])

            for i, athlete in enumerate(athletes):
                name = athlete.get('displayName', '')
                if not name:
                    continue
                team = athlete.get('team', {}).get('displayName', '')

                if type_id in GOAL_IDS or detail.get('scoringPlay', False):
                    if i == 0:  # first athlete = scorer
                        player_stats[name]['goals'] += 1
                        player_stats[name]['team'] = team
                    elif i == 1:  # second athlete = assister
                        player_stats[name]['assists'] += 1
                        player_stats[name]['team'] = team
                elif type_id in ASSIST_IDS:
                    player_stats[name]['assists'] += 1
                    player_stats[name]['team'] = team
                elif type_id in YELLOW_IDS:
                    player_stats[name]['yellow'] += 1
                    player_stats[name]['team'] = team
                elif type_id in RED_IDS:
                    player_stats[name]['red'] += 1
                    player_stats[name]['team'] = team

    # Determine clean sheet teams (allowed 0 goals)
    # team_scores: [(home_team_name, home_score), (away_team_name, away_score)]
    clean_sheet_teams = set()
    if len(team_scores) == 2:
        (ht, hs), (at, as_) = team_scores
        if as_ == 0:
            clean_sheet_teams.add(ht.lower())
        if hs == 0:
            clean_sheet_teams.add(at.lower())

    return dict(player_stats), clean_sheet_teams


# ── Aggregate stats across all completed matches ──────────────────────────────

def aggregate_player_stats(events):
    """Return dict: player_display_name_lower → accumulated stats."""
    aggregated = defaultdict(lambda: {
        'goals': 0, 'assists': 0, 'yellow': 0, 'red': 0,
        'clean_sheets': 0, 'saves': 0, 'matches': 0, 'team': '',
    })

    for ev in events:
        print(f'    Fetching match summary: {" vs ".join(ev["teams"])}...')
        hs, as_ = ev['score']
        teams_and_scores = []
        if len(ev['teams']) >= 2:
            teams_and_scores = [(ev['teams'][0], hs), (ev['teams'][1], as_)]

        stats, clean_teams = parse_match_summary(ev['id'], teams_and_scores)

        for name, s in stats.items():
            key = name.lower()
            aggregated[key]['goals']   += s['goals']
            aggregated[key]['assists'] += s['assists']
            aggregated[key]['yellow']  += s['yellow']
            aggregated[key]['red']     += s['red']
            aggregated[key]['saves']   += s['saves']
            aggregated[key]['matches'] += 1
            if s['team']:
                aggregated[key]['team'] = s['team']

        # Clean sheet bonus
        for team_name in clean_teams:
            for name, s in stats.items():
                if s.get('team', '').lower() == team_name:
                    aggregated[name.lower()]['clean_sheets'] += 1

    return aggregated


def calc_pts(stats, is_gk=False, is_def=False):
    """Compute DFS fantasy points from aggregated stats."""
    pts = 0
    pts += stats['goals']   * POINTS['goal']
    pts += stats['assists']  * POINTS['assist']
    pts += stats['yellow']   * POINTS['yellow']
    pts += stats['red']      * POINTS['red']
    if is_gk or is_def:
        pts += stats['clean_sheets'] * POINTS['clean_sheet']
    if is_gk:
        pts += (stats['saves'] // 3) * POINTS['save_bonus']
    return pts


# ── Parse and update fantasy.html ────────────────────────────────────────────

PLAYERS_BLOCK_RE = re.compile(
    r'(const PLAYERS\s*=\s*\[)(.*?)(\];)',
    re.DOTALL
)

PLAYER_RE = re.compile(
    r'\{id:(\d+),name:"([^"]+)",team:"([^"]+)",flag:"([^"]+)",pos:"([^"]+)",pts:(\d+),own:"([^"]+)",price:(\d+)\}'
)


def update_fantasy_html(aggregated_stats):
    with open(HTML_PATH, encoding='utf-8') as f:
        html = f.read()

    block_match = PLAYERS_BLOCK_RE.search(html)
    if not block_match:
        print('  ERROR: Could not find PLAYERS array in fantasy.html')
        sys.exit(1)

    players_js = block_match.group(2)
    updated_rows = []
    stat_lines   = []

    for pm in PLAYER_RE.finditer(players_js):
        pid, name, team, flag, pos, pts_base, own_base, price = (
            pm.group(1), pm.group(2), pm.group(3), pm.group(4),
            pm.group(5), int(pm.group(6)), pm.group(7), int(pm.group(8))
        )

        # Look up stats by partial name match (last name or full name)
        name_lower = name.lower()
        matched_key = None
        for key in aggregated_stats:
            if name_lower in key or key in name_lower:
                matched_key = key
                break

        if matched_key:
            s       = aggregated_stats[matched_key]
            is_gk   = pos == 'GK'
            is_def  = pos == 'DEF'
            earned  = calc_pts(s, is_gk=is_gk, is_def=is_def)
            new_pts = pts_base + earned  # base (pre-tournament) + earned in tournament

            # Adjust ownership: goals drive interest
            own_int = int(own_base.replace('%', ''))
            goal_boost = s['goals'] * 4
            new_own = min(80, max(1, own_int + goal_boost))
            new_own_str = f'{new_own}%'
            stat_lines.append(f'    {name}: +{earned}pts ({s["goals"]}G {s["assists"]}A) → {new_pts}pts, own {new_own_str}')
        else:
            new_pts     = pts_base
            new_own_str = own_base

        updated_rows.append(
            f'  {{id:{pid},name:"{name}",team:"{team}",flag:"{flag}",pos:"{pos}",'
            f'pts:{new_pts},own:"{new_own_str}",price:{price}}}'
        )

    new_block = block_match.group(1) + '\n' + ',\n'.join(updated_rows) + '\n' + block_match.group(3)
    new_html  = PLAYERS_BLOCK_RE.sub(new_block, html)

    return new_html, stat_lines


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'\nPitchIQ fantasy updater — {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')

    print('Step 1: Fetch completed match IDs from ESPN...')
    events = fetch_completed_event_ids()
    print(f'  {len(events)} completed matches\n')

    if not events:
        print('  No completed matches found. Nothing to update.')
        return

    print('Step 2: Fetch match summaries and aggregate player stats...')
    aggregated = aggregate_player_stats(events)
    scorers = [k for k, v in aggregated.items() if v['goals'] > 0]
    print(f'\n  {len(aggregated)} players with event data, {len(scorers)} scorers\n')

    if aggregated:
        print('  Top scorers found:')
        top = sorted(aggregated.items(), key=lambda x: x[1]['goals'], reverse=True)[:10]
        for name, s in top:
            print(f'    {name.title()}: {s["goals"]}G {s["assists"]}A')
        print()

    print('Step 3: Calculate updated fantasy points...')
    updated_html, stat_lines = update_fantasy_html(aggregated)

    print('  Changes:')
    if stat_lines:
        for line in stat_lines:
            print(line)
    else:
        print('    No players matched — scorer data may be incomplete in ESPN summaries.')
        print('    The PLAYERS array will be left unchanged.')

    if DRY:
        print('\n[DRY RUN] No files written.\n')
        return

    print('\nStep 4: Write fantasy.html...')
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print('  Done.')
    print('\nPush when ready:')
    print('  git add fantasy.html && git commit -m "fantasy stats update" && git push')


if __name__ == '__main__':
    main()
