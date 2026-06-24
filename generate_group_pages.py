#!/usr/bin/env python3
"""
PitchIQ — Group qualification scenario page generator
Reads group_data.py, generates group-a.html through group-l.html.

Usage:
    python3 generate_group_pages.py          # all 12 groups
    python3 generate_group_pages.py A C L    # specific groups
"""

import os, sys

PROJ = os.path.dirname(os.path.abspath(__file__))


def pts(t): return t['W'] * 3 + t['D']
def gd(t):  return t['GF'] - t['GA']
def gp(t):  return t['W'] + t['D'] + t['L']


def sorted_standings(teams):
    return sorted(teams, key=lambda t: (pts(t), gd(t), t['GF']), reverse=True)


def build_standings_rows(teams):
    rows = ''
    for i, t in enumerate(sorted_standings(teams), 1):
        p = pts(t)
        advance = i <= 2
        row_style = 'background:rgba(0,150,63,.06);' if advance else ''
        border_left = 'border-left:3px solid var(--grn);' if advance else 'border-left:3px solid transparent;'
        rows += f'''<tr style="{row_style}">
          <td style="padding:10px 12px;{border_left}font-weight:700;color:var(--t3);font-family:var(--cond);font-size:13px;">{i}</td>
          <td style="padding:10px 12px;">
            <div style="display:flex;align-items:center;gap:8px;">
              <img src="https://flagcdn.com/w20/{t["code"]}.png" alt="{t["name"]}" style="height:14px;border-radius:2px;" loading="lazy">
              <span style="font-weight:600;color:var(--t1);font-size:14px;">{t["name"]}</span>
              {"<span style='font-family:var(--cond);font-size:10px;font-weight:800;letter-spacing:.06em;background:var(--grn);color:#fff;padding:2px 6px;border-radius:3px;margin-left:6px;'>ADVANCE</span>" if advance else ""}
            </div>
          </td>
          <td style="padding:10px 12px;text-align:center;color:var(--t2);">{gp(t)}</td>
          <td style="padding:10px 12px;text-align:center;color:var(--t2);">{t["W"]}</td>
          <td style="padding:10px 12px;text-align:center;color:var(--t2);">{t["D"]}</td>
          <td style="padding:10px 12px;text-align:center;color:var(--t2);">{t["L"]}</td>
          <td style="padding:10px 12px;text-align:center;color:var(--t2);">{t["GF"]}:{t["GA"]}</td>
          <td style="padding:10px 12px;text-align:center;color:var(--t2);{"color:var(--grn);" if gd(t) > 0 else "color:var(--red);" if gd(t) < 0 else ""}font-weight:600;">{f"+{gd(t)}" if gd(t) > 0 else gd(t)}</td>
          <td style="padding:10px 12px;text-align:center;font-family:var(--cond);font-size:18px;font-weight:900;color:var(--t1);">{p}</td>
        </tr>\n'''
    return rows


def build_fixtures_rows(fixtures):
    rows = ''
    for f in fixtures:
        result = f.get('result')
        if result:
            result_html = f'<span style="font-family:var(--cond);font-size:16px;font-weight:900;color:var(--t1);">{result}</span>'
            link_start = f'<a href="/{f["slug"]}-result" style="text-decoration:none;">' if f.get('slug') else ''
            link_end = '</a>' if f.get('slug') else ''
        else:
            result_html = '<span style="font-size:12px;color:var(--t3);font-style:italic;">Upcoming</span>'
            link_start = f'<a href="/{f["slug"]}" style="text-decoration:none;">' if f.get('slug') else ''
            link_end = '</a>' if f.get('slug') else ''

        rows += f'''{link_start}<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid var(--b1);">
          <div style="font-size:13px;font-weight:600;color:var(--t1);flex:1;">{f["home"]}</div>
          <div style="text-align:center;min-width:100px;">{result_html}</div>
          <div style="font-size:13px;font-weight:600;color:var(--t1);flex:1;text-align:right;">{f["away"]}</div>
          <div style="font-size:11px;color:var(--t3);min-width:48px;text-align:right;margin-left:12px;">{f["date"]}</div>
        </div>{link_end}\n'''
    return rows


def build_scenario_rows(scenarios):
    rows = ''
    for s in scenarios:
        rows += f'<div style="padding:10px 14px;border-bottom:1px solid var(--b1);font-size:14px;color:var(--t2);line-height:1.55;">• {s}</div>\n'
    return rows


def build_page(group_id, g):
    teams = g['teams']
    standings_rows = build_standings_rows(teams)
    fixture_rows = build_fixtures_rows(g['fixtures'])
    scenario_rows = build_scenario_rows(g['scenarios'])
    sorted_teams = sorted_standings(teams)
    leader = sorted_teams[0]
    second = sorted_teams[1] if len(sorted_teams) > 1 else sorted_teams[0]

    # Related groups nav
    all_groups = 'ABCDEFGHIJKL'
    group_links = ' '.join(
        f'<a href="/group-{gid.lower()}" style="display:inline-block;padding:5px 10px;font-family:var(--cond);font-size:12px;font-weight:800;letter-spacing:.06em;border-radius:var(--r);{"background:var(--grn);color:#fff" if gid == group_id else "background:var(--surf);color:var(--t2);border:1px solid var(--b1)"};">{gid}</a>'
        for gid in all_groups
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="theme-color" content="#071D36"/>
  <title>World Cup 2026 Group {group_id} Standings, Results & Qualification Scenarios | PitchIQ</title>
  <meta name="description" content="World Cup 2026 Group {group_id} standings, results, remaining fixtures and qualification scenarios. Who advances? Updated after every match."/>
  <meta name="robots" content="index, follow"/>
  <link rel="canonical" href="https://getpitchiq.net/group-{group_id.lower()}"/>
  <meta name="author" content="PitchIQ"/>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="PitchIQ"/>
  <meta property="og:url" content="https://getpitchiq.net/group-{group_id.lower()}"/>
  <meta property="og:title" content="World Cup 2026 Group {group_id} Standings & Qualification Scenarios"/>
  <meta property="og:description" content="Who advances from Group {group_id}? Live standings, results and every scenario explained."/>
  <meta property="og:image" content="https://getpitchiq.net/pitchiq-banner.png"/>
  <meta property="og:image:width" content="1200"/>
  <meta property="og:image:height" content="630"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:site" content="@getpitchiq"/>
  <meta name="twitter:title" content="World Cup 2026 Group {group_id} Standings & Qualification Scenarios"/>
  <meta name="twitter:description" content="Who advances from Group {group_id}? Live standings and scenario breakdown."/>
  <meta name="twitter:image" content="https://getpitchiq.net/pitchiq-banner.png"/>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://getpitchiq.net"}},{{"@type":"ListItem","position":2,"name":"Standings","item":"https://getpitchiq.net/standings"}},{{"@type":"ListItem","position":3,"name":"Group {group_id}"}}]}}
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-N9PX9ZKHLR"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-N9PX9ZKHLR');</script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23071D36'/><text x='16' y='23' text-anchor='middle' font-family='Arial Black,sans-serif' font-weight='900' font-size='20' fill='%2300963F'>P</text></svg>" type="image/svg+xml"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Barlow+Condensed:wght@700;800;900&display=swap" rel="stylesheet"/>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--nav:#071D36;--grn:#00963F;--grn-h:#007A32;--gold:#D97706;--red:#DC2626;--bg:#EEF1F6;--surf:#fff;--t1:#0F1923;--t2:#3C5168;--t3:#7C92A8;--b1:#E2E8F0;--b2:#C8D5E0;--r:6px;--r2:12px;--sh:0 1px 3px rgba(0,0,0,.07),0 4px 12px rgba(0,0,0,.05);--sans:'Inter',system-ui,sans-serif;--cond:'Barlow Condensed','Arial Narrow',sans-serif}}
    body{{font-family:var(--sans);background:var(--bg);color:var(--t1);-webkit-font-smoothing:antialiased}}
    a{{color:inherit;text-decoration:none}}
    .w{{max-width:1100px;margin:0 auto;padding:0 20px}}
    .nav{{background:var(--nav);height:56px;display:flex;align-items:center;box-shadow:0 2px 12px rgba(0,0,0,.25);position:sticky;top:0;z-index:100}}
    .nav-inner{{max-width:1320px;margin:0 auto;padding:0 20px;width:100%;display:flex;align-items:center;justify-content:space-between;gap:16px}}
    .nav-logo{{font-family:var(--cond);font-size:22px;font-weight:900;color:#fff}}
    .nav-logo span{{color:var(--grn)}}
    .nav-links{{display:flex;gap:4px}}
    .nav-links a{{font-family:var(--cond);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.65);padding:6px 12px;border-radius:var(--r);transition:color .15s,background .15s}}
    .nav-links a:hover{{color:#fff;background:rgba(255,255,255,.08)}}
    .nav-links a.active{{color:#fff}}
    .btn-pro{{font-family:var(--cond);font-size:12px;font-weight:800;letter-spacing:.06em;color:var(--nav);background:var(--grn);padding:7px 14px;border-radius:var(--r)}}
    .group-hero{{background:var(--nav);padding:36px 0 32px;margin-bottom:28px}}
    .group-badge{{font-family:var(--cond);font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--grn);margin-bottom:10px}}
    .group-headline{{font-family:var(--cond);font-size:clamp(30px,5vw,52px);font-weight:900;color:#fff;line-height:1.05;letter-spacing:-.01em;margin-bottom:8px}}
    .group-subhead{{font-size:15px;color:rgba(255,255,255,.65);line-height:1.5;max-width:600px}}
    .breadcrumb{{padding:12px 0;font-size:12px;color:var(--t3)}}
    .breadcrumb a{{color:var(--t3)}}
    .breadcrumb a:hover{{color:var(--grn)}}
    .breadcrumb span{{margin:0 6px}}
    .content-grid{{display:grid;grid-template-columns:1fr 300px;gap:28px;align-items:start;padding-bottom:48px}}
    @media(max-width:860px){{.content-grid{{grid-template-columns:1fr}}.sidebar{{display:none}}}}
    .card{{background:var(--surf);border:1px solid var(--b1);border-radius:var(--r2);overflow:hidden;margin-bottom:20px;box-shadow:var(--sh)}}
    .card-head{{background:var(--nav);padding:12px 18px;display:flex;align-items:center;justify-content:space-between}}
    .card-title{{font-family:var(--cond);font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.85)}}
    .card-badge{{font-family:var(--cond);font-size:10px;font-weight:800;letter-spacing:.08em;background:var(--grn);color:#fff;padding:3px 8px;border-radius:4px}}
    .standings-table{{width:100%;border-collapse:collapse}}
    .standings-table th{{background:rgba(7,29,54,.05);padding:8px 12px;font-family:var(--cond);font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--t3);text-align:center}}
    .standings-table th:nth-child(2){{text-align:left}}
    .standings-table tr{{border-bottom:1px solid var(--b1)}}
    .standings-table tr:last-child{{border-bottom:none}}
    .analysis-p{{font-size:14px;line-height:1.72;color:var(--t2);padding:14px 18px;}}
    .sidebar-card{{background:var(--surf);border:1px solid var(--b1);border-radius:var(--r2);overflow:hidden;margin-bottom:20px;box-shadow:var(--sh)}}
    .sc-head{{background:var(--nav);padding:12px 16px;font-family:var(--cond);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.7)}}
    .sc-body{{padding:14px 16px}}
    .footer{{background:var(--nav);color:rgba(255,255,255,.5);font-size:11px;padding:24px 0;margin-top:40px;text-align:center;line-height:1.8}}
    .footer a{{color:rgba(255,255,255,.5);text-decoration:underline}}
    .footer a:hover{{color:#fff}}
  </style>
</head>
<body>

<nav class="nav" aria-label="Primary navigation">
  <div class="nav-inner">
    <a class="nav-logo" href="/">Pitch<span>IQ</span></a>
    <div class="nav-links">
      <a class="nav-link" href="/predictions">Picks</a>
      <a class="nav-link active" href="/standings">Standings</a>
      <a class="nav-link" href="/fantasy">Fantasy</a>
      <a class="nav-link" href="/picks-record">Record</a>
    </div>
    <a class="btn-pro" href="#">Go Pro ↗</a>
  </div>
</nav>

<!-- Group Hero -->
<div class="group-hero">
  <div class="w">
    <div class="group-badge">⚽ FIFA World Cup 2026 · Group Stage</div>
    <h1 class="group-headline">Group {group_id} Standings &amp; Qualification Scenarios</h1>
    <p class="group-subhead">
      {leader["name"]} lead. {second["name"]} are in second.
      {g["analysis"].split(".")[0]}.
    </p>
  </div>
</div>

<div class="w" style="padding-bottom:8px;">
  <div class="breadcrumb">
    <a href="/">Home</a><span>›</span>
    <a href="/standings">Standings</a><span>›</span>
    Group {group_id}
  </div>
</div>

<!-- Group nav -->
<div class="w" style="margin-bottom:24px;">
  <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center;">
    <span style="font-family:var(--cond);font-size:11px;font-weight:800;letter-spacing:.06em;color:var(--t3);text-transform:uppercase;margin-right:4px;">All Groups:</span>
    {group_links}
  </div>
</div>

<div style="text-align:center;margin-bottom:24px;">
  <ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px;max-width:100%" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<div class="w">
  <div class="content-grid">
    <div>

      <!-- Standings Table -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">Group {group_id} Standings</div>
          <div class="card-badge">LIVE</div>
        </div>
        <table class="standings-table">
          <thead>
            <tr>
              <th>#</th>
              <th style="text-align:left;">Team</th>
              <th>GP</th>
              <th>W</th>
              <th>D</th>
              <th>L</th>
              <th>G</th>
              <th>GD</th>
              <th>PTS</th>
            </tr>
          </thead>
          <tbody>
            {standings_rows}
          </tbody>
        </table>
        <div style="padding:8px 14px;font-size:11px;color:var(--t3);border-top:1px solid var(--b1);">
          🟢 Top 2 teams advance to Round of 32
        </div>
      </div>

      <!-- Results & Fixtures -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">Results &amp; Fixtures</div>
        </div>
        {fixture_rows}
      </div>

      <!-- Qualification Scenarios -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">Qualification Scenarios</div>
          <div class="card-badge">ANALYSIS</div>
        </div>
        {scenario_rows}
      </div>

      <!-- Analysis -->
      <div class="card">
        <div class="card-head"><div class="card-title">✦ PitchIQ Group Analysis</div></div>
        <p class="analysis-p">{g["analysis"]}</p>
        <div style="padding:0 18px 14px;">
          <a href="/predictions" style="font-family:var(--cond);font-size:13px;font-weight:700;color:var(--grn);letter-spacing:.04em;">View all AI match picks →</a>
        </div>
      </div>

    </div>

    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-card">
        <div class="sc-head">Group {group_id} Teams</div>
        <div class="sc-body">
          {"".join(f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--b1);"><img src="https://flagcdn.com/w20/{t["code"]}.png" style="height:14px;border-radius:2px;" loading="lazy"><span style="font-size:13px;font-weight:600;color:var(--t1);">{t["name"]}</span><span style="margin-left:auto;font-family:var(--cond);font-size:16px;font-weight:900;color:var(--t1);">{pts(t)} pts</span></div>' for t in sorted_standings(teams))}
        </div>
      </div>

      <div class="sidebar-card">
        <div class="sc-head">All Groups</div>
        <div class="sc-body">
          {"".join(f'<a href="/group-{gid.lower()}" style="display:block;padding:7px 0;border-bottom:1px solid var(--b1);font-size:13px;{"font-weight:700;color:var(--grn);" if gid == group_id else "color:var(--t2);"}">{"→ " if gid == group_id else ""}Group {gid}</a>' for gid in "ABCDEFGHIJKL")}
        </div>
      </div>

      <div style="text-align:center;margin-bottom:20px;">
        <ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div class="sidebar-card">
        <div class="sc-head">Quick Links</div>
        <div class="sc-body">
          <a href="/picks-record" style="display:block;padding:9px 0;border-bottom:1px solid var(--b1);font-size:13px;color:var(--t1);font-weight:500;">AI Pick Record →</a>
          <a href="/fantasy" style="display:block;padding:9px 0;border-bottom:1px solid var(--b1);font-size:13px;color:var(--t1);font-weight:500;">Fantasy Lineup Builder →</a>
          <a href="/predictions" style="display:block;padding:9px 0;font-size:13px;color:var(--t1);font-weight:500;">Match Predictions →</a>
        </div>
      </div>
    </aside>
  </div>
</div>

<footer class="footer">
  <div style="margin-bottom:10px;">
    <a href="https://twitter.com/getpitchiq" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:20px;padding:8px 18px;color:#fff;font-family:'Barlow Condensed',Arial,sans-serif;font-weight:700;font-size:13px;letter-spacing:.06em;text-decoration:none;">
      𝕏 Follow @getpitchiq for live picks &amp; match updates
    </a>
  </div>
  © 2026 PitchIQ · <a href="/">getpitchiq.net</a> · Entertainment purposes only · Must be 21+ to bet · <a href="https://www.ncpgambling.org" target="_blank" rel="noopener">Responsible Gambling</a>
</footer>

</body>
</html>'''


if __name__ == '__main__':
    try:
        from group_data import GROUPS
    except ImportError as e:
        print(f'ERROR: {e}. Run from the project directory.')
        sys.exit(1)

    filter_groups = set(g.upper() for g in sys.argv[1:])
    generated = 0
    errors = 0

    for group_id, g in GROUPS.items():
        if filter_groups and group_id not in filter_groups:
            continue
        try:
            content = build_page(group_id, g)
            out_path = os.path.join(PROJ, f'group-{group_id.lower()}.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            teams_str = ' · '.join(t['name'] for t in g['teams'])
            print(f'  group-{group_id.lower()}.html  [{teams_str}]')
            generated += 1
        except Exception as e:
            print(f'  ERROR Group {group_id}: {e}')
            import traceback; traceback.print_exc()
            errors += 1

    print(f'\n  Generated {generated} group pages', end='')
    if errors:
        print(f', {errors} errors')
    else:
        print()
    print()
    print('  Add to sitemap.xml (priority 0.8, changefreq daily) and link from standings.html')
