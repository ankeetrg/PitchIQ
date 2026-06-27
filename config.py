#!/usr/bin/env python3
"""
PitchIQ data source configuration.

THIS IS THE ONE FILE TO EDIT WHEN MIGRATING TO A NEW API.
Set DATA_SOURCE to the key of the provider you want, then update
the corresponding block below with your credentials and endpoints.

Current providers:
  'odds-api'  — The Odds API (https://the-odds-api.com)  [ACTIVE]
  'espn'      — ESPN free scoreboard API                  [scores/standings]
  'mock'      — static fixtures from match_data.py        [dev/testing]
"""

import os

# ── Active data source ───────────────────────────────────────────────────────
# Change this string to switch providers. All scripts import from here.
DATA_SOURCE = 'odds-api'

# ── Provider configs ─────────────────────────────────────────────────────────

PROVIDERS = {

    'odds-api': {
        'name':        'The Odds API v4',
        'base_url':    'https://api.the-odds-api.com/v4',
        'api_key_env': 'ODDS_API_KEY',          # env var that holds the key
        'sport_keys':  [                         # tried in order until one works
            'soccer_fifa_world_cup_2026',
            'soccer_world_cup',
            'soccer_fifa_world_cup',
        ],
        'regions':     'us',
        'markets':     'h2h,totals',
        'odds_format': 'american',
        'preferred_books': ['draftkings', 'fanduel', 'betmgm', 'caesars', 'betonlineag'],
    },

    'espn': {
        'name':        'ESPN Scoreboard (free)',
        'base_url':    'https://site.api.espn.com/apis/site/v2/sports/soccer',
        'league':      'FIFA.WORLD',
        'api_key_env': None,                     # no key required
    },

    'mock': {
        'name':        'Mock (match_data.py only)',
        'api_key_env': None,
    },
}

# ── Output paths ─────────────────────────────────────────────────────────────

import pathlib
PROJ    = pathlib.Path(__file__).parent
DATA_DIR = PROJ / 'data'
DATA_DIR.mkdir(exist_ok=True)

LIVE_JSON      = DATA_DIR / 'live.json'       # written by generate_live_data.py
SCHEMA_VERSION = '1'                           # bump when shape changes

# ── Helper: get active provider config ───────────────────────────────────────

def active_provider():
    p = PROVIDERS.get(DATA_SOURCE)
    if not p:
        raise ValueError(f'Unknown DATA_SOURCE: {DATA_SOURCE!r}. '
                         f'Valid options: {list(PROVIDERS)}')
    return p


def api_key():
    """Return the API key for the active provider, or '' if none needed."""
    p = active_provider()
    env = p.get('api_key_env')
    if not env:
        return ''
    key = os.environ.get(env, '')
    return key
