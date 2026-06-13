# PitchIQ — EMERGENCY SCHEDULE FIX
## Run with: claude --dangerously-skip-permissions

---

## SITUATION

The site has 9 match pages for matches that DO NOT EXIST in World Cup 2026.
These must be deleted immediately. v3 already correctly built Groups A, B, and C.
This prompt deletes the wrong pages and builds all remaining real matches (Groups D–L).

---

## VERIFIED GROUPS (source: FIFA / Al Jazeera / Yahoo Sports, June 2026)

```
Group A: Mexico, South Africa, Korea Republic, Czechia
Group B: Canada, Bosnia and Herzegovina, Qatar, Switzerland
Group C: Brazil, Morocco, Haiti, Scotland
Group D: USA, Paraguay, Australia, Türkiye
Group E: Germany, Curaçao, Ivory Coast, Ecuador
Group F: Netherlands, Japan, Sweden, Tunisia
Group G: Belgium, Egypt, Iran, New Zealand
Group H: Spain, Cape Verde, Saudi Arabia, Uruguay
Group I: France, Senegal, Iraq, Norway
Group J: Argentina, Algeria, Austria, Jordan
Group K: Portugal, DR Congo, Uzbekistan, Colombia
Group L: England, Croatia, Ghana, Panama
```

---

## PHASE 1 — DELETE WRONG PAGES (do this first)

```python
import os

WRONG_PAGES = [
    'uruguay-serbia.html',
    'france-albania.html',
    'argentina-peru.html',
    'colombia-ecuador.html',
    'england-senegal.html',
    'portugal-indonesia.html',
    'croatia-australia.html',
    'senegal-slovakia.html',
    'usa-bolivia.html',
]

deleted = []
for page in WRONG_PAGES:
    if os.path.exists(page):
        os.remove(page)
        deleted.append(page)
        print(f'DELETED: {page}')
    else:
        print(f'NOT FOUND (already gone): {page}')

print(f'\nDeleted {len(deleted)} wrong pages.')
```

Also check if any other pages reference these slugs and remove those links:
```bash
grep -rl "uruguay-serbia\|france-albania\|argentina-peru\|colombia-ecuador\|england-senegal\|portugal-indonesia\|croatia-australia\|senegal-slovakia\|usa-bolivia" *.html | head -20
```
Remove any `href` links to deleted pages from index.html, predictions.html, and standings.html.

---

## PHASE 2 — BUILD REMAINING REAL MATCH PAGES

### Already correctly built (DO NOT rebuild):
```
Groups A, B, C — all 18 pages built by v3 ✅
germany-curacao (Group E, Jun 14) ✅
netherlands-japan (Group F, Jun 14) ✅
spain-capeverde (Group H, Jun 15) ✅
belgium-newzealand (Group G, Jun 26) ✅
```

### Build these 50 pages — full verified data below:

Use brazil-morocco.html as the master template. Write a Python generator.
Read brazil-morocco.html fully before starting.

#### COMPLETE MATCH DATA — ALL REMAINING MATCHES

```python
MATCHES = [

  # ── GROUP D ────────────────────────────────────────────────────────────
  {
    'slug': 'usa-paraguay', 'home': 'United States', 'away': 'Paraguay',
    'home_code': 'us', 'away_code': 'py', 'home_rank': '#11 FIFA', 'away_rank': '#63 FIFA',
    'group': 'D', 'matchday': 1, 'date': 'June 12, 2026', 'time': '9:00 PM ET',
    'venue': 'Los Angeles Stadium, Inglewood, CA',
    'home_prob': 58, 'draw_prob': 22, 'away_prob': 20,
    'home_ml': '-165', 'draw_ml': '+270', 'away_ml': '+430',
    'ai_pick': 'USA Win', 'over_under': '2.5',
    'photo_id': '1430232324554-8f4aebd06683',
    'json_date': '2026-06-12T21:00:00-07:00',
  },
  {
    'slug': 'australia-turkey', 'home': 'Australia', 'away': 'Türkiye',
    'home_code': 'au', 'away_code': 'tr', 'home_rank': '#23 FIFA', 'away_rank': '#26 FIFA',
    'group': 'D', 'matchday': 1, 'date': 'June 13, 2026', 'time': '12:00 AM ET',
    'venue': 'BC Place, Vancouver, Canada',
    'home_prob': 34, 'draw_prob': 28, 'away_prob': 38,
    'home_ml': '+210', 'draw_ml': '+230', 'away_ml': '+155',
    'ai_pick': 'Türkiye Win', 'over_under': '2.5',
    'photo_id': '1569531955323-33c6b2dca44b',
    'json_date': '2026-06-13T00:00:00-07:00',
  },
  {
    'slug': 'usa-australia', 'home': 'United States', 'away': 'Australia',
    'home_code': 'us', 'away_code': 'au', 'home_rank': '#11 FIFA', 'away_rank': '#23 FIFA',
    'group': 'D', 'matchday': 2, 'date': 'June 19, 2026', 'time': '3:00 PM ET',
    'venue': 'Lumen Field, Seattle, WA',
    'home_prob': 52, 'draw_prob': 24, 'away_prob': 24,
    'home_ml': '-130', 'draw_ml': '+260', 'away_ml': '+350',
    'ai_pick': 'USA Win', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-19T15:00:00-07:00',
  },
  {
    'slug': 'turkey-paraguay', 'home': 'Türkiye', 'away': 'Paraguay',
    'home_code': 'tr', 'away_code': 'py', 'home_rank': '#26 FIFA', 'away_rank': '#63 FIFA',
    'group': 'D', 'matchday': 2, 'date': 'June 19, 2026', 'time': '11:00 PM ET',
    'venue': "Levi's Stadium, Santa Clara, CA",
    'home_prob': 54, 'draw_prob': 24, 'away_prob': 22,
    'home_ml': '-145', 'draw_ml': '+270', 'away_ml': '+380',
    'ai_pick': 'Türkiye Win', 'over_under': '2.5',
    'photo_id': '1556816214-6d16c62fbbf6',
    'json_date': '2026-06-19T23:00:00-07:00',
  },
  {
    'slug': 'turkey-usa', 'home': 'Türkiye', 'away': 'United States',
    'home_code': 'tr', 'away_code': 'us', 'home_rank': '#26 FIFA', 'away_rank': '#11 FIFA',
    'group': 'D', 'matchday': 3, 'date': 'June 25, 2026', 'time': '10:00 PM ET',
    'venue': 'Los Angeles Stadium, Inglewood, CA',
    'home_prob': 32, 'draw_prob': 28, 'away_prob': 40,
    'home_ml': '+240', 'draw_ml': '+230', 'away_ml': '+140',
    'ai_pick': 'USA Win or Draw', 'over_under': '2.5',
    'photo_id': '1430232324554-8f4aebd06683',
    'json_date': '2026-06-25T22:00:00-07:00',
  },
  {
    'slug': 'paraguay-australia', 'home': 'Paraguay', 'away': 'Australia',
    'home_code': 'py', 'away_code': 'au', 'home_rank': '#63 FIFA', 'away_rank': '#23 FIFA',
    'group': 'D', 'matchday': 3, 'date': 'June 25, 2026', 'time': '10:00 PM ET',
    'venue': "Levi's Stadium, Santa Clara, CA",
    'home_prob': 28, 'draw_prob': 26, 'away_prob': 46,
    'home_ml': '+310', 'draw_ml': '+240', 'away_ml': '+115',
    'ai_pick': 'Australia Win', 'over_under': '2.5',
    'photo_id': '1599158150601-1417ebbaafdd',
    'json_date': '2026-06-25T22:00:00-07:00',
  },

  # ── GROUP E ────────────────────────────────────────────────────────────
  {
    'slug': 'ivorycoast-ecuador', 'home': 'Ivory Coast', 'away': 'Ecuador',
    'home_code': 'ci', 'away_code': 'ec', 'home_rank': '#19 FIFA', 'away_rank': '#34 FIFA',
    'group': 'E', 'matchday': 1, 'date': 'June 14, 2026', 'time': '7:00 PM ET',
    'venue': 'Lincoln Financial Field, Philadelphia, PA',
    'home_prob': 44, 'draw_prob': 26, 'away_prob': 30,
    'home_ml': '-115', 'draw_ml': '+240', 'away_ml': '+310',
    'ai_pick': 'Ivory Coast Win', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-14T19:00:00-04:00',
  },
  {
    'slug': 'germany-ivorycoast', 'home': 'Germany', 'away': 'Ivory Coast',
    'home_code': 'de', 'away_code': 'ci', 'home_rank': '#12 FIFA', 'away_rank': '#19 FIFA',
    'group': 'E', 'matchday': 2, 'date': 'June 20, 2026', 'time': '4:00 PM ET',
    'venue': 'BMO Field, Toronto, Canada',
    'home_prob': 55, 'draw_prob': 23, 'away_prob': 22,
    'home_ml': '-150', 'draw_ml': '+270', 'away_ml': '+390',
    'ai_pick': 'Germany Win', 'over_under': '2.5',
    'photo_id': '1489944440615-453fc2b6a9a9',
    'json_date': '2026-06-20T16:00:00-04:00',
  },
  {
    'slug': 'ecuador-curacao', 'home': 'Ecuador', 'away': 'Curaçao',
    'home_code': 'ec', 'away_code': 'cw', 'home_rank': '#34 FIFA', 'away_rank': '#84 FIFA',
    'group': 'E', 'matchday': 2, 'date': 'June 20, 2026', 'time': '8:00 PM ET',
    'venue': 'Arrowhead Stadium, Kansas City, MO',
    'home_prob': 72, 'draw_prob': 17, 'away_prob': 11,
    'home_ml': '-280', 'draw_ml': '+370', 'away_ml': '+750',
    'ai_pick': 'Ecuador Win', 'over_under': '2.5',
    'photo_id': '1651421738652-12124d47c917',
    'json_date': '2026-06-20T20:00:00-04:00',
  },
  {
    'slug': 'curacao-ivorycoast', 'home': 'Curaçao', 'away': 'Ivory Coast',
    'home_code': 'cw', 'away_code': 'ci', 'home_rank': '#84 FIFA', 'away_rank': '#19 FIFA',
    'group': 'E', 'matchday': 3, 'date': 'June 25, 2026', 'time': '4:00 PM ET',
    'venue': 'Lincoln Financial Field, Philadelphia, PA',
    'home_prob': 15, 'draw_prob': 20, 'away_prob': 65,
    'home_ml': '+500', 'draw_ml': '+310', 'away_ml': '-210',
    'ai_pick': 'Ivory Coast Win', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-25T16:00:00-04:00',
  },
  {
    'slug': 'ecuador-germany', 'home': 'Ecuador', 'away': 'Germany',
    'home_code': 'ec', 'away_code': 'de', 'home_rank': '#34 FIFA', 'away_rank': '#12 FIFA',
    'group': 'E', 'matchday': 3, 'date': 'June 25, 2026', 'time': '4:00 PM ET',
    'venue': 'MetLife Stadium, East Rutherford, NJ',
    'home_prob': 22, 'draw_prob': 26, 'away_prob': 52,
    'home_ml': '+340', 'draw_ml': '+240', 'away_ml': '-125',
    'ai_pick': 'Germany Win', 'over_under': '2.5',
    'photo_id': '1556816214-6d16c62fbbf6',
    'json_date': '2026-06-25T16:00:00-04:00',
  },

  # ── GROUP F ────────────────────────────────────────────────────────────
  {
    'slug': 'sweden-tunisia', 'home': 'Sweden', 'away': 'Tunisia',
    'home_code': 'se', 'away_code': 'tn', 'home_rank': '#24 FIFA', 'away_rank': '#33 FIFA',
    'group': 'F', 'matchday': 1, 'date': 'June 14, 2026', 'time': '10:00 PM ET',
    'venue': 'Estadio BBVA, Monterrey, Mexico',
    'home_prob': 46, 'draw_prob': 28, 'away_prob': 26,
    'home_ml': '-120', 'draw_ml': '+250', 'away_ml': '+330',
    'ai_pick': 'Sweden Win or Draw', 'over_under': '2.5',
    'photo_id': '1705593973313-75de7bf95b56',
    'json_date': '2026-06-14T22:00:00-04:00',
  },
  {
    'slug': 'netherlands-sweden', 'home': 'Netherlands', 'away': 'Sweden',
    'home_code': 'nl', 'away_code': 'se', 'home_rank': '#7 FIFA', 'away_rank': '#24 FIFA',
    'group': 'F', 'matchday': 2, 'date': 'June 20, 2026', 'time': '1:00 PM ET',
    'venue': 'NRG Stadium, Houston, TX',
    'home_prob': 58, 'draw_prob': 22, 'away_prob': 20,
    'home_ml': '-175', 'draw_ml': '+290', 'away_ml': '+440',
    'ai_pick': 'Netherlands Win', 'over_under': '2.5',
    'photo_id': '1569531955323-33c6b2dca44b',
    'json_date': '2026-06-20T13:00:00-04:00',
  },
  {
    'slug': 'tunisia-japan', 'home': 'Tunisia', 'away': 'Japan',
    'home_code': 'tn', 'away_code': 'jp', 'home_rank': '#33 FIFA', 'away_rank': '#17 FIFA',
    'group': 'F', 'matchday': 2, 'date': 'June 20, 2026', 'time': '12:00 AM ET',
    'venue': 'Estadio BBVA, Monterrey, Mexico',
    'home_prob': 28, 'draw_prob': 28, 'away_prob': 44,
    'home_ml': '+280', 'draw_ml': '+240', 'away_ml': '-115',
    'ai_pick': 'Japan Win', 'over_under': '2.5',
    'photo_id': '1705593973313-75de7bf95b56',
    'json_date': '2026-06-20T00:00:00-06:00',
  },
  {
    'slug': 'japan-sweden', 'home': 'Japan', 'away': 'Sweden',
    'home_code': 'jp', 'away_code': 'se', 'home_rank': '#17 FIFA', 'away_rank': '#24 FIFA',
    'group': 'F', 'matchday': 3, 'date': 'June 25, 2026', 'time': '7:00 PM ET',
    'venue': 'AT&T Stadium, Arlington, TX',
    'home_prob': 42, 'draw_prob': 28, 'away_prob': 30,
    'home_ml': '+110', 'draw_ml': '+240', 'away_ml': '+260',
    'ai_pick': 'Japan Win or Draw', 'over_under': '2.5',
    'photo_id': '1569531955323-33c6b2dca44b',
    'json_date': '2026-06-25T19:00:00-04:00',
  },
  {
    'slug': 'tunisia-netherlands', 'home': 'Tunisia', 'away': 'Netherlands',
    'home_code': 'tn', 'away_code': 'nl', 'home_rank': '#33 FIFA', 'away_rank': '#7 FIFA',
    'group': 'F', 'matchday': 3, 'date': 'June 25, 2026', 'time': '7:00 PM ET',
    'venue': 'Arrowhead Stadium, Kansas City, MO',
    'home_prob': 16, 'draw_prob': 22, 'away_prob': 62,
    'home_ml': '+480', 'draw_ml': '+290', 'away_ml': '-195',
    'ai_pick': 'Netherlands Win', 'over_under': '2.5',
    'photo_id': '1651421738652-12124d47c917',
    'json_date': '2026-06-25T19:00:00-04:00',
  },

  # ── GROUP G ────────────────────────────────────────────────────────────
  {
    'slug': 'belgium-egypt', 'home': 'Belgium', 'away': 'Egypt',
    'home_code': 'be', 'away_code': 'eg', 'home_rank': '#3 FIFA', 'away_rank': '#36 FIFA',
    'group': 'G', 'matchday': 1, 'date': 'June 15, 2026', 'time': '3:00 PM ET',
    'venue': 'Lumen Field, Seattle, WA',
    'home_prob': 66, 'draw_prob': 20, 'away_prob': 14,
    'home_ml': '-220', 'draw_ml': '+310', 'away_ml': '+580',
    'ai_pick': 'Belgium Win', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-15T15:00:00-07:00',
  },
  {
    'slug': 'iran-newzealand', 'home': 'Iran', 'away': 'New Zealand',
    'home_code': 'ir', 'away_code': 'nz', 'home_rank': '#21 FIFA', 'away_rank': '#97 FIFA',
    'group': 'G', 'matchday': 1, 'date': 'June 15, 2026', 'time': '9:00 PM ET',
    'venue': 'Los Angeles Stadium, Inglewood, CA',
    'home_prob': 68, 'draw_prob': 18, 'away_prob': 14,
    'home_ml': '-240', 'draw_ml': '+340', 'away_ml': '+620',
    'ai_pick': 'Iran Win', 'over_under': '2.5',
    'photo_id': '1430232324554-8f4aebd06683',
    'json_date': '2026-06-15T21:00:00-07:00',
  },
  {
    'slug': 'belgium-iran', 'home': 'Belgium', 'away': 'Iran',
    'home_code': 'be', 'away_code': 'ir', 'home_rank': '#3 FIFA', 'away_rank': '#21 FIFA',
    'group': 'G', 'matchday': 2, 'date': 'June 21, 2026', 'time': '3:00 PM ET',
    'venue': 'Los Angeles Stadium, Inglewood, CA',
    'home_prob': 62, 'draw_prob': 22, 'away_prob': 16,
    'home_ml': '-195', 'draw_ml': '+290', 'away_ml': '+500',
    'ai_pick': 'Belgium Win', 'over_under': '2.5',
    'photo_id': '1430232324554-8f4aebd06683',
    'json_date': '2026-06-21T15:00:00-07:00',
  },
  {
    'slug': 'newzealand-egypt', 'home': 'New Zealand', 'away': 'Egypt',
    'home_code': 'nz', 'away_code': 'eg', 'home_rank': '#97 FIFA', 'away_rank': '#36 FIFA',
    'group': 'G', 'matchday': 2, 'date': 'June 21, 2026', 'time': '9:00 PM ET',
    'venue': 'BC Place, Vancouver, Canada',
    'home_prob': 28, 'draw_prob': 28, 'away_prob': 44,
    'home_ml': '+280', 'draw_ml': '+240', 'away_ml': '-120',
    'ai_pick': 'Egypt Win', 'over_under': '2.5',
    'photo_id': '1569531955323-33c6b2dca44b',
    'json_date': '2026-06-21T21:00:00-07:00',
  },
  {
    'slug': 'egypt-iran', 'home': 'Egypt', 'away': 'Iran',
    'home_code': 'eg', 'away_code': 'ir', 'home_rank': '#36 FIFA', 'away_rank': '#21 FIFA',
    'group': 'G', 'matchday': 3, 'date': 'June 26, 2026', 'time': '11:00 PM ET',
    'venue': 'Lumen Field, Seattle, WA',
    'home_prob': 30, 'draw_prob': 30, 'away_prob': 40,
    'home_ml': '+240', 'draw_ml': '+230', 'away_ml': '+135',
    'ai_pick': 'Iran Win or Draw', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-26T23:00:00-07:00',
  },

  # ── GROUP H ────────────────────────────────────────────────────────────
  {
    'slug': 'saudiarabia-uruguay', 'home': 'Saudi Arabia', 'away': 'Uruguay',
    'home_code': 'sa', 'away_code': 'uy', 'home_rank': '#56 FIFA', 'away_rank': '#15 FIFA',
    'group': 'H', 'matchday': 1, 'date': 'June 15, 2026', 'time': '6:00 PM ET',
    'venue': 'Hard Rock Stadium, Miami, FL',
    'home_prob': 22, 'draw_prob': 24, 'away_prob': 54,
    'home_ml': '+340', 'draw_ml': '+250', 'away_ml': '-140',
    'ai_pick': 'Uruguay Win', 'over_under': '2.5',
    'photo_id': '1599158150601-1417ebbaafdd',
    'json_date': '2026-06-15T18:00:00-04:00',
  },
  {
    'slug': 'spain-saudiarabia', 'home': 'Spain', 'away': 'Saudi Arabia',
    'home_code': 'es', 'away_code': 'sa', 'home_rank': '#1 FIFA', 'away_rank': '#56 FIFA',
    'group': 'H', 'matchday': 2, 'date': 'June 21, 2026', 'time': '12:00 PM ET',
    'venue': 'Mercedes-Benz Stadium, Atlanta, GA',
    'home_prob': 76, 'draw_prob': 14, 'away_prob': 10,
    'home_ml': '-360', 'draw_ml': '+450', 'away_ml': '+900',
    'ai_pick': 'Spain Win & Over 2.5', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-21T12:00:00-04:00',
  },
  {
    'slug': 'uruguay-capeverde', 'home': 'Uruguay', 'away': 'Cape Verde',
    'home_code': 'uy', 'away_code': 'cv', 'home_rank': '#15 FIFA', 'away_rank': '#79 FIFA',
    'group': 'H', 'matchday': 2, 'date': 'June 21, 2026', 'time': '6:00 PM ET',
    'venue': 'Hard Rock Stadium, Miami, FL',
    'home_prob': 70, 'draw_prob': 18, 'away_prob': 12,
    'home_ml': '-260', 'draw_ml': '+360', 'away_ml': '+680',
    'ai_pick': 'Uruguay Win', 'over_under': '2.5',
    'photo_id': '1599158150601-1417ebbaafdd',
    'json_date': '2026-06-21T18:00:00-04:00',
  },
  {
    'slug': 'capeverde-saudiarabia', 'home': 'Cape Verde', 'away': 'Saudi Arabia',
    'home_code': 'cv', 'away_code': 'sa', 'home_rank': '#79 FIFA', 'away_rank': '#56 FIFA',
    'group': 'H', 'matchday': 3, 'date': 'June 26, 2026', 'time': '8:00 PM ET',
    'venue': 'NRG Stadium, Houston, TX',
    'home_prob': 30, 'draw_prob': 28, 'away_prob': 42,
    'home_ml': '+260', 'draw_ml': '+240', 'away_ml': '+120',
    'ai_pick': 'Saudi Arabia Win or Draw', 'over_under': '2.5',
    'photo_id': '1651421738652-12124d47c917',
    'json_date': '2026-06-26T20:00:00-04:00',
  },
  {
    'slug': 'uruguay-spain', 'home': 'Uruguay', 'away': 'Spain',
    'home_code': 'uy', 'away_code': 'es', 'home_rank': '#15 FIFA', 'away_rank': '#1 FIFA',
    'group': 'H', 'matchday': 3, 'date': 'June 26, 2026', 'time': '8:00 PM ET',
    'venue': 'Estadio Akron, Guadalajara, Mexico',
    'home_prob': 20, 'draw_prob': 24, 'away_prob': 56,
    'home_ml': '+390', 'draw_ml': '+250', 'away_ml': '-155',
    'ai_pick': 'Spain Win', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-26T20:00:00-06:00',
  },

  # ── GROUP I ────────────────────────────────────────────────────────────
  {
    'slug': 'france-senegal', 'home': 'France', 'away': 'Senegal',
    'home_code': 'fr', 'away_code': 'sn', 'home_rank': '#2 FIFA', 'away_rank': '#19 FIFA',
    'group': 'I', 'matchday': 1, 'date': 'June 16, 2026', 'time': '3:00 PM ET',
    'venue': 'MetLife Stadium, East Rutherford, NJ',
    'home_prob': 62, 'draw_prob': 22, 'away_prob': 16,
    'home_ml': '-210', 'draw_ml': '+300', 'away_ml': '+520',
    'ai_pick': 'France Win', 'over_under': '2.5',
    'photo_id': '1556816214-6d16c62fbbf6',
    'json_date': '2026-06-16T15:00:00-04:00',
  },
  {
    'slug': 'iraq-norway', 'home': 'Iraq', 'away': 'Norway',
    'home_code': 'iq', 'away_code': 'no', 'home_rank': '#68 FIFA', 'away_rank': '#10 FIFA',
    'group': 'I', 'matchday': 1, 'date': 'June 16, 2026', 'time': '6:00 PM ET',
    'venue': 'Gillette Stadium, Foxborough, MA',
    'home_prob': 16, 'draw_prob': 24, 'away_prob': 60,
    'home_ml': '+480', 'draw_ml': '+270', 'away_ml': '-190',
    'ai_pick': 'Norway Win', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-16T18:00:00-04:00',
  },
  {
    'slug': 'france-iraq', 'home': 'France', 'away': 'Iraq',
    'home_code': 'fr', 'away_code': 'iq', 'home_rank': '#2 FIFA', 'away_rank': '#68 FIFA',
    'group': 'I', 'matchday': 2, 'date': 'June 22, 2026', 'time': '5:00 PM ET',
    'venue': 'Lincoln Financial Field, Philadelphia, PA',
    'home_prob': 78, 'draw_prob': 14, 'away_prob': 8,
    'home_ml': '-400', 'draw_ml': '+480', 'away_ml': '+950',
    'ai_pick': 'France Win & Over 2.5', 'over_under': '2.5',
    'photo_id': '1705593973313-75de7bf95b56',
    'json_date': '2026-06-22T17:00:00-04:00',
  },
  {
    'slug': 'norway-senegal', 'home': 'Norway', 'away': 'Senegal',
    'home_code': 'no', 'away_code': 'sn', 'home_rank': '#10 FIFA', 'away_rank': '#19 FIFA',
    'group': 'I', 'matchday': 2, 'date': 'June 22, 2026', 'time': '8:00 PM ET',
    'venue': 'MetLife Stadium, East Rutherford, NJ',
    'home_prob': 42, 'draw_prob': 28, 'away_prob': 30,
    'home_ml': '-105', 'draw_ml': '+240', 'away_ml': '+290',
    'ai_pick': 'Norway Win or Draw', 'over_under': '2.5',
    'photo_id': '1556816214-6d16c62fbbf6',
    'json_date': '2026-06-22T20:00:00-04:00',
  },
  {
    'slug': 'norway-france', 'home': 'Norway', 'away': 'France',
    'home_code': 'no', 'away_code': 'fr', 'home_rank': '#10 FIFA', 'away_rank': '#2 FIFA',
    'group': 'I', 'matchday': 3, 'date': 'June 26, 2026', 'time': '3:00 PM ET',
    'venue': 'Gillette Stadium, Foxborough, MA',
    'home_prob': 26, 'draw_prob': 26, 'away_prob': 48,
    'home_ml': '+290', 'draw_ml': '+260', 'away_ml': '-115',
    'ai_pick': 'France Win', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-26T15:00:00-04:00',
  },
  {
    'slug': 'senegal-iraq', 'home': 'Senegal', 'away': 'Iraq',
    'home_code': 'sn', 'away_code': 'iq', 'home_rank': '#19 FIFA', 'away_rank': '#68 FIFA',
    'group': 'I', 'matchday': 3, 'date': 'June 26, 2026', 'time': '3:00 PM ET',
    'venue': 'BMO Field, Toronto, Canada',
    'home_prob': 64, 'draw_prob': 20, 'away_prob': 16,
    'home_ml': '-215', 'draw_ml': '+310', 'away_ml': '+540',
    'ai_pick': 'Senegal Win', 'over_under': '2.5',
    'photo_id': '1569531955323-33c6b2dca44b',
    'json_date': '2026-06-26T15:00:00-04:00',
  },

  # ── GROUP J ────────────────────────────────────────────────────────────
  {
    'slug': 'argentina-algeria', 'home': 'Argentina', 'away': 'Algeria',
    'home_code': 'ar', 'away_code': 'dz', 'home_rank': '#4 FIFA', 'away_rank': '#31 FIFA',
    'group': 'J', 'matchday': 1, 'date': 'June 16, 2026', 'time': '9:00 PM ET',
    'venue': 'Arrowhead Stadium, Kansas City, MO',
    'home_prob': 66, 'draw_prob': 20, 'away_prob': 14,
    'home_ml': '-230', 'draw_ml': '+320', 'away_ml': '+580',
    'ai_pick': 'Argentina Win', 'over_under': '2.5',
    'photo_id': '1599158150601-1417ebbaafdd',
    'json_date': '2026-06-16T21:00:00-04:00',
  },
  {
    'slug': 'austria-jordan', 'home': 'Austria', 'away': 'Jordan',
    'home_code': 'at', 'away_code': 'jo', 'home_rank': '#25 FIFA', 'away_rank': '#87 FIFA',
    'group': 'J', 'matchday': 1, 'date': 'June 17, 2026', 'time': '12:00 AM ET',
    'venue': "Levi's Stadium, Santa Clara, CA",
    'home_prob': 64, 'draw_prob': 20, 'away_prob': 16,
    'home_ml': '-210', 'draw_ml': '+310', 'away_ml': '+530',
    'ai_pick': 'Austria Win', 'over_under': '2.5',
    'photo_id': '1489944440615-453fc2b6a9a9',
    'json_date': '2026-06-17T00:00:00-07:00',
  },
  {
    'slug': 'argentina-austria', 'home': 'Argentina', 'away': 'Austria',
    'home_code': 'ar', 'away_code': 'at', 'home_rank': '#4 FIFA', 'away_rank': '#25 FIFA',
    'group': 'J', 'matchday': 2, 'date': 'June 22, 2026', 'time': '1:00 PM ET',
    'venue': 'AT&T Stadium, Arlington, TX',
    'home_prob': 60, 'draw_prob': 22, 'away_prob': 18,
    'home_ml': '-185', 'draw_ml': '+290', 'away_ml': '+460',
    'ai_pick': 'Argentina Win', 'over_under': '2.5',
    'photo_id': '1651421738652-12124d47c917',
    'json_date': '2026-06-22T13:00:00-04:00',
  },
  {
    'slug': 'jordan-algeria', 'home': 'Jordan', 'away': 'Algeria',
    'home_code': 'jo', 'away_code': 'dz', 'home_rank': '#87 FIFA', 'away_rank': '#31 FIFA',
    'group': 'J', 'matchday': 2, 'date': 'June 22, 2026', 'time': '11:00 PM ET',
    'venue': "Levi's Stadium, Santa Clara, CA",
    'home_prob': 24, 'draw_prob': 28, 'away_prob': 48,
    'home_ml': '+310', 'draw_ml': '+240', 'away_ml': '-110',
    'ai_pick': 'Algeria Win', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-22T23:00:00-07:00',
  },
  {
    'slug': 'jordan-argentina', 'home': 'Jordan', 'away': 'Argentina',
    'home_code': 'jo', 'away_code': 'ar', 'home_rank': '#87 FIFA', 'away_rank': '#4 FIFA',
    'group': 'J', 'matchday': 3, 'date': 'June 27, 2026', 'time': '10:00 PM ET',
    'venue': 'AT&T Stadium, Arlington, TX',
    'home_prob': 10, 'draw_prob': 18, 'away_prob': 72,
    'home_ml': '+700', 'draw_ml': '+380', 'away_ml': '-310',
    'ai_pick': 'Argentina Win', 'over_under': '2.5',
    'photo_id': '1651421738652-12124d47c917',
    'json_date': '2026-06-27T22:00:00-04:00',
  },
  {
    'slug': 'algeria-austria', 'home': 'Algeria', 'away': 'Austria',
    'home_code': 'dz', 'away_code': 'at', 'home_rank': '#31 FIFA', 'away_rank': '#25 FIFA',
    'group': 'J', 'matchday': 3, 'date': 'June 27, 2026', 'time': '10:00 PM ET',
    'venue': 'Arrowhead Stadium, Kansas City, MO',
    'home_prob': 32, 'draw_prob': 28, 'away_prob': 40,
    'home_ml': '+220', 'draw_ml': '+235', 'away_ml': '+135',
    'ai_pick': 'Austria Win or Draw', 'over_under': '2.5',
    'photo_id': '1489944440615-453fc2b6a9a9',
    'json_date': '2026-06-27T22:00:00-04:00',
  },

  # ── GROUP K ────────────────────────────────────────────────────────────
  {
    'slug': 'portugal-drc', 'home': 'Portugal', 'away': 'DR Congo',
    'home_code': 'pt', 'away_code': 'cd', 'home_rank': '#6 FIFA', 'away_rank': '#53 FIFA',
    'group': 'K', 'matchday': 1, 'date': 'June 17, 2026', 'time': '1:00 PM ET',
    'venue': 'NRG Stadium, Houston, TX',
    'home_prob': 68, 'draw_prob': 18, 'away_prob': 14,
    'home_ml': '-245', 'draw_ml': '+340', 'away_ml': '+620',
    'ai_pick': 'Portugal Win', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-17T13:00:00-04:00',
  },
  {
    'slug': 'uzbekistan-colombia', 'home': 'Uzbekistan', 'away': 'Colombia',
    'home_code': 'uz', 'away_code': 'co', 'home_rank': '#72 FIFA', 'away_rank': '#9 FIFA',
    'group': 'K', 'matchday': 1, 'date': 'June 17, 2026', 'time': '10:00 PM ET',
    'venue': 'Estadio Azteca, Mexico City, Mexico',
    'home_prob': 14, 'draw_prob': 22, 'away_prob': 64,
    'home_ml': '+520', 'draw_ml': '+280', 'away_ml': '-215',
    'ai_pick': 'Colombia Win', 'over_under': '2.5',
    'photo_id': '1705593973313-75de7bf95b56',
    'json_date': '2026-06-17T22:00:00-06:00',
  },
  {
    'slug': 'portugal-uzbekistan', 'home': 'Portugal', 'away': 'Uzbekistan',
    'home_code': 'pt', 'away_code': 'uz', 'home_rank': '#6 FIFA', 'away_rank': '#72 FIFA',
    'group': 'K', 'matchday': 2, 'date': 'June 23, 2026', 'time': '1:00 PM ET',
    'venue': 'NRG Stadium, Houston, TX',
    'home_prob': 78, 'draw_prob': 14, 'away_prob': 8,
    'home_ml': '-390', 'draw_ml': '+480', 'away_ml': '+980',
    'ai_pick': 'Portugal Win & Over 2.5', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-23T13:00:00-04:00',
  },
  {
    'slug': 'colombia-drc', 'home': 'Colombia', 'away': 'DR Congo',
    'home_code': 'co', 'away_code': 'cd', 'home_rank': '#9 FIFA', 'away_rank': '#53 FIFA',
    'group': 'K', 'matchday': 2, 'date': 'June 23, 2026', 'time': '10:00 PM ET',
    'venue': 'Estadio Akron, Guadalajara, Mexico',
    'home_prob': 60, 'draw_prob': 22, 'away_prob': 18,
    'home_ml': '-185', 'draw_ml': '+290', 'away_ml': '+460',
    'ai_pick': 'Colombia Win', 'over_under': '2.5',
    'photo_id': '1599158150601-1417ebbaafdd',
    'json_date': '2026-06-23T22:00:00-06:00',
  },
  {
    'slug': 'colombia-portugal', 'home': 'Colombia', 'away': 'Portugal',
    'home_code': 'co', 'away_code': 'pt', 'home_rank': '#9 FIFA', 'away_rank': '#6 FIFA',
    'group': 'K', 'matchday': 3, 'date': 'June 27, 2026', 'time': '7:30 PM ET',
    'venue': 'Hard Rock Stadium, Miami, FL',
    'home_prob': 32, 'draw_prob': 26, 'away_prob': 42,
    'home_ml': '+230', 'draw_ml': '+250', 'away_ml': '+130',
    'ai_pick': 'Portugal Win', 'over_under': '2.5',
    'photo_id': '1599158150601-1417ebbaafdd',
    'json_date': '2026-06-27T19:30:00-04:00',
  },
  {
    'slug': 'drc-uzbekistan', 'home': 'DR Congo', 'away': 'Uzbekistan',
    'home_code': 'cd', 'away_code': 'uz', 'home_rank': '#53 FIFA', 'away_rank': '#72 FIFA',
    'group': 'K', 'matchday': 3, 'date': 'June 27, 2026', 'time': '7:30 PM ET',
    'venue': 'Mercedes-Benz Stadium, Atlanta, GA',
    'home_prob': 46, 'draw_prob': 28, 'away_prob': 26,
    'home_ml': '-115', 'draw_ml': '+250', 'away_ml': '+320',
    'ai_pick': 'DR Congo Win or Draw', 'over_under': '2.5',
    'photo_id': '1706675780107-7c43cc487928',
    'json_date': '2026-06-27T19:30:00-04:00',
  },

  # ── GROUP L ────────────────────────────────────────────────────────────
  {
    'slug': 'england-croatia', 'home': 'England', 'away': 'Croatia',
    'home_code': 'gb-eng', 'away_code': 'hr', 'home_rank': '#5 FIFA', 'away_rank': '#14 FIFA',
    'group': 'L', 'matchday': 1, 'date': 'June 17, 2026', 'time': '4:00 PM ET',
    'venue': 'AT&T Stadium, Arlington, TX',
    'home_prob': 56, 'draw_prob': 24, 'away_prob': 20,
    'home_ml': '-160', 'draw_ml': '+280', 'away_ml': '+430',
    'ai_pick': 'England Win', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-17T16:00:00-04:00',
  },
  {
    'slug': 'ghana-panama', 'home': 'Ghana', 'away': 'Panama',
    'home_code': 'gh', 'away_code': 'pa', 'home_rank': '#60 FIFA', 'away_rank': '#74 FIFA',
    'group': 'L', 'matchday': 1, 'date': 'June 17, 2026', 'time': '7:00 PM ET',
    'venue': 'BMO Field, Toronto, Canada',
    'home_prob': 44, 'draw_prob': 28, 'away_prob': 28,
    'home_ml': '-110', 'draw_ml': '+240', 'away_ml': '+290',
    'ai_pick': 'Ghana Win or Draw', 'over_under': '2.5',
    'photo_id': '1569531955323-33c6b2dca44b',
    'json_date': '2026-06-17T19:00:00-04:00',
  },
  {
    'slug': 'england-ghana', 'home': 'England', 'away': 'Ghana',
    'home_code': 'gb-eng', 'away_code': 'gh', 'home_rank': '#5 FIFA', 'away_rank': '#60 FIFA',
    'group': 'L', 'matchday': 2, 'date': 'June 23, 2026', 'time': '4:00 PM ET',
    'venue': 'Gillette Stadium, Foxborough, MA',
    'home_prob': 66, 'draw_prob': 20, 'away_prob': 14,
    'home_ml': '-225', 'draw_ml': '+310', 'away_ml': '+570',
    'ai_pick': 'England Win', 'over_under': '2.5',
    'photo_id': '1571754472834-677ab0a62ba7',
    'json_date': '2026-06-23T16:00:00-04:00',
  },
  {
    'slug': 'panama-croatia', 'home': 'Panama', 'away': 'Croatia',
    'home_code': 'pa', 'away_code': 'hr', 'home_rank': '#74 FIFA', 'away_rank': '#14 FIFA',
    'group': 'L', 'matchday': 2, 'date': 'June 23, 2026', 'time': '7:00 PM ET',
    'venue': 'BMO Field, Toronto, Canada',
    'home_prob': 16, 'draw_prob': 22, 'away_prob': 62,
    'home_ml': '+500', 'draw_ml': '+290', 'away_ml': '-200',
    'ai_pick': 'Croatia Win', 'over_under': '2.5',
    'photo_id': '1489944440615-453fc2b6a9a9',
    'json_date': '2026-06-23T19:00:00-04:00',
  },
  {
    'slug': 'panama-england', 'home': 'Panama', 'away': 'England',
    'home_code': 'pa', 'away_code': 'gb-eng', 'home_rank': '#74 FIFA', 'away_rank': '#5 FIFA',
    'group': 'L', 'matchday': 3, 'date': 'June 27, 2026', 'time': '5:00 PM ET',
    'venue': 'MetLife Stadium, East Rutherford, NJ',
    'home_prob': 10, 'draw_prob': 18, 'away_prob': 72,
    'home_ml': '+680', 'draw_ml': '+360', 'away_ml': '-295',
    'ai_pick': 'England Win', 'over_under': '2.5',
    'photo_id': '1556816214-6d16c62fbbf6',
    'json_date': '2026-06-27T17:00:00-04:00',
  },
  {
    'slug': 'croatia-ghana', 'home': 'Croatia', 'away': 'Ghana',
    'home_code': 'hr', 'away_code': 'gh', 'home_rank': '#14 FIFA', 'away_rank': '#60 FIFA',
    'group': 'L', 'matchday': 3, 'date': 'June 27, 2026', 'time': '5:00 PM ET',
    'venue': 'Lincoln Financial Field, Philadelphia, PA',
    'home_prob': 54, 'draw_prob': 24, 'away_prob': 22,
    'home_ml': '-145', 'draw_ml': '+270', 'away_ml': '+390',
    'ai_pick': 'Croatia Win', 'over_under': '2.5',
    'photo_id': '1489944440615-453fc2b6a9a9',
    'json_date': '2026-06-27T17:00:00-04:00',
  },
]
```

---

## PHASE 3 — GENERATE ALL 50 PAGES

Write a Python generator using brazil-morocco.html as the template.
For each match, customize:
- Page title, meta description, canonical URL
- JSON-LD SportsEvent (startDate, teams, venue)
- Match header (teams, flags, date, time, venue, group)
- Odds strip (home ML, draw ML, away ML)
- AI prediction (pick text, probability bars)
- Sportsbook comparison card (use same home team ML for all 4 books ±5 pts)
- Player picks (generate 5 plausible players per match — real names from those nations)
- Trending searches (5 real searches people make for that match)
- Up Next card (the other 2 matches in the same group — look up from MATCHES data)
- Stadium Unsplash photo

**Writing style rules apply** — no AI fluff. Every analysis sentence must be specific.
Reference real players, real stats, real tactical contexts. Not "Team A looks strong."

---

## PHASE 4 — UPDATE HUB PAGES

### index.html
- Remove all fixture cards and prediction links pointing to deleted pages
- Add fixture cards for all new matches grouped by date (Jun 12 through Jun 27)
- Add date filter tabs for each new date
- Ensure fixture cards link to correct slugs

### predictions.html
- Remove prediction cards for deleted pages
- Add prediction cards for all 50 new pages
- Add date tabs Jun 16 through Jun 27

### standings.html
Already has Group A–D. Add groups E through L with all 12 teams.
Use correct group compositions from the verified data above.

### sitemap.xml
Update to include all pages. Count and report final URL total.

---

## PHASE 5 — FINAL VERIFICATION

```bash
# Confirm wrong pages are gone
for slug in uruguay-serbia france-albania argentina-peru colombia-ecuador england-senegal portugal-indonesia croatia-australia senegal-slovakia usa-bolivia; do
  [ -f "${slug}.html" ] && echo "❌ STILL EXISTS: ${slug}.html" || echo "✅ DELETED: ${slug}"
done

# Count total match pages
ls *.html | grep -v -E "(index|fantasy|standings|predictions|picks-record|404)" | wc -l
# Expected: 72

# Verify JSON-LD on all match pages
python3 -c "
import re, glob, json
pages = [f for f in glob.glob('*.html') if f not in ('index.html','fantasy.html','standings.html','predictions.html','picks-record.html','404.html')]
bad = []
for p in pages:
    with open(p) as f: c = f.read()
    m = re.search(r'application/ld\+json[^>]*>(.*?)</script>', c, re.DOTALL)
    if not m: bad.append(f'NO JSON-LD: {p}'); continue
    try: json.loads(m.group(1))
    except: bad.append(f'INVALID JSON-LD: {p}')
print('Issues:', bad if bad else 'NONE')
print(f'Checked {len(pages)} pages')
"

# No wrong domains
grep -r "pitchiq\.com" *.html && echo "❌ WRONG DOMAIN" || echo "✅ Domain clean"
```

---

## COMPLETION REPORT FORMAT

```
=== PITCHIQ EMERGENCY FIX — COMPLETE ===
Pages deleted: [N]
Pages built: [N]
Total match pages: [N] (target: 72)
JSON-LD valid: [N/N]
Wrong pages remaining: [list or NONE]
Hub pages updated: index / predictions / standings / sitemap
Sitemap URL count: [N]

DEPLOY:
cd ~/Claude/Projects/PitchIQ
git add -A
git commit -m "Emergency fix: correct schedule, 72 real match pages"
git push origin main
```
