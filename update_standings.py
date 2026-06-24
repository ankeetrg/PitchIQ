#!/usr/bin/env python3
"""
PitchIQ — Live standings updater
Source: ESPN hidden JSON API (no key required, free, reliable)

Usage:
    python3 update_standings.py          # fetch + update group_data.py + regenerate pages
    python3 update_standings.py --dry    # print standings only, don't write files

Run this after each match day to keep group pages current.
"""

import json, sys, re, os, urllib.request, urllib.error
from datetime import datetime

PROJ   = os.path.dirname(os.path.abspath(__file__))
DRY    = '--dry' in sys.argv

# Primary + fallback URLs — script tries each in order until one works
CANDIDATE_URLS = [
    'https://site.api.espn.com/apis/v2/sports/soccer/FIFA.WORLD/standings',
    'https://site.api.espn.com/apis/site/v2/sports/soccer/FIFA.WORLD/standings',
    'https://site.web.api.espn.com/apis/v2/sports/soccer/FIFA.WORLD/standings',
]

# Map ESPN group labels (e.g. "Group A") to our group IDs
GROUP_ID_RE = re.compile(r'Group ([A-L])', re.IGNORECASE)

# Map ESPN team names → our group_data.py team names (fix mismatches here if needed)
NAME_MAP = {
    'IR Iran':           'Iran',
    'Türkiye':           'Turkey',
    "Côte d'Ivoire":     'Ivory Coast',
    'Korea Republic':    'Korea Republic',
    'South Korea':       'Korea Republic',
    'DR Congo':          'DR Congo',
    'Congo DR':          'DR Congo',
    'New Zealand':       'New Zealand',
    'Saudi Arabia':      'Saudi Arabia',
    'Cape Verde':        'Cape Verde',
    'United States':     'USA',
    'Curaçao':           'Curacao',
    'Curacao':           'Curacao',
    'South Africa':      'South Africa',
    'Bosnia and Herzegovina': 'Bosnia',
    'Bosnia & Herzegovina':   'Bosnia',
    'Bosnia-Herzegovina':     'Bosnia',
}

def espn_name(raw):
    return NAME_MAP.get(raw, raw)


def fetch_standings():
    """Fetch group standings from ESPN API. Tries each candidate URL in order."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    for url in CANDIDATE_URLS:
        print(f'  Trying: {url}')
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.load(r)
            print(f'  ✓ Success')
            return data
        except urllib.error.HTTPError as e:
            print(f'  HTTP {e.code} — trying next')
        except urllib.error.URLError as e:
            print(f'  Connection error: {e.reason} — trying next')
    print('\n  ERROR: All ESPN URLs failed. Check your internet connection.')
    print('  You can also paste scores manually into group_data.py.')
    sys.exit(1)


def parse_standings(data):
    """
    Parse ESPN standings response into a dict:
    { 'A': [{'name': 'Mexico', 'W': 2, 'D': 0, 'L': 0, 'GF': 4, 'GA': 0}, ...], ... }
    """
    groups = {}

    # ESPN standings structure varies — try both known shapes
    standings_list = (
        data.get('standings', []) or
        data.get('children', []) or
        []
    )

    for group_block in standings_list:
        # Get group label
        label = (
            group_block.get('name') or
            group_block.get('abbreviation') or
            group_block.get('shortName') or ''
        )
        m = GROUP_ID_RE.search(label)
        if not m:
            continue
        gid = m.group(1).upper()

        teams = []
        entries = (
            group_block.get('standings', {}).get('entries', []) or
            group_block.get('entries', []) or
            []
        )
        for entry in entries:
            team_name = (
                entry.get('team', {}).get('displayName') or
                entry.get('team', {}).get('name') or
                entry.get('teamDisplayName') or
                'Unknown'
            )
            stats_raw = entry.get('stats', [])
            stats = {s['name']: s.get('value', 0) for s in stats_raw if 'name' in s}

            # ESPN stat keys vary; try common aliases
            W  = int(stats.get('wins',           stats.get('gamesWon',   0)))
            D  = int(stats.get('ties',            stats.get('gamesTied',  0)))
            L  = int(stats.get('losses',          stats.get('gamesLost',  0)))
            GF = int(stats.get('pointsFor',       stats.get('goalsFor',   0)))
            GA = int(stats.get('pointsAgainst',   stats.get('goalsAgainst', 0)))

            teams.append({
                'name': espn_name(team_name),
                'W': W, 'D': D, 'L': L, 'GF': GF, 'GA': GA
            })

        if teams:
            groups[gid] = teams

    return groups


def update_group_data(live_groups):
    """
    Read group_data.py, patch W/D/L/GF/GA for each team, write back.
    Only updates numeric fields — preserves all other content (fixtures, scenarios, analysis).
    """
    path = os.path.join(PROJ, 'group_data.py')
    with open(path, encoding='utf-8') as f:
        src = f.read()

    updated = 0
    for gid, teams in live_groups.items():
        for t in teams:
            name = t['name']
            # Match the dict line:  dict(name='Mexico', ..., W=1, D=0, L=0, GF=2, GA=0)
            # We patch W= D= L= GF= GA= values in place using regex
            pattern = (
                r"(dict\(name='" + re.escape(name) + r"'[^)]*?)"
                r"W=\d+,\s*D=\d+,\s*L=\d+,\s*GF=\d+,\s*GA=\d+"
            )
            replacement = (
                r"\g<1>"
                f"W={t['W']}, D={t['D']}, L={t['L']}, GF={t['GF']}, GA={t['GA']}"
            )
            new_src, n = re.subn(pattern, replacement, src, flags=re.DOTALL)
            if n:
                src = new_src
                updated += n
                print(f'    ✓ Group {gid}: {name}  W={t["W"]} D={t["D"]} L={t["L"]} GF={t["GF"]} GA={t["GA"]}')
            else:
                print(f'    ⚠ Group {gid}: no match for "{name}" in group_data.py — add to NAME_MAP if needed')

    if not DRY:
        # Stamp the update date in the file header
        src = re.sub(
            r'(# Last updated:.*)',
            f'# Last updated: {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}',
            src
        )
        with open(path, 'w', encoding='utf-8') as f:
            f.write(src)
        print(f'\n  group_data.py updated ({updated} team records patched)')
    else:
        print(f'\n  [DRY RUN] Would have patched {updated} team records')

    return updated


def regenerate_pages():
    """Run generate_group_pages.py to rebuild all 12 HTML pages."""
    import subprocess
    script = os.path.join(PROJ, 'generate_group_pages.py')
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=PROJ)
    print(result.stdout.strip())
    if result.returncode != 0:
        print('  ERRORS:', result.stderr.strip())


def print_table(live_groups):
    """Pretty-print the fetched standings."""
    for gid in sorted(live_groups):
        teams = sorted(live_groups[gid], key=lambda t: (t['W']*3 + t['D'], t['GF']-t['GA']), reverse=True)
        print(f'\n  Group {gid}')
        print(f'  {"Team":<22} {"W":>2} {"D":>2} {"L":>2} {"GF":>3} {"GA":>3} {"GD":>4} {"PTS":>4}')
        print(f'  {"-"*50}')
        for t in teams:
            pts = t['W']*3 + t['D']
            gd  = t['GF'] - t['GA']
            print(f'  {t["name"]:<22} {t["W"]:>2} {t["D"]:>2} {t["L"]:>2} {t["GF"]:>3} {t["GA"]:>3} {gd:>+4} {pts:>4}')


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print(f'\nPitchIQ standings updater — {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}\n')

    print('Step 1: Fetch live standings from ESPN...')
    data = fetch_standings()

    print('\nStep 2: Parse response...')
    live_groups = parse_standings(data)

    if not live_groups:
        print('\n  ERROR: Could not parse any groups from ESPN response.')
        print('  The API response structure may have changed.')
        print('  Raw keys:', list(data.keys()))
        sys.exit(1)

    print(f'  Found {len(live_groups)} groups: {", ".join(sorted(live_groups))}\n')
    print_table(live_groups)

    print('\nStep 3: Patch group_data.py...')
    update_group_data(live_groups)

    if DRY:
        print('\n  [DRY RUN] Would regenerate group pages with generate_group_pages.py')
        sys.exit(0)

    print('\nStep 4: Regenerate group pages...')
    regenerate_pages()

    print('\nDone. Push to Vercel when ready:')
    print('  git add group_data.py group-*.html && git commit -m "standings update" && git push')
