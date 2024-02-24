import leaguepedia_parser
import sys
from pprint import pprint
import json
from random import random
from math import log, exp
from itertools import permutations

#LEAGUES = LFL, LEC, LFL_Division_2
LEAGUE = sys.argv[1].replace("_", " ")
YEAR = sys.argv[2]
SEASON = sys.argv[3]

games = leaguepedia_parser.get_games("{}/{} Season/{} Season".format(LEAGUE, YEAR, SEASON))
g_json = [(g.teams.BLUE.sources.leaguepedia.name, g.teams.RED.sources.leaguepedia.name, [g.teams.BLUE.sources.leaguepedia.name, g.teams.RED.sources.leaguepedia.name][g.winner=='RED']) for g in games if g.winner in ['BLUE', 'RED']]

with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-games.out', 'w') as f:
	json.dump(g_json, f)

logos = dict()
for T in g_json:
	for name in T:
		if name not in logos:
			logos[name] = leaguepedia_parser.get_team_logo(name)


with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-logos.out', 'w') as f:
	json.dump(logos, f)
