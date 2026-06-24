#!/usr/bin/env python3
"""Generate PitchIQ post-match result pages from result_data.py."""

import html
import os
import sys

PROJ = os.path.dirname(os.path.abspath(__file__))

FLAG = {
    'mx': '🇲🇽', 'za': '🇿🇦', 'kr': '🇰🇷', 'cz': '🇨🇿', 'ca': '🇨🇦', 'ba': '🇧🇦',
    'us': '🇺🇸', 'py': '🇵🇾', 'qa': '🇶🇦', 'ch': '🇨🇭', 'br': '🇧🇷', 'ma': '🇲🇦',
    'ht': '🇭🇹', 'gb-sct': '🏴󠁧󠁢󠁳󠁣󠁴󠁿', 'au': '🇦🇺', 'tr': '🇹🇷',
}


def esc(value):
    return html.escape(str(value), quote=True)


def sentences(text, limit=3):
    parts = [p.strip() for p in text.split('. ') if p.strip()]
    if len(parts) <= limit:
        return text
    trimmed = '. '.join(parts[:limit])
    return trimmed if trimmed.endswith('.') else trimmed + '.'


def result_headline(r):
    return f"{r['home']} {r['home_score']}–{r['away_score']} {r['away']}: {r['man_of_match']} Sets the Tone"


def build_page(slug, r, match):
    outcome = r['pick_result'].upper()
    pick_class = 'win' if outcome == 'WIN' else 'loss'
    pick_text = '✓ WIN' if outcome == 'WIN' else '✗ LOSS'
    home_flag = FLAG.get(r.get('home_iso'), match.get('home_emoji', '🏳'))
    away_flag = FLAG.get(r.get('away_iso'), match.get('away_emoji', '🏳'))
    scorers = ''.join(f'<li>{esc(s)}</li>' for s in r.get('scorers', [])) or '<li>No goalscorers listed</li>'
    next_match = r.get('next_match', {})
    next_href = '/' + next_match.get('slug', '')
    next_label = f"{next_match.get('home', '')} vs {next_match.get('away', '')}"
    next_date = next_match.get('date', '')
    summary = sentences(r.get('ai_summary', ''), 3)
    headline = result_headline(r)
    description = f"Final score, scorers, AI match summary and PitchIQ pick result for {r['home']} vs {r['away']} at the 2026 FIFA World Cup."
    photo = match.get('photo', '1556816214-6d16c62fbbf6')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <meta name="theme-color" content="#071D36"/>
  <title>{esc(headline)} | PitchIQ</title>
  <meta name="description" content="{esc(description)}"/>
  <meta name="robots" content="index, follow"/>
  <link rel="canonical" href="https://getpitchiq.net/{esc(slug)}-result"/>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="PitchIQ"/>
  <meta property="og:url" content="https://getpitchiq.net/{esc(slug)}-result"/>
  <meta property="og:title" content="{esc(headline)}"/>
  <meta property="og:description" content="{esc(description)}"/>
  <meta property="og:image" content="https://getpitchiq.net/pitchiq-banner.png"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:site" content="@getpitchiq"/>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article","headline":"{esc(headline)}","description":"{esc(description)}","author":{{"@type":"Organization","name":"PitchIQ","url":"https://getpitchiq.net"}},"publisher":{{"@type":"Organization","name":"PitchIQ","url":"https://getpitchiq.net"}}}}
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
    .nav-logo{{font-family:var(--cond);font-size:22px;font-weight:900;color:#fff}} .nav-logo span{{color:var(--grn)}}
    .nav-links{{display:flex;gap:4px}} .nav-links a{{font-family:var(--cond);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.65);padding:6px 12px;border-radius:var(--r)}} .nav-links a:hover{{color:#fff;background:rgba(255,255,255,.08)}}
    .btn-pro{{font-family:var(--cond);font-size:12px;font-weight:800;letter-spacing:.06em;color:#fff;background:var(--grn);padding:7px 14px;border-radius:var(--r)}}
    .hero{{background:var(--nav);background-image:linear-gradient(rgba(7,29,54,.90),rgba(7,29,54,.96)),url('https://images.unsplash.com/photo-{esc(photo)}?w=1600&q=80&fit=crop');background-size:cover;background-position:center top;padding:38px 0 34px;margin-bottom:26px;text-align:center}}
    .hero-kicker{{font-family:var(--cond);font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--grn);margin-bottom:18px}}
    .score{{display:flex;align-items:center;justify-content:center;gap:22px;margin-bottom:18px}}
    .team{{width:170px;text-align:center}} .flag{{font-size:42px;margin-bottom:6px}} .name{{font-family:var(--cond);font-size:22px;font-weight:900;color:#fff;line-height:1.05}}
    .scoreline{{font-family:var(--cond);font-size:72px;font-weight:900;line-height:1;color:#fff;white-space:nowrap}}
    h1{{font-family:var(--cond);font-size:clamp(25px,4.5vw,40px);font-weight:900;line-height:1.05;color:#fff;max-width:780px;margin:0 auto 10px}}
    .sub{{font-size:15px;color:rgba(255,255,255,.68);line-height:1.5;max-width:650px;margin:0 auto}}
    .grid{{display:grid;grid-template-columns:1fr 300px;gap:24px;align-items:start;padding-bottom:48px}} @media(max-width:850px){{.grid{{grid-template-columns:1fr}}.score{{gap:10px}}.team{{width:110px}}.scoreline{{font-size:48px}}.nav-links{{display:none}}}}
    .card{{background:var(--surf);border:1px solid var(--b1);border-radius:var(--r2);overflow:hidden;margin-bottom:18px;box-shadow:var(--sh)}}
    .card-head{{background:var(--nav);padding:12px 18px;display:flex;align-items:center;justify-content:space-between;gap:12px}}
    .card-title{{font-family:var(--cond);font-size:13px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.85)}}
    .card-body{{padding:18px}} .p{{font-size:14px;line-height:1.72;color:var(--t2)}}
    .scorers{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px 18px;list-style:none}} .scorers li{{font-size:14px;color:var(--t2);padding:8px 0;border-bottom:1px solid var(--b1)}}
    .pick-badge{{font-family:var(--cond);font-size:13px;font-weight:900;letter-spacing:.08em;padding:6px 12px;border-radius:var(--r);color:#fff;background:var(--grn)}} .pick-badge.loss{{background:var(--red)}}
    .motm{{font-family:var(--cond);font-size:30px;font-weight:900;color:var(--t1);line-height:1}} .motm span{{color:var(--grn)}}
    .next{{display:flex;align-items:center;justify-content:space-between;gap:18px;background:rgba(0,150,63,.08);border:1px solid rgba(0,150,63,.2);border-radius:var(--r);padding:16px;color:var(--t1)}} .next strong{{font-family:var(--cond);font-size:22px;font-weight:900;display:block}} .next small{{color:var(--t3)}} .next b{{font-family:var(--cond);color:var(--grn);font-size:14px;letter-spacing:.04em}}
    .side-card{{background:var(--surf);border:1px solid var(--b1);border-radius:var(--r2);overflow:hidden;margin-bottom:18px;box-shadow:var(--sh)}} .side-head{{background:var(--nav);padding:12px 16px;font-family:var(--cond);font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.7)}} .side-body{{padding:16px}}
    .footer{{background:var(--nav);color:rgba(255,255,255,.5);font-size:11px;padding:24px 0;margin-top:40px;text-align:center;line-height:1.8}} .footer a{{color:rgba(255,255,255,.5);text-decoration:underline}} .footer a:hover{{color:#fff}}
  </style>
</head>
<body>
<nav class="nav" aria-label="Primary navigation"><div class="nav-inner"><a class="nav-logo" href="/">Pitch<span>IQ</span></a><div class="nav-links"><a href="/predictions">Picks</a><a href="/standings">Standings</a><a href="/fantasy">Fantasy</a><a href="/picks-record">Record</a></div><a class="btn-pro" href="#">Go Pro ↗</a></div></nav>
<section class="hero">
  <div class="w">
    <div class="hero-kicker">FIFA World Cup 2026 · Group {esc(r['group'])} · Final</div>
    <div class="score">
      <div class="team"><div class="flag">{home_flag}</div><div class="name">{esc(r['home'])}</div></div>
      <div class="scoreline">{r['home_score']}–{r['away_score']}</div>
      <div class="team"><div class="flag">{away_flag}</div><div class="name">{esc(r['away'])}</div></div>
    </div>
    <h1>{esc(headline)}</h1>
    <p class="sub">{esc(r['date'])} · {esc(r['venue'])}</p>
  </div>
</section>
<main class="w grid">
  <div>
    <section class="card"><div class="card-head"><div class="card-title">Final Score</div></div><div class="card-body"><div class="scoreline" style="color:var(--t1);text-align:center">{r['home_score']}–{r['away_score']}</div></div></section>
    <section class="card"><div class="card-head"><div class="card-title">Scorers</div></div><div class="card-body"><ul class="scorers">{scorers}</ul></div></section>
    <section class="card"><div class="card-head"><div class="card-title">PitchIQ Pick Result</div><div class="pick-badge {pick_class}">{pick_text}</div></div><div class="card-body"><p class="p"><strong>{esc(r['pitchiq_pick'])}</strong> finished as a {esc(outcome)}.</p></div></section>
    <section class="card"><div class="card-head"><div class="card-title">AI Match Summary</div></div><div class="card-body"><p class="p">{esc(summary)}</p></div></section>
    <section class="card"><div class="card-head"><div class="card-title">Man of the Match</div></div><div class="card-body"><div class="motm"><span>★</span> {esc(r['man_of_match'])}</div></div></section>
    <a class="next" href="{esc(next_href)}"><span><small>Next match · {esc(next_date)}</small><strong>{esc(next_label)}</strong></span><b>Preview →</b></a>
  </div>
  <aside>
    <div class="side-card"><div class="side-head">Match Info</div><div class="side-body"><p class="p">Group {esc(r['group'])}<br>{esc(r['date'])}<br>{esc(r['venue'])}</p></div></div>
    <div class="side-card"><div class="side-head">Related</div><div class="side-body"><a href="/{esc(slug)}">Original preview ↗</a><br><br><a href="/predictions">All predictions ↗</a><br><br><a href="/picks-record">Pick record ↗</a></div></div>
  </aside>
</main>
<footer class="footer">© 2026 PitchIQ · <a href="/">getpitchiq.net</a> · <a href="/predictions.html">More predictions →</a> · Entertainment purposes only · Must be 21+ to bet · <a href="https://www.ncpgambling.org" target="_blank" rel="noopener">Responsible Gambling</a></footer>
</body>
</html>"""


def main():
    try:
        from result_data import RESULTS
        from match_data import MATCHES
    except ImportError as e:
        print(f"ERROR: {e}. Run this script from the project directory.")
        sys.exit(1)

    match_index = {m['slug']: m for m in MATCHES}
    filter_slugs = set(sys.argv[1:])
    generated = 0
    errors = 0

    for slug, result in RESULTS.items():
        if filter_slugs and slug not in filter_slugs:
            continue
        match = match_index.get(slug, {})
        if not match:
            print(f'  WARNING: No match data found for slug "{slug}" — using result data only')
        try:
            content = build_page(slug, result, match)
            out_path = os.path.join(PROJ, slug + '-result.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  {slug}-result.html [{result['pick_result']}]")
            generated += 1
        except Exception as e:
            print(f"  ERROR {slug}: {e}")
            errors += 1

    print(f"\n  Generated {generated} result pages", end="")
    if errors:
        print(f", {errors} errors")
    else:
        print()


if __name__ == '__main__':
    main()
