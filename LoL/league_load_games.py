import leaguepedia_parser
import sys
from pprint import pprint
import json
from random import random
from math import log, exp
from itertools import permutations
from datetime import datetime

#LEAGUES = LFL, LEC, LFL_Division_2
LEAGUE = sys.argv[1].replace("_", " ").strip()
YEAR = sys.argv[2].strip()
SEASON = sys.argv[3].strip()

games = leaguepedia_parser.get_games("{}/{} Season/{} Season".format(LEAGUE, YEAR, SEASON))
games = list(sorted(games, key=lambda g:(sorted([g.teams.BLUE.sources.leaguepedia.name, g.teams.RED.sources.leaguepedia.name]), datetime.strptime(g.start[:19], format="%Y-%m-%dT%H:%M:%S"), g.gameInSeries)))
g_json = [(g.teams.BLUE.sources.leaguepedia.name, g.teams.RED.sources.leaguepedia.name, [g.teams.BLUE.sources.leaguepedia.name, g.teams.RED.sources.leaguepedia.name][g.winner=='RED'], g.gameInSeries) for g in games if g.winner in ['BLUE', 'RED']]

"""
g_json += [("Vitality.Bee", "Karmine Corp Blue", "Karmine Corp Blue")]
g_json += [("Team BDS Academy", "Solary", "Team BDS Academy")]
g_json += [("Team Du Sud", "GameWard", "GameWard")]
g_json += [("Aegis (French Team)", "Team GO", "Team GO")]
g_json += [("Gentle Mates", "BK ROG Esports", "Team Du Sud")]
"""
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-games.out', 'w') as f:
	json.dump(g_json, f)

logos = dict()
for T in g_json:
	for name in T[:2]:
		if name not in logos:
			logos[name] = leaguepedia_parser.get_team_logo(name)


with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-logos.out', 'w') as f:
	json.dump(logos, f)
