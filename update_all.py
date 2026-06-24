#!/usr/bin/env python3
"""
PitchIQ — Master updater
Runs all site updaters in sequence.

Usage:
    python3 update_all.py              # run everything
    python3 update_all.py --dry        # dry run (print only, write nothing)
    python3 update_all.py --skip-odds  # skip odds (saves API quota)
    python3 update_all.py --only standings|picks|odds|fantasy

Run this after each match day to keep the entire site current.

Updater order:
  1. update_standings.py  — group standings + group pages (ESPN, free)
  2. update_picks_record.py — grades AI picks, updates W/L/ROI (ESPN, free)
  3. update_odds.py        — refreshes match page odds (The Odds API, costs quota)
  4. update_fantasy.py     — updates fantasy player pts/ownership (ESPN, free)

The --skip-odds flag is useful mid-tournament when odds for completed games
are already off the board and you just want standings + picks + fantasy.
"""

import sys, os, subprocess, time
from datetime import datetime

PROJ = os.path.dirname(os.path.abspath(__file__))

DRY        = '--dry' in sys.argv
SKIP_ODDS  = '--skip-odds' in sys.argv
ONLY_FLAG  = next((sys.argv[i+1] for i, a in enumerate(sys.argv) if a == '--only'), None)

SCRIPTS = [
    ('standings', 'update_standings.py',    'Group standings + pages'),
    ('picks',     'update_picks_record.py', 'AI picks grading + W/L/ROI'),
    ('odds',      'update_odds.py',         'Match page odds (costs API quota)'),
    ('fantasy',   'update_fantasy.py',      'Fantasy player pts + ownership'),
]


def run(name, script, label):
    path = os.path.join(PROJ, script)
    if not os.path.exists(path):
        print(f'  ⚠  {script} not found — skipping {label}')
        return False

    args = [sys.executable, path]
    if DRY:
        args.append('--dry')

    print(f'\n{"─" * 60}')
    print(f'  {label}')
    print(f'  Running: python3 {script}{"  --dry" if DRY else ""}')
    print(f'{"─" * 60}\n')

    result = subprocess.run(args, cwd=PROJ)

    if result.returncode != 0:
        print(f'\n  ✗ {script} exited with code {result.returncode}')
        return False

    print(f'\n  ✓ {label} complete')
    return True


def main():
    print(f'\n{"=" * 60}')
    print(f'  PitchIQ master updater')
    print(f'  {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}')
    if DRY:
        print(f'  MODE: DRY RUN — no files will be written')
    print(f'{"=" * 60}')

    results = {}

    for name, script, label in SCRIPTS:
        # --only filter
        if ONLY_FLAG and name != ONLY_FLAG:
            print(f'\n  Skipping {label} (--only {ONLY_FLAG})')
            continue

        # --skip-odds
        if name == 'odds' and SKIP_ODDS:
            print(f'\n  Skipping odds updater (--skip-odds)')
            print(f'  To update odds: python3 update_odds.py')
            continue

        ok = run(name, script, label)
        results[name] = ok

        # Brief pause between scripts to avoid ESPN rate limits
        if name != SCRIPTS[-1][0]:
            time.sleep(1)

    # Summary
    print(f'\n{"=" * 60}')
    print(f'  Summary')
    print(f'{"=" * 60}')
    for name, script, label in SCRIPTS:
        if name in results:
            icon = '✓' if results[name] else '✗'
            print(f'  [{icon}] {label}')
        else:
            print(f'  [–] {label} (skipped)')

    if not DRY and any(results.values()):
        changed = [s for n, s, _ in SCRIPTS if results.get(n)]
        print(f'\nPush to Vercel when ready:')
        print(f'  git add -A && git commit -m "match day update" && git push')

    print()


if __name__ == '__main__':
    main()
