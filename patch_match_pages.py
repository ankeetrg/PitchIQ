#!/usr/bin/env python3
"""
PitchIQ — one-time patch for all existing match preview pages.

Adds to each match page:
  1. Three <meta> tags so pitchiq-live.js knows the page context:
       <meta name="pitchiq:page"  content="match">
       <meta name="pitchiq:slug"  content="brazil-morocco">
       <meta name="pitchiq:home"  content="Brazil">
       <meta name="pitchiq:away"  content="Morocco">
  2. Two <script> tags before </body>:
       <script src="/js/pitchiq-config.js">
       <script src="/js/pitchiq-live.js">

Safe to re-run — skips pages that already have the tags.

Run once after cloning, and again if you add new match pages:
    python3 patch_match_pages.py
    python3 patch_match_pages.py --dry    # preview changes only
"""

import os, re, sys, importlib.util, pathlib

PROJ    = pathlib.Path(__file__).parent
DRY     = '--dry' in sys.argv

# Load match data
spec = importlib.util.spec_from_file_location('match_data', PROJ / 'match_data.py')
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
MATCHES = mod.MATCHES

META_SENTINEL = 'pitchiq:slug'   # presence check — skip if already patched
SCRIPTS = '''\
  <script src="/js/pitchiq-config.js"></script>
  <script src="/js/pitchiq-live.js"></script>
</body>'''


def build_meta(m):
    return (
        f'  <meta name="pitchiq:page"  content="match"/>\n'
        f'  <meta name="pitchiq:slug"  content="{m["slug"]}"/>\n'
        f'  <meta name="pitchiq:home"  content="{m["home"]}"/>\n'
        f'  <meta name="pitchiq:away"  content="{m["away"]}"/>\n'
    )


def patch(path, meta_block):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if META_SENTINEL in html:
        return False   # already patched

    # Insert meta tags before </head>
    if '</head>' not in html:
        print(f'  WARN: no </head> in {path.name} — skipping')
        return False
    html = html.replace('</head>', meta_block + '</head>', 1)

    # Insert scripts before </body>
    if '</body>' not in html:
        print(f'  WARN: no </body> in {path.name} — skipping')
        return False
    html = html.replace('</body>', SCRIPTS, 1)

    if not DRY:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return True


def main():
    patched = 0
    skipped = 0
    for m in MATCHES:
        path = PROJ / f'{m["slug"]}.html'
        if not path.exists():
            skipped += 1
            continue
        changed = patch(path, build_meta(m))
        if changed:
            patched += 1
            label = '[DRY] ' if DRY else ''
            print(f'  {label}✓ {m["slug"]}.html')
        else:
            skipped += 1

    print(f'\n{patched} pages patched, {skipped} skipped (already done or missing).')
    if DRY:
        print('Run without --dry to apply.')


if __name__ == '__main__':
    main()
