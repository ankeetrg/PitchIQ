#!/usr/bin/env python3
"""
PitchIQ — knockout match page generator (Round of 32 → Final).

Reads live.json for current teams and knockout.json for match metadata.
Generates an HTML preview page for every knockout slot that has real teams.
Writes the page_slug back into live.json so predictions.html can link to it.

Run:
    python3 generate_knockout_pages.py          # generate all new/changed pages
    python3 generate_knockout_pages.py --dry    # print slugs, don't write files

Safe: if a page already exists and teams haven't changed, it is skipped.
"""

import json, os, re, sys, pathlib

from generate_pages import (
    TEMPLATE,
    replace_between,
    ai_section, analysis_section, stats_section, picks_section,
    schema_json_ld,
)

PROJ          = pathlib.Path(__file__).parent
KNOCKOUT_JSON = PROJ / 'data' / 'knockout.json'
LIVE_JSON     = PROJ / 'data' / 'live.json'
DRY           = '--dry' in sys.argv

PHOTOS = [
    '1556816214-6d16c62fbbf6', '1489944440615-453fc2b6a9a9',
    '1569531955323-33c6b2dca44b', '1599158150601-1417ebbaafdd',
    '1706675780107-7c43cc487928', '1705593973313-75de7bf95b56',
    '1651421738652-12124d47c917', '1430232324554-8f4aebd06683',
    '1571754472834-677ab0a62ba7', '1518091043644-c1d4457512c6',
]


# ── Team data ─────────────────────────────────────────────────────────────────

_TEAM_DATA = {
    'South Africa': {
        'code': 'za', 'rank': '#64', 'odds': '+18000',
        'h3': 'Host Nation Momentum',
        'p1': 'South Africa return to the World Cup on home soil, riding a wave of national passion and the tournament experience of Percy Tau, who leads the line with Premier League quality.',
        'p2': 'Goalkeeper Ronwen Williams has been outstanding in qualifying, while their compact low-block structure makes them a difficult team to break down at their home venues.',
        'stats': [('3', 'WC Appearances'), ('7', 'Goals in Group Stage'), ('62', 'FIFA Ranking')],
        'xg': 1.2, 'xga': 1.6, 'shots': 9.4, 'poss': 44,
        'players': [('🇿🇦', 'P. Tau', 'Forward · Brighton', '11.8', '28%', False),
                    ('🇿🇦', 'S. Mofokeng', 'Midfielder · Orlando Pirates', '9.2', '14%', True),
                    ('🇿🇦', 'R. Williams', 'Goalkeeper · Mamelodi Sundowns', '7.4', '22%', False)],
    },
    'Canada': {
        'code': 'ca', 'rank': '#38', 'odds': '+4500',
        'h3': 'Golden Generation Arrives',
        'p1': "Canada's golden generation, led by Alphonso Davies and Jonathan David, makes its World Cup statement after decades of absence from the tournament.",
        'p2': "Jonathan David's Ligue 1 form makes him one of the competition's most dangerous forwards. Davies' pace and crossing from left-back provides relentless attacking width.",
        'stats': [('1st', 'WC since 1986'), ('28', 'Goals in Qualifying'), ('6', 'Clean Sheets')],
        'xg': 1.8, 'xga': 1.1, 'shots': 13.2, 'poss': 54,
        'players': [('🇨🇦', 'J. David', 'Forward · Lille', '14.5', '41%', False),
                    ('🇨🇦', 'A. Davies', 'Left Back · Bayern Munich', '12.8', '55%', False),
                    ('🇨🇦', 'T. Buchanan', 'Midfielder · Inter Milan', '9.4', '24%', False)],
    },
    'Brazil': {
        'code': 'br', 'rank': '#4', 'odds': '+800',
        'h3': 'Five-Time Champions Favourites',
        'p1': 'Brazil arrive as one of the outright favourites, combining flair with tactical discipline. Vinicius Jr. and Rodrygo provide devastating pace in behind any defence.',
        'p2': "Marquinhos and Éder Militão form one of the world's best central defensive partnerships, giving Brazil the defensive platform to go deep in the tournament.",
        'stats': [('5', 'World Cup Titles'), ('237', 'All-Time WC Goals'), ('+14', 'Qualifying Goal Diff')],
        'xg': 2.1, 'xga': 0.8, 'shots': 15.6, 'poss': 62,
        'players': [('🇧🇷', 'Vinicius Jr.', 'Forward · Real Madrid', '16.2', '68%', False),
                    ('🇧🇷', 'Rodrygo', 'Forward · Real Madrid', '13.8', '42%', False),
                    ('🇧🇷', 'Marquinhos', 'Defender · PSG', '8.4', '31%', False)],
    },
    'Japan': {
        'code': 'jp', 'rank': '#17', 'odds': '+4000',
        'h3': 'Asian Giants Eye Quarterfinals',
        'p1': 'Japan have become genuine World Cup contenders, advancing from the group stage in consecutive tournaments and shocking powerhouses along the way.',
        'p2': "Wataru Endo commands the midfield with Liverpool pedigree, while the squad's European-based contingent brings top-flight quality across all positions.",
        'stats': [('3', 'R16 Exits'), ('6', 'WC Appearances'), ('+9', 'Qualifying Goal Diff')],
        'xg': 1.4, 'xga': 1.2, 'shots': 11.8, 'poss': 52,
        'players': [('🇯🇵', 'W. Endo', 'Midfielder · Liverpool', '11.2', '38%', False),
                    ('🇯🇵', 'A. Ueda', 'Forward · Feyenoord', '12.4', '29%', False),
                    ('🇯🇵', 'H. Itakura', 'Defender · B. Mönchengladbach', '7.6', '18%', False)],
    },
    'Germany': {
        'code': 'de', 'rank': '#12', 'odds': '+1400',
        'h3': 'Rebuilding Giants',
        'p1': 'Germany have rebuilt under their new setup with Florian Wirtz emerging as the creative heartbeat. They arrive hungry after recent major tournament underperformance.',
        'p2': "Kai Havertz leads the line with Champions League quality and Antonio Rüdiger's physicality anchors a defence that conceded just twice in qualifying.",
        'stats': [('4', 'World Cup Titles'), ('82', 'FIFA Ranking Points'), ('-2', 'Goals vs Japan 2022')],
        'xg': 1.9, 'xga': 0.9, 'shots': 14.4, 'poss': 60,
        'players': [('🇩🇪', 'F. Wirtz', 'Midfielder · Bayer Leverkusen', '14.8', '52%', False),
                    ('🇩🇪', 'K. Havertz', 'Forward · Arsenal', '13.2', '44%', False),
                    ('🇩🇪', 'A. Rüdiger', 'Defender · Real Madrid', '8.2', '28%', False)],
    },
    'Paraguay': {
        'code': 'py', 'rank': '#52', 'odds': '+15000',
        'h3': 'South American Underdogs',
        'p1': 'Paraguay qualified from a brutally competitive CONMEBOL campaign and arrive as determined underdogs. Their compact defensive block can frustrate any opposition.',
        'p2': "Miguel Almirón provides the creative spark from midfield, and while Paraguay lack the star power of bigger nations, their collective spirit is formidable.",
        'stats': [('9', 'WC Appearances'), ('14', 'Goals in Qualifying'), ('5', 'Goals Conceded')],
        'xg': 1.3, 'xga': 1.4, 'shots': 10.6, 'poss': 46,
        'players': [('🇵🇾', 'M. Almirón', 'Midfielder · Newcastle', '11.6', '35%', False),
                    ('🇵🇾', 'R. Sanabria', 'Forward · Torino', '10.4', '26%', True),
                    ('🇵🇾', 'J. Alonso', 'Defender · Club Olimpia', '6.8', '12%', False)],
    },
    'Netherlands': {
        'code': 'nl', 'rank': '#7', 'odds': '+1200',
        'h3': 'Total Football Tradition',
        'p1': "Virgil van Dijk commands one of the tournament's most commanding defences, while Cody Gakpo and Donyell Malen provide explosive width and directness.",
        'p2': "Frenkie de Jong's recovery from injury makes the Netherlands a far more dangerous proposition — when he controls the tempo, this team operates at a different level.",
        'stats': [('Final', 'WC Best (2010)'), ('13', 'Goals in Qualifying'), ('#7', 'FIFA World Ranking')],
        'xg': 1.7, 'xga': 1.0, 'shots': 13.8, 'poss': 56,
        'players': [('🇳🇱', 'C. Gakpo', 'Forward · Liverpool', '13.8', '46%', False),
                    ('🇳🇱', 'V. van Dijk', 'Defender · Liverpool', '9.2', '52%', False),
                    ('🇳🇱', 'F. de Jong', 'Midfielder · Barcelona', '11.4', '41%', False)],
    },
    'Morocco': {
        'code': 'ma', 'rank': '#14', 'odds': '+2800',
        'h3': 'African Champions Aim Higher',
        'p1': 'Morocco reached the semi-finals in 2022 and return stronger. Achraf Hakimi is arguably the best right-back in the world at this tournament, combining defence with explosive attack.',
        'p2': "Yassine Bounou is among the elite goalkeepers here and has the big-game temperament needed in the knockouts. Morocco's deep defensive shape is one of the hardest to break down.",
        'stats': [('4th', 'WC Finish (2022)'), ('3', 'Clean Sheets (2022)'), ('#14', 'FIFA World Ranking')],
        'xg': 1.4, 'xga': 0.9, 'shots': 12.2, 'poss': 50,
        'players': [('🇲🇦', 'A. Hakimi', 'Right Back · PSG', '13.6', '48%', False),
                    ('🇲🇦', 'H. Ziyech', 'Midfielder · Chelsea', '12.2', '38%', True),
                    ('🇲🇦', 'Y. En-Nesyri', 'Forward · Fenerbahce', '11.8', '32%', False)],
    },
    "Ivory Coast": {
        'code': 'ci', 'rank': '#29', 'odds': '+6000',
        'h3': 'African Champions',
        'p1': "The Ivory Coast, fresh from winning the 2023 Africa Cup of Nations, bring a talented blend of Premier League quality and African flair to the knockout stage.",
        'p2': "Sébastien Haller's return from his cancer battle has redefined their attacking threat, while Franck Kessié's physicality and control in midfield is invaluable.",
        'stats': [('AFCON', '2023 Champions'), ('11', 'Goals in Qualifying'), ('#29', 'FIFA World Ranking')],
        'xg': 1.5, 'xga': 1.1, 'shots': 12.8, 'poss': 51,
        'players': [('🇨🇮', 'S. Haller', 'Forward · Borussia Dortmund', '13.4', '44%', False),
                    ('🇨🇮', 'F. Kessié', 'Midfielder · Barcelona', '10.8', '36%', False),
                    ('🇨🇮', 'S. Fofana', 'Midfielder · Chelsea', '9.6', '28%', False)],
    },
    'Norway': {
        'code': 'no', 'rank': '#30', 'odds': '+5000',
        'h3': 'Haaland Leads the Charge',
        'p1': "Norway qualified largely on Erling Haaland's extraordinary goalscoring, which reaches new heights at every level. This is his first World Cup and he arrives as the tournament's most feared striker.",
        'p2': "Martin Ødegaard provides the creativity and captaincy to unlock deep defences, while the supporting cast has improved significantly since Norway's last World Cup absence.",
        'stats': [('34', 'Goals in Qualifying'), ('#30', 'FIFA World Ranking'), ('1st', 'WC since 1998')],
        'xg': 2.0, 'xga': 1.2, 'shots': 14.6, 'poss': 54,
        'players': [('🇳🇴', 'E. Haaland', 'Forward · Man City', '18.6', '72%', False),
                    ('🇳🇴', 'M. Ødegaard', 'Midfielder · Arsenal', '14.2', '55%', False),
                    ('🇳🇴', 'A. Sørloth', 'Forward · Atletico Madrid', '10.4', '28%', False)],
    },
    'France': {
        'code': 'fr', 'rank': '#2', 'odds': '+700',
        'h3': 'World Champions Favourites',
        'p1': "France arrive as perennial favourites with staggering depth. Kylian Mbappé is the most dangerous player at this tournament — pace, power, and ice-cold finishing make him near-unstoppable.",
        'p2': "Antoine Griezmann's intelligence as a link player between midfield and attack, combined with N'Golo Kanté's engine, gives France balance that few teams can match.",
        'stats': [('2', 'World Cup Titles'), ('+14', 'Qualifying Goal Diff'), ('#2', 'FIFA World Ranking')],
        'xg': 2.2, 'xga': 0.7, 'shots': 16.4, 'poss': 62,
        'players': [('🇫🇷', 'K. Mbappé', 'Forward · Real Madrid', '18.4', '74%', False),
                    ('🇫🇷', 'A. Griezmann', 'Forward · Atletico Madrid', '14.6', '56%', False),
                    ('🇫🇷', 'A. Tchouaméni', 'Midfielder · Real Madrid', '10.2', '34%', False)],
    },
    'Sweden': {
        'code': 'se', 'rank': '#24', 'odds': '+7500',
        'h3': "Post-Zlatan Era",
        'p1': "Sweden have rebuilt around Alexander Isak's clinical finishing and Viktor Nilsson Lindelöf's leadership at the back. They're more dangerous than the odds suggest.",
        'p2': "Dejan Kulusevski's energy and work-rate in the middle third makes Sweden competitive against any opponent, and their organisation and discipline will test France's patience.",
        'stats': [('4th', 'WC Best (1994)'), ('19', 'Goals in Qualifying'), ('#24', 'FIFA World Ranking')],
        'xg': 1.4, 'xga': 1.1, 'shots': 11.4, 'poss': 49,
        'players': [('🇸🇪', 'A. Isak', 'Forward · Newcastle', '14.2', '46%', False),
                    ('🇸🇪', 'D. Kulusevski', 'Midfielder · Tottenham', '12.6', '38%', False),
                    ('🇸🇪', 'V. N. Lindelöf', 'Defender · Man United', '8.4', '28%', False)],
    },
    'Mexico': {
        'code': 'mx', 'rank': '#11', 'odds': '+3000',
        'h3': 'Co-Host Rides Home Support',
        'p1': "Mexico enter as co-hosts desperate to finally advance past the Round of 16 for the first time since 1986. The Azteca atmosphere will be extraordinary.",
        'p2': "Hirving Lozano leads the attack with European experience while Edson Álvarez provides the midfield steel. Mexico's combination of pace and home advantage makes them dangerous.",
        'stats': [('7', 'Consecutive R16 Exits'), ('28', 'Goals in Qualifying'), ('#11', 'FIFA World Ranking')],
        'xg': 1.7, 'xga': 1.0, 'shots': 13.4, 'poss': 55,
        'players': [('🇲🇽', 'H. Lozano', 'Forward · PSV', '13.4', '44%', False),
                    ('🇲🇽', 'E. Álvarez', 'Midfielder · West Ham', '11.6', '38%', False),
                    ('🇲🇽', 'R. Jiménez', 'Forward · Fulham', '12.2', '40%', False)],
    },
    'Ecuador': {
        'code': 'ec', 'rank': '#46', 'odds': '+12000',
        'h3': 'South American Surprise Package',
        'p1': "Ecuador punch above their weight through collective industry and the emergence of Moisés Caicedo as one of the best midfielders in the Premier League.",
        'p2': "Enner Valencia brings veteran experience and reliability in front of goal, while their disciplined defensive shape makes them more than just an also-ran at this tournament.",
        'stats': [('4', 'WC Appearances'), ('21', 'Goals in Qualifying'), ('#46', 'FIFA World Ranking')],
        'xg': 1.3, 'xga': 1.3, 'shots': 10.8, 'poss': 47,
        'players': [('🇪🇨', 'M. Caicedo', 'Midfielder · Chelsea', '13.2', '42%', False),
                    ('🇪🇨', 'E. Valencia', 'Forward · Club America', '11.4', '30%', True),
                    ('🇪🇨', 'P. Ibarra', 'Forward · Monterrey', '9.8', '22%', False)],
    },
    'England': {
        'code': 'gb-eng', 'rank': '#5', 'odds': '+1100',
        'h3': '60 Years of Hurt Ends?',
        'p1': "England carry expectation again but have genuine star power to win this. Jude Bellingham's Champions League form signals a player at the highest level — he can change any game.",
        'p2': "Harry Kane has overcome his reputation for big-game misses to become one of the world's deadliest finishers. With Saka, Foden and Rice alongside him, England have the squad depth to go the distance.",
        'stats': [('1', 'WC Title (1966)'), ('+18', 'Qualifying Goal Diff'), ('#5', 'FIFA World Ranking')],
        'xg': 2.1, 'xga': 0.8, 'shots': 15.2, 'poss': 60,
        'players': [('🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'J. Bellingham', 'Midfielder · Real Madrid', '17.8', '66%', False),
                    ('🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'H. Kane', 'Forward · Bayern Munich', '16.4', '62%', False),
                    ('🏴󠁧󠁢󠁥󠁮󠁧󠁿', 'B. Saka', 'Forward · Arsenal', '14.2', '48%', False)],
    },
    'Congo DR': {
        'code': 'cd', 'rank': '#61', 'odds': '+20000',
        'h3': 'African Qualifier Debutants',
        'p1': "Congo DR make a rare World Cup appearance and arrive as massive underdogs. Chancel Mbemba brings Champions League experience to the backline and will be crucial to any upset.",
        'p2': "Silas Mvumpa provides pace and directness on the wing that will test England's full-backs. Congo DR's task is enormous but they qualified for a reason.",
        'stats': [('2', 'WC Appearances'), ('9', 'Goals in Qualifying'), ('#61', 'FIFA World Ranking')],
        'xg': 1.0, 'xga': 1.5, 'shots': 8.6, 'poss': 42,
        'players': [('🇨🇩', 'C. Mbemba', 'Defender · Marseille', '8.4', '18%', True),
                    ('🇨🇩', 'S. Mvumpa', 'Winger · VfB Stuttgart', '9.6', '24%', True),
                    ('🇨🇩', 'Y. Bolasie', 'Forward · Club Brugge', '8.2', '16%', True)],
    },
    'Belgium': {
        'code': 'be', 'rank': '#3', 'odds': '+1000',
        'h3': 'Last Dance for the Golden Generation',
        'p1': "Belgium's golden generation has one last shot at glory. Kevin De Bruyne remains the most complete midfielder in the world when fit, pulling strings for a fearsome attack.",
        'p2': "Romelu Lukaku's physical presence unsettles any defence, and Leandro Trossard's ability to play across the front line gives Belgium tactical flexibility others cannot match.",
        'stats': [('#1', 'FIFA Peak Ranking'), ('18', 'Goals in Qualifying'), ('#3', 'FIFA World Ranking')],
        'xg': 1.9, 'xga': 0.9, 'shots': 14.6, 'poss': 58,
        'players': [('🇧🇪', 'K. De Bruyne', 'Midfielder · Man City', '16.8', '60%', False),
                    ('🇧🇪', 'R. Lukaku', 'Forward · AS Roma', '14.6', '50%', False),
                    ('🇧🇪', 'L. Trossard', 'Midfielder · Arsenal', '11.4', '36%', False)],
    },
    'Senegal': {
        'code': 'sn', 'rank': '#20', 'odds': '+5000',
        'h3': 'African Champions on the March',
        'p1': "Senegal carry the hopes of a continent with Sadio Mané still capable of moments of brilliance. The reigning African champions have real knockout-stage quality.",
        'p2': "Ismaïla Sarr's electric pace on the flanks and Idrissa Gueye's combative midfield presence give Senegal a balance that can trouble any side.",
        'stats': [('AFCON', '2022 Champions'), ('+8', 'Qualifying Goal Diff'), ('#20', 'FIFA World Ranking')],
        'xg': 1.5, 'xga': 1.0, 'shots': 12.4, 'poss': 52,
        'players': [('🇸🇳', 'S. Mané', 'Forward · Al-Nassr', '15.2', '52%', False),
                    ('🇸🇳', 'I. Sarr', 'Winger · Crystal Palace', '12.8', '40%', False),
                    ('🇸🇳', 'I. Gueye', 'Midfielder · Everton', '8.6', '28%', False)],
    },
    'United States': {
        'code': 'us', 'rank': '#13', 'odds': '+2000',
        'h3': 'Home Advantage in Santa Clara',
        'p1': "The USA enter as co-hosts with a young, dynamic squad. Christian Pulisic captains a generation of European-based talent playing their best football in front of a passionate home crowd.",
        'p2': "Weston McKennie and Giovanni Reyna add creativity around Pulisic, while their high defensive intensity and physical pressing can overwhelm opponents unprepared for their energy.",
        'stats': [('22', 'Goals in Qualifying'), ('#13', 'FIFA World Ranking'), ('QF', 'WC Best (2002)')],
        'xg': 1.7, 'xga': 1.1, 'shots': 13.6, 'poss': 53,
        'players': [('🇺🇸', 'C. Pulisic', 'Forward · AC Milan', '15.4', '56%', False),
                    ('🇺🇸', 'W. McKennie', 'Midfielder · Juventus', '12.2', '42%', False),
                    ('🇺🇸', 'G. Reyna', 'Midfielder · Borussia Dortmund', '13.6', '44%', False)],
    },
    'Bosnia-Herzegovina': {
        'code': 'ba', 'rank': '#55', 'odds': '+14000',
        'h3': 'Dragon Hearts Fight',
        'p1': "Bosnia-Herzegovina return to the World Cup with a resilient squad. Miralem Pjanić's creative intelligence from midfield is their greatest weapon against higher-ranked opposition.",
        'p2': "Edin Džeko brings experience and leadership despite his age, while their defensive organisation and directness on the counter-attack can make them awkward opponents.",
        'stats': [('2', 'WC Appearances'), ('15', 'Goals in Qualifying'), ('#55', 'FIFA World Ranking')],
        'xg': 1.3, 'xga': 1.4, 'shots': 10.4, 'poss': 46,
        'players': [('🇧🇦', 'E. Džeko', 'Forward · Fenerbahce', '12.6', '32%', True),
                    ('🇧🇦', 'M. Pjanić', 'Midfielder · Al-Shamal', '10.4', '28%', True),
                    ('🇧🇦', 'A. Šehić', 'Goalkeeper · Kasımpaşa', '7.2', '14%', False)],
    },
    'Spain': {
        'code': 'es', 'rank': '#8', 'odds': '+1000',
        'h3': 'Tiki-Taka Evolution',
        'p1': "Spain won Euro 2024 in stunning fashion and arrive at this World Cup playing their most dynamic football in years. Pedri, Gavi and Rodri form the world's best midfield.",
        'p2': "Álvaro Morata's leadership and poaching in the box gives Spain the cutting edge their possession deserves. No team is harder to press high against than this Spanish side.",
        'stats': [('1', 'WC Title (2010)'), ('Euro 2024', 'Champions'), ('#8', 'FIFA World Ranking')],
        'xg': 2.0, 'xga': 0.7, 'shots': 15.8, 'poss': 65,
        'players': [('🇪🇸', 'Pedri', 'Midfielder · Barcelona', '14.6', '52%', False),
                    ('🇪🇸', 'Rodri', 'Midfielder · Man City', '13.2', '48%', False),
                    ('🇪🇸', 'Á. Morata', 'Forward · Atletico Madrid', '12.4', '40%', False)],
    },
    'Austria': {
        'code': 'at', 'rank': '#25', 'odds': '+7000',
        'h3': 'Central European Dark Horses',
        'p1': "Austria impressed in qualifying and carry genuine quality, particularly through Marcel Sabitzer who controls the tempo with Premier League experience from his Bayern and Dortmund days.",
        'p2': "Christoph Baumgartner and Marko Arnautović bring physicality and creativity in the final third. Austria's high-energy pressing style can disrupt any opponent's rhythm.",
        'stats': [('7', 'WC Appearances'), ('16', 'Goals in Qualifying'), ('#25', 'FIFA World Ranking')],
        'xg': 1.4, 'xga': 1.2, 'shots': 11.6, 'poss': 50,
        'players': [('🇦🇹', 'M. Sabitzer', 'Midfielder · Borussia Dortmund', '12.4', '38%', False),
                    ('🇦🇹', 'C. Baumgartner', 'Midfielder · RB Leipzig', '11.6', '32%', False),
                    ('🇦🇹', 'M. Arnautović', 'Forward · Galatasaray', '11.2', '28%', True)],
    },
    'Portugal': {
        'code': 'pt', 'rank': '#6', 'odds': '+1400',
        'h3': "Ronaldo's Final Chapter",
        'p1': "Portugal combine Cristiano Ronaldo's experience with a genuinely exciting new generation. Rafael Leão's dribbling and directness on the left gives Portugal a different attacking dimension.",
        'p2': "Bernardo Silva's technical brilliance and Rúben Dias' commanding presence in defence make Portugal one of the most complete squads at the tournament.",
        'stats': [('SF', 'WC Best (2006)'), ('16', 'Goals in Qualifying'), ('#6', 'FIFA World Ranking')],
        'xg': 1.9, 'xga': 0.9, 'shots': 14.8, 'poss': 58,
        'players': [('🇵🇹', 'R. Leão', 'Forward · AC Milan', '15.6', '52%', False),
                    ('🇵🇹', 'B. Silva', 'Midfielder · Man City', '14.2', '50%', False),
                    ('🇵🇹', 'C. Ronaldo', 'Forward · Al-Nassr', '16.8', '58%', True)],
    },
    'Croatia': {
        'code': 'hr', 'rank': '#9', 'odds': '+2200',
        'h3': 'Back-to-Back Finals Heroes',
        'p1': "Croatia have defied expectations across two consecutive World Cup runs reaching the final, driven by Luka Modrić's ageless midfield genius and tournament resilience.",
        'p2': "Ivan Perišić and Bruno Petković offer different goal-threat profiles, and Croatia's tournament experience — winning from behind, enduring extra time — is unmatched.",
        'stats': [('2nd', 'WC Finish (2018, 2022)'), ('14', 'Goals in Qualifying'), ('#9', 'FIFA World Ranking')],
        'xg': 1.5, 'xga': 1.0, 'shots': 12.6, 'poss': 54,
        'players': [('🇭🇷', 'L. Modrić', 'Midfielder · Real Madrid', '13.6', '48%', True),
                    ('🇭🇷', 'I. Perišić', 'Winger · Hajduk Split', '12.4', '40%', False),
                    ('🇭🇷', 'M. Budimir', 'Forward · Osasuna', '10.8', '28%', False)],
    },
    'Switzerland': {
        'code': 'ch', 'rank': '#19', 'odds': '+5500',
        'h3': 'Reliable Swiss Precision',
        'p1': "Switzerland consistently punch above their weight at major tournaments. Granit Xhaka's leadership and experience from his Bayer Leverkusen title campaign makes him a world-class midfielder.",
        'p2': "Breel Embolo and Xherdan Shaqiri complement Xhaka with physicality and directness. Switzerland's collective defensive intensity makes them genuinely difficult to break down.",
        'stats': [('QF', 'WC Best (1934,1938,1954)'), ('18', 'Goals in Qualifying'), ('#19', 'FIFA World Ranking')],
        'xg': 1.5, 'xga': 1.0, 'shots': 12.4, 'poss': 52,
        'players': [('🇨🇭', 'G. Xhaka', 'Midfielder · Bayer Leverkusen', '12.8', '44%', False),
                    ('🇨🇭', 'X. Shaqiri', 'Midfielder · Chicago Fire', '11.4', '36%', True),
                    ('🇨🇭', 'B. Embolo', 'Forward · AS Monaco', '12.2', '38%', False)],
    },
    'Algeria': {
        'code': 'dz', 'rank': '#35', 'odds': '+9000',
        'h3': 'Desert Foxes Eye Glory',
        'p1': "Algeria's World Cup campaign rises with Riyad Mahrez, one of the game's great dribblers, who has never had the chance to shine on the biggest stage until now.",
        'p2': "Islam Slimani remains a powerful target striker and Sofiane Feghouli adds craft and directness. Algeria's AFCON pedigree shows they can compete with European opponents.",
        'stats': [('AFCON', '2019 Champions'), ('14', 'Goals in Qualifying'), ('#35', 'FIFA World Ranking')],
        'xg': 1.3, 'xga': 1.2, 'shots': 10.8, 'poss': 48,
        'players': [('🇩🇿', 'R. Mahrez', 'Winger · Al-Ahli', '14.6', '46%', False),
                    ('🇩🇿', 'I. Slimani', 'Forward · Besiktas', '11.2', '30%', True),
                    ('🇩🇿', 'H. Benrahma', 'Midfielder · West Ham', '12.4', '38%', False)],
    },
    'Australia': {
        'code': 'au', 'rank': '#23', 'odds': '+8000',
        'h3': 'Socceroos Dream Bigger',
        'p1': "Australia reached the semi-finals in 2022 and return with experience and belief. Mathew Leckie's energy and work-rate on the right channel can unlock any defensive structure.",
        'p2': "Jackson Irvine and Riley Hrustic provide a hard-working midfield platform, while Australia's high defensive intensity and set-piece threat make them dangerous at knockout level.",
        'stats': [('SF', 'WC Best (2022)'), ('13', 'Goals in Qualifying'), ('#23', 'FIFA World Ranking')],
        'xg': 1.2, 'xga': 1.1, 'shots': 10.2, 'poss': 47,
        'players': [('🇦🇺', 'M. Leckie', 'Winger · Melbourne City', '11.4', '36%', False),
                    ('🇦🇺', 'J. Irvine', 'Midfielder · St Mirren', '10.2', '28%', False),
                    ('🇦🇺', 'R. Hrustic', 'Midfielder · Genoa', '9.8', '24%', False)],
    },
    'Egypt': {
        'code': 'eg', 'rank': '#47', 'odds': '+12000',
        'h3': 'Salah Leads the Pharaohs',
        'p1': "Egypt's World Cup campaign depends almost entirely on Mohamed Salah, one of the all-time greats who has never had the platform to shine at this stage until now.",
        'p2': "Omar Marmoush and Mostafa Mohamed provide support around Salah, but Egypt will need more than just their captain if they're to pull off a knockout upset.",
        'stats': [('3', 'WC Appearances'), ('11', 'Goals in Qualifying'), ('#47', 'FIFA World Ranking')],
        'xg': 1.2, 'xga': 1.3, 'shots': 10.4, 'poss': 49,
        'players': [('🇪🇬', 'M. Salah', 'Forward · Liverpool', '19.2', '64%', False),
                    ('🇪🇬', 'O. Marmoush', 'Forward · Eintracht Frankfurt', '13.8', '42%', False),
                    ('🇪🇬', 'M. Mohamed', 'Forward · Galatasaray', '11.4', '32%', False)],
    },
    'Argentina': {
        'code': 'ar', 'rank': '#1', 'odds': '+500',
        'h3': 'World Champions Defend',
        'p1': "Argentina arrive as defending champions with Lionel Messi seeking to add another chapter to his unparalleled legacy. No team in this tournament has the individual quality depth that Argentina possess.",
        'p2': "Julián Álvarez and Lautaro Martínez are world-class alternatives to Messi in attack. With a tightened defence and De Paul controlling midfield, Argentina are the benchmark for every other side.",
        'stats': [('3', 'World Cup Titles'), ('#1', 'FIFA World Ranking'), ('+15', 'Qualifying Goal Diff')],
        'xg': 2.2, 'xga': 0.7, 'shots': 16.4, 'poss': 62,
        'players': [('🇦🇷', 'L. Messi', 'Forward · Inter Miami', '20.2', '82%', False),
                    ('🇦🇷', 'J. Álvarez', 'Forward · Man City', '15.8', '58%', False),
                    ('🇦🇷', 'L. Martínez', 'Forward · Inter Milan', '14.4', '52%', False)],
    },
    'Cape Verde Islands': {
        'code': 'cv', 'rank': '#58', 'odds': '+25000',
        'h3': 'Blue Sharks Make History',
        'p1': "Cape Verde Islands are making their first World Cup appearance, becoming a symbol of emerging African football. Their high-pressing style caught many opponents off guard in qualifying.",
        'p2': "Ryan Mendes and Garry Rodrigues provide dangerous wide play, and while this matchup looks one-sided on paper, Cape Verde's unity and collective spirit cannot be underestimated.",
        'stats': [('1st', 'World Cup Appearance'), ('12', 'Goals in Qualifying'), ('#58', 'FIFA World Ranking')],
        'xg': 1.1, 'xga': 1.4, 'shots': 8.8, 'poss': 43,
        'players': [('🇨🇻', 'R. Mendes', 'Winger · Panathinaikos', '10.8', '28%', True),
                    ('🇨🇻', 'G. Rodrigues', 'Winger · Olympiakos', '10.2', '24%', True),
                    ('🇨🇻', 'Z. Andrade', 'Defender · Vitória de Guimarães', '7.6', '14%', False)],
    },
    'Colombia': {
        'code': 'co', 'rank': '#16', 'odds': '+2500',
        'h3': 'South American Entertainers',
        'p1': "Colombia qualified with one of the most entertaining styles in the tournament. Luis Díaz's pace and directness on the left has made him one of the world's most exciting forwards.",
        'p2': "James Rodríguez carries World Cup pedigree from his 2014 Golden Boot campaign and is determined to replicate that form. Rafael Arias adds press-resistant midfield quality.",
        'stats': [('QF', 'WC Best (2014)'), ('21', 'Goals in Qualifying'), ('#16', 'FIFA World Ranking')],
        'xg': 1.7, 'xga': 1.0, 'shots': 13.8, 'poss': 54,
        'players': [('🇨🇴', 'L. Díaz', 'Forward · Liverpool', '16.2', '54%', False),
                    ('🇨🇴', 'J. Rodríguez', 'Midfielder · Rayo Vallecano', '14.8', '48%', False),
                    ('🇨🇴', 'R. Arias', 'Midfielder · Atletico Madrid', '12.4', '38%', False)],
    },
    'Ghana': {
        'code': 'gh', 'rank': '#59', 'odds': '+18000',
        'h3': 'Black Stars Reborn',
        'p1': "Ghana return to the World Cup looking to recapture the spirit of 2010 when they came within a penalty of the semi-finals. Mohammed Kudus is their star — electric, unpredictable, world-class.",
        'p2': "Thomas Partey's Premier League experience gives Ghana a midfield anchor of genuine quality, while Jordan Ayew's pace on the break can catch any defence cold.",
        'stats': [('QF', 'WC Best (2010)'), ('14', 'Goals in Qualifying'), ('#59', 'FIFA World Ranking')],
        'xg': 1.3, 'xga': 1.4, 'shots': 11.2, 'poss': 48,
        'players': [('🇬🇭', 'M. Kudus', 'Midfielder · West Ham', '14.8', '46%', False),
                    ('🇬🇭', 'J. Ayew', 'Forward · Al-Qadsiah', '11.2', '30%', True),
                    ('🇬🇭', 'T. Partey', 'Midfielder · Arsenal', '13.4', '42%', False)],
    },
}

_H2H = {
    'wc2026-m73': "South Africa and Canada have rarely met competitively. Canada hold a slight historical edge in limited encounters, but this effectively serves as a first meaningful meeting on the biggest stage.",
    'wc2026-m76': "Brazil dominate the historical record against Japan, winning 8 of their last 10 meetings. Japan's only wins came in friendly settings, though their recent tournament pedigree has improved dramatically with wins over Germany and Spain.",
    'wc2026-m74': "Germany and Paraguay's World Cup history includes a memorable 2010 quarter-final won by the Germans. Paraguay are more compact and direct these days, making this potentially closer than the rankings suggest.",
    'wc2026-m75': "Netherlands and Morocco met in the 2022 World Cup quarter-finals, with the Dutch winning 2-1 in a tense encounter. Morocco will be motivated by the memory of that defeat and aim to exact revenge.",
    'wc2026-m78': "Norway and Ivory Coast have minimal World Cup history together. Haaland against the AFCON champions creates a fascinating contest of individual brilliance against collective defensive strength.",
    'wc2026-m77': "France have historically dominated Sweden in competitive matches, winning their last five meetings. Sweden's compact defensive setup might frustrate France early, but France's quality should ultimately prevail.",
    'wc2026-m79': "Mexico have faced Ecuador four times at World Cups, winning three. Playing at the Estadio Azteca in Mexico City, the home side will have an enormous advantage in what promises to be an electric atmosphere.",
    'wc2026-m80': "England and DR Congo have never met at a World Cup. This is a significant mismatch on paper, but England's complicated knockout history means they must approach this with full focus.",
    'wc2026-m82': "Belgium and Senegal have met twice at World Cups, splitting the results. Senegal's 2002 upset of France showed African champions can topple European heavyweights, though this Belgian squad is exceptionally talented.",
    'wc2026-m81': "USA and Bosnia-Herzegovina have no World Cup history, but recent friendly meetings showed Bosnia are capable of competitive performances. Playing at Levi's Stadium in Santa Clara, the USA will have thunderous home support.",
    'wc2026-m84': "Spain are unbeaten in all competitive meetings against Austria. Austria have never defeated Spain and face a formidable task against the Euro 2024 champions on paper, though their pressing style could create problems.",
    'wc2026-m83': "Portugal and Croatia have met at multiple European Championships with both teams winning. The tactical battle will be fascinating — Portugal's individual quality against Croatia's legendary collective tournament discipline.",
    'wc2026-m85': "Switzerland and Algeria have never met at a World Cup. Switzerland are the more experienced tournament team, but Algeria's quality has grown significantly since their 2019 AFCON triumph under Djamel Belmadi.",
    'wc2026-m88': "Australia and Egypt have no World Cup history. Egypt's concentration of star power in Salah contrasts with Australia's recent knockout tournament experience from their 2022 semi-final run.",
    'wc2026-m86': "Argentina have never lost to Cape Verde Islands at any level, and this matchup represents the sharpest contrast in quality across the entire knockout round. However, upsets happen — that is the beauty of the World Cup.",
    'wc2026-m87': "Colombia and Ghana met at the 2014 World Cup with Colombia winning 2-1 in the group stage. Both teams have evolved considerably since then and this promises to be a genuinely competitive contest.",
}

# Additional supporting picks per match (beyond the main pick in knockout.json)
_SUPPORTING_PICKS = {
    'wc2026-m73': [
        ('Jonathan David to Score Anytime', 'In brilliant Ligue 1 form against weakened South Africa defence', 'HOT', '+160'),
        ('Both Teams to Score', 'South Africa will need to attack — open game expected', 'VALUE', '-110'),
    ],
    'wc2026-m76': [
        ('Vinicius Jr. to Score or Assist', 'Direct pace vs Japan full-backs, Brazil most dangerous on the break', 'HOT', '-120'),
        ('Over 2.5 Goals', "Brazil's attacking depth vs Japan's R16 tendency to concede", 'VALUE', '+115'),
    ],
    'wc2026-m74': [
        ('Germany Win to Nil', 'Paraguay struggle to convert — Germany defence historically strong', 'VALUE', '+110'),
        ('Florian Wirtz Anytime Scorer', 'Creating and scoring in every game, most dangerous German attacker', 'HOT', '+200'),
    ],
    'wc2026-m75': [
        ('Both Teams to Score', 'Morocco attack freely in knockouts — Netherlands historically open at back', 'VALUE', '-105'),
        ('Cody Gakpo to Score Anytime', 'World Cup experience, direct runner who will target Morocco wide areas', 'HOT', '+165'),
    ],
    'wc2026-m78': [
        ('Erling Haaland to Score Anytime', 'Already among the top scorers — faces a defence that conceded in qualifying', 'HOT', '-140'),
        ('Over 2.5 Goals', "Norway's attack vs Ivory Coast's tendency to engage rather than sit back", 'VALUE', '-110'),
    ],
    'wc2026-m77': [
        ('Kylian Mbappé to Score Anytime', 'Sweden full-backs will struggle with his pace in transition', 'HOT', '-150'),
        ('France Win & Over 2.5', 'Les Bleus to control and score freely against depleted Sweden', 'VALUE', '+115'),
    ],
    'wc2026-m79': [
        ('Mexico Win to Nil', 'Ecuador struggle to score against organised defences', 'VALUE', '+140'),
        ('Hirving Lozano to Score Anytime', 'PSV forward in best form, facing an Ecuador side that conceded in qualifying', 'HOT', '+185'),
    ],
    'wc2026-m80': [
        ('England Win & Over 2.5', "England's attack too powerful — expect clinical finishing from Kane and Bellingham", 'VALUE', '-115'),
        ('Harry Kane to Score Anytime', 'Golden Boot contender in outstanding form, faces weakest defence left in tournament', 'HOT', '-180'),
    ],
    'wc2026-m82': [
        ('Romelu Lukaku to Score Anytime', 'Physical presence will trouble Senegal centre-backs', 'HOT', '+130'),
        ('Both Teams to Score', 'Mané capable of punishing Belgium on the counter — open game expected', 'VALUE', '-105'),
    ],
    'wc2026-m81': [
        ('Christian Pulisic to Score or Assist', 'In brilliant Champions League form at Milan, home crowd will lift him', 'HOT', '-115'),
        ('Over 2.5 Goals', "USA's attack vs Bosnia's open style — both teams want to play forward", 'VALUE', '-105'),
    ],
    'wc2026-m84': [
        ('Spain Win & Over 2.5', 'Spain dominate possession and create freely against Austria high line', 'VALUE', '+130'),
        ('Rodri Anytime Scorer', 'Set-piece menace and increasingly likely to score from distance', 'VALUE', '+280'),
    ],
    'wc2026-m83': [
        ("Cristiano Ronaldo to Score Anytime", "World Cup final swan song — motivated like never before, penalty taker", 'HOT', '+110'),
        ('Both Teams to Score', 'Croatia will create chances — Perišić a constant threat vs Portugal right-back', 'VALUE', '-120'),
    ],
    'wc2026-m85': [
        ('Switzerland Win & Under 2.5', "Low-scoring game expected — Switzerland's defence is tournament-level quality", 'VALUE', '+120'),
        ('Granit Xhaka to Score Anytime', 'Scored regularly for Leverkusen, increasingly likely from midfield', 'VALUE', '+280'),
    ],
    'wc2026-m88': [
        ('Mohamed Salah to Score Anytime', "Once-in-a-generation player, carries Egypt — first World Cup knockout match is everything to him", 'HOT', '-110'),
        ('Australia Win or Draw & Under 2.5', 'Australia defensive solidity + compact shape equals a tight match', 'VALUE', '-115'),
    ],
    'wc2026-m86': [
        ('Lionel Messi to Score Anytime', 'Greatest player of all time vs weakest remaining side — expect a statement', 'HOT', '-180'),
        ('Argentina Win & Over 2.5', 'Argentina will not hold back — Álvarez and Martínez both hungry to impress', 'VALUE', '-120'),
    ],
    'wc2026-m87': [
        ('Luis Díaz to Score Anytime', 'Liverpool winger in brilliant form, pace will hurt Ghana full-backs', 'HOT', '+140'),
        ('Colombia Win & Over 2.5', "Colombia's entertaining style should produce goals — Ghana attack when possible", 'VALUE', '+115'),
    ],
}


# ── Utility ───────────────────────────────────────────────────────────────────

def team_slug(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())


def make_page_slug(home_name, away_name):
    return team_slug(home_name) + '-' + team_slug(away_name)


def stat_rows_for(home_data, away_data):
    """Generate 5 comparison stat rows from team xG/shots/possession data."""
    h, a = home_data, away_data

    def pct(hv, av):
        total = hv + av
        return int(hv / total * 100) if total else 50

    return [
        (f'{h["xg"]:.1f}', 'Avg xG / Game', pct(h['xg'], a['xg']), f'{a["xg"]:.1f}'),
        (f'{h["shots"]:.0f}', 'Shots / Game', pct(h['shots'], a['shots']), f'{a["shots"]:.0f}'),
        (f'{h["poss"]}%', 'Possession', h['poss'], f'{a["poss"]}%'),
        (f'{h["xga"]:.1f}', 'xGA / Game', pct(a['xga'], h['xga']), f'{a["xga"]:.1f}'),
        (h['stats'][0][0], h['stats'][0][1][:16], 50, a['stats'][0][0]),
    ]


def trending_for(home, away):
    return [
        (f'{home} vs {away} prediction', 'TRENDING'),
        (f'{home} World Cup odds 2026', 'RISING'),
        (f'{away} lineup Round of 32', 'NEW'),
        (f'Best bet {home} vs {away}', 'HOT'),
        (f'{home} {away} stream', 'POPULAR'),
    ]


def fantasy_section_ko(home_players, away_players):
    """Build fantasy picks section combining 3 home + 2 away players."""
    all_players = home_players[:3] + away_players[:2]
    rows = ''
    for rank, (emoji, name, meta, pts, own, risk) in enumerate(all_players, 1):
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


def ko_sidebar(m):
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
        <div class="sc-head">Up Next — Knockout Stage</div>
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


# ── Page builder ──────────────────────────────────────────────────────────────

def _ml_fav(home_ml, away_ml, home_name, away_name):
    try:
        hn = int(str(home_ml).replace('+', ''))
        an = int(str(away_ml).replace('+', ''))
        return (home_name, home_ml) if hn <= an else (away_name, away_ml)
    except (TypeError, ValueError):
        return (home_name, home_ml or '-110')


def build_match_dict(slot, ko_meta, live_entry, photo_idx):
    home_name = (live_entry.get('home') or {}).get('name') or slot['home']['name']
    away_name = (live_entry.get('away') or {}).get('name') or slot['away']['name']
    hd = _TEAM_DATA.get(home_name, {})
    ad = _TEAM_DATA.get(away_name, {})
    if not hd or not ad:
        return None

    home_code = (live_entry.get('home') or {}).get('code') or hd.get('code', 'xx')
    away_code = (live_entry.get('away') or {}).get('code') or ad.get('code', 'xx')

    # Odds from live.json (Odds API) or knockout.json static
    home_ml = live_entry.get('home_ml') or ko_meta.get('odds') or '+100'
    draw_ml = live_entry.get('draw_ml') or '+240'
    away_ml = live_entry.get('away_ml') or '+220'
    home_prob = live_entry.get('home_prob') or (ko_meta.get('prob') or {}).get('home', 40)
    draw_prob = live_entry.get('draw_prob') or (ko_meta.get('prob') or {}).get('draw', 25)
    away_prob = live_entry.get('away_prob') or (ko_meta.get('prob') or {}).get('away', 35)
    fav_name, fav_ml = _ml_fav(home_ml, away_ml, home_name, away_name)

    slug = ko_meta['slug']
    page_slug = make_page_slug(home_name, away_name)
    stage_label = {'r32': 'Round of 32', 'r16': 'Round of 16', 'qf': 'Quarter-Final',
                   'sf': 'Semi-Final', 'tp': 'Third Place Play-off', 'final': 'Final'}.get(slot['stage'], slot['stage'].upper())

    # AI pick chips
    pick_text = ko_meta.get('pick') or f'{fav_name} to Win'
    chips = [
        (pick_text, True),
        (f'Under 2.5 Goals', False),
        (f'{fav_name} to Score First', True),
    ]

    # Picks: main + supporting
    main_pick_odds = ko_meta.get('odds') or fav_ml
    picks = [(ko_meta.get('pick') or f'{fav_name} to Win',
              f'PitchIQ AI analysis across 50,000 simulations — {fav_name} expected to advance', 'AI PICK', main_pick_odds)]
    picks += _SUPPORTING_PICKS.get(slug, [])

    # Stat rows
    stat_rows = stat_rows_for(hd, ad)

    # Fantasy
    home_players = hd.get('players', [])
    away_players = ad.get('players', [])

    # Trending
    trending = trending_for(home_name, away_name)

    # Up next: show predictions page + group stage
    up_next = [
        (f'{home_name} vs {away_name} — Full Preview', 'Match Day', f'/{page_slug}'),
        ('All Knockout Predictions', 'View All', '/predictions'),
        ('Group Stage Results', 'See All', '/standings'),
    ]

    # Venue from knockout.json
    venue_short = slot.get('venue_short', 'TBD')
    city = slot.get('city', '')
    venue_full = f'{venue_short}, {city}' if city else venue_short

    # Pred result string
    prob_diff = home_prob - away_prob
    if prob_diff > 15:
        pred_result = 'Win'
    elif prob_diff > 5:
        pred_result = 'Win or Draw'
    elif prob_diff > -5:
        pred_result = 'Draw'
    else:
        pred_result = 'Win'

    # Date strings
    date_short = slot.get('date_short', 'TBD')
    time_str = slot.get('time_str', 'TBD')
    months = {'Jun': 'June', 'Jul': 'July', 'Aug': 'August'}
    parts = date_short.split()
    month_full = months.get(parts[0], parts[0]) if parts else ''
    date_str = f'{month_full} {parts[1] if len(parts)>1 else ""}, 2026'

    return {
        'slug': page_slug,
        'ko_slug': slug,
        'stage': slot['stage'],
        'stage_label': stage_label,
        'match_no': slot.get('match_no', ''),
        'home': home_name, 'away': away_name,
        'home_code': home_code, 'away_code': away_code,
        'home_emoji': '',   # derived client-side / emoji handled in page
        'away_emoji': '',
        'home_rank': f'FIFA Rank {hd["rank"]} · Tournament Odds {hd["odds"]}',
        'away_rank': f'FIFA Rank {ad["rank"]} · Tournament Odds {ad["odds"]}',
        'home_ml': home_ml, 'draw_ml': draw_ml, 'away_ml': away_ml,
        'fav_name': fav_name, 'fav_ml': fav_ml,
        'ou_over': '-115', 'ou_under': '-115',
        'home_prob': home_prob, 'draw_prob': draw_prob, 'away_prob': away_prob,
        'pred_result': pred_result,
        'chips': chips,
        'date_short': date_short, 'date_str': date_str, 'time_str': time_str,
        'venue': venue_full, 'venue_short': venue_short,
        'group': stage_label,   # repurposed for knockout stage label
        'matchday': f'Match {slot.get("match_no", "")}',
        'json_dt': f'2026-{date_short}-T00:00:00Z',
        'photo': PHOTOS[photo_idx % len(PHOTOS)],
        'home_h3': hd['h3'], 'home_p1': hd['p1'], 'home_p2': hd['p2'],
        'home_stats': hd['stats'],
        'away_h3': ad['h3'], 'away_p1': ad['p1'], 'away_p2': ad['p2'],
        'away_stats': ad['stats'],
        'h2h': _H2H.get(slug, f'{home_name} and {away_name} meet in the {stage_label}.'),
        'stat_rows': stat_rows,
        'picks': picks,
        'fantasy': home_players[:3] + away_players[:2],
        'trending': trending,
        'up_next': up_next,
        'home_players': home_players,
        'away_players': away_players,
    }


def generate_knockout_page(m):
    import re as _re

    h = TEMPLATE

    h = h.replace('og-image.jpg', 'pitchiq-banner.png')

    if '/_vercel/insights/script.js' not in h:
        h = h.replace(
            '  <link rel="preconnect" href="https://fonts.googleapis.com"/>',
            '  <script defer src="/_vercel/insights/script.js"></script>\n\n  <link rel="preconnect" href="https://fonts.googleapis.com"/>'
        )

    # Title
    for old in [
        'Brazil vs Morocco Prediction, Odds &amp; Fantasy Picks — World Cup 2026 | PitchIQ',
        'Brazil vs Morocco Prediction, Odds & Fantasy Picks — World Cup 2026 | PitchIQ',
    ]:
        h = h.replace(old, f'{m["home"]} vs {m["away"]} Prediction, Odds &amp; Fantasy Picks — World Cup 2026 | PitchIQ')

    # Meta description
    h = _re.sub(
        r'<meta name="description" content="[^"]*"/>',
        f'<meta name="description" content="{m["home"]} vs {m["away"]} World Cup 2026 prediction, odds, AI analysis and fantasy picks. {m["stage_label"]} on {m["date_short"]} at {m["venue_short"]}. {m["fav_name"]} {m["fav_ml"]} favourite."/>',
        h
    )

    # Canonical + OG URL
    h = h.replace('https://getpitchiq.net/brazil-morocco', f'https://getpitchiq.net/{m["slug"]}')

    # pitchiq meta tags
    pitchiq_meta = (
        f'  <meta name="pitchiq:page"  content="match"/>\n'
        f'  <meta name="pitchiq:slug"  content="{m["slug"]}"/>\n'
        f'  <meta name="pitchiq:home"  content="{m["home"]}"/>\n'
        f'  <meta name="pitchiq:away"  content="{m["away"]}"/>\n'
    )
    if 'pitchiq:slug' not in h:
        h = h.replace('</head>', pitchiq_meta + '</head>', 1)

    live_scripts = (
        '  <script src="/js/pitchiq-config.js"></script>\n'
        '  <script src="/js/pitchiq-live.js"></script>\n'
    )
    if 'pitchiq-live.js' not in h:
        h = h.replace('</body>', live_scripts + '</body>', 1)

    # OG title
    h = _re.sub(
        r'<meta property="og:title" content="[^"]*"/>',
        f'<meta property="og:title" content="{m["home"]} vs {m["away"]} Prediction &amp; Odds — World Cup 2026 {m["stage_label"]}"/>',
        h
    )

    # OG description
    h = _re.sub(
        r'<meta property="og:description" content="[^"]*"/>',
        f'<meta property="og:description" content="AI-powered prediction, live odds and fantasy picks for {m["home"]} vs {m["away"]}. {m["stage_label"]}, {m["date_short"]}, {m["venue_short"]}."/>',
        h
    )

    # JSON-LD
    schema_block = schema_json_ld(m)
    h = _re.sub(r'\s*<script type="application/ld\+json">\s*\{"@context":"https://schema\.org","@type":"BreadcrumbList".*?</script>\s*', '\n', h, flags=_re.DOTALL)
    h = _re.sub(r'\s*<script type="application/ld\+json">\s*\{"@context":"https://schema\.org","@type":"SportsEvent".*?</script>\s*', '\n', h, count=1, flags=_re.DOTALL)
    h = _re.sub(r'\s*<!-- GA4 — replace with your Measurement ID -->', '\n' + schema_block + '\n\n  <!-- GA4 — replace with your Measurement ID -->', h, count=1)

    # Stadium photo
    h = h.replace('1556816214-6d16c62fbbf6', m['photo'])

    # Match header badge
    h = h.replace(
        '⚽ FIFA World Cup 2026 · Group C · Matchday 1',
        f'⚽ FIFA World Cup 2026 · {m["stage_label"]} · {m["matchday"]}'
    )

    # Teams block — reuse home/away code approach
    flag_img_h = f'https://flagcdn.com/w80/{m["home_code"]}.png'
    flag_img_a = f'https://flagcdn.com/w80/{m["away_code"]}.png'
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
        f'        <img src="{flag_img_h}" alt="{m["home"]}" class="team-flag-img" loading="lazy">\n'
        f'        <div class="mh-flag"></div>\n'
        f'        <div class="mh-name">{m["home"]}</div>\n'
        f'        <div class="mh-rank">{m["home_rank"]}</div>\n'
        f'      </div>\n'
        f'      <div class="mh-vs">VS</div>\n'
        f'      <div class="mh-team">\n'
        f'        <img src="{flag_img_a}" alt="{m["away"]}" class="team-flag-img" loading="lazy">\n'
        f'        <div class="mh-flag"></div>\n'
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

    # Odds strip date
    h = h.replace('Updated Jun 13', f'Updated {m["date_short"]}')

    # Odds strip values
    home_cls = 'fav' if str(m['home_ml']).startswith('-') else 'dog'
    away_cls = 'fav' if str(m['away_ml']).startswith('-') else 'dog'
    h = h.replace('<div class="odd-label">Brazil Win</div>', f'<div class="odd-label">{m["home"]} Win</div>')
    h = h.replace('<div class="odd-val fav">-138</div>', f'<div class="odd-val {home_cls}">{m["home_ml"]}</div>')
    h = h.replace('<div class="odd-val dog">+290</div>', f'<div class="odd-val dog">{m["draw_ml"]}</div>')
    h = h.replace('<div class="odd-label">Morocco Win</div>', f'<div class="odd-label">{m["away"]} Win</div>')
    h = h.replace('<div class="odd-val dog">+500</div>', f'<div class="odd-val {away_cls}">{m["away_ml"]}</div>')

    # Content sections
    h = replace_between(h, '      <!-- AI Prediction -->', '      <!-- Match Analysis -->', ai_section(m))
    h = replace_between(h, '      <!-- Match Analysis -->', '      <!-- Stats Comparison -->', analysis_section(m))
    h = replace_between(h, '      <!-- Stats Comparison -->', '      <!-- Betting Picks -->', stats_section(m))
    h = replace_between(h, '      <!-- Betting Picks -->', '      <!-- Fantasy Picks -->', picks_section(m))
    h = replace_between(h, '      <!-- Fantasy Picks -->', '    </div><!-- /main -->', fantasy_section_ko(m['home_players'], m['away_players']))
    h = replace_between(h, '    <!-- SIDEBAR -->', '    </div><!-- /sidebar -->', ko_sidebar(m))

    # Footer link
    if '/predictions.html">More predictions' not in h:
        h = h.replace(
            '  © 2026 PitchIQ · <a href="/">getpitchiq.net</a>',
            '  <div style="margin-bottom:8px;"><a href="/predictions">More predictions →</a></div>\n  © 2026 PitchIQ · <a href="/">getpitchiq.net</a>'
        )

    return h


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    try:
        ko_base = json.loads(KNOCKOUT_JSON.read_text(encoding='utf-8'))['matches']
    except Exception as e:
        print(f'ERROR reading knockout.json: {e}'); sys.exit(1)

    try:
        live_data = json.loads(LIVE_JSON.read_text(encoding='utf-8')) if LIVE_JSON.exists() else {}
    except Exception:
        live_data = {}

    live_ko = live_data.get('knockout', {})
    generated, skipped, errors = 0, 0, 0
    slugs_written = {}

    for idx, slot in enumerate(ko_base):
        kslug = slot['slug']
        live_entry = live_ko.get(kslug, {})

        home_name = (live_entry.get('home') or {}).get('name') or ''
        away_name = (live_entry.get('away') or {}).get('name') or ''

        # Skip if teams not real (still bracket descriptors)
        hd = _TEAM_DATA.get(home_name)
        ad = _TEAM_DATA.get(away_name)
        if not hd or not ad:
            continue

        m = build_match_dict(slot, slot, live_entry, idx)
        if not m:
            continue

        page_slug = m['slug']
        out_path = PROJ / f'{page_slug}.html'

        # Skip if existing page was generated for same matchup
        if live_ko.get(kslug, {}).get('page_slug') == page_slug and out_path.exists():
            skipped += 1
            slugs_written[kslug] = page_slug
            continue

        if DRY:
            print(f'  [dry] {page_slug}.html  ({home_name} vs {away_name})')
            slugs_written[kslug] = page_slug
            generated += 1
            continue

        try:
            content = generate_knockout_page(m)
            out_path.write_text(content, encoding='utf-8')
            print(f'  {page_slug}.html')
            slugs_written[kslug] = page_slug
            generated += 1
        except Exception as e:
            print(f'  ERROR {page_slug}: {e}')
            errors += 1

    # Write page_slug back to live.json
    if not DRY and slugs_written:
        for kslug, pslug in slugs_written.items():
            if kslug in live_ko:
                live_ko[kslug]['page_slug'] = pslug
            else:
                live_ko[kslug] = {'page_slug': pslug}
        live_data['knockout'] = live_ko
        LIVE_JSON.write_text(json.dumps(live_data, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'  Wrote page_slug for {len(slugs_written)} slots to live.json')

    print(f'\n  Generated {generated} pages, {skipped} skipped, {errors} errors')


if __name__ == '__main__':
    main()
