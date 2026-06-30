#!/usr/bin/env python3
import urllib.request, json, os

api_key = 'cb3c8e9a31cf4cd4a5932d4a41b4067a'
url = "https://api.football-data.org/v4/competitions/WC/standings"
headers = {"X-Auth-Token": api_key}
req = urllib.request.Request(url, headers=headers)

data = json.load(urllib.request.urlopen(req, timeout=10))
for st in data.get('standings', []):
    group = st.get('group', '')
    if 'B' in group:
        print(f"\n{group}:")
        for team in st.get('table', []):
            name = team['team'].get('name', 'Unknown')
            short = team['team'].get('shortName', 'N/A')
            tla = team['team'].get('tla', 'N/A')
            if 'osnia' in name.lower():
                print(f"  Full name: {name}")
                print(f"  Short name: {short}")
                print(f"  TLA: {tla}")
