#!/usr/bin/env python3
"""PitchIQ v3 Match Page Generator — all 72 WC2026 group stage matches"""
import os, re, sys

PROJ = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PROJ, 'brazil-morocco.html'), encoding='utf-8') as f:
    TEMPLATE = f.read()

PHOTOS = [
    '1556816214-6d16c62fbbf6',
    '1489944440615-453fc2b6a9a9',
    '1569531955323-33c6b2dca44b',
    '1599158150601-1417ebbaafdd',
    '1706675780107-7c43cc487928',
    '1705593973313-75de7bf95b56',
    '1651421738652-12124d47c917',
    '1430232324554-8f4aebd06683',
    '1571754472834-677ab0a62ba7',
    '1518091043644-c1d4457512c6',
]

def ph(i):
    return PHOTOS[i % len(PHOTOS)]


def replace_between(html, start, end, new_content):
    """Replace html[s:e] (start inclusive, end exclusive) with new_content."""
    s = html.index(start)
    e = html.index(end, s)
    return html[:s] + new_content + html[e:]


# ── Section builders ──────────────────────────────────────────────────────────

def ai_section(m):
    chips_html = ''
    for text, pos in m['chips']:
        cls = 'pred-chip pos' if pos else 'pred-chip'
        chips_html += f'            <div class="{cls}">{text}</div>\n'
    return f'''      <!-- AI Prediction -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">✦ PitchIQ AI Prediction</div>
          <div class="card-badge badge-ai">50,000 SIMULATIONS</div>
        </div>
        <div class="card-body">
          <div class="pred-label">Most likely result</div>
          <div class="pred-result"><span>{m["fav_name"]}</span> {m["pred_result"]}</div>
          <div class="prob-bar-wrap">
            <div class="prob-seg home" style="width:{m["home_prob"]}%"></div>
            <div class="prob-seg draw" style="width:{m["draw_prob"]}%"></div>
            <div class="prob-seg away" style="width:{m["away_prob"]}%"></div>
          </div>
          <div class="prob-labels">
            <div><strong>{m["home_prob"]}%</strong><br>{m["home"]} Win</div>
            <div style="text-align:center"><strong>{m["draw_prob"]}%</strong><br>Draw</div>
            <div style="text-align:right"><strong>{m["away_prob"]}%</strong><br>{m["away"]} Win</div>
          </div>
          <div class="pred-chips">
{chips_html}          </div>
        </div>
      </div>
'''


def analysis_section(m):
    hs = ''.join(
        f'            <div class="key-stat"><div class="key-stat-val">{v}</div>'
        f'<div class="key-stat-lbl">{l}</div></div>\n'
        for v, l in m['home_stats']
    )
    as_ = ''.join(
        f'            <div class="key-stat"><div class="key-stat-val">{v}</div>'
        f'<div class="key-stat-lbl">{l}</div></div>\n'
        for v, l in m['away_stats']
    )
    return f'''      <!-- Match Analysis -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">Match Analysis</div>
        </div>
        <div class="card-body">
          <h3 class="analysis-h3">{m["home"]}: {m["home_h3"]}</h3>
          <p class="analysis-para">{m["home_p1"]}</p>
          <p class="analysis-para">{m["home_p2"]}</p>
          <div class="key-stat-grid">
{hs}          </div>
          <h3 class="analysis-h3">{m["away"]}: {m["away_h3"]}</h3>
          <p class="analysis-para">{m["away_p1"]}</p>
          <p class="analysis-para">{m["away_p2"]}</p>
          <div class="key-stat-grid">
{as_}          </div>
          <h3 class="analysis-h3">Head-to-Head</h3>
          <p class="analysis-para">{m["h2h"]}</p>
        </div>
      </div>
'''


def stats_section(m):
    rows = ''
    for hv, lbl, pct, av in m['stat_rows']:
        rows += f'''          <div class="stat-row">
            <div class="stat-val">{hv}</div>
            <div class="stat-bar-wrap">
              <div class="stat-label" style="margin-bottom:4px;font-size:11px;text-align:center;color:var(--t3)">{lbl}</div>
              <div class="stat-bar-bg"><div class="stat-bar-fill" style="width:{pct}%"></div></div>
            </div>
            <div class="stat-val">{av}</div>
          </div>\n'''
    return f'''      <!-- Stats Comparison -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">Team Stats Comparison</div>
          <div style="display:flex;gap:16px;font-size:11px;font-weight:700;">
            <span style="color:var(--grn)">{m["home_emoji"]} {m["home"]}</span>
            <span style="color:#E2383A">{m["away_emoji"]} {m["away"]}</span>
          </div>
        </div>
        <div class="card-body">
{rows}        </div>
      </div>
'''


def picks_section(m):
    TAG_CLS = {'AI PICK': 'tag-ai', 'HOT': 'tag-hot', 'VALUE': 'tag-value', 'RISKY': 'tag-value'}
    rows = ''
    for name, detail, tag, odds in m['picks']:
        cls = TAG_CLS.get(tag, 'tag-value')
        rows += f'''          <div class="pick-row">
            <div class="pick-info">
              <div class="pick-name">{name}</div>
              <div class="pick-detail">{detail}</div>
            </div>
            <div class="pick-tag {cls}">{tag}</div>
            <div class="pick-odds">{odds}</div>
          </div>\n'''
    return f'''      <!-- Betting Picks -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">⚡ AI Betting Picks</div>
          <div class="card-badge badge-value">BEST VALUE</div>
        </div>
        <div class="card-body">
{rows}          <a class="bet-cta" href="#" data-aff="draftkings" rel="noopener sponsored" target="_blank">Place These Bets at DraftKings →</a>
        </div>
      </div>
'''


def fantasy_section(m):
    rows = ''
    for rank, (emoji, name, meta, pts, own, risk) in enumerate(m['fantasy'], 1):
        bg = 'rgba(220,38,38,.1)' if risk else 'rgba(0,150,63,.1)'
        rows += f'''          <div class="fp-row">
            <div class="fp-rank">{rank}</div>
            <div class="fp-avatar" style="background:{bg}">{emoji}</div>
            <div class="fp-info">
              <div class="fp-name">{name}</div>
              <div class="fp-meta">{meta}</div>
            </div>
            <div>
              <div class="fp-pts">{pts}</div>
              <div class="fp-pts-lbl">Proj. Pts</div>
            </div>
            <div class="fp-own">{own}</div>
          </div>\n'''
    return f'''      <!-- Fantasy Picks -->
      <div class="card">
        <div class="card-head">
          <div class="card-title">⭐ Fantasy Picks — This Match</div>
          <div class="card-badge badge-ai">DFS OPTIMIZED</div>
        </div>
        <div class="card-body">
{rows}        </div>
      </div>
'''


def sidebar_section(m):
    trending_html = ''
    for i, (text, badge) in enumerate(m['trending'], 1):
        trending_html += f'''          <div class="trending-row">
            <div class="trend-num">{i}</div>
            <div class="trend-text">{text}</div>
            <div class="trend-badge">{badge}</div>
          </div>\n'''

    up_next_html = ''
    for text, time_lbl, href in m['up_next']:
        up_next_html += f'''          <a href="{href}" class="trending-row" style="text-decoration:none;display:flex;justify-content:space-between;align-items:center;">
            <div class="trend-text" style="font-weight:600">{text}</div>
            <div style="font-size:11px;color:var(--t3)">{time_lbl}</div>
          </a>\n'''

    return f'''    <!-- SIDEBAR -->
    <div>

      <!-- Stadium thumbnail -->
      <div style="border-radius:var(--r2);overflow:hidden;margin-bottom:16px;aspect-ratio:16/9;">
        <img src="https://images.unsplash.com/photo-{m["photo"]}?w=1600&q=80&fit=crop" alt="Match venue" style="width:100%;height:100%;object-fit:cover;" loading="lazy">
      </div>

      <!-- Sportsbook comparison -->
      <div class="sidebar-card">
        <div class="sc-head">Best Odds: {m["fav_name"]} Win</div>
        <div class="sc-body">
          <a class="sb-book-row" href="#" data-aff="draftkings" rel="noopener sponsored" target="_blank">
            <div><div class="sb-book-name">DraftKings</div><div class="sb-book-bonus">Bet $5, Get $200</div></div>
            <div class="sb-book-odds">{m["fav_ml"]}</div>
          </a>
          <a class="sb-book-row" href="#" data-aff="fanduel" rel="noopener sponsored" target="_blank">
            <div><div class="sb-book-name">FanDuel</div><div class="sb-book-bonus">$200 Bonus Bets</div></div>
            <div class="sb-book-odds">{m["fav_ml"]}</div>
          </a>
          <a class="sb-book-row" href="#" data-aff="betmgm" rel="noopener sponsored" target="_blank">
            <div><div class="sb-book-name">BetMGM</div><div class="sb-book-bonus">Up to $1,500 Back</div></div>
            <div class="sb-book-odds">{m["fav_ml"]}</div>
          </a>
          <a class="sb-book-row" href="#" data-aff="caesars" rel="noopener sponsored" target="_blank">
            <div><div class="sb-book-name">Caesars</div><div class="sb-book-bonus">$1,000 First Bet</div></div>
            <div class="sb-book-odds">{m["fav_ml"]}</div>
          </a>
          <div style="font-size:10px;color:var(--t3);margin-top:10px;">21+ only · T&amp;Cs apply · Odds subject to change</div>
        </div>
      </div>

      <!-- Trending searches -->
      <div class="sidebar-card">
        <div class="sc-head">🔥 Trending Searches</div>
        <div class="sc-body">
{trending_html}        </div>
      </div>

      <!-- Ad slot sidebar -->
      <div style="text-align:center;margin-bottom:16px;">
        <ins class="adsbygoogle" style="display:inline-block;width:300px;height:250px" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <!-- Next matches -->
      <div class="sidebar-card">
        <div class="sc-head">Up Next — Group {m["group"]}</div>
        <div class="sc-body">
{up_next_html}        </div>
      </div>

      <!-- 𝕏 Analyst Feed -->
      <div class="sidebar-card">
        <div class="sc-head">𝕏 Analyst Feed</div>
        <div style="padding:12px 12px 0;font-size:11px;color:var(--t3);font-family:var(--cond);letter-spacing:.04em;margin-bottom:8px;">LIVE FROM @FIFAWORLDCUP &amp; @OPTAJOE</div>
        <div style="overflow:hidden;max-height:460px;">
          <a class="twitter-timeline"
             href="https://twitter.com/FIFAWorldCup"
             data-tweet-limit="3"
             data-chrome="nofooter noheader noborders transparent"
             data-theme="light"
             data-dnt="true">
            Loading match tweets…
          </a>
        </div>
        <div style="padding:10px 12px;border-top:1px solid var(--b1);text-align:center;">
          <a href="https://twitter.com/getpitchiq" target="_blank" rel="noopener noreferrer"
             style="font-family:var(--cond);font-size:11px;font-weight:700;color:var(--grn);letter-spacing:.06em;text-transform:uppercase;">
            Follow @getpitchiq for live picks →
          </a>
        </div>
      </div>

    '''


# ── Page assembler ────────────────────────────────────────────────────────────

def generate_page(m):
    h = TEMPLATE

    # Fix og:image bug
    h = h.replace('og-image.jpg', 'pitchiq-banner.png')

    # Vercel Analytics injection
    if '/_vercel/insights/script.js' not in h:
        h = h.replace(
            '  <link rel="preconnect" href="https://fonts.googleapis.com"/>',
            '  <script defer src="/_vercel/insights/script.js"></script>\n\n  <link rel="preconnect" href="https://fonts.googleapis.com"/>'
        )

    # Title
    h = h.replace(
        'Brazil vs Morocco Prediction, Odds &amp; Fantasy Picks — World Cup 2026 | PitchIQ',
        f'{m["home"]} vs {m["away"]} Prediction, Odds &amp; Fantasy Picks — World Cup 2026 | PitchIQ'
    )
    h = h.replace(
        'Brazil vs Morocco Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ',
        f'{m["home"]} vs {m["away"]} Prediction, Odds &amp; Fantasy Picks — World Cup 2026 | PitchIQ'
    )

    # Meta description
    h = re.sub(
        r'<meta name="description" content="[^"]*"/>',
        f'<meta name="description" content="{m["home"]} vs {m["away"]} World Cup 2026 prediction, betting odds, AI analysis and fantasy picks. Group {m["group"]} match on {m["date_short"]} at {m["venue_short"]}. {m["fav_name"]} {m["fav_ml"]} favorite."/>',
        h
    )

    # Canonical + OG URL (both use same value in template)
    h = h.replace('https://getpitchiq.net/brazil-morocco', f'https://getpitchiq.net/{m["slug"]}')

    # OG title
    h = re.sub(
        r'<meta property="og:title" content="[^"]*"/>',
        f'<meta property="og:title" content="{m["home"]} vs {m["away"]} Prediction &amp; Odds — World Cup 2026 Group {m["group"]}"/>',
        h
    )

    # OG description
    h = re.sub(
        r'<meta property="og:description" content="[^"]*"/>',
        f'<meta property="og:description" content="AI-powered prediction, live odds and fantasy picks for {m["home"]} vs {m["away"]}. Group {m["group"]}, {m["date_short"]}, {m["venue_short"]}."/>',
        h
    )

    # JSON-LD SportsEvent
    h = re.sub(
        r'\{"@context":"https://schema\.org","@type":"SportsEvent"[^<]*\}',
        f'{{"@context":"https://schema.org","@type":"SportsEvent","name":"{m["home"]} vs {m["away"]}","startDate":"{m["json_dt"]}","location":{{"@type":"Place","name":"{m["venue_name"]}","address":"{m["venue_addr"]}"}},"sport":"Soccer","description":"FIFA World Cup 2026 Group {m["group"]} match between {m["home"]} and {m["away"]}"}}',
        h
    )

    # Stadium background photo (appears twice: header + sidebar thumbnail)
    h = h.replace('1556816214-6d16c62fbbf6', m['photo'])

    # Match header badge
    h = h.replace(
        '⚽ FIFA World Cup 2026 · Group C · Matchday 1',
        f'⚽ FIFA World Cup 2026 · Group {m["group"]} · Matchday {m["matchday"]}'
    )

    # Match header teams block
    old_teams = (
        '      <div class="mh-team">\n'
        '        <img src="https://flagcdn.com/w80/br.png" alt="Brazil" class="team-flag-img" loading="lazy">\n'
        '        <div class="mh-flag">🇧🇷</div>\n'
        '        <div class="mh-name">Brazil</div>\n'
        '        <div class="mh-rank">FIFA Rank #4 · Tournament Odds +800</div>\n'
        '      </div>\n'
        '      <div class="mh-vs">VS</div>\n'
        '      <div class="mh-team">\n'
        '        <img src="https://flagcdn.com/w80/ma.png" alt="Morocco" class="team-flag-img" loading="lazy">\n'
        '        <div class="mh-flag">🇲🇦</div>\n'
        '        <div class="mh-name">Morocco</div>\n'
        '        <div class="mh-rank">FIFA Rank #14 · Tournament Odds +5000</div>\n'
        '      </div>'
    )
    new_teams = (
        f'      <div class="mh-team">\n'
        f'        <img src="https://flagcdn.com/w80/{m["home_code"]}.png" alt="{m["home"]}" class="team-flag-img" loading="lazy">\n'
        f'        <div class="mh-flag">{m["home_emoji"]}</div>\n'
        f'        <div class="mh-name">{m["home"]}</div>\n'
        f'        <div class="mh-rank">{m["home_rank"]}</div>\n'
        f'      </div>\n'
        f'      <div class="mh-vs">VS</div>\n'
        f'      <div class="mh-team">\n'
        f'        <img src="https://flagcdn.com/w80/{m["away_code"]}.png" alt="{m["away"]}" class="team-flag-img" loading="lazy">\n'
        f'        <div class="mh-flag">{m["away_emoji"]}</div>\n'
        f'        <div class="mh-name">{m["away"]}</div>\n'
        f'        <div class="mh-rank">{m["away_rank"]}</div>\n'
        f'      </div>'
    )
    h = h.replace(old_teams, new_teams)

    # Date / time / venue
    h = h.replace('📅 Saturday, June 13, 2026', f'📅 {m["date_str"]}')
    h = h.replace('🕕 6:00 PM ET', f'🕕 {m["time_str"]}')
    h = h.replace('🏟 MetLife Stadium, East Rutherford, NJ', f'🏟 {m["venue"]}')

    # Breadcrumb
    h = h.replace('    Brazil vs Morocco\n', f'    {m["home"]} vs {m["away"]}\n')

    # Odds strip — date
    h = h.replace('Updated Jun 13', f'Updated {m["date_short"]}')

    # Odds strip — cards (replace Brazil-specific values)
    home_cls = 'fav' if m['home_ml'].startswith('-') else 'dog'
    h = h.replace('<div class="odd-label">Brazil Win</div>', f'<div class="odd-label">{m["home"]} Win</div>')
    h = h.replace('<div class="odd-val fav">-138</div>', f'<div class="odd-val {home_cls}">{m["home_ml"]}</div>')
    h = h.replace('<div class="odd-val dog">+290</div>', f'<div class="odd-val dog">{m["draw_ml"]}</div>')
    h = h.replace('<div class="odd-label">Morocco Win</div>', f'<div class="odd-label">{m["away"]} Win</div>')
    away_cls = 'fav' if m['away_ml'].startswith('-') else 'dog'
    h = h.replace('<div class="odd-val dog">+500</div>', f'<div class="odd-val {away_cls}">{m["away_ml"]}</div>')
    h = h.replace('<div class="odd-val dog">-110</div>', f'<div class="odd-val dog">{m["ou_over"]}</div>')
    h = h.replace('<div class="odd-val dog">-120</div>', f'<div class="odd-val dog">{m["ou_under"]}</div>')

    # Replace content sections via markers
    h = replace_between(h, '      <!-- AI Prediction -->', '      <!-- Match Analysis -->', ai_section(m))
    h = replace_between(h, '      <!-- Match Analysis -->', '      <!-- Stats Comparison -->', analysis_section(m))
    h = replace_between(h, '      <!-- Stats Comparison -->', '      <!-- Betting Picks -->', stats_section(m))
    h = replace_between(h, '      <!-- Betting Picks -->', '      <!-- Fantasy Picks -->', picks_section(m))
    h = replace_between(h, '      <!-- Fantasy Picks -->', '    </div><!-- /main -->', fantasy_section(m))
    h = replace_between(h, '    <!-- SIDEBAR -->', '    </div><!-- /sidebar -->', sidebar_section(m))

    return h


# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        from match_data import MATCHES
    except ImportError:
        print('ERROR: match_data.py not found. Run this script from the project directory.')
        sys.exit(1)

    filter_slugs = set(sys.argv[1:])  # optional: pass slugs to regenerate only those
    generated = 0
    errors = 0

    for m in MATCHES:
        if filter_slugs and m['slug'] not in filter_slugs:
            continue
        try:
            content = generate_page(m)
            out_path = os.path.join(PROJ, m['slug'] + '.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  {m["slug"]}.html')
            generated += 1
        except Exception as e:
            print(f'  ERROR {m["slug"]}: {e}')
            errors += 1

    print(f'\n  Generated {generated} pages', end='')
    if errors:
        print(f', {errors} errors')
    else:
        print()
