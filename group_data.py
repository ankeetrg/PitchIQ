#!/usr/bin/env python3
"""
PitchIQ — Group stage standings and scenario data
Update after each match day, then run: python3 generate_group_pages.py

Standings fields per team: W, D, L, GF, GA (goals for/against)
Points = W*3 + D*1. GD = GF - GA.

HOW TO UPDATE AFTER EACH MATCH:
  1. Find the team in the correct group dict below
  2. Add 1 to W (win), D (draw), or L (loss)
  3. Add goals scored to GF, goals conceded to GA
  4. Update the relevant fixture dict: set result='X–Y'
  5. Run: python3 generate_group_pages.py
  6. Push to Vercel

CONFIRMED RESULTS (verified from match data — do not change):
  ✓ Mexico 2–0 South Africa (Jun 11, Group A MD1)
  ✓ Korea Republic 2–1 Czechia (Jun 11, Group A MD1)
  ✓ Canada 1–1 Bosnia (Jun 12, Group B MD1)
  ✓ USA 4–1 Paraguay (Jun 12, Group D MD1)

NEEDS UPDATE — these are estimated/placeholder (marked with # ⚠️ UNVERIFIED):
  All MD2 results, and MD1 results for Groups C, E, F, G, H, I, J, K, L
"""

GROUPS = {

# ─────────────────────────────────────────────────────────────────────────────
# GROUP A — MD1 FULLY CONFIRMED ✓
# Mexico 2-0 South Africa | Korea Republic 2-1 Czechia
# MD2 (Jun 18): Mexico vs Korea, Czechia vs South Africa — UPDATE BELOW
# ─────────────────────────────────────────────────────────────────────────────
'A': dict(
    name='Group A',
    teams=[
        dict(name='Mexico',          emoji='🇲🇽', code='mx', slug='mexico',       W=1, D=0, L=0, GF=2, GA=0),   # ✓ MD1 only — update after MD2
        dict(name='Korea Republic',  emoji='🇰🇷', code='kr', slug='korea',        W=1, D=0, L=0, GF=2, GA=1),   # ✓ MD1 only — update after MD2
        dict(name='Czechia',         emoji='🇨🇿', code='cz', slug='czechia',      W=0, D=0, L=1, GF=1, GA=2),   # ✓ MD1 only — update after MD2
        dict(name='South Africa',    emoji='🇿🇦', code='za', slug='southafrica',  W=0, D=0, L=1, GF=0, GA=2),   # ✓ MD1 only — update after MD2
    ],
    fixtures=[
        dict(home='Mexico', away='South Africa', date='Jun 11', result='2–0', slug='mexico-southafrica'),
        dict(home='Korea Republic', away='Czechia', date='Jun 11', result='2–1', slug='korea-czechia'),
        dict(home='Mexico', away='Korea Republic', date='Jun 18', result=None, slug='mexico-korea'),         # ⚠️ UPDATE
        dict(home='Czechia', away='South Africa', date='Jun 18', result=None, slug='czechia-southafrica'),   # ⚠️ UPDATE
        dict(home='Mexico', away='Czechia', date='Jun 25', result=None, slug=None),
        dict(home='South Africa', away='Korea Republic', date='Jun 25', result=None, slug=None),
    ],
    scenarios=[
        "Mexico lead Group A with 3 points after MD1. A win or draw vs Korea (MD2) books their place.",
        "Korea Republic are level with Mexico on goal difference — their MD2 clash is effectively a knockout.",
        "Czechia must beat South Africa in MD2 and hope Mexico drop points to have any path to second.",
        "South Africa need wins in both remaining games and results to go their way — long shot.",
    ],
    analysis="Mexico and Korea are the two quality sides in this group — both won MD1 convincingly. Their head-to-head in MD2 will define the group. Czechia and South Africa are fighting for third-place scenario points.",
),

# ─────────────────────────────────────────────────────────────────────────────
# GROUP B — MD1 PARTIALLY CONFIRMED
# ✓ Canada 1–1 Bosnia | Qatar vs Switzerland — ⚠️ UNVERIFIED
# ─────────────────────────────────────────────────────────────────────────────
'B': dict(
    name='Group B',
    teams=[
        dict(name='Canada',          emoji='🇨🇦', code='ca', slug='canada',       W=0, D=1, L=0, GF=1, GA=1),   # ✓ confirmed
        dict(name='Bosnia',          emoji='🇧🇦', code='ba', slug='bosnia',       W=0, D=1, L=0, GF=1, GA=1),   # ✓ confirmed
        dict(name='Qatar',           emoji='🇶🇦', code='qa', slug='qatar',        W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED — update MD1 result
        dict(name='Switzerland',     emoji='🇨🇭', code='ch', slug='switzerland',  W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED — update MD1 result
    ],
    fixtures=[
        dict(home='Canada', away='Bosnia', date='Jun 12', result='1–1', slug='canada-bosnia'),
        dict(home='Qatar', away='Switzerland', date='Jun 12', result=None, slug='qatar-switzerland'),        # ⚠️ UPDATE with actual score
        dict(home='Canada', away='Qatar', date='Jun 19', result=None, slug='canada-qatar'),
        dict(home='Switzerland', away='Bosnia', date='Jun 19', result=None, slug='switzerland-bosnia'),
        dict(home='Canada', away='Switzerland', date='Jun 26', result=None, slug='switzerland-canada'),
        dict(home='Bosnia', away='Qatar', date='Jun 26', result=None, slug='bosnia-qatar'),
    ],
    scenarios=[
        "Canada and Bosnia drew MD1 — both need wins in MD2 to stay on track for qualification.",
        "Qatar vs Switzerland result determines the group dynamic — update once confirmed.",
        "MD2 (Canada vs Qatar, Switzerland vs Bosnia) will clarify the top-two picture significantly.",
        "All four teams are realistically still in contention until Qatar/Switzerland MD1 result is known.",
    ],
    analysis="Canada drew their opener against Bosnia having led — that's the defining story of MD1. Qatar and Switzerland played the same day; update that result to complete the picture.",
),

# ─────────────────────────────────────────────────────────────────────────────
# GROUP C — ⚠️ MD1 UNVERIFIED
# Brazil vs Morocco | Haiti vs Scotland — update with actual scores
# ─────────────────────────────────────────────────────────────────────────────
'C': dict(
    name='Group C',
    teams=[
        dict(name='Brazil',          emoji='🇧🇷', code='br', slug='brazil',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Morocco',         emoji='🇲🇦', code='ma', slug='morocco',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Scotland',        emoji='🏴󠁧󠁢󠁳󠁣󠁴󠁿', code='gb-sct', slug='scotland',  W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Haiti',           emoji='🇭🇹', code='ht', slug='haiti',        W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Brazil', away='Morocco', date='Jun 13', result=None, slug='brazil-morocco'),              # ⚠️ UPDATE
        dict(home='Haiti', away='Scotland', date='Jun 13', result=None, slug='haiti-scotland'),              # ⚠️ UPDATE
        dict(home='Brazil', away='Scotland', date='Jun 20', result=None, slug='scotland-brazil'),
        dict(home='Morocco', away='Haiti', date='Jun 20', result=None, slug='morocco-haiti'),
        dict(home='Brazil', away='Haiti', date='Jun 27', result=None, slug='brazil-haiti'),
        dict(home='Morocco', away='Scotland', date='Jun 27', result=None, slug='scotland-morocco'),
    ],
    scenarios=[
        "Brazil are heavy favorites to top Group C — Vinicius Jr. is the most dangerous player in the group.",
        "Morocco's defensive record is exceptional. They could challenge Brazil for first if they win MD1.",
        "Scotland and Haiti are outmatched at this level but could cause an upset on any given day.",
        "The Brazil vs Morocco dynamic will define the group — watch goal difference carefully.",
    ],
    analysis="Group C is the toughest on paper after Group D. Brazil and Morocco are both serious teams. Update MD1 scores to see the real picture. Scotland and Haiti are the clear underdogs.",
),

# ─────────────────────────────────────────────────────────────────────────────
# GROUP D — MD1 PARTIALLY CONFIRMED
# ✓ USA 4–1 Paraguay | Australia vs Turkey — ⚠️ UNVERIFIED
# ─────────────────────────────────────────────────────────────────────────────
'D': dict(
    name='Group D',
    teams=[
        dict(name='USA',             emoji='🇺🇸', code='us', slug='usa',          W=1, D=0, L=0, GF=4, GA=1),   # ✓ confirmed
        dict(name='Paraguay',        emoji='🇵🇾', code='py', slug='paraguay',     W=0, D=0, L=1, GF=1, GA=4),   # ✓ confirmed
        dict(name='Turkey',          emoji='🇹🇷', code='tr', slug='turkey',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED — update MD1 result
        dict(name='Australia',       emoji='🇦🇺', code='au', slug='australia',    W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED — update MD1 result
    ],
    fixtures=[
        dict(home='USA', away='Paraguay', date='Jun 12', result='4–1', slug='usa-paraguay'),
        dict(home='Australia', away='Turkey', date='Jun 12', result=None, slug='australia-turkey'),          # ⚠️ UPDATE with actual score
        dict(home='USA', away='Australia', date='Jun 19', result=None, slug='usa-australia'),
        dict(home='Turkey', away='Paraguay', date='Jun 19', result=None, slug='turkey-paraguay'),
        dict(home='USA', away='Turkey', date='Jun 26', result=None, slug='turkey-usa'),
        dict(home='Paraguay', away='Australia', date='Jun 26', result=None, slug='paraguay-australia'),
    ],
    scenarios=[
        "USA crushed Paraguay 4–1 in the opener — they're the clear group favorites on home soil.",
        "Turkey vs Australia result determines who challenges USA for second — update once confirmed.",
        "Paraguay face an early crisis — conceding 4 goals in MD1. They need an immediate response.",
        "USA vs Turkey in MD3 could be the biggest home crowd moment of the group stage.",
    ],
    analysis="USA made a massive statement with a 4–1 win. The group is theirs to lose. Turkey and Australia's MD1 result completes the picture — one of those two will likely take second.",
),

# ─────────────────────────────────────────────────────────────────────────────
# GROUPS E–L: ⚠️ ALL STANDINGS UNVERIFIED — update with real MD1/MD2 results
# ─────────────────────────────────────────────────────────────────────────────

'E': dict(
    name='Group E',
    teams=[
        dict(name='Germany',         emoji='🇩🇪', code='de', slug='germany',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Ivory Coast',     emoji='🇨🇮', code='ci', slug='ivorycoast',   W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Ecuador',         emoji='🇪🇨', code='ec', slug='ecuador',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Curacao',         emoji='🇨🇼', code='cw', slug='curacao',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Germany', away='Curacao', date='Jun 14', result=None, slug='germany-curacao'),            # ⚠️ UPDATE
        dict(home='Ivory Coast', away='Ecuador', date='Jun 14', result=None, slug='cotedivoire-ecuador'),    # ⚠️ UPDATE
        dict(home='Germany', away='Ivory Coast', date='Jun 21', result=None, slug='germany-cotedivoire'),
        dict(home='Ecuador', away='Curacao', date='Jun 21', result=None, slug='ecuador-curacao'),
        dict(home='Germany', away='Ecuador', date='Jun 28', result=None, slug='ecuador-germany'),
        dict(home='Curacao', away='Ivory Coast', date='Jun 28', result=None, slug='curacao-cotedivoire'),
    ],
    scenarios=[
        "Germany are overwhelming favorites to top Group E — they're the highest-ranked team in the group.",
        "Ivory Coast (AFCON 2024 champions) are the realistic contenders for second place.",
        "Ecuador and Curacao are fighting for any advancement path — both need wins immediately.",
        "Germany vs Ivory Coast in MD2 is the defining match in this group.",
    ],
    analysis="Update MD1 results to see the Group E picture. Germany are expected to dominate — Ivory Coast are the credible second team. Add actual scores from germany-curacao and cotedivoire-ecuador.",
),

'F': dict(
    name='Group F',
    teams=[
        dict(name='Netherlands',     emoji='🇳🇱', code='nl', slug='netherlands',  W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Sweden',          emoji='🇸🇪', code='se', slug='sweden',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Japan',           emoji='🇯🇵', code='jp', slug='japan',        W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Tunisia',         emoji='🇹🇳', code='tn', slug='tunisia',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Netherlands', away='Japan', date='Jun 14', result=None, slug='netherlands-japan'),        # ⚠️ UPDATE
        dict(home='Sweden', away='Tunisia', date='Jun 14', result=None, slug='sweden-tunisia'),              # ⚠️ UPDATE
        dict(home='Netherlands', away='Sweden', date='Jun 21', result=None, slug='netherlands-sweden'),
        dict(home='Japan', away='Tunisia', date='Jun 21', result=None, slug='tunisia-japan'),
        dict(home='Netherlands', away='Tunisia', date='Jun 28', result=None, slug='tunisia-netherlands'),
        dict(home='Sweden', away='Japan', date='Jun 28', result=None, slug='japan-sweden'),
    ],
    scenarios=[
        "Netherlands and Sweden are the expected top-two — their MD2 clash will determine the seeding.",
        "Japan are giant-killers — never count them out after their 2022 results vs Germany and Spain.",
        "Tunisia need early points to stay relevant. MD1 vs Sweden is must-not-lose.",
        "Netherlands vs Sweden in MD2 is one of the group stage's marquee matchups.",
    ],
    analysis="Update MD1 scores (netherlands-japan, sweden-tunisia) to complete the picture. Netherlands are favorites; Sweden are the main challengers. Japan could cause upsets.",
),

'G': dict(
    name='Group G',
    teams=[
        dict(name='Belgium',         emoji='🇧🇪', code='be', slug='belgium',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Iran',            emoji='🇮🇷', code='ir', slug='iran',         W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Egypt',           emoji='🇪🇬', code='eg', slug='egypt',        W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='New Zealand',     emoji='🇳🇿', code='nz', slug='newzealand',   W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Belgium', away='Egypt', date='Jun 15', result=None, slug='belgium-egypt'),                # ⚠️ UPDATE
        dict(home='Iran', away='New Zealand', date='Jun 15', result=None, slug='iran-newzealand'),           # ⚠️ UPDATE
        dict(home='Belgium', away='Iran', date='Jun 22', result=None, slug='belgium-iran'),
        dict(home='New Zealand', away='Egypt', date='Jun 22', result=None, slug='newzealand-egypt'),
        dict(home='Belgium', away='New Zealand', date='Jun 29', result=None, slug='belgium-newzealand'),
        dict(home='Egypt', away='Iran', date='Jun 29', result=None, slug='egypt-iran'),
    ],
    scenarios=[
        "Belgium are the group favorites — De Bruyne at the peak of his powers.",
        "Iran have punched above their weight in qualifying. They're a credible second-place side.",
        "Egypt's threat depends heavily on Salah's form and fitness — watch his status.",
        "New Zealand are the weakest team in Group G but will fight hard for every point.",
    ],
    analysis="Update belgium-egypt and iran-newzealand MD1 results. Belgium and Iran are the likely top two. Egypt with Salah is a wildcard. Belgium vs Iran in MD2 is the group's defining match.",
),

'H': dict(
    name='Group H',
    teams=[
        dict(name='Spain',           emoji='🇪🇸', code='es', slug='spain',        W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Saudi Arabia',    emoji='🇸🇦', code='sa', slug='saudiarabia',  W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Uruguay',         emoji='🇺🇾', code='uy', slug='uruguay',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Cape Verde',      emoji='🇨🇻', code='cv', slug='capeverde',    W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Spain', away='Cape Verde', date='Jun 15', result=None, slug='spain-capeverde'),           # ⚠️ UPDATE
        dict(home='Saudi Arabia', away='Uruguay', date='Jun 15', result=None, slug='saudiarabia-uruguay'),   # ⚠️ UPDATE
        dict(home='Spain', away='Saudi Arabia', date='Jun 22', result=None, slug='spain-saudiarabia'),
        dict(home='Uruguay', away='Cape Verde', date='Jun 22', result=None, slug='uruguay-capeverde'),
        dict(home='Spain', away='Uruguay', date='Jun 29', result=None, slug='uruguay-spain'),
        dict(home='Cape Verde', away='Saudi Arabia', date='Jun 29', result=None, slug='capeverde-saudiarabia'),
    ],
    scenarios=[
        "Spain are the clear Group H favorites — their tiki-taka system is world-class.",
        "Saudi Arabia caused a huge upset vs Argentina in 2022 — Uruguay will be wary.",
        "Uruguay have the quality to challenge for second but need to avoid an early slip.",
        "Cape Verde are making their World Cup debut — every point is historic for them.",
    ],
    analysis="Update spain-capeverde and saudiarabia-uruguay MD1 scores. Spain are expected to top this group. Saudi Arabia vs Uruguay is the key second-place battle. Cape Verde are the tournament's Cinderella side.",
),

'I': dict(
    name='Group I',
    teams=[
        dict(name='France',          emoji='🇫🇷', code='fr', slug='france',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Norway',          emoji='🇳🇴', code='no', slug='norway',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Senegal',         emoji='🇸🇳', code='sn', slug='senegal',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Iraq',            emoji='🇮🇶', code='iq', slug='iraq',         W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='France', away='Senegal', date='Jun 16', result=None, slug='france-senegal'),              # ⚠️ UPDATE
        dict(home='Iraq', away='Norway', date='Jun 16', result=None, slug='iraq-norway'),                    # ⚠️ UPDATE
        dict(home='France', away='Iraq', date='Jun 23', result=None, slug='france-iraq'),
        dict(home='Norway', away='Senegal', date='Jun 23', result=None, slug='norway-senegal'),
        dict(home='France', away='Norway', date='Jun 30', result=None, slug='norway-france'),
        dict(home='Senegal', away='Iraq', date='Jun 30', result=None, slug='senegal-iraq'),
    ],
    scenarios=[
        "France are tournament-level favorites — Mbappé, Griezmann, Camavinga in peak form.",
        "Norway with Haaland are the only team in Group I capable of beating France.",
        "Senegal (AFCON champions) are better than their seeding suggests — Mané is world-class.",
        "Iraq are the lowest-ranked side in this group — every point they take is historic.",
    ],
    analysis="Update france-senegal and iraq-norway MD1 results. France are overwhelming favorites to top Group I. Norway vs France in MD3 could be a blockbuster if both are through.",
),

'J': dict(
    name='Group J',
    teams=[
        dict(name='Argentina',       emoji='🇦🇷', code='ar', slug='argentina',    W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Austria',         emoji='🇦🇹', code='at', slug='austria',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Algeria',         emoji='🇩🇿', code='dz', slug='algeria',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Jordan',          emoji='🇯🇴', code='jo', slug='jordan',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Argentina', away='Algeria', date='Jun 16', result=None, slug='argentina-algeria'),        # ⚠️ UPDATE
        dict(home='Austria', away='Jordan', date='Jun 16', result=None, slug='austria-jordan'),              # ⚠️ UPDATE
        dict(home='Argentina', away='Austria', date='Jun 23', result=None, slug='argentina-austria'),
        dict(home='Algeria', away='Jordan', date='Jun 23', result=None, slug='jordan-algeria'),
        dict(home='Argentina', away='Jordan', date='Jun 30', result=None, slug='jordan-argentina'),
        dict(home='Algeria', away='Austria', date='Jun 30', result=None, slug='algeria-austria'),
    ],
    scenarios=[
        "Argentina are the reigning world champions and strong favorites to top Group J.",
        "Austria are organised and dangerous — a surprise package capable of second place.",
        "Algeria have quality in Mahrez — they could beat anyone on a good day.",
        "Jordan are the significant underdogs here. Any points would be historic.",
    ],
    analysis="Update argentina-algeria and austria-jordan MD1 results. Argentina are defending champions and huge favorites. Argentina vs Austria in MD2 will decide the group.",
),

'K': dict(
    name='Group K',
    teams=[
        dict(name='Portugal',        emoji='🇵🇹', code='pt', slug='portugal',     W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Colombia',        emoji='🇨🇴', code='co', slug='colombia',     W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='DR Congo',        emoji='🇨🇩', code='cd', slug='drc',          W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Uzbekistan',      emoji='🇺🇿', code='uz', slug='uzbekistan',   W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='Portugal', away='DR Congo', date='Jun 17', result=None, slug='portugal-congodr'),         # ⚠️ UPDATE
        dict(home='Uzbekistan', away='Colombia', date='Jun 17', result=None, slug='uzbekistan-colombia'),    # ⚠️ UPDATE
        dict(home='Portugal', away='Colombia', date='Jun 24', result=None, slug='colombia-portugal'),
        dict(home='DR Congo', away='Uzbekistan', date='Jun 24', result=None, slug='drc-uzbekistan'),
        dict(home='Portugal', away='Uzbekistan', date='Jul 1', result=None, slug='portugal-uzbekistan'),
        dict(home='DR Congo', away='Colombia', date='Jul 1', result=None, slug='colombia-drc'),
    ],
    scenarios=[
        "Portugal are the group favorites with Ronaldo hunting tournament records.",
        "Colombia are the main challengers — their MD2 head-to-head vs Portugal is the key match.",
        "DR Congo are Africa's representative and will be competitive against all sides.",
        "Uzbekistan are making their debut — every clean sheet is a milestone.",
    ],
    analysis="Update portugal-congodr and uzbekistan-colombia MD1 results. Portugal vs Colombia in MD2 is the group-defining match. Both are expected to advance.",
),

'L': dict(
    name='Group L',
    teams=[
        dict(name='England',         emoji='🏴󠁧󠁢󠁥󠁮󠁧󠁿', code='gb-eng', slug='england',    W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Croatia',         emoji='🇭🇷', code='hr', slug='croatia',      W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Panama',          emoji='🇵🇦', code='pa', slug='panama',       W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
        dict(name='Ghana',           emoji='🇬🇭', code='gh', slug='ghana',        W=0, D=0, L=0, GF=0, GA=0),   # ⚠️ UNVERIFIED
    ],
    fixtures=[
        dict(home='England', away='Croatia', date='Jun 17', result=None, slug='england-croatia'),            # ⚠️ UPDATE
        dict(home='Ghana', away='Panama', date='Jun 17', result=None, slug='ghana-panama'),                  # ⚠️ UPDATE
        dict(home='England', away='Panama', date='Jun 24', result=None, slug='panama-england'),
        dict(home='Croatia', away='Ghana', date='Jun 24', result=None, slug='croatia-ghana'),
        dict(home='England', away='Ghana', date='Jul 1', result=None, slug='england-ghana'),
        dict(home='Croatia', away='Panama', date='Jul 1', result=None, slug='panama-croatia'),
    ],
    scenarios=[
        "England are the group favorites — Bellingham, Saka, Foden in the same XI is a serious threat.",
        "Croatia are tournament veterans with Modric still pulling strings. Never underestimate them.",
        "Panama are physical and well-drilled — they caused upsets in CONCACAF qualifying.",
        "Ghana have Premier League talent throughout — they'll compete with anyone in this group.",
    ],
    analysis="Update england-croatia and ghana-panama MD1 results. England vs Croatia is the group's marquee opener. Both are expected to advance but neither will take the other lightly.",
),

}
