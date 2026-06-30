#!/usr/bin/env python3
"""
PitchIQ — live standings sync from football-data.org.

Fetches live group standings from the free football-data.org API and rewrites
the group cards in standings.html with live W/D/L/GF/GA/GD/Pts.

Designed to run unattended from the GitHub Action every 20 minutes.

To use:
    FOOTBALL_DATA_API_KEY=<key> python3 sync_standings.py
    python3 sync_standings.py --dry      # compute + print, don't write

Source of truth: football-data.org World Cup standings API (v4/competitions/WC/standings)
"""

import json, sys, os, re, urllib.request, urllib.error
from datetime import datetime, timezone

# Make stdout UTF-8 so emoji/✓ in log lines never crash on a cp1252 console.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    pass

PROJ = os.path.dirname(os.path.abspath(__file__))
STANDINGS_HTML = os.path.join(PROJ, 'standings.html')

DRY = '--dry' in sys.argv

# Get API key from environment (passed by GitHub Action)
API_KEY = os.environ.get('FOOTBALL_DATA_API_KEY', '').strip()
if not API_KEY:
    print('ERROR: FOOTBALL_DATA_API_KEY environment variable not set.')
    print('Set it in GitHub Secrets and pass via: env: { FOOTBALL_DATA_API_KEY: ${{ secrets.FOOTBALL_DATA_API_KEY }} }')
    sys.exit(1)

FOOTBALL_DATA_URL = 'https://api.football-data.org/v4/competitions/WC/standings'


# ── Fetch from football-data.org ──────────────────────────────────────────────

def fetch_json(url, headers=None, timeout=15):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def fetch_standings():
    """Fetch live World Cup standings from football-data.org. Returns dict keyed by group."""
    headers = {'X-Auth-Token': API_KEY}
    try:
        data = fetch_json(FOOTBALL_DATA_URL, headers=headers)
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.read().decode()[:200]}')
        return {}
    except Exception as e:
        print(f'  Fetch failed: {e}')
        return {}

    standings = {}
    for st in data.get('standings', []):
        group = st.get('group')  # e.g., 'Group A'
        if not group:
            continue
        # Extract group letter (A–L)
        m = re.search(r'Group ([A-L])', group)
        if not m:
            continue
        gid = m.group(1)
        standings[gid] = {
            'stage': st.get('stage'),
            'type': st.get('type'),
            'matchday': data.get('season', {}).get('currentMatchday'),
            'table': st.get('table', []),
        }
    return standings


# ── HTML rendering ───────────────────────────────────────────────────────────

def get_status_badge(table):
    """Determine group status (LIVE / COMPLETE / X/6 PLAYED / UPCOMING)."""
    if not table:
        return ('upcoming', 'UPCOMING')

    played = sum(1 for t in table if t['playedGames'] > 0)
    total = 6  # 6 fixtures per group

    # All teams have played 3 games each = all 6 fixtures done
    if all(t['playedGames'] == 3 for t in table):
        return ('ft', 'COMPLETE')

    # No games played
    if played == 0:
        return ('upcoming', 'UPCOMING')

    # Some games in progress (will be marked live only if current matchday matches)
    # For simplicity, use "X/6 PLAYED"
    return ('ft', f'{played}/6 PLAYED')


def render_row(t, qualify):
    """Render a single team row in the standings table."""
    gd = t['goalDifference']
    gd_str = f'+{gd}' if gd > 0 else str(gd)
    gd_cls = 'gd-pos' if gd > 0 else 'gd-neg' if gd < 0 else ''
    cls = ' class="qualify"' if qualify else ''
    gd_td = f'<td class="{gd_cls}">{gd_str}</td>' if gd_cls else f'<td>{gd_str}</td>'

    team_name = t['team'].get('shortName', t['team'].get('name', 'Unknown'))
    # Normalize team name for emoji/flag lookup (will be handled by hardcoded team data)

    return (
        f'          <tr{cls}><td>'
        f'<img src="https://flagcdn.com/w40/{_team_code(team_name)}.png" alt="{team_name}" '
        f'style="width:20px;height:auto;border-radius:2px;vertical-align:middle;margin-right:6px;" loading="lazy">'
        f'<span class="team-flag">{_team_emoji(team_name)}</span>{team_name}</td>'
        f'<td>{t["playedGames"]}</td><td>{t["won"]}</td><td>{t["draw"]}</td><td>{t["lost"]}</td>'
        f'<td>{t["goalsFor"]}</td><td>{t["goalsAgainst"]}</td>{gd_td}'
        f'<td class="pts">{t["points"]}</td></tr>'
    )


# Hardcoded team metadata (name → flag code, emoji)
_TEAM_META = {
    'Mexico': ('mx', '🇲🇽'),
    'South Africa': ('za', '🇿🇦'),
    'South Korea': ('kr', '🇰🇷'),
    'Korea Republic': ('kr', '🇰🇷'),
    'Czechia': ('cz', '🇨🇿'),
    'Canada': ('ca', '🇨🇦'),
    'Bosnia': ('ba', '🇧🇦'),
    'Bosnia and Herzegovina': ('ba', '🇧🇦'),
    'Bosnia-Herzegovina': ('ba', '🇧🇦'),
    'Bosnia-H.': ('ba', '🇧🇦'),
    'Qatar': ('qa', '🇶🇦'),
    'Switzerland': ('ch', '🇨🇭'),
    'Brazil': ('br', '🇧🇷'),
    'Morocco': ('ma', '🇲🇦'),
    'Haiti': ('ht', '🇭🇹'),
    'Scotland': ('gb-sct', '🏴󠁧󠁢󠁳󠁣󠁴󠁿'),
    'USA': ('us', '🇺🇸'),
    'Paraguay': ('py', '🇵🇾'),
    'Australia': ('au', '🇦🇺'),
    'Türkiye': ('tr', '🇹🇷'),
    'Turkey': ('tr', '🇹🇷'),
    'Germany': ('de', '🇩🇪'),
    'Ivory Coast': ('ci', '🇨🇮'),
    "Côte d'Ivoire": ('ci', '🇨🇮'),
    'Ecuador': ('ec', '🇪🇨'),
    'Curaçao': ('cw', '🇨🇼'),
    'Curacao': ('cw', '🇨🇼'),
    'Netherlands': ('nl', '🇳🇱'),
    'Sweden': ('se', '🇸🇪'),
    'Japan': ('jp', '🇯🇵'),
    'Tunisia': ('tn', '🇹🇳'),
    'Belgium': ('be', '🇧🇪'),
    'Iran': ('ir', '🇮🇷'),
    'Egypt': ('eg', '🇪🇬'),
    'New Zealand': ('nz', '🇳🇿'),
    'Spain': ('es', '🇪🇸'),
    'Cape Verde': ('cv', '🇨🇻'),
    'Saudi Arabia': ('sa', '🇸🇦'),
    'Uruguay': ('uy', '🇺🇾'),
    'France': ('fr', '🇫🇷'),
    'Norway': ('no', '🇳🇴'),
    'Senegal': ('sn', '🇸🇳'),
    'Iraq': ('iq', '🇮🇶'),
    'Argentina': ('ar', '🇦🇷'),
    'Austria': ('at', '🇦🇹'),
    'Algeria': ('dz', '🇩🇿'),
    'Jordan': ('jo', '🇯🇴'),
    'Portugal': ('pt', '🇵🇹'),
    'Colombia': ('co', '🇨🇴'),
    'DR Congo': ('cd', '🇨🇩'),
    'Congo DR': ('cd', '🇨🇩'),
    'Uzbekistan': ('uz', '🇺🇿'),
    'England': ('gb-eng', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
    'Croatia': ('hr', '🇭🇷'),
    'Panama': ('pa', '🇵🇦'),
    'Ghana': ('gh', '🇬🇭'),
}

def _team_code(name):
    return _TEAM_META.get(name, ('xx', '🌍'))[0]

def _team_emoji(name):
    return _TEAM_META.get(name, ('xx', '🌍'))[1]


def render_card(gid, table, status):
    """Render a single group card."""
    status_cls, status_label = status
    head = (
        '      <thead><tr><th>Team</th><th title="Games Played">GP</th>'
        '<th title="Wins">W</th><th title="Draws">D</th><th title="Losses">L</th>'
        '<th title="Goals For">GF</th><th title="Goals Against">GA</th>'
        '<th title="Goal Difference">GD</th><th title="Points">Pts</th></tr></thead>'
    )
    rows = '\n'.join(render_row(t, i < 2) for i, t in enumerate(table))
    return (
        f'    <!-- GROUP {gid} -->\n'
        f'    <div class="group-card">\n'
        f'      <div class="group-head"><span class="group-label">GROUP {gid}</span>'
        f'<span class="group-status {status_cls}">{status_label}</span></div>\n'
        f'      <table class="standings-table">\n'
        f'{head}\n'
        f'        <tbody>\n'
        f'{rows}\n'
        f'        </tbody>\n'
        f'      </table>\n'
        f'    </div>'
    )


def render_grid(standings_by_gid):
    """Render all 12 group cards."""
    cards = []
    for gid in 'ABCDEFGHIJKL':
        st = standings_by_gid.get(gid, {})
        table = st.get('table', [])
        status = get_status_badge(table)
        cards.append(render_card(gid, table, status))
    return '\n\n'.join(cards)


def update_html(grid_html, generated_at):
    """Replace the groups-grid section in standings.html."""
    with open(STANDINGS_HTML, encoding='utf-8') as f:
        html = f.read()

    # Replace everything between the groups-grid opening tag and its end marker.
    pattern = re.compile(
        r'(<div class="groups-grid" id="groupsGrid">\n).*?(\n\s*</div><!-- /groups-grid -->)',
        re.DOTALL,
    )
    if not pattern.search(html):
        raise RuntimeError('groups-grid markers not found in standings.html')
    html = pattern.sub(lambda m: m.group(1) + '\n' + grid_html + '\n' + m.group(2), html, count=1)

    # Refresh the hero note.
    stamp = generated_at.strftime('%b %d, %Y · %H:%M UTC')
    html = re.sub(
        r'<div class="hero-note">.*?</div>',
        f'<div class="hero-note">🔄 Standings auto-sync from live match scores. Last updated {stamp}.</div>',
        html, count=1, flags=re.DOTALL,
    )
    return html


# ── Main ──────────────────────────────────────────────────────────────────────

def build_live_json_standings(standings_by_gid):
    """Convert standings to the format expected by live.json (matches index.html renderTable)."""
    standings = {}
    for gid in 'ABCDEFGHIJKL':
        st = standings_by_gid.get(gid, {})
        table = st.get('table', [])
        standings[gid] = [
            {
                'name': _normalize_team_name(t['team'].get('name', 'Unknown')),
                'iso': _team_code(_normalize_team_name(t['team'].get('name', 'Unknown'))),
                'p': t['playedGames'],
                'w': t['won'],
                'd': t['draw'],
                'l': t['lost'],
                'gf': t['goalsFor'],
                'ga': t['goalsAgainst'],
                'gd': t['goalDifference'],
                'pts': t['points'],
            }
            for t in table
        ]
    return standings


def _normalize_team_name(name):
    """Normalize team names for display (e.g. 'Bosnia-Herzegovina' → 'Bosnia')."""
    return {
        'Bosnia-Herzegovina': 'Bosnia',
        'South Korea': 'Korea Republic',
    }.get(name, name)


def update_live_json(standings_data, generated_at):
    """Merge standings into live.json, preserving existing odds/scores/ticker data."""
    live_json_path = os.path.join(PROJ, 'data', 'live.json')

    # Load existing live.json if it exists
    existing = {}
    if os.path.exists(live_json_path):
        try:
            with open(live_json_path, encoding='utf-8') as f:
                existing = json.load(f)
        except Exception:
            pass

    # Update or create the structure
    existing['_meta'] = {
        'generated_at': generated_at.isoformat(),
        'source': 'football-data.org + espn',
        'schema_version': '2',
    }
    existing['standings'] = standings_data

    os.makedirs(os.path.dirname(live_json_path), exist_ok=True)
    with open(live_json_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return live_json_path


def main():
    print(f'\nPitchIQ standings sync — {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}\n')

    print('Step 1: Fetch standings from football-data.org...')
    standings_by_gid = fetch_standings()
    if not standings_by_gid:
        print('  No standings returned. Check API key and connectivity.')
        sys.exit(1)

    total_teams = sum(len(st.get('table', [])) for st in standings_by_gid.values())
    print(f'  ✓ {len(standings_by_gid)} groups, {total_teams} teams\n')

    print('Step 2: Render HTML grid...')
    generated_at = datetime.now(timezone.utc)
    grid_html = render_grid(standings_by_gid)
    new_html = update_html(grid_html, generated_at)
    print(f'  ✓ Grid rendered\n')

    print('Step 3: Update live.json for home page + client-side sync...')
    standings_data = build_live_json_standings(standings_by_gid)
    live_path = update_live_json(standings_data, generated_at)
    print(f'  ✓ {live_path}\n')

    if DRY:
        print(grid_html[:2000])
        print('\n... (output truncated)')
        return

    with open(STANDINGS_HTML, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'  ✓ {STANDINGS_HTML}\n')
    print('Done.')


if __name__ == '__main__':
    main()
