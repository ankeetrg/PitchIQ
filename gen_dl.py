#!/usr/bin/env python3
"""Groups D-L generator — authoritative WC2026 schedule data"""
import os, sys
PROJ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJ)
from generate_pages import generate_page

VENUE_META = {
    'Los Angeles Stadium, Inglewood, CA': ('Los Angeles Stadium', 'Los Angeles Stadium', 'Inglewood, CA'),
    'BC Place, Vancouver, Canada': ('BC Place', 'BC Place', 'Vancouver, Canada'),
    "Levi's Stadium, Santa Clara, CA": ("Levi's Stadium", "Levi's Stadium", 'Santa Clara, CA'),
    'Lumen Field, Seattle, WA': ('Lumen Field', 'Lumen Field', 'Seattle, WA'),
    'Lincoln Financial Field, Philadelphia, PA': ('Lincoln Financial Field', 'Lincoln Financial Field', 'Philadelphia, PA'),
    'BMO Field, Toronto, Canada': ('BMO Field', 'BMO Field', 'Toronto, Canada'),
    'Arrowhead Stadium, Kansas City, MO': ('Arrowhead Stadium', 'Arrowhead Stadium', 'Kansas City, MO'),
    'MetLife Stadium, East Rutherford, NJ': ('MetLife Stadium', 'MetLife Stadium', 'East Rutherford, NJ'),
    'NRG Stadium, Houston, TX': ('NRG Stadium', 'NRG Stadium', 'Houston, TX'),
    'Mercedes-Benz Stadium, Atlanta, GA': ('Mercedes-Benz Stadium', 'Mercedes-Benz Stadium', 'Atlanta, GA'),
    'Hard Rock Stadium, Miami, FL': ('Hard Rock Stadium', 'Hard Rock Stadium', 'Miami, FL'),
    'AT&T Stadium, Arlington, TX': ('AT&T Stadium', 'AT&T Stadium', 'Arlington, TX'),
    'Gillette Stadium, Foxborough, MA': ('Gillette Stadium', 'Gillette Stadium', 'Foxborough, MA'),
    'Estadio BBVA, Monterrey, Mexico': ('Estadio BBVA', 'Estadio BBVA', 'Monterrey, Mexico'),
    'Estadio Akron, Guadalajara, Mexico': ('Estadio Akron', 'Estadio Akron', 'Guadalajara, Mexico'),
    'Estadio Azteca, Mexico City, Mexico': ('Estadio Azteca', 'Estadio Azteca', 'Mexico City, Mexico'),
}

DAYS = {
    '2026-06-12': 'Friday', '2026-06-13': 'Saturday', '2026-06-14': 'Sunday',
    '2026-06-15': 'Monday', '2026-06-16': 'Tuesday', '2026-06-17': 'Wednesday',
    '2026-06-18': 'Thursday', '2026-06-19': 'Friday', '2026-06-20': 'Saturday',
    '2026-06-21': 'Sunday', '2026-06-22': 'Monday', '2026-06-23': 'Tuesday',
    '2026-06-24': 'Wednesday', '2026-06-25': 'Thursday', '2026-06-26': 'Friday',
    '2026-06-27': 'Saturday', '2026-06-28': 'Sunday',
}

MONTH = {
    '06-12': 'June 12', '06-13': 'June 13', '06-14': 'June 14',
    '06-15': 'June 15', '06-16': 'June 16', '06-17': 'June 17',
    '06-18': 'June 18', '06-19': 'June 19', '06-20': 'June 20',
    '06-21': 'June 21', '06-22': 'June 22', '06-23': 'June 23',
    '06-24': 'June 24', '06-25': 'June 25', '06-26': 'June 26',
    '06-27': 'June 27', '06-28': 'June 28',
}

# ── Team knowledge base ───────────────────────────────────────────────────────
T = {
'United States': dict(
    emoji='🇺🇸', code='us', rank='#11', todds='+1500',
    xg='2.3', gc='0.8', poss='60%', pass_acc='83%',
    h3='Host Nation With Tournament Pedigree',
    p1='The United States enter WC2026 as co-hosts with their deepest squad in history. Gregg Berhalter\'s 4-3-3 presses aggressively from the front — Christian Pulisic (Chelsea) leads the line, generating chances through movement and running channels at pace.',
    p2='Gio Reyna provides the creative link from #10, distributing with his back to goal and running beyond the striker. Weston McKennie (Juventus) and Tyler Adams (Bournemouth) cover the defensive midfield positions — both are top-level pressers who win the ball high.',
    players=[
        ('FWD','Christian Pulisic',27,'Chelsea · 12 US goals in 2024 · takes penalties'),
        ('MID','Gio Reyna',23,'Borussia Dortmund · creative link play · 3 qualifying assists'),
        ('MID','Weston McKennie',27,'Juventus · box-to-box · 4 CONCACAF qualifying goals'),
        ('FWD','Ricardo Pepi',23,'PSV Eindhoven · 8 qualifying goals · physical target man'),
        ('MID','Tyler Adams',26,'Bournemouth · press engine · 96% pass accuracy in qualifying'),
    ],
    qrec='7W-3D-0L CONCACAF Final Round',
),
'Paraguay': dict(
    emoji='🇵🇾', code='py', rank='#63', todds='+25000',
    xg='1.1', gc='1.4', poss='46%', pass_acc='76%',
    h3='Counter-Punching Outsiders',
    p1='Paraguay qualified via the Copa América repechage route and arrive as genuine Group D underdogs. Their 5-3-2 system aims to absorb pressure and transition quickly — Antonio Sanabria (Real Betis) leads the line with physicality and holds play up effectively.',
    p2='Julio Enciso (Brighton) provides the spark from midfield, carrying in wide areas and arriving late into the box. Miguel Almirón (Newcastle) remains a key attacking threat off the right, even at 30. Paraguay\'s vulnerability is when they face sustained high press — they struggle to play out under pressure.',
    players=[
        ('FWD','Antonio Sanabria',29,'Real Betis · aerial threat · holds play up well'),
        ('MID','Julio Enciso',21,'Brighton · direct runner · 4 qualifying goals'),
        ('MID','Miguel Almirón',30,'Newcastle · right-side drive · pace and directness'),
        ('DEF','Gustavo Gómez',31,'Palmeiras · captain · organizer at centre-back'),
        ('DEF','Omar Alderete',27,'Getafe · physical defender · aerial duel winner'),
    ],
    qrec='4W-3D-3L CONMEBOL Qualifying',
),
'Australia': dict(
    emoji='🇦🇺', code='au', rank='#23', todds='+6000',
    xg='1.6', gc='1.1', poss='50%', pass_acc='79%',
    h3='Socceroos Aim for Another Deep Run',
    p1='Australia reached the WC2022 quarterfinal and arrive at 2026 with legitimate belief. Graham Arnold\'s 4-4-2 mid-block is disciplined defensively — Harry Souttar and Miloš Degenek hold the center-back partnership. Their transition game is rapid when Mitchell Duke wins the first ball.',
    p2='Mitchell Duke (Fagiano Okayama) remains the target man, winning aerial duels at elite rates. Martin Boyle (Panathinaikos) supplies pace and directness on the right wing. Mathew Leckie\'s experience at 33 gives them leadership in attacking areas when Australia push forward in transition.',
    players=[
        ('FWD','Mitchell Duke',33,'Fagiano Okayama · target striker · 68% aerial duel win rate'),
        ('FWD','Martin Boyle',31,'Panathinaikos · right-wing pace · 5 qualifying goals'),
        ('MID','Mathew Leckie',33,'Melbourne City · experience · direct runner'),
        ('DEF','Harry Souttar',25,'Stoke City · dominant centre-back · tall aerial threat'),
        ('GK','Mat Ryan',32,'AZ Alkmaar · experienced WC GK · shot-stopper'),
    ],
    qrec='5W-3D-2L AFC Third Round',
),
'Türkiye': dict(
    emoji='🇹🇷', code='tr', rank='#26', todds='+5000',
    xg='1.8', gc='0.9', poss='54%', pass_acc='82%',
    h3='Arda Güler\'s Moment Has Arrived',
    p1='Türkiye arrive at WC2026 as one of the most exciting dark horses, built around Real Madrid\'s Arda Güler. At 20, Güler is already delivering at club level — his combination of dribbling, shooting, and vision makes him one of the most dangerous number 10s in the tournament.',
    p2='Hakan Çalhanoğlu (Inter Milan) controls the tempo from deep midfield — his range of passing and set-piece delivery are elite. Kerem Aktürkoğlu (Galatasaray) provides the left-wing thrust. Türkiye conceded just 7 goals in 10 UEFA qualifying matches — their defensive structure is one of the best in Group D.',
    players=[
        ('MID','Arda Güler',20,'Real Madrid · number 10 · direct shooter · 7 club goals 2024'),
        ('MID','Hakan Çalhanoğlu',30,'Inter Milan · deep playmaker · elite set pieces'),
        ('FWD','Kerem Aktürkoğlu',26,'Galatasaray · left-wing · pace and directness'),
        ('FWD','Baris Alper Yilmaz',24,'Galatasaray · right-side · 4 qualifying goals'),
        ('DEF','Merih Demiral',26,'Al-Qadsiah · composed centre-back · aerial duels'),
    ],
    qrec='6W-2D-2L UEFA Qualifying Group D',
),
'Germany': dict(
    emoji='🇩🇪', code='de', rank='#12', todds='+900',
    xg='3.1', gc='0.7', poss='64%', pass_acc='88%',
    h3='Wirtz and Musiala Elevate Germany to Title Contenders',
    p1='Germany are widely regarded as WC2026\'s most dangerous attacking team. Jamal Musiala (Bayern Munich) and Florian Wirtz (Bayer Leverkusen) form the best creative midfield pairing in the tournament — both players carry with pace, shoot from distance, and link with movement that defenders struggle to track.',
    p2='Julian Nagelsmann\'s 4-2-3-1 uses Kai Havertz (Arsenal) as the false nine, dropping deep to create overloads while Musiala and Wirtz run beyond. Joshua Kimmich\'s distribution from deep is elite — 92% pass accuracy in qualifying. Germany averaged 3.1 xG per 90 across UEFA qualifying.',
    players=[
        ('MID','Florian Wirtz',22,'Bayer Leverkusen · creative genius · 12 Bundesliga goals 2024'),
        ('MID','Jamal Musiala',21,'Bayern Munich · carries past defenders · 15 club goals 2024'),
        ('FWD','Kai Havertz',26,'Arsenal · false nine · hold-up + movement · 14 PL goals 2024'),
        ('MID','Joshua Kimmich',29,'Bayern Munich · deep playmaker · 92% pass accuracy'),
        ('GK','Manuel Neuer',40,'Bayern Munich · commanding shot-stopper · sweeper keeper'),
    ],
    qrec='8W-1D-1L UEFA Qualifying Group A',
),
'Curaçao': dict(
    emoji='🇨🇼', code='cw', rank='#84', todds='+150000',
    xg='0.9', gc='1.8', poss='42%', pass_acc='72%',
    h3='Debut on the World Stage',
    p1='Curaçao make their World Cup debut — a historic moment for the Caribbean island nation. Their CONCACAF success relied on compact defending and set-piece effectiveness. Leandro Bacuna (Leeuwarden) is their most technical player and leads from midfield.',
    p2='Jürgen Locadia brings top-level experience from his time in the Premier League. Eloy Room (Columbus Crew) in goal is a genuine quality keeper who kept multiple clean sheets in CONCACAF qualifying. Curaçao will aim for organization and discipline against Group E giants.',
    players=[
        ('MID','Leandro Bacuna',32,'Leeuwarden · technical leader · set piece taker'),
        ('FWD','Jürgen Locadia',30,'Retired/Semi-pro · experienced forward · target man'),
        ('GK','Eloy Room',32,'Columbus Crew · shot-stopper · clean sheet specialist'),
        ('DEF','Cuco Martina',35,'ADO Den Haag · experienced right-back · defensive anchor'),
        ('FWD','Jurickson Profar',33,'San Diego Padres · athlete · dual sport · pace on counter'),
    ],
    qrec='3W-2D-5L CONCACAF Final Round',
),
'Ivory Coast': dict(
    emoji='🇨🇮', code='ci', rank='#19', todds='+10000',
    xg='1.7', gc='0.9', poss='53%', pass_acc='80%',
    h3='AFCON Champions Bring African Swagger',
    p1='Ivory Coast arrive as reigning AFCON champions, defeating Nigeria 2-1 in the final on home soil. Sébastien Haller leads the attack — his hold-up play and heading ability make him a unique threat. Amad Diallo (Manchester United) on the right wing is one of the most exciting 22-year-olds in the tournament.',
    p2='Franck Kessie provides the physical and technical balance in central midfield — 4 qualifying goals from box-to-box runs. Emerse Faé\'s 4-3-3 builds possession through wing play and uses Haller as the reference point. Simon on the left and Diallo on the right provide width and pace — defenders rarely get comfortable.',
    players=[
        ('FWD','Sébastien Haller',30,'Borussia Dortmund · AFCON top scorer · aerial dominance'),
        ('FWD','Amad Diallo',22,'Manchester United · right wing · pace · 1v1 direct'),
        ('MID','Franck Kessie',28,'Al-Ahli · box-to-box · 4 qualifying goals'),
        ('FWD','Nicolas Pépé',29,'Club Brugge · left wing · directness · set pieces'),
        ('DEF','Eric Bailly',30,'Stade Rennais · experienced centre-back · physical'),
    ],
    qrec='6W-2D-2L CAF Qualifying Group C',
),
'Ecuador': dict(
    emoji='🇪🇨', code='ec', rank='#34', todds='+12000',
    xg='1.6', gc='1.2', poss='50%', pass_acc='78%',
    h3='Young Guns Carrying Ecuador Forward',
    p1='Ecuador finished 4th in CONMEBOL qualifying — an impressive result that reflects the growth of their squad. Moisés Caicedo (Chelsea) is now one of the best defensive midfielders in the world, anchoring the structure and breaking up opposition play. Gonzalo Plata provides the left-side thrust.',
    p2='Enner Valencia at 36 remains the emotional leader and still dangerous from set pieces and second-ball situations. Piero Hincapié (Bayer Leverkusen) has developed into one of CONMEBOL\'s most reliable left-backs. Félix Sánchez\'s direct approach — press high, win it early, play quick — suits their personnel.',
    players=[
        ('MID','Moisés Caicedo',23,'Chelsea · elite defensive MF · ball-winner · 97% tackle rate'),
        ('FWD','Gonzalo Plata',23,'Nottingham Forest · left wing · pace · 4 qualifying goals'),
        ('FWD','Enner Valencia',36,'LDU Quito · veteran captain · aerial threat · set pieces'),
        ('DEF','Piero Hincapié',22,'Bayer Leverkusen · left-back · carrying ability'),
        ('MID','Jeremy Sarmiento',23,'Brighton · right-side pace · dribbling · direct'),
    ],
    qrec='7W-2D-1L CONMEBOL Qualifying',
),
'Netherlands': dict(
    emoji='🇳🇱', code='nl', rank='#7', todds='+700',
    xg='2.8', gc='0.6', poss='62%', pass_acc='87%',
    h3='Van Dijk and De Ligt Anchor Elite Defense',
    p1='The Netherlands arrive at WC2026 as legitimate title contenders. Ronald Koeman\'s 4-3-3 is built on an elite defensive foundation — Virgil van Dijk (Liverpool) and Matthijs de Ligt (Bayern Munich) are arguably the best center-back pair in the tournament. Xavi Simons (PSG) provides the creative spark from the right.',
    p2='Cody Gakpo (Liverpool) is their most dangerous attacker in tournament football — 3 WC2022 goals proved his big-game ability. Frenkie de Jong controls tempo from central midfield when fit. Memphis Depay provides experience and conversion quality from forward positions. The Dutch have beaten everyone they\'ve played in UEFA qualifying.',
    players=[
        ('FWD','Cody Gakpo',25,'Liverpool · left wing · 3 WC2022 goals · big-game player'),
        ('MID','Xavi Simons',22,'PSG · right inside forward · dribbling · shooting'),
        ('DEF','Virgil van Dijk',34,'Liverpool · captain · dominant · elite aerial'),
        ('MID','Frenkie de Jong',27,'Barcelona · deep playmaker · distribution'),
        ('FWD','Memphis Depay',30,'Corinthians · experienced striker · penalties'),
    ],
    qrec='8W-1D-1L UEFA Qualifying Group G',
),
'Japan': dict(
    emoji='🇯🇵', code='jp', rank='#17', todds='+5000',
    xg='2.0', gc='0.7', poss='56%', pass_acc='84%',
    h3='Blue Samurai Target Group Stage Exit Record',
    p1='Japan have evolved into a genuine international force. Hajime Moriyasu\'s 4-2-3-1 has beaten Germany and Spain in competitive matches. Ritsu Doan (Freiburg) and Junya Ito (Reims) provide pace on both wings. The Japanese press is organized and suffocating — they force turnovers by compressing space in deep blocks.',
    p2='Takumi Minamino (Monaco) links the midfield to the attack with clever movement. Hidemasa Morita (Sporting CP) anchors the defensive midfield — his discipline and positioning are central to Japan\'s defensive compactness. Daichi Kamada (Crystal Palace) offers creativity from the #10 role. Japan only conceded 5 goals in 12 AFC qualifying matches.',
    players=[
        ('FWD','Ritsu Doan',26,'Freiburg · right wing · shooting · 5 qualifying goals'),
        ('FWD','Junya Ito',31,'Reims · left wing · pace · direct'),
        ('MID','Daichi Kamada',28,'Crystal Palace · number 10 · link play'),
        ('MID','Hidemasa Morita',29,'Sporting CP · defensive MF · positioning · disruptor'),
        ('FWD','Takumi Minamino',30,'Monaco · second striker · movement'),
    ],
    qrec='9W-1D-0L AFC Third Round',
),
'Sweden': dict(
    emoji='🇸🇪', code='se', rank='#24', todds='+8000',
    xg='1.9', gc='0.8', poss='54%', pass_acc='81%',
    h3='Isak Leads Sweden Into the Modern Era',
    p1='Post-Zlatan Sweden have found a different identity — Alexander Isak (Newcastle) is the new focal point, and at 26 he\'s in the form of his life. His 24 Premier League goals in 2024-25 make him one of the most dangerous strikers in the tournament. Dejan Kulusevski (Spurs) provides the right-wing energy.',
    p2='Emil Forsberg (RB Leipzig) remains influential from the #10 role at 32. Victor Lindelöf (Manchester United) anchors the defense. Sweden\'s 4-4-2 is well-drilled under Janne Andersson — they conceded just 7 goals in 10 UEFA qualifying matches, suggesting real defensive organization.',
    players=[
        ('FWD','Alexander Isak',26,'Newcastle · striker · 24 PL goals 2024-25 · pace'),
        ('MID','Dejan Kulusevski',25,'Tottenham · right wing · direct · assists'),
        ('MID','Emil Forsberg',32,'RB Leipzig · creative · set pieces · experience'),
        ('DEF','Victor Lindelöf',30,'Manchester United · centre-back · organized'),
        ('FWD','Marcus Berg',36,'Al-Qadsiah · experienced striker · aerial threat'),
    ],
    qrec='6W-2D-2L UEFA Qualifying Group E',
),
'Tunisia': dict(
    emoji='🇹🇳', code='tn', rank='#33', todds='+20000',
    xg='1.4', gc='1.0', poss='48%', pass_acc='77%',
    h3='Eagles of Carthage Built on Defensive Solidity',
    p1='Tunisia qualified through a competitive CAF group and arrive as the most organized defensive team in Group F. Issam Jebali (OGC Nice) is their primary goal threat — his movement and pressing make him a constant nuisance for defenders.',
    p2='Hannibal Mejbri (Sevilla) provides creative energy from midfield at 22 — technically one of the most gifted young players in the African game. Wahbi Khazri remains influential in the final third. Tunisia\'s discipline and set-piece threat mean they can create moments against any opponent in a tight match.',
    players=[
        ('FWD','Issam Jebali',28,'OGC Nice · striker · pressing · movement'),
        ('MID','Hannibal Mejbri',22,'Sevilla · creative MF · dribbling · young talent'),
        ('MID','Wahbi Khazri',34,'Montpellier · experienced · set pieces · late runs'),
        ('DEF','Yassine Meriah',31,'Esperance · captain · center-back · headers'),
        ('MID','Ferjani Sassi',33,'Al-Taawon · box-to-box · defensive cover'),
    ],
    qrec='5W-3D-2L CAF Qualifying Group J',
),
'Belgium': dict(
    emoji='🇧🇪', code='be', rank='#3', todds='+1200',
    xg='3.0', gc='0.5', poss='62%', pass_acc='87%',
    h3='Golden Generation Has One Last Shot',
    p1='Belgium\'s golden generation — De Bruyne, Lukaku, Courtois — are entering what will likely be their final World Cup. Kevin De Bruyne (Manchester City) at 34 remains one of the best playmakers in world football. His range of passing and set-piece delivery are unmatched in this tournament.',
    p2='Romelu Lukaku (Napoli) leads the attack with physicality — 79 international goals make him Belgium\'s all-time scorer. Jeremy Doku (Manchester City) provides the right-wing threat with pace and directness. Thibaut Courtois (Real Madrid) is arguably the best keeper in this World Cup. Belgium average 3.0 xG/90 in qualifying — they can destroy any team in Group G.',
    players=[
        ('MID','Kevin De Bruyne',34,'Man City · playmaker · passing · set pieces · elite'),
        ('FWD','Romelu Lukaku',31,'Napoli · all-time top scorer · 79 goals · physical'),
        ('FWD','Jeremy Doku',23,'Man City · right wing · pace · direct 1v1'),
        ('GK','Thibaut Courtois',32,'Real Madrid · world-class keeper · shot-stopper'),
        ('MID','Amadou Onana',23,'Aston Villa · defensive MF · physique · aerial'),
    ],
    qrec='8W-1D-1L UEFA Qualifying Group B',
),
'Egypt': dict(
    emoji='🇪🇬', code='eg', rank='#36', todds='+12000',
    xg='1.5', gc='1.1', poss='50%', pass_acc='79%',
    h3='Salah Carries Egypt\'s World Cup Dream',
    p1='Mohamed Salah (Liverpool) is Egypt\'s entire attacking plan — at 34 he remains a top-5 player in the world and Egypt\'s only genuine world-class talent. His movement, finishing, and set-piece delivery give Egypt options no other team of similar ranking possesses.',
    p2='Omar Marmoush (Manchester City) has emerged as Salah\'s ideal partner — his pressing and movement complement Salah\'s tendency to drift inside. Essam El Hadary retired long ago; Ahmad El Shenawy is now the first-choice keeper. Egypt\'s defensive organization from 4-4-2 can frustrate, but they struggle against sustained high press.',
    players=[
        ('FWD','Mohamed Salah',34,'Liverpool · 60 Egypt goals · world-class · penalties'),
        ('FWD','Omar Marmoush',26,'Man City · pressing forward · 22 Bundesliga goals 2024'),
        ('MID','Emam Ashour',26,'Pyramids FC · creative link · assists'),
        ('DEF','Mohamed Elneny',32,'Fenerbahce · midfield shield · experience'),
        ('GK','Ahmad El Shenawy',33,'Al-Ahly · commanding keeper · shot-stopper'),
    ],
    qrec='6W-2D-2L CAF Qualifying Group D',
),
'Iran': dict(
    emoji='🇮🇷', code='ir', rank='#21', todds='+7000',
    xg='2.0', gc='0.8', poss='52%', pass_acc='80%',
    h3='Team Melli Armed With European Quality',
    p1='Iran arrive as one of Asia\'s strongest teams, having dominated AFC qualifying. Mehdi Taremi (Inter Milan) is one of the most complete strikers in the tournament — his movement, hold-up play, and finishing in tight spaces are elite. Sardar Azmoun (Fenerbahçe) provides the pace and direct threat alongside him.',
    p2='Alireza Jahanbakhsh (Club Brugge) on the right wing combines with overlapping full-backs to create width. Carlos Queiroz\'s 4-2-3-1 is tactically sophisticated — Iran can switch between possession and direct play seamlessly. They conceded just 4 goals in 12 AFC qualifying matches.',
    players=[
        ('FWD','Mehdi Taremi',32,'Inter Milan · hold-up play · finishing · penalties'),
        ('FWD','Sardar Azmoun',29,'Fenerbahce · pace · direct · aerial threat'),
        ('FWD','Alireza Jahanbakhsh',31,'Club Brugge · right wing · direct · assists'),
        ('MID','Saman Ghoddos',31,'AIK · creative · link play · set pieces'),
        ('DEF','Majid Hosseini',27,'Trabzonspor · centre-back · aerial · organized'),
    ],
    qrec='8W-2D-0L AFC Third Round',
),
'New Zealand': dict(
    emoji='🇳🇿', code='nz', rank='#97', todds='+100000',
    xg='0.8', gc='1.6', poss='41%', pass_acc='72%',
    h3='All Whites Making History',
    p1='New Zealand qualified through OFC and make their WC return as massive underdogs in Group G. Chris Wood (Nottingham Forest) is their sole player at consistent top-level club football — 17 Premier League goals in 2023-24 demonstrate his quality as a target striker.',
    p2='Marko Stamenic (Charlotte FC) provides the creative spark in midfield, while Logan Rogerson offers pace in attacking areas. New Zealand\'s 4-5-1 compact defensive block is their primary tool — they will sit deep and try to nick goals on the counter through Wood\'s hold-up and flick-ons.',
    players=[
        ('FWD','Chris Wood',32,'Nottingham Forest · target striker · 17 PL goals 2023-24'),
        ('MID','Marko Stamenic',23,'Charlotte FC · creative · assists · link play'),
        ('FWD','Logan Rogerson',22,'Columbus Crew · pace · runs behind · direct'),
        ('DEF','Liberato Cacace',23,'Empoli · left-back · carrying · crosses'),
        ('MID','Elijah Just',24,'FK Bodo/Glimt · industrious · pressing · energy'),
    ],
    qrec='6W-1D-1L OFC Nations Cup qualifying',
),
'Spain': dict(
    emoji='🇪🇸', code='es', rank='#1', todds='+400',
    xg='3.2', gc='0.4', poss='70%', pass_acc='92%',
    h3='European Champions Arrive as World Cup Favorites',
    p1='Spain are the FIFA #1 ranked team and defending European champions — their tiki-taka evolution under Luis de la Fuente is the most sophisticated possession system in world football. Pedri (Barcelona) and Gavi anchor the midfield with ball-playing excellence and pressing intensity.',
    p2='Álvaro Morata leads the attack with movement and linking play. Ferran Torres provides the right-side thrust and pressing. Spain averaged 70% possession and 3.2 xG/90 in UEFA qualifying — they dominated every match. Unai Simón (Athletic Club) is a commanding keeper. No team in this tournament plays better football consistently.',
    players=[
        ('MID','Pedri',23,'Barcelona · playmaker · dribbling · vision · elite'),
        ('MID','Gavi',21,'Barcelona · press trigger · ball-winner · assists'),
        ('FWD','Álvaro Morata',33,'Atletico Madrid · target striker · movement'),
        ('FWD','Ferran Torres',25,'Barcelona · right side · pressing · scoring'),
        ('GK','Unai Simón',27,'Athletic Club · sweeper-keeper · distribution'),
    ],
    qrec='9W-0D-1L UEFA Qualifying Group A',
),
'Cape Verde': dict(
    emoji='🇨🇻', code='cv', rank='#79', todds='+50000',
    xg='1.0', gc='1.3', poss='44%', pass_acc='74%',
    h3='Blue Sharks Defy the Odds Again',
    p1='Cape Verde continue to punch well above their weight in international football. Ryan Mendes and Garry Rodrigues are the most experienced attackers — both have played at decent European club levels. Their 5-3-2 system creates defensive solidity that makes them hard to break down.',
    p2='Jovane Cabral (Lazio) is their most technical player and provides individual moments of quality. Cape Verde\'s set-piece organization helped them qualify — they score and defend corners at a rate above their ranking would suggest. They won\'t be here just to make up the numbers.',
    players=[
        ('FWD','Jovane Cabral',26,'Lazio · creative forward · dribbling · individual quality'),
        ('FWD','Ryan Mendes',34,'Pacos Ferreira · experienced forward · set pieces'),
        ('FWD','Garry Rodrigues',33,'Pacos Ferreira · left side · pace · crosses'),
        ('DEF','Carlos Ponck',29,'Konyaspor · centre-back · captain · aerial'),
        ('DEF','Stopira',36,'Deportivo La Coruna · experienced · leader'),
    ],
    qrec='5W-2D-3L CAF Qualifying Group I',
),
'Saudi Arabia': dict(
    emoji='🇸🇦', code='sa', rank='#56', todds='+15000',
    xg='1.3', gc='1.2', poss='47%', pass_acc='76%',
    h3='Green Falcons Built on Domestic League Depth',
    p1='Saudi Arabia\'s investment in the Saudi Pro League has created a deeper squad than their 2022 World Cup team. Mohammed Al-Dawsari (Al-Hilal) remains their most dangerous creator — the man who scored THAT goal against Argentina in 2022. Salem Al-Dawsari offers width and directness.',
    p2='Saleh Al-Shehri (Al-Hilal) leads the attack with physicality and movement. Herve Renard\'s disciplined 4-4-2 defensive block was the foundation for the famous 2022 Argentina upset. Saudi Arabia will use that same organized defensive structure — they aim to frustrate and convert on the counter.',
    players=[
        ('FWD','Mohammed Al-Dawsari',32,'Al-Hilal · creative · scored vs Argentina 2022 · set pieces'),
        ('FWD','Saleh Al-Shehri',30,'Al-Hilal · target striker · movement · finals'),
        ('MID','Salem Al-Dawsari',32,'Al-Hilal · left wing · pace · directness'),
        ('DEF','Ali Al-Bulaihi',33,'Al-Hilal · centre-back · captain · experience'),
        ('MID','Sami Al-Najei',27,'Al-Hilal · right-back · overlapping · crosses'),
    ],
    qrec='5W-2D-3L AFC Third Round',
),
'Uruguay': dict(
    emoji='🇺🇾', code='uy', rank='#15', todds='+2500',
    xg='2.1', gc='0.9', poss='54%', pass_acc='81%',
    h3='Darwin Nuñez Leads Uruguay\'s Attack',
    p1='Uruguay\'s squad transitions from the Suárez-Cavani era to Darwin Nuñez (Liverpool) leading the line. At 25, Nuñez has the pace, physicality, and finishing combination to trouble any defence. Federico Valverde (Real Madrid) drives from midfield — one of the world\'s best box-to-box players.',
    p2='Ronald Araújo (Barcelona) and José María Giménez anchor a defense that conceded just 9 goals in CONMEBOL qualifying. Rodrigo Bentancur (Tottenham) provides the technical quality in the engine room. Uruguay\'s 4-3-3 presses aggressively and transitions quickly — the Garra Charrúa mentality remains their psychological foundation.',
    players=[
        ('FWD','Darwin Nuñez',25,'Liverpool · pace · power · finishing · direct'),
        ('MID','Federico Valverde',26,'Real Madrid · box-to-box · goals · energy · elite'),
        ('DEF','Ronald Araújo',25,'Barcelona · centre-back · aggressive · headers'),
        ('MID','Rodrigo Bentancur',27,'Tottenham · midfield quality · distribution'),
        ('FWD','Facundo Torres',24,'Orlando City · pace on right · direct · quick'),
    ],
    qrec='7W-2D-1L CONMEBOL Qualifying',
),
'France': dict(
    emoji='🇫🇷', code='fr', rank='#2', todds='+450',
    xg='2.9', gc='0.5', poss='60%', pass_acc='88%',
    h3='Les Bleus: The Deepest Squad at WC2026',
    p1='France arrive at WC2026 as the bookmakers\' joint-favorite alongside Spain. Kylian Mbappé (Real Madrid) is the best player in world football and the most dangerous forward in this tournament — his combination of pace, finishing, and big-game delivery is unmatched.',
    p2='Antoine Griezmann provides the creative link and pressing intensity in the #10 role at 35. Ousmane Dembélé (PSG) delivers the right-side direct threat and is one of the best 1v1 players alive. N\'Golo Kanté (Al-Ittihad) returns to provide the defensive midfield anchor. France conceded just 3 goals in 10 UEFA qualifying matches.',
    players=[
        ('FWD','Kylian Mbappé',27,'Real Madrid · best player in WC2026 · pace · finishing'),
        ('MID','Antoine Griezmann',35,'Atletico Madrid · link play · pressing · key passes'),
        ('FWD','Ousmane Dembélé',28,'PSG · right wing · direct · 1v1 · crosses'),
        ('MID','N\'Golo Kanté',35,'Al-Ittihad · midfield shield · ball recovery'),
        ('DEF','Jules Koundé',26,'Barcelona · right-back · pace · carrying ability'),
    ],
    qrec='8W-1D-1L UEFA Qualifying Group B',
),
'Senegal': dict(
    emoji='🇸🇳', code='sn', rank='#19', todds='+4000',
    xg='1.9', gc='0.7', poss='52%', pass_acc='80%',
    h3='Mané\'s Legacy, Pape Matar\'s Future',
    p1='Senegal are the Lions of Teranga and Africa\'s strongest team entering WC2026. While Sadio Mané (Al-Nassr) provides the experience and finishing quality at 34, it\'s Pape Matar Sarr (Tottenham) who defines their future — his energy, pressing, and late runs from midfield are dynamic.',
    p2='Ismaïla Sarr (Crystal Palace) provides the right-wing pace and directness. Kalidou Koulibaly (Al-Hilal) leads the defense with authority at 33. Senegal averaged 1.9 xG/90 in CAF qualifying and conceded just 7 goals in 10 matches. They are well-organized and defensively serious, while carrying genuine offensive quality.',
    players=[
        ('FWD','Sadio Mané',34,'Al-Nassr · experienced · finishing · set pieces · 35+ goals'),
        ('MID','Pape Matar Sarr',22,'Tottenham · energy · late runs · box-to-box · future star'),
        ('FWD','Ismaïla Sarr',26,'Crystal Palace · right wing · pace · directness'),
        ('DEF','Kalidou Koulibaly',33,'Al-Hilal · captain · commanding centre-back'),
        ('MID','Idrissa Gana Gueye',35,'Everton · midfield shield · experience · tackling'),
    ],
    qrec='6W-3D-1L CAF Qualifying Group B',
),
'Iraq': dict(
    emoji='🇮🇶', code='iq', rank='#68', todds='+40000',
    xg='1.1', gc='1.5', poss='45%', pass_acc='74%',
    h3='Lions of Mesopotamia On the World Stage',
    p1='Iraq qualified through the AFC process and make their return to the World Cup stage. Mohanad Ali is their most potent forward — direct, physical, and capable of scoring from limited chances. Ali Adnan provides the creative link from left midfield.',
    p2='Bashar Resan (Al-Talaba) is their defensive midfielder and captain — his experience organizing the defensive structure is vital. Iraq\'s 4-4-2 is compact and well-drilled but lacks the individual quality to compete with elite teams. Their best chance in Group I is creating moments from set pieces and counter-attacks.',
    players=[
        ('FWD','Mohanad Ali',28,'Al-Zawraa · direct striker · physical · target man'),
        ('MID','Ali Adnan',30,'Colorado Rapids · experienced left MF · deliveries'),
        ('MID','Bashar Resan',30,'Al-Talaba · captain · midfield shield · organization'),
        ('FWD','Amjad Attwan',27,'Al-Quwa Al-Jawiya · pace · counter-attack threat'),
        ('DEF','Ahmed Ibrahim',29,'Al-Zawraa · centre-back · aerial · experience'),
    ],
    qrec='5W-2D-3L AFC Third Round',
),
'Norway': dict(
    emoji='🇳🇴', code='no', rank='#10', todds='+2000',
    xg='2.4', gc='0.7', poss='56%', pass_acc='83%',
    h3='Haaland Gives Norway Genuine World Cup Ambition',
    p1='Norway\'s qualification is built around one of the most devastating strikers in football history — Erling Haaland (Manchester City). At 26, Haaland scored 17 goals in 10 UEFA qualifying matches, giving Norway a genuinely elite option. No defender in this World Cup has faced someone like him.',
    p2='Martin Ødegaard (Arsenal) at #10 is Norway\'s second world-class player — his technical quality and chance creation are at the highest level. Alexander Sørloth (Atletico Madrid) and Sander Berge provide the supporting cast. Norway\'s 4-3-3 presses with intensity when they have the lead, but they can play over the top to Haaland when they need a goal.',
    players=[
        ('FWD','Erling Haaland',26,'Man City · 17 qualifying goals · most feared striker alive'),
        ('MID','Martin Ødegaard',27,'Arsenal · playmaker · assists · vision · elite'),
        ('FWD','Alexander Sørloth',29,'Atletico Madrid · backup striker · physical · tall'),
        ('MID','Sander Berge',27,'Burnley · midfield engine · covering · distribution'),
        ('DEF','Kristoffer Ajer',26,'Brentford · right-back · carrying · pace'),
    ],
    qrec='8W-1D-1L UEFA Qualifying Group G',
),
'Argentina': dict(
    emoji='🇦🇷', code='ar', rank='#4', todds='+500',
    xg='2.7', gc='0.7', poss='58%', pass_acc='86%',
    h3='World Champions Defend the Crown',
    p1='Argentina arrive as defending World Champions, led by Lionel Messi (Inter Miami) in what will be his final World Cup appearance. At 38, Messi remains brilliant in tournament football — his vision, pressing contribution, and set-piece delivery define Argentina\'s attack even with reduced mobility.',
    p2='Julián Álvarez (Atletico Madrid) is the new primary striker — his WC2022 performances (4 goals) proved he delivers on the biggest stage. Enzo Fernández (Chelsea) controls the midfield tempo. Rodrigo De Paul provides the engine. Emiliano Martínez (Aston Villa) is one of the best keepers in this tournament. Argentina conceded just 9 goals in 18 CONMEBOL qualifying matches.',
    players=[
        ('FWD','Lionel Messi',38,'Inter Miami · last WC · vision · set pieces · still elite'),
        ('FWD','Julián Álvarez',25,'Atletico Madrid · 4 WC2022 goals · movement · pressing'),
        ('MID','Enzo Fernández',24,'Chelsea · midfield engine · passing · ball-winning'),
        ('MID','Rodrigo De Paul',30,'Atletico Madrid · energy · pressing · link play'),
        ('GK','Emiliano Martínez',32,'Aston Villa · penalty specialist · shot-stopper'),
    ],
    qrec='10W-2D-2L CONMEBOL Qualifying',
),
'Algeria': dict(
    emoji='🇩🇿', code='dz', rank='#31', todds='+10000',
    xg='1.5', gc='1.0', poss='50%', pass_acc='78%',
    h3='Desert Foxes Armed With European Stars',
    p1='Algeria qualified via CAF with a strong squad built predominantly from French Ligue 1 and Ligue 2. Riyad Mahrez (Al-Ahli) at 33 is their most recognizable name — his right-side creativity and goal threat in big games make him Algeria\'s primary attacking outlet.',
    p2='Ismael Bennacer (AC Milan) organizes from central midfield — his technical quality and reading of the game are genuinely elite level. Youcef Belaïli provides the left-side direct threat. Algeria\'s compact 4-3-3 can frustrate top teams — their strong collective spirit under coach Djamel Belmadi gives them belief in any match.',
    players=[
        ('FWD','Riyad Mahrez',33,'Al-Ahli · right wing · creativity · direct shots · leader'),
        ('MID','Ismael Bennacer',26,'AC Milan · central MF · passing · pressing · elite'),
        ('FWD','Youcef Belaïli',32,'Metz · left wing · direct · pace · 1v1'),
        ('FWD','Islam Slimani',35,'Brest · experienced striker · aerial · set pieces'),
        ('DEF','Ramy Bensebaini',29,'Borussia Dortmund · left-back · attacking runs · dead balls'),
    ],
    qrec='6W-2D-2L CAF Qualifying Group H',
),
'Austria': dict(
    emoji='🇦🇹', code='at', rank='#25', todds='+8000',
    xg='1.8', gc='0.9', poss='54%', pass_acc='82%',
    h3='Sabitzer\'s Austria Ready to Compete',
    p1='Austria qualify for successive World Cups with their most talented generation since the 1990s. Marcel Sabitzer (Borussia Dortmund) leads from midfield — his late runs, shooting, and defensive cover are box-to-box excellence. Christoph Baumgartner (RB Leipzig) provides the creativity from #10.',
    p2='Marko Arnautović brings experience and physical presence at 36, though his starting role is less certain. David Alaba (Real Madrid) — fitness permitting — is their most technically gifted defender. Ralf Rangnick\'s high-press system demands incredible work-rate from every player, and Austria\'s squad is uniquely suited to it.',
    players=[
        ('MID','Marcel Sabitzer',31,'Borussia Dortmund · box-to-box · goals from runs · leader'),
        ('MID','Christoph Baumgartner',25,'RB Leipzig · #10 · creative · direct shots'),
        ('FWD','Marko Arnautović',36,'Bologna · experienced striker · aerial · power'),
        ('DEF','David Alaba',32,'Real Madrid · technical · left-back or CB · distribution'),
        ('MID','Patrick Wimmer',23,'VfL Wolfsburg · right wing · pace · directness'),
    ],
    qrec='6W-3D-1L UEFA Qualifying Group F',
),
'Jordan': dict(
    emoji='🇯🇴', code='jo', rank='#87', todds='+60000',
    xg='0.9', gc='1.4', poss='43%', pass_acc='73%',
    h3='Nashama Making History',
    p1='Jordan make their World Cup debut — arguably the most historic moment for football in the Arab world since Qatar 2022. Hamza Al-Dardour is their most experienced forward, providing the physical hold-up and converting from limited chances. Their Asian Cup run to the final in 2023 showed what this team can achieve.',
    p2='Baha Faisal is the creative fulcrum — his technical quality and ability to link play is the best Jordan possesses. Their defensive 5-4-1 block will be tested severely against Argentina and Austria. Jordan\'s best hope lies in discipline and counter-attacks. Set pieces could yield results against more technically dominant opponents.',
    players=[
        ('FWD','Hamza Al-Dardour',31,'Al-Jazeera · experienced striker · hold-up · physical'),
        ('MID','Baha Faisal',28,'Al-Wahdat · creative · playmaker · most technical Jordan player'),
        ('MID','Ahmad Salah',30,'Al-Qaisumah · right-side · direct · crosses'),
        ('DEF','Khaled Al-Sahawneh',29,'Al-Faisaly · captain · centre-back · organizer'),
        ('GK','Yazeed Abulaila',27,'Al-Wahdat · confident keeper · shot-stopper'),
    ],
    qrec='5W-3D-2L AFC Third Round',
),
'Portugal': dict(
    emoji='🇵🇹', code='pt', rank='#6', todds='+900',
    xg='3.0', gc='0.5', poss='60%', pass_acc='87%',
    h3='Ronaldo\'s Final Act in World Cup History',
    p1='Portugal arrive with arguably their greatest-ever squad depth — and the question of whether Cristiano Ronaldo (Al-Nassr) starts remains one of the tournament\'s biggest storylines. Roberto Martínez built the team around young stars: Bruno Fernandes (Manchester United) as the creative hub and Rafael Leão (AC Milan) as the left-wing destroyer.',
    p2='Bernardo Silva (Manchester City) provides the technical excellence in midfield. Rúben Dias (Manchester City) anchors the defense with authority. Portugal\'s front three of Diogo Jota, Leão, and Fernandes creates one of the most dynamic attacks in the tournament — even without Ronaldo starting. 10 goals conceded in 10 UEFA qualifying games.',
    players=[
        ('FWD','Cristiano Ronaldo',41,'Al-Nassr · all-time scorer · set pieces · experience'),
        ('MID','Bruno Fernandes',30,'Man United · creative · set pieces · goals from MF'),
        ('FWD','Rafael Leão',25,'AC Milan · left wing · pace · 1v1 · directness'),
        ('MID','Bernardo Silva',30,'Man City · technical · press-resistant · key passes'),
        ('DEF','Rúben Dias',28,'Man City · dominant centre-back · composure · headers'),
    ],
    qrec='8W-1D-1L UEFA Qualifying Group J',
),
'DR Congo': dict(
    emoji='🇨🇩', code='cd', rank='#53', todds='+20000',
    xg='1.4', gc='1.2', poss='47%', pass_acc='76%',
    h3='Leopards Roar Back to the World Cup',
    p1='DR Congo return to the World Cup for the first time in decades — a historic achievement for Central African football. Yoane Wissa (Brentford) is their most explosive attacker — his pace and movement in behind defenders creates unique problems. Cédric Bakambu brings the tournament experience.',
    p2='Chancel Mbemba (Olympique Marseille) leads the defense — his experience at top European level gives DR Congo a solid defensive foundation. Théo Bongonda provides pace on the right wing. Their direct style suits their personnel and can create problems in transition. DR Congo\'s physicality and pace could surprise more technical opponents.',
    players=[
        ('FWD','Yoane Wissa',28,'Brentford · pace · movement · directness · finishing'),
        ('FWD','Cédric Bakambu',34,'Olympique Marseille · experienced forward · hold-up'),
        ('DEF','Chancel Mbemba',30,'Olympique Marseille · centre-back · experience · aerial'),
        ('FWD','Théo Bongonda',28,'Gent · right wing · pace · directness'),
        ('MID','Merveille Bope',25,'TP Mazembe · creative MF · assists · technical'),
    ],
    qrec='5W-3D-2L CAF Qualifying Group C',
),
'Uzbekistan': dict(
    emoji='🇺🇿', code='uz', rank='#72', todds='+40000',
    xg='1.1', gc='1.3', poss='44%', pass_acc='74%',
    h3='White Wolves Make Their Debut',
    p1='Uzbekistan make their World Cup debut in 2026 — a landmark moment for Central Asian football. Eldor Shomurodov (Roma) is their best-known player in European football, providing a genuine quality striker option at the top level. Jasur Yakhshiboev adds pace and creativity.',
    p2='Jaloliddin Masharipov is the technical leader in midfield — his dribbling and set-piece delivery give Uzbekistan moments of quality. Their qualifying run in AFC was impressive — they topped their group. The defensive record was mixed but their attacking potential surprised several stronger opponents in qualifying.',
    players=[
        ('FWD','Eldor Shomurodov',27,'Roma · experienced Europe-based striker · hold-up'),
        ('MID','Jaloliddin Masharipov',31,'Pakhtakor · creative · set pieces · technical leader'),
        ('FWD','Jasur Yakhshiboev',26,'Pakhtakor · pace · direct · scoring threat'),
        ('MID','Odil Ahmedov',34,'Pakhtakor · captain · experience · defensive MF'),
        ('DEF','Eldor Mukhitdinov',25,'AGMK · right-back · overlapping · crosses'),
    ],
    qrec='6W-2D-2L AFC Third Round',
),
'Colombia': dict(
    emoji='🇨🇴', code='co', rank='#9', todds='+2500',
    xg='2.2', gc='0.8', poss='56%', pass_acc='83%',
    h3='James and Díaz Lead Colombia\'s New Golden Era',
    p1='Colombia arrived at their Copa América 2024 final unbeaten — 28 matches without defeat — and WC2026 represents the next step. James Rodríguez (Rayo Vallecano) at 34 remains one of the most technically gifted midfielders alive. His range of passing and dead-ball delivery can unlock any defense.',
    p2='Luis Díaz (Liverpool) is the left-wing destroyer — his pace, directness, and finishing ability have made him one of the Premier League\'s best players. Richard Rios provides the midfield engine. Jhon Arias (Fluminense) offers the right-side threat. Colombia conceded just 8 goals in 18 CONMEBOL qualifying matches — they are well organized defensively too.',
    players=[
        ('MID','James Rodríguez',34,'Rayo Vallecano · playmaker · dead balls · experience · elite'),
        ('FWD','Luis Díaz',28,'Liverpool · left wing · pace · direct · PL quality'),
        ('MID','Richard Rios',25,'Fluminense · midfield engine · pressing · ball-winner'),
        ('FWD','Jhon Arias',27,'Fluminense · right wing · pace · direct · goals'),
        ('DEF','Dávinson Sánchez',28,'Galatasaray · centre-back · aerial · physical'),
    ],
    qrec='8W-4D-2L CONMEBOL Qualifying',
),
'England': dict(
    emoji='🏴󠁧󠁢󠁥󠁮󠁧󠁿', code='gb-eng', rank='#5', todds='+700',
    xg='2.8', gc='0.5', poss='61%', pass_acc='87%',
    h3='Three Lions Hunting First World Title Since 1966',
    p1='England arrive at WC2026 following Euro 2024 final heartbreak, with Gareth Southgate\'s squad arguably stronger than ever. Harry Kane (Bayern Munich) is the tournament\'s best traditional center-forward — his movement, link-up play, and penalty-box finishing combine with 91 England goals.',
    p2='Jude Bellingham (Real Madrid) at 22 is the most complete midfielder in English football history — his defensive work, attacking runs, and goals from late positions make him unique. Bukayo Saka (Arsenal) delivers consistent quality from the right. Phil Foden (Manchester City) brings creative flair. Jordan Pickford\'s experience in tournament football is a genuine asset.',
    players=[
        ('FWD','Harry Kane',31,'Bayern Munich · 91 England goals · movement · penalties'),
        ('MID','Jude Bellingham',22,'Real Madrid · box-to-box · goals · elite · complete'),
        ('FWD','Bukayo Saka',24,'Arsenal · right wing · consistent · assists · goals'),
        ('MID','Phil Foden',26,'Man City · creative · flair · final third quality'),
        ('GK','Jordan Pickford',31,'Everton · penalty specialist · experienced · WC keeper'),
    ],
    qrec='8W-2D-0L UEFA Qualifying Group C',
),
'Croatia': dict(
    emoji='🇭🇷', code='hr', rank='#14', todds='+4000',
    xg='1.8', gc='0.8', poss='54%', pass_acc='83%',
    h3='Modrić\'s Croatia Aim for One More Miracle',
    p1='Croatia reached the WC2022 semifinal and WC2018 final — their tournament experience is unmatched. Luka Modrić (Real Madrid) at 41 defies age with his ability to control tempo and create in tight spaces. Mateo Kovačić (Manchester City) is the midfield engine beside him.',
    p2='Andrej Kramarić (Hoffenheim) provides the goals — consistently Croatia\'s top scorer. Ivan Perišić\'s injury history remains a concern. Dominik Livaković is a quality keeper, proven in penalty shootouts. Croatia\'s 4-3-3 rotates intelligently and creates overloads through wide play — their tactical sophistication compensates for the ageing midfield.',
    players=[
        ('MID','Luka Modrić',41,'Real Madrid · living legend · tempo · vision · set pieces'),
        ('MID','Mateo Kovačić',31,'Man City · midfield engine · pressing · distribution'),
        ('FWD','Andrej Kramarić',34,'Hoffenheim · goals from runs · movement · clinical'),
        ('FWD','Bruno Petković',31,'Dinamo Zagreb · physical presence · hold-up play'),
        ('GK','Dominik Livaković',29,'Fenerbahce · penalties specialist · shot-stopper'),
    ],
    qrec='7W-2D-1L UEFA Qualifying Group D',
),
'Ghana': dict(
    emoji='🇬🇭', code='gh', rank='#60', todds='+20000',
    xg='1.4', gc='1.2', poss='48%', pass_acc='76%',
    h3='Black Stars Revived Under New Leadership',
    p1='Ghana rebuild after their disappointing WC2022 exit, with Mohammed Kudus (West Ham) now the central figure. At 24, Kudus is the most dynamic player Ghana has produced since Michael Essien — his energy, dribbling, and late runs from midfield create problems at the highest level.',
    p2='Thomas Partey (Arsenal) provides the defensive midfield anchor when fit — his experience is vital. Jordan Ayew (Crystal Palace) leads the attack with physical presence and link-up play. Lawrence Ati-Zigi is an underrated keeper at championship level. Ghana\'s 4-3-3 aims to counter-press and create through quick transitions.',
    players=[
        ('MID','Mohammed Kudus',24,'West Ham · dynamic · dribbling · goals · best Ghana player'),
        ('MID','Thomas Partey',31,'Arsenal · midfield shield · experience · distribution'),
        ('FWD','Jordan Ayew',33,'Crystal Palace · experienced forward · link play · work rate'),
        ('FWD','Antoine Semenyo',24,'Bournemouth · right wing · pace · directness'),
        ('GK','Lawrence Ati-Zigi',27,'St. Gallen · consistent keeper · shot-stopper'),
    ],
    qrec='5W-3D-2L CAF Qualifying Group I',
),
'Panama': dict(
    emoji='🇵🇦', code='pa', rank='#74', todds='+60000',
    xg='0.9', gc='1.3', poss='43%', pass_acc='73%',
    h3='Los Canaleros Prove Their Worth Again',
    p1='Panama made history with their 2018 World Cup debut and return in 2026 as CONCACAF\'s fifth qualifier. Ismael Díaz provides the attacking creativity — his movement between the lines causes problems for organized defenses.',
    p2='Alberto Quintero brings experience and directness from wide areas. Eric Davis anchors the defensive midfield and provides the organizational core. Panama\'s 5-3-2 is well-drilled and defensively compact — they aim to stay tight and create from set pieces and counter-attacks. Beating Ghana in Group L would be a genuine result.',
    players=[
        ('FWD','Ismael Díaz',25,'Girondins Bordeaux · creative forward · movement · link play'),
        ('MID','Alberto Quintero',32,'CD Marathón · experienced · right side · directness'),
        ('MID','Eric Davis',28,'CD Universitario · defensive MF · captain · organizer'),
        ('FWD','Valentín Pimentel',26,'Deportivo La Guaira · left wing · pace · direct'),
        ('DEF','Harold Cummings',27,'San Jose Earthquakes · centre-back · physical · aerial'),
    ],
    qrec='4W-2D-4L CONCACAF Final Round',
),
}

# ── Head-to-head lookup ───────────────────────────────────────────────────────
H2H = {
    ('United States','Paraguay'): 'USA lead all-time 5–2. No prior World Cup meetings. Last friendly: USA 1–0 Paraguay in 2021.',
    ('Australia','Türkiye'): 'Series level at 3–3. No prior World Cup meetings. Last meeting: 1–1 friendly in 2021.',
    ('United States','Australia'): 'USA lead 3–1. World Cup meeting: USA 3–0 Australia in 2006 group stage.',
    ('Türkiye','Paraguay'): 'Türkiye lead all-time 2–0. No World Cup meetings. Last friendly: 0–0 in 2018.',
    ('Türkiye','United States'): 'Türkiye lead 2–1. No World Cup meetings. Last friendly: USA 2–1 Türkiye in 2010.',
    ('Paraguay','Australia'): 'Paraguay lead 3–0. No World Cup meetings. Last friendly: Paraguay 2–0 Australia in 2014.',
    ('Ivory Coast','Ecuador'): 'Ivory Coast lead 2–1 all-time. No World Cup meetings.',
    ('Germany','Ivory Coast'): 'Germany lead 2–1. Last meeting: 2–1 Germany win in 2010 World Cup group stage.',
    ('Ecuador','Curaçao'): 'No previous meetings recorded. Curaçao debut at senior level.',
    ('Curaçao','Ivory Coast'): 'No previous senior meetings. First competitive match between the nations.',
    ('Ecuador','Germany'): 'Germany lead 4–0 all-time. World Cup meeting: Germany 3–0 Ecuador in 2006 group stage.',
    ('Netherlands','Japan'): 'Netherlands lead 3–1. World Cup meeting: Netherlands 0–1 Japan in WC2022 round of 16.',
    ('Sweden','Tunisia'): 'Sweden lead 2–0. No World Cup meetings. Last friendly: 1–1 in 2022.',
    ('Netherlands','Sweden'): 'Netherlands lead 8–3–5. Last World Cup meeting: Netherlands 0–0 Sweden in 2006.',
    ('Tunisia','Japan'): 'Japan lead 3–1. No prior World Cup meetings.',
    ('Japan','Sweden'): 'Japan lead 2–1. No prior World Cup meetings since 2002.',
    ('Tunisia','Netherlands'): 'Netherlands lead 4–0. World Cup meeting: Netherlands 1–1 Tunisia in 1998.',
    ('Belgium','Egypt'): 'Belgium lead 2–0. No World Cup meetings. Last friendly: Belgium 3–0 Egypt in 2022.',
    ('Iran','New Zealand'): 'Iran lead 3–0. No World Cup meetings. First competitive meeting between nations.',
    ('Belgium','Iran'): 'Belgium lead 3–1. No World Cup meetings. Last friendly: Belgium 2–0 Iran in 2023.',
    ('New Zealand','Egypt'): 'No competitive meetings. One friendly recorded — 1–1 in 2018.',
    ('Egypt','Iran'): 'Iran lead 2–1. Both eliminated early in WC2018. No WC meetings head-to-head.',
    ('Belgium','New Zealand'): 'Belgium lead 4–0 all-time. WC1990 meeting: Belgium 2–0 New Zealand.',
    ('Spain','Cape Verde'): 'Spain lead 1–0. Only meeting: 2–0 Spain win in 2022 UEFA Nations League play-off.',
    ('Saudi Arabia','Uruguay'): 'Uruguay lead 3–0. No World Cup meetings since 1970. Last friendly: 1–0 Uruguay in 2023.',
    ('Spain','Saudi Arabia'): 'Spain lead 4–0. No World Cup meetings. Last friendly: Spain 3–1 Saudi Arabia in 2022.',
    ('Uruguay','Cape Verde'): 'No competitive meetings. Uruguay have never played Cape Verde.',
    ('Cape Verde','Saudi Arabia'): 'Saudi Arabia lead 1–0. First World Cup meeting. Only met once before in 2022.',
    ('Uruguay','Spain'): 'Uruguay lead 4–3 historically. World Cup: 0–1 Spain in 2010 semifinal.',
    ('France','Senegal'): 'France lead 6–0 all-time. World Cup meeting: France 2–1 Senegal in WC2002 group stage.',
    ('Iraq','Norway'): 'Norway lead 2–1. No World Cup meetings. Last friendly: 1–1 in 2021.',
    ('France','Iraq'): 'France lead 2–0. No World Cup meetings. Last friendly: France 2–0 Iraq in 2015.',
    ('Norway','Senegal'): 'Norway lead 2–1. No World Cup meetings. Last friendly: 1–0 Norway in 2022.',
    ('Norway','France'): 'France lead 7–4. No World Cup meetings. Last competitive match: 1–1 UEFA Nations League 2020.',
    ('Senegal','Iraq'): 'Senegal lead 1–0. No World Cup meetings. First competitive meeting between nations.',
    ('Argentina','Algeria'): 'Argentina lead 3–1. No World Cup meetings. Last friendly: 3–1 Argentina in 2022.',
    ('Austria','Jordan'): 'Austria lead 2–0. No competitive meetings prior to WC2026.',
    ('Argentina','Austria'): 'Argentina lead 7–2. World Cup: Argentina beat Austria 1–0 in 1998 round of 16.',
    ('Jordan','Algeria'): 'Algeria lead 2–1. No World Cup meetings.',
    ('Jordan','Argentina'): 'Argentina lead 3–0. Jordan debut on the World Cup stage.',
    ('Algeria','Austria'): 'Austria lead 2–1. No World Cup meetings. First competitive meeting since 1994 WC qualification.',
    ('Portugal','DR Congo'): 'Portugal lead 3–0. No World Cup meetings. Last friendly: Portugal 3–0 DR Congo in 2023.',
    ('Uzbekistan','Colombia'): 'No competitive meetings. Colombia lead 1–0 in single friendly in 2019.',
    ('Portugal','Uzbekistan'): 'No competitive meetings. Portugal first played Uzbekistan in a 2023 friendly, won 1–0.',
    ('Colombia','DR Congo'): 'Colombia lead 2–0. No World Cup meetings. Last friendly: Colombia 1–0 DR Congo in 2022.',
    ('Colombia','Portugal'): 'Portugal lead 3–1. World Cup meeting: Portugal 1–0 Colombia in WC2014 group stage.',
    ('DR Congo','Uzbekistan'): 'No competitive meetings. First time these nations have met at senior level.',
    ('England','Croatia'): 'England lead 8–6 all-time. World Cup: England 2–1 Croatia in 2018 semifinal (Trippier free kick).',
    ('Ghana','Panama'): 'Ghana lead 1–0. Only meeting: 2–0 Ghana in 2022 friendly. First World Cup encounter.',
    ('England','Ghana'): 'England lead 5–1. No World Cup meetings. Last friendly: England 3–0 Ghana in 2011.',
    ('Panama','Croatia'): 'Croatia lead 2–0. First World Cup meeting. Last friendly: 1–0 Croatia in 2020.',
    ('Panama','England'): 'England lead 1–0 (only meeting). World Cup: England 6–1 Panama in 2018 group stage.',
    ('Croatia','Ghana'): 'Croatia lead 2–1. World Cup: Croatia 1–0 Ghana in 2006, drew 1–1 in 2022.',
}

# ── Simple match data (authoritative schedule) ────────────────────────────────
SIMPLE = [
# GROUP D
dict(slug='usa-paraguay', home='United States', away='Paraguay', hc='us', ac='py',
     group='D', md=1, date='2026-06-12', time='9:00 PM ET',
     venue='Los Angeles Stadium, Inglewood, CA', hp=58, dp=22, ap=20,
     hml='-165', dml='+270', aml='+430', ai_pick='USA Win',
     ou='2.5', photo='1430232324554-8f4aebd06683', jdt='2026-06-12T21:00:00-07:00'),
dict(slug='australia-turkey', home='Australia', away='Türkiye', hc='au', ac='tr',
     group='D', md=1, date='2026-06-13', time='12:00 AM ET',
     venue='BC Place, Vancouver, Canada', hp=34, dp=28, ap=38,
     hml='+210', dml='+230', aml='+155', ai_pick='Türkiye Win',
     ou='2.5', photo='1569531955323-33c6b2dca44b', jdt='2026-06-13T00:00:00-07:00'),
dict(slug='usa-australia', home='United States', away='Australia', hc='us', ac='au',
     group='D', md=2, date='2026-06-19', time='3:00 PM ET',
     venue='Lumen Field, Seattle, WA', hp=52, dp=24, ap=24,
     hml='-130', dml='+260', aml='+350', ai_pick='USA Win',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-19T15:00:00-07:00'),
dict(slug='turkey-paraguay', home='Türkiye', away='Paraguay', hc='tr', ac='py',
     group='D', md=2, date='2026-06-19', time='11:00 PM ET',
     venue="Levi's Stadium, Santa Clara, CA", hp=54, dp=24, ap=22,
     hml='-145', dml='+270', aml='+380', ai_pick='Türkiye Win',
     ou='2.5', photo='1556816214-6d16c62fbbf6', jdt='2026-06-19T23:00:00-07:00'),
dict(slug='turkey-usa', home='Türkiye', away='United States', hc='tr', ac='us',
     group='D', md=3, date='2026-06-25', time='10:00 PM ET',
     venue='Los Angeles Stadium, Inglewood, CA', hp=32, dp=28, ap=40,
     hml='+240', dml='+230', aml='+140', ai_pick='USA Win or Draw',
     ou='2.5', photo='1430232324554-8f4aebd06683', jdt='2026-06-25T22:00:00-07:00'),
dict(slug='paraguay-australia', home='Paraguay', away='Australia', hc='py', ac='au',
     group='D', md=3, date='2026-06-25', time='10:00 PM ET',
     venue="Levi's Stadium, Santa Clara, CA", hp=28, dp=26, ap=46,
     hml='+310', dml='+240', aml='+115', ai_pick='Australia Win',
     ou='2.5', photo='1599158150601-1417ebbaafdd', jdt='2026-06-25T22:00:00-07:00'),
# GROUP E — germany-curacao already built, skip
dict(slug='ivorycoast-ecuador', home='Ivory Coast', away='Ecuador', hc='ci', ac='ec',
     group='E', md=1, date='2026-06-14', time='7:00 PM ET',
     venue='Lincoln Financial Field, Philadelphia, PA', hp=44, dp=26, ap=30,
     hml='-115', dml='+240', aml='+310', ai_pick='Ivory Coast Win',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-14T19:00:00-04:00'),
dict(slug='germany-ivorycoast', home='Germany', away='Ivory Coast', hc='de', ac='ci',
     group='E', md=2, date='2026-06-20', time='4:00 PM ET',
     venue='BMO Field, Toronto, Canada', hp=55, dp=23, ap=22,
     hml='-150', dml='+270', aml='+390', ai_pick='Germany Win',
     ou='2.5', photo='1489944440615-453fc2b6a9a9', jdt='2026-06-20T16:00:00-04:00'),
dict(slug='ecuador-curacao', home='Ecuador', away='Curaçao', hc='ec', ac='cw',
     group='E', md=2, date='2026-06-20', time='8:00 PM ET',
     venue='Arrowhead Stadium, Kansas City, MO', hp=72, dp=17, ap=11,
     hml='-280', dml='+370', aml='+750', ai_pick='Ecuador Win',
     ou='2.5', photo='1651421738652-12124d47c917', jdt='2026-06-20T20:00:00-04:00'),
dict(slug='curacao-ivorycoast', home='Curaçao', away='Ivory Coast', hc='cw', ac='ci',
     group='E', md=3, date='2026-06-25', time='4:00 PM ET',
     venue='Lincoln Financial Field, Philadelphia, PA', hp=15, dp=20, ap=65,
     hml='+500', dml='+310', aml='-210', ai_pick='Ivory Coast Win',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-25T16:00:00-04:00'),
dict(slug='ecuador-germany', home='Ecuador', away='Germany', hc='ec', ac='de',
     group='E', md=3, date='2026-06-25', time='4:00 PM ET',
     venue='MetLife Stadium, East Rutherford, NJ', hp=22, dp=26, ap=52,
     hml='+340', dml='+240', aml='-125', ai_pick='Germany Win',
     ou='2.5', photo='1556816214-6d16c62fbbf6', jdt='2026-06-25T16:00:00-04:00'),
# GROUP F — netherlands-japan already built, skip
dict(slug='sweden-tunisia', home='Sweden', away='Tunisia', hc='se', ac='tn',
     group='F', md=1, date='2026-06-14', time='10:00 PM ET',
     venue='Estadio BBVA, Monterrey, Mexico', hp=46, dp=28, ap=26,
     hml='-120', dml='+250', aml='+330', ai_pick='Sweden Win or Draw',
     ou='2.5', photo='1705593973313-75de7bf95b56', jdt='2026-06-14T22:00:00-04:00'),
dict(slug='netherlands-sweden', home='Netherlands', away='Sweden', hc='nl', ac='se',
     group='F', md=2, date='2026-06-20', time='1:00 PM ET',
     venue='NRG Stadium, Houston, TX', hp=58, dp=22, ap=20,
     hml='-175', dml='+290', aml='+440', ai_pick='Netherlands Win',
     ou='2.5', photo='1569531955323-33c6b2dca44b', jdt='2026-06-20T13:00:00-04:00'),
dict(slug='tunisia-japan', home='Tunisia', away='Japan', hc='tn', ac='jp',
     group='F', md=2, date='2026-06-20', time='12:00 AM ET',
     venue='Estadio BBVA, Monterrey, Mexico', hp=28, dp=28, ap=44,
     hml='+280', dml='+240', aml='-115', ai_pick='Japan Win',
     ou='2.5', photo='1705593973313-75de7bf95b56', jdt='2026-06-20T00:00:00-06:00'),
dict(slug='japan-sweden', home='Japan', away='Sweden', hc='jp', ac='se',
     group='F', md=3, date='2026-06-25', time='7:00 PM ET',
     venue='AT&T Stadium, Arlington, TX', hp=42, dp=28, ap=30,
     hml='+110', dml='+240', aml='+260', ai_pick='Japan Win or Draw',
     ou='2.5', photo='1569531955323-33c6b2dca44b', jdt='2026-06-25T19:00:00-04:00'),
dict(slug='tunisia-netherlands', home='Tunisia', away='Netherlands', hc='tn', ac='nl',
     group='F', md=3, date='2026-06-25', time='7:00 PM ET',
     venue='Arrowhead Stadium, Kansas City, MO', hp=16, dp=22, ap=62,
     hml='+480', dml='+290', aml='-195', ai_pick='Netherlands Win',
     ou='2.5', photo='1651421738652-12124d47c917', jdt='2026-06-25T19:00:00-04:00'),
# GROUP G — belgium-newzealand not yet built, include here
dict(slug='belgium-egypt', home='Belgium', away='Egypt', hc='be', ac='eg',
     group='G', md=1, date='2026-06-15', time='3:00 PM ET',
     venue='Lumen Field, Seattle, WA', hp=66, dp=20, ap=14,
     hml='-220', dml='+310', aml='+580', ai_pick='Belgium Win',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-15T15:00:00-07:00'),
dict(slug='iran-newzealand', home='Iran', away='New Zealand', hc='ir', ac='nz',
     group='G', md=1, date='2026-06-15', time='9:00 PM ET',
     venue='Los Angeles Stadium, Inglewood, CA', hp=68, dp=18, ap=14,
     hml='-240', dml='+340', aml='+620', ai_pick='Iran Win',
     ou='2.5', photo='1430232324554-8f4aebd06683', jdt='2026-06-15T21:00:00-07:00'),
dict(slug='belgium-iran', home='Belgium', away='Iran', hc='be', ac='ir',
     group='G', md=2, date='2026-06-21', time='3:00 PM ET',
     venue='Los Angeles Stadium, Inglewood, CA', hp=62, dp=22, ap=16,
     hml='-195', dml='+290', aml='+500', ai_pick='Belgium Win',
     ou='2.5', photo='1430232324554-8f4aebd06683', jdt='2026-06-21T15:00:00-07:00'),
dict(slug='newzealand-egypt', home='New Zealand', away='Egypt', hc='nz', ac='eg',
     group='G', md=2, date='2026-06-21', time='9:00 PM ET',
     venue='BC Place, Vancouver, Canada', hp=28, dp=28, ap=44,
     hml='+280', dml='+240', aml='-120', ai_pick='Egypt Win',
     ou='2.5', photo='1569531955323-33c6b2dca44b', jdt='2026-06-21T21:00:00-07:00'),
dict(slug='belgium-newzealand', home='Belgium', away='New Zealand', hc='be', ac='nz',
     group='G', md=3, date='2026-06-26', time='11:00 PM ET',
     venue='Mercedes-Benz Stadium, Atlanta, GA', hp=84, dp=12, ap=4,
     hml='-420', dml='+550', aml='+1100', ai_pick='Belgium Win',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-26T23:00:00-04:00'),
dict(slug='egypt-iran', home='Egypt', away='Iran', hc='eg', ac='ir',
     group='G', md=3, date='2026-06-26', time='11:00 PM ET',
     venue='Lumen Field, Seattle, WA', hp=30, dp=30, ap=40,
     hml='+240', dml='+230', aml='+135', ai_pick='Iran Win or Draw',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-26T23:00:00-07:00'),
# GROUP H — spain-capeverde already built, skip
dict(slug='saudiarabia-uruguay', home='Saudi Arabia', away='Uruguay', hc='sa', ac='uy',
     group='H', md=1, date='2026-06-15', time='6:00 PM ET',
     venue='Hard Rock Stadium, Miami, FL', hp=22, dp=24, ap=54,
     hml='+340', dml='+250', aml='-140', ai_pick='Uruguay Win',
     ou='2.5', photo='1599158150601-1417ebbaafdd', jdt='2026-06-15T18:00:00-04:00'),
dict(slug='spain-saudiarabia', home='Spain', away='Saudi Arabia', hc='es', ac='sa',
     group='H', md=2, date='2026-06-21', time='12:00 PM ET',
     venue='Mercedes-Benz Stadium, Atlanta, GA', hp=76, dp=14, ap=10,
     hml='-360', dml='+450', aml='+900', ai_pick='Spain Win & Over 2.5',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-21T12:00:00-04:00'),
dict(slug='uruguay-capeverde', home='Uruguay', away='Cape Verde', hc='uy', ac='cv',
     group='H', md=2, date='2026-06-21', time='6:00 PM ET',
     venue='Hard Rock Stadium, Miami, FL', hp=70, dp=18, ap=12,
     hml='-260', dml='+360', aml='+680', ai_pick='Uruguay Win',
     ou='2.5', photo='1599158150601-1417ebbaafdd', jdt='2026-06-21T18:00:00-04:00'),
dict(slug='capeverde-saudiarabia', home='Cape Verde', away='Saudi Arabia', hc='cv', ac='sa',
     group='H', md=3, date='2026-06-26', time='8:00 PM ET',
     venue='NRG Stadium, Houston, TX', hp=30, dp=28, ap=42,
     hml='+260', dml='+240', aml='+120', ai_pick='Saudi Arabia Win or Draw',
     ou='2.5', photo='1651421738652-12124d47c917', jdt='2026-06-26T20:00:00-04:00'),
dict(slug='uruguay-spain', home='Uruguay', away='Spain', hc='uy', ac='es',
     group='H', md=3, date='2026-06-26', time='8:00 PM ET',
     venue='Estadio Akron, Guadalajara, Mexico', hp=20, dp=24, ap=56,
     hml='+390', dml='+250', aml='-155', ai_pick='Spain Win',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-26T20:00:00-06:00'),
# GROUP I
dict(slug='france-senegal', home='France', away='Senegal', hc='fr', ac='sn',
     group='I', md=1, date='2026-06-16', time='3:00 PM ET',
     venue='MetLife Stadium, East Rutherford, NJ', hp=62, dp=22, ap=16,
     hml='-210', dml='+300', aml='+520', ai_pick='France Win',
     ou='2.5', photo='1556816214-6d16c62fbbf6', jdt='2026-06-16T15:00:00-04:00'),
dict(slug='iraq-norway', home='Iraq', away='Norway', hc='iq', ac='no',
     group='I', md=1, date='2026-06-16', time='6:00 PM ET',
     venue='Gillette Stadium, Foxborough, MA', hp=16, dp=24, ap=60,
     hml='+480', dml='+270', aml='-190', ai_pick='Norway Win',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-16T18:00:00-04:00'),
dict(slug='france-iraq', home='France', away='Iraq', hc='fr', ac='iq',
     group='I', md=2, date='2026-06-22', time='5:00 PM ET',
     venue='Lincoln Financial Field, Philadelphia, PA', hp=78, dp=14, ap=8,
     hml='-400', dml='+480', aml='+950', ai_pick='France Win & Over 2.5',
     ou='2.5', photo='1705593973313-75de7bf95b56', jdt='2026-06-22T17:00:00-04:00'),
dict(slug='norway-senegal', home='Norway', away='Senegal', hc='no', ac='sn',
     group='I', md=2, date='2026-06-22', time='8:00 PM ET',
     venue='MetLife Stadium, East Rutherford, NJ', hp=42, dp=28, ap=30,
     hml='-105', dml='+240', aml='+290', ai_pick='Norway Win or Draw',
     ou='2.5', photo='1556816214-6d16c62fbbf6', jdt='2026-06-22T20:00:00-04:00'),
dict(slug='norway-france', home='Norway', away='France', hc='no', ac='fr',
     group='I', md=3, date='2026-06-26', time='3:00 PM ET',
     venue='Gillette Stadium, Foxborough, MA', hp=26, dp=26, ap=48,
     hml='+290', dml='+260', aml='-115', ai_pick='France Win',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-26T15:00:00-04:00'),
dict(slug='senegal-iraq', home='Senegal', away='Iraq', hc='sn', ac='iq',
     group='I', md=3, date='2026-06-26', time='3:00 PM ET',
     venue='BMO Field, Toronto, Canada', hp=64, dp=20, ap=16,
     hml='-215', dml='+310', aml='+540', ai_pick='Senegal Win',
     ou='2.5', photo='1569531955323-33c6b2dca44b', jdt='2026-06-26T15:00:00-04:00'),
# GROUP J
dict(slug='argentina-algeria', home='Argentina', away='Algeria', hc='ar', ac='dz',
     group='J', md=1, date='2026-06-16', time='9:00 PM ET',
     venue='Arrowhead Stadium, Kansas City, MO', hp=66, dp=20, ap=14,
     hml='-230', dml='+320', aml='+580', ai_pick='Argentina Win',
     ou='2.5', photo='1599158150601-1417ebbaafdd', jdt='2026-06-16T21:00:00-04:00'),
dict(slug='austria-jordan', home='Austria', away='Jordan', hc='at', ac='jo',
     group='J', md=1, date='2026-06-17', time='12:00 AM ET',
     venue="Levi's Stadium, Santa Clara, CA", hp=64, dp=20, ap=16,
     hml='-210', dml='+310', aml='+530', ai_pick='Austria Win',
     ou='2.5', photo='1489944440615-453fc2b6a9a9', jdt='2026-06-17T00:00:00-07:00'),
dict(slug='argentina-austria', home='Argentina', away='Austria', hc='ar', ac='at',
     group='J', md=2, date='2026-06-22', time='1:00 PM ET',
     venue='AT&T Stadium, Arlington, TX', hp=60, dp=22, ap=18,
     hml='-185', dml='+290', aml='+460', ai_pick='Argentina Win',
     ou='2.5', photo='1651421738652-12124d47c917', jdt='2026-06-22T13:00:00-04:00'),
dict(slug='jordan-algeria', home='Jordan', away='Algeria', hc='jo', ac='dz',
     group='J', md=2, date='2026-06-22', time='11:00 PM ET',
     venue="Levi's Stadium, Santa Clara, CA", hp=24, dp=28, ap=48,
     hml='+310', dml='+240', aml='-110', ai_pick='Algeria Win',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-22T23:00:00-07:00'),
dict(slug='jordan-argentina', home='Jordan', away='Argentina', hc='jo', ac='ar',
     group='J', md=3, date='2026-06-27', time='10:00 PM ET',
     venue='AT&T Stadium, Arlington, TX', hp=10, dp=18, ap=72,
     hml='+700', dml='+380', aml='-310', ai_pick='Argentina Win',
     ou='2.5', photo='1651421738652-12124d47c917', jdt='2026-06-27T22:00:00-04:00'),
dict(slug='algeria-austria', home='Algeria', away='Austria', hc='dz', ac='at',
     group='J', md=3, date='2026-06-27', time='10:00 PM ET',
     venue='Arrowhead Stadium, Kansas City, MO', hp=32, dp=28, ap=40,
     hml='+220', dml='+235', aml='+135', ai_pick='Austria Win or Draw',
     ou='2.5', photo='1489944440615-453fc2b6a9a9', jdt='2026-06-27T22:00:00-04:00'),
# GROUP K
dict(slug='portugal-drc', home='Portugal', away='DR Congo', hc='pt', ac='cd',
     group='K', md=1, date='2026-06-17', time='1:00 PM ET',
     venue='NRG Stadium, Houston, TX', hp=68, dp=18, ap=14,
     hml='-245', dml='+340', aml='+620', ai_pick='Portugal Win',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-17T13:00:00-04:00'),
dict(slug='uzbekistan-colombia', home='Uzbekistan', away='Colombia', hc='uz', ac='co',
     group='K', md=1, date='2026-06-17', time='10:00 PM ET',
     venue='Estadio Azteca, Mexico City, Mexico', hp=14, dp=22, ap=64,
     hml='+520', dml='+280', aml='-215', ai_pick='Colombia Win',
     ou='2.5', photo='1705593973313-75de7bf95b56', jdt='2026-06-17T22:00:00-06:00'),
dict(slug='portugal-uzbekistan', home='Portugal', away='Uzbekistan', hc='pt', ac='uz',
     group='K', md=2, date='2026-06-23', time='1:00 PM ET',
     venue='NRG Stadium, Houston, TX', hp=78, dp=14, ap=8,
     hml='-390', dml='+480', aml='+980', ai_pick='Portugal Win & Over 2.5',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-23T13:00:00-04:00'),
dict(slug='colombia-drc', home='Colombia', away='DR Congo', hc='co', ac='cd',
     group='K', md=2, date='2026-06-23', time='10:00 PM ET',
     venue='Estadio Akron, Guadalajara, Mexico', hp=60, dp=22, ap=18,
     hml='-185', dml='+290', aml='+460', ai_pick='Colombia Win',
     ou='2.5', photo='1599158150601-1417ebbaafdd', jdt='2026-06-23T22:00:00-06:00'),
dict(slug='colombia-portugal', home='Colombia', away='Portugal', hc='co', ac='pt',
     group='K', md=3, date='2026-06-27', time='7:30 PM ET',
     venue='Hard Rock Stadium, Miami, FL', hp=32, dp=26, ap=42,
     hml='+230', dml='+250', aml='+130', ai_pick='Portugal Win',
     ou='2.5', photo='1599158150601-1417ebbaafdd', jdt='2026-06-27T19:30:00-04:00'),
dict(slug='drc-uzbekistan', home='DR Congo', away='Uzbekistan', hc='cd', ac='uz',
     group='K', md=3, date='2026-06-27', time='7:30 PM ET',
     venue='Mercedes-Benz Stadium, Atlanta, GA', hp=46, dp=28, ap=26,
     hml='-115', dml='+250', aml='+320', ai_pick='DR Congo Win or Draw',
     ou='2.5', photo='1706675780107-7c43cc487928', jdt='2026-06-27T19:30:00-04:00'),
# GROUP L
dict(slug='england-croatia', home='England', away='Croatia', hc='gb-eng', ac='hr',
     group='L', md=1, date='2026-06-17', time='4:00 PM ET',
     venue='AT&T Stadium, Arlington, TX', hp=56, dp=24, ap=20,
     hml='-160', dml='+280', aml='+430', ai_pick='England Win',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-17T16:00:00-04:00'),
dict(slug='ghana-panama', home='Ghana', away='Panama', hc='gh', ac='pa',
     group='L', md=1, date='2026-06-17', time='7:00 PM ET',
     venue='BMO Field, Toronto, Canada', hp=44, dp=28, ap=28,
     hml='-110', dml='+240', aml='+290', ai_pick='Ghana Win or Draw',
     ou='2.5', photo='1569531955323-33c6b2dca44b', jdt='2026-06-17T19:00:00-04:00'),
dict(slug='england-ghana', home='England', away='Ghana', hc='gb-eng', ac='gh',
     group='L', md=2, date='2026-06-23', time='4:00 PM ET',
     venue='Gillette Stadium, Foxborough, MA', hp=66, dp=20, ap=14,
     hml='-225', dml='+310', aml='+570', ai_pick='England Win',
     ou='2.5', photo='1571754472834-677ab0a62ba7', jdt='2026-06-23T16:00:00-04:00'),
dict(slug='panama-croatia', home='Panama', away='Croatia', hc='pa', ac='hr',
     group='L', md=2, date='2026-06-23', time='7:00 PM ET',
     venue='BMO Field, Toronto, Canada', hp=16, dp=22, ap=62,
     hml='+500', dml='+290', aml='-200', ai_pick='Croatia Win',
     ou='2.5', photo='1489944440615-453fc2b6a9a9', jdt='2026-06-23T19:00:00-04:00'),
dict(slug='panama-england', home='Panama', away='England', hc='pa', ac='gb-eng',
     group='L', md=3, date='2026-06-27', time='5:00 PM ET',
     venue='MetLife Stadium, East Rutherford, NJ', hp=10, dp=18, ap=72,
     hml='+680', dml='+360', aml='-295', ai_pick='England Win',
     ou='2.5', photo='1556816214-6d16c62fbbf6', jdt='2026-06-27T17:00:00-04:00'),
dict(slug='croatia-ghana', home='Croatia', away='Ghana', hc='hr', ac='gh',
     group='L', md=3, date='2026-06-27', time='5:00 PM ET',
     venue='Lincoln Financial Field, Philadelphia, PA', hp=54, dp=24, ap=22,
     hml='-145', dml='+270', aml='+390', ai_pick='Croatia Win',
     ou='2.5', photo='1489944440615-453fc2b6a9a9', jdt='2026-06-27T17:00:00-04:00'),
]

# ── Group context for sidebar ─────────────────────────────────────────────────
from collections import defaultdict
GROUP_MAP = defaultdict(list)
for s in SIMPLE:
    GROUP_MAP[s['group']].append(s)

def up_next_for(slug, group):
    others = [s for s in GROUP_MAP[group] if s['slug'] != slug]
    result = []
    for s in others[:3]:
        mn = MONTH[s['date'][5:]]
        hname = T.get(s['home'], {}).get('emoji', '') + ' ' + s['home'].split()[-1]
        aname = s['away'].split()[-1]
        label = f'{s["home"].split()[-1]} vs {s["away"].split()[-1]}'
        result.append((label, f'{mn} · {s["time"].split()[0]}', f'/{s["slug"]}'))
    return result

# ── Match builder ─────────────────────────────────────────────────────────────
def favs(s):
    if int(s['hml'].replace('+','')) < 0 if s['hml'].startswith('-') else False:
        return s['home'], s['hml']
    if s['hml'].startswith('-'):
        return s['home'], s['hml']
    if s['aml'].startswith('-'):
        return s['away'], s['aml']
    # Both positive — pick higher prob
    if s['hp'] >= s['ap']:
        return s['home'], s['hml']
    return s['away'], s['aml']

def pred_txt(s, fav):
    pick = s['ai_pick']
    if 'Draw' in pick and 'Win' in pick:
        return 'to Win or Draw'
    if 'Over' in pick:
        return 'to Win & Over 2.5 Goals'
    if 'Win' in pick and fav in pick:
        margin = '1–0 or 2–0' if s['hp'] > 60 else '2–1'
        return f'to Win — {margin}'
    if 'Win' in pick:
        # away team pick
        margin = '1–0'
        return f'to Win — {margin}'
    return 'to Draw — 1–1 or 0–0'

def ou_odds(line):
    # standard juice based on line
    return ('+105', '-125')  # over, under for 2.5

def build_chips(s, ht, at):
    chips = []
    fav_name, _ = favs(s)
    # Chip 1: AI confidence + main pick
    if s['hp'] > 60:
        chips.append((f'High AI confidence — {fav_name} {s["hp"]}% win probability', True))
    elif s['hp'] > 50:
        chips.append((f'{fav_name} slight edge — {s["hp"]}% win probability, {s["dp"]}% draw', True))
    else:
        chips.append((f'Tight match — {s["home"]} {s["hp"]}% | Draw {s["dp"]}% | {s["away"]} {s["ap"]}%', False))
    # Chip 2: home team key fact
    chips.append((f'{s["home"]}: {ht["qrec"]} in qualifying — {ht["xg"]} xG per 90', True if s['hp'] > 50 else False))
    # Chip 3: away team key fact
    chips.append((f'{s["away"]}: ranked {at["rank"]} · {at["qrec"]}', False))
    # Chip 4: bet chip
    if s['ou'] == '2.5':
        chips.append((f'Over/Under 2.5 Goals: key betting angle — watch first-half tempo', False))
    return chips

def build_picks(s, ht, at):
    fav_name, fav_ml = favs(s)
    picks = []
    # Pick 1: AI main pick
    main_detail = f'{s["home"]} {s["hp"]}% vs {s["away"]} {s["ap"]}% — {ht["xg"]} xG/90 vs {at["xg"]} xG/90'
    picks.append((s['ai_pick'], main_detail, 'AI PICK', fav_ml))
    # Pick 2: player scorer from home team top player
    hp = ht['players'][0]
    player_name = hp[1]
    player_detail = f'{hp[3]}'
    picks.append((f'{player_name} Anytime Goalscorer', player_detail, 'HOT', '+180'))
    # Pick 3: value bet
    if s['dp'] >= 26:
        picks.append(('Draw / Both Teams to Score', f'Both teams have {ht["xg"]} and {at["xg"]} xG/90 — goals expected both ways', 'VALUE', '+280'))
    else:
        picks.append((f'Over {s["ou"]} Goals', f'{s["home"]} {ht["xg"]} xG + {s["away"]} {at["xg"]} xG — high-scoring expected', 'VALUE', '-115'))
    return picks

def build_fantasy(s, ht, at):
    fantasy = []
    pts_base = [38.5, 30.2, 26.8, 22.4, 19.0]
    owns = ['24% owned', '16% owned', '12% owned', '8% owned', '5% owned']
    risks = [False, False, True, False, True]
    # home top 3, away top 2
    order = [(ht, 0), (ht, 1), (at, 0), (ht, 2), (at, 1)]
    for idx, (team, pi) in enumerate(order):
        if pi >= len(team['players']):
            continue
        pos, name, age, desc = team['players'][pi]
        is_away = (team == at)
        emoji = at['emoji'] if is_away else ht['emoji']
        nation = s['away'] if is_away else s['home']
        meta = f'{pos} · {nation} · {age} yrs · {desc.split("·")[0].strip()}'
        fantasy.append((emoji, name, meta, str(pts_base[idx]), owns[idx], risks[idx]))
    return fantasy

def build_trending(s):
    return [
        (f'{s["home"]} vs {s["away"]} prediction WC 2026', 'HOT'),
        (f'{s["home"]} {s["away"]} odds World Cup', 'HOT'),
        (f'Group {s["group"]} standings WC 2026', '↑'),
    ]

def build_stat_rows(s, ht, at):
    hposs = int(ht['poss'].replace('%',''))
    aposs = int(at['poss'].replace('%',''))
    poss_pct = int(hposs / (hposs + aposs) * 100)
    hxg = float(ht['xg'])
    axg = float(at['xg'])
    xg_pct = int(hxg / (hxg + axg) * 100)
    return [
        (ht['xg'], 'xG per 90', xg_pct, at['xg']),
        (ht['poss'], 'Possession', poss_pct, at['poss']),
        (ht['gc'], 'Goals Conceded/90', max(20, min(80, int(float(at['gc'])/(float(ht['gc'])+float(at['gc']))*100))), at['gc']),
        (ht['pass_acc'], 'Pass Accuracy', int(ht['pass_acc'].replace('%','')), at['pass_acc']),
    ]

def make_date_str(date):
    day = DAYS[date]
    y, m, d = date.split('-')
    return f'{day}, {MONTH[m+"-"+d]}, {y}'

def build_match(s):
    ht = T[s['home']]
    at = T[s['away']]
    fav_name, fav_ml = favs(s)
    vs = VENUE_META[s['venue']]
    mn = MONTH[s['date'][5:]]
    date_short = mn  # e.g. "Jun 12"
    ou_over, ou_under = ou_odds(s['ou'])
    # h2h lookup
    h2h_key = (s['home'], s['away'])
    h2h_key2 = (s['away'], s['home'])
    h2h_txt = H2H.get(h2h_key, H2H.get(h2h_key2,
        f'Limited World Cup history between {s["home"]} and {s["away"]}. First competitive meeting at this level.'))

    return dict(
        slug=s['slug'],
        home=s['home'], away=s['away'],
        home_code=s['hc'], away_code=s['ac'],
        home_emoji=ht['emoji'], away_emoji=at['emoji'],
        group=s['group'], matchday=s['md'],
        date_str=make_date_str(s['date']),
        date_short=date_short,
        time_str=s['time'],
        venue=s['venue'], venue_short=vs[0], venue_name=vs[1], venue_addr=vs[2],
        json_dt=s['jdt'],
        home_ml=s['hml'], draw_ml=s['dml'], away_ml=s['aml'],
        ou_line=s['ou'], ou_over=ou_over, ou_under=ou_under,
        home_prob=s['hp'], draw_prob=s['dp'], away_prob=s['ap'],
        fav_name=fav_name, fav_ml=fav_ml,
        pred_result=pred_txt(s, fav_name),
        home_rank=f'FIFA Rank {ht["rank"]} · Tournament Odds {ht["todds"]}',
        away_rank=f'FIFA Rank {at["rank"]} · Tournament Odds {at["todds"]}',
        photo=s['photo'],
        chips=build_chips(s, ht, at),
        home_h3=ht['h3'],
        home_p1=ht['p1'],
        home_p2=ht['p2'],
        home_stats=[(ht['xg'], 'xG/90 in Qualifying'), (ht['qrec'], 'Qualifying Record'), (ht['todds'], 'Tournament Odds')],
        away_h3=at['h3'],
        away_p1=at['p1'],
        away_p2=at['p2'],
        away_stats=[(at['xg'], 'xG/90 in Qualifying'), (at['qrec'], 'Qualifying Record'), (at['todds'], 'Tournament Odds')],
        h2h=h2h_txt,
        stat_rows=build_stat_rows(s, ht, at),
        picks=build_picks(s, ht, at),
        fantasy=build_fantasy(s, ht, at),
        trending=build_trending(s),
        up_next=up_next_for(s['slug'], s['group']),
    )

# ── Runner ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    filter_slugs = set(sys.argv[1:])
    ok = err = 0
    for s in SIMPLE:
        if filter_slugs and s['slug'] not in filter_slugs:
            continue
        try:
            m = build_match(s)
            html = generate_page(m)
            path = os.path.join(PROJ, s['slug'] + '.html')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'  ✓ {s["slug"]}.html')
            ok += 1
        except Exception as e:
            import traceback
            print(f'  ✗ {s["slug"]}: {e}')
            traceback.print_exc()
            err += 1
    print(f'\n{ok} generated, {err} errors')
