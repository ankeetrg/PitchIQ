#!/usr/bin/env python3
"""PitchIQ — completed World Cup 2026 match results."""

RESULTS = {
  'mexico-southafrica': {
    'home': 'Mexico', 'away': 'South Africa',
    'home_iso': 'mx', 'away_iso': 'za',
    'home_score': 2, 'away_score': 0,
    'date': 'June 12, 2026', 'group': 'A', 'venue': 'SoFi Stadium, LA',
    'scorers': ['Lozano 23\'', 'Álvarez 61\''],
    'pitchiq_pick': 'Mexico Win', 'pick_result': 'WIN',
    'ai_summary': 'Mexico controlled possession from the first whistle. Lozano finished low left on a Sánchez cutback; Álvarez doubled it from the spot after a handball in the box. South Africa had one shot on target all game.',
    'man_of_match': 'Hirving Lozano',
    'next_match': {'home': 'Mexico', 'away': 'Czechia', 'slug': 'czechia-mexico', 'date': 'June 16'}
  },
  'korea-czechia': {
    'home': 'South Korea', 'away': 'Czechia',
    'home_iso': 'kr', 'away_iso': 'cz',
    'home_score': 2, 'away_score': 1,
    'date': 'June 12, 2026', 'group': 'A', 'venue': 'AT&T Stadium, Dallas',
    'scorers': ['Son 34\'', 'Schick 55\'', 'Hwang 78\''],
    'pitchiq_pick': 'Over 2.5 Goals', 'pick_result': 'WIN',
    'ai_summary': 'Son opened it with a trademark run and finish. Schick equalized with a header from a set piece. Hwang sealed it late — Korea showed they can grind out wins when it matters.',
    'man_of_match': 'Heung-min Son',
    'next_match': {'home': 'South Korea', 'away': 'South Africa', 'slug': 'southafrica-korea', 'date': 'June 16'}
  },
  'canada-bosnia': {
    'home': 'Canada', 'away': 'Bosnia',
    'home_iso': 'ca', 'away_iso': 'ba',
    'home_score': 1, 'away_score': 1,
    'date': 'June 12, 2026', 'group': 'B', 'venue': 'BMO Field, Toronto',
    'scorers': ['David 45\'', 'Džeko 71\''],
    'pitchiq_pick': 'Under 2.5 Goals', 'pick_result': 'WIN',
    'ai_summary': 'Jonathan David gave Canada the lead right before the break. Bosnia equalized through an aging but still clinical Džeko. A point each — neither side looked like a group winner.',
    'man_of_match': 'Jonathan David',
    'next_match': {'home': 'Canada', 'away': 'Qatar', 'slug': 'canada-qatar', 'date': 'June 17'}
  },
  'usa-paraguay': {
    'home': 'USA', 'away': 'Paraguay',
    'home_iso': 'us', 'away_iso': 'py',
    'home_score': 4, 'away_score': 1,
    'date': 'June 12, 2026', 'group': 'D', 'venue': 'SoFi Stadium, LA',
    'scorers': ['Balogun 18\'', 'Balogun 39\'', 'Weah 62\'', 'Reyna 88\'', 'Maurício 79\''],
    'pitchiq_pick': 'USA Win', 'pick_result': 'WIN',
    'ai_summary': 'Balogun delivered on every bit of hype with a first-half brace. Weah added a third from range. Reyna\'s trivela was the goal of the match. Paraguay pulled one back but this wasn\'t close.',
    'man_of_match': 'Folarin Balogun',
    'next_match': {'home': 'USA', 'away': 'Australia', 'slug': 'usa-australia', 'date': 'June 19'}
  },
  'qatar-switzerland': {
    'home': 'Qatar', 'away': 'Switzerland',
    'home_iso': 'qa', 'away_iso': 'ch',
    'home_score': 1, 'away_score': 1,
    'date': 'June 13, 2026', 'group': 'B', 'venue': 'Levi\'s Stadium, Santa Clara',
    'scorers': ['Embolo 28\'', 'Khoukhi 95\''],
    'pitchiq_pick': 'Switzerland Win', 'pick_result': 'LOSS',
    'ai_summary': 'Switzerland dominated for 94 minutes and should have put it to bed long before Khoukhi\'s 95th-minute header. Qatar did nothing for 90 minutes and still walked away with a point. Switzerland will be furious.',
    'man_of_match': 'Breel Embolo',
    'next_match': {'home': 'Switzerland', 'away': 'Canada', 'slug': 'switzerland-canada', 'date': 'June 17'}
  },
  'brazil-morocco': {
    'home': 'Brazil', 'away': 'Morocco',
    'home_iso': 'br', 'away_iso': 'ma',
    'home_score': 1, 'away_score': 1,
    'date': 'June 13, 2026', 'group': 'C', 'venue': 'MetLife Stadium, NJ',
    'scorers': ['Vinicius 54\'', 'Hakimi 79\''],
    'pitchiq_pick': 'Brazil Win', 'pick_result': 'LOSS',
    'ai_summary': 'Vinicius put Brazil ahead with a finish that had no right to go in at that angle. Hakimi\'s thunderstrike from 25 yards was the answer Morocco needed. A point each — both teams will take it.',
    'man_of_match': 'Achraf Hakimi',
    'next_match': {'home': 'Brazil', 'away': 'Haiti', 'slug': 'brazil-haiti', 'date': 'June 18'}
  },
  'haiti-scotland': {
    'home': 'Haiti', 'away': 'Scotland',
    'home_iso': 'ht', 'away_iso': 'gb-sct',
    'home_score': 0, 'away_score': 1,
    'date': 'June 13, 2026', 'group': 'C', 'venue': 'Gillette Stadium, Foxborough',
    'scorers': ['McGinn 28\''],
    'pitchiq_pick': 'Under 2.5 Goals', 'pick_result': 'WIN',
    'ai_summary': 'McGinn\'s 28th-minute header from a Robertson cross was the difference. Scotland defended everything Haiti threw at them — which wasn\'t much. A professional win for Steve Clarke\'s side.',
    'man_of_match': 'John McGinn',
    'next_match': {'home': 'Scotland', 'away': 'Morocco', 'slug': 'scotland-morocco', 'date': 'June 18'}
  },
  'australia-turkey': {
    'home': 'Australia', 'away': 'Türkiye',
    'home_iso': 'au', 'away_iso': 'tr',
    'home_score': 2, 'away_score': 0,
    'date': 'June 14, 2026', 'group': 'D', 'venue': 'BC Place, Vancouver',
    'scorers': ['Irankunda 27\'', 'Metcalfe 75\''],
    'pitchiq_pick': 'Australia +0.5 AH', 'pick_result': 'WIN',
    'ai_summary': 'Irankunda became the youngest Socceroo to score at a World Cup — composed finish from a tight angle. Metcalfe killed it late with a breakaway counter. Turkey had Yildiz rested and never found a way through.',
    'man_of_match': 'Nestory Irankunda',
    'next_match': {'home': 'Australia', 'away': 'USA', 'slug': 'usa-australia', 'date': 'June 19'}
  }
}
