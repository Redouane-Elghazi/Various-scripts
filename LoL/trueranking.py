import sys
from pprint import pprint
import json
from random import random
from math import log, exp
from itertools import permutations
import datetime as dt

#LEAGUES = LFL, LEC, LFL_Division_2
LEAGUE = sys.argv[1].replace("_", " ")
YEAR = sys.argv[2]
SEASON = sys.argv[3]
if len(sys.argv)>4:
	cut = int(sys.argv[4])
else:
	cut = 1

def newmatch(t1, t2, w):
	void = lambda :(lambda :())
	res = void()
	res.teams = void()
	res.teams.BLUE = void()
	res.teams.RED = void()
	for t in [res.teams.BLUE, res.teams.RED]:
		t.sources = void()
		t.sources.leaguepedia = void()
	res.teams.BLUE.sources.leaguepedia.name = t1
	res.teams.RED.sources.leaguepedia.name = t2
	if w == t1:
		res.winner = "BLUE"
	else:
		res.winner = "RED"
	return res
#games = leaguepedia_parser.get_games("{}/{} Season/{} Season".format(LEAGUE, YEAR, SEASON))
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-games.out', 'r') as f:
	g_json = json.load(f)
games = [newmatch(*teams) for teams in g_json]

def estimaT(adv):
	if estimaT.start == None:
		estimaT.start = dt.datetime.now()
		estimaT.sadv = adv
		return (estimaT.start.strftime("%d-%m %H:%M:%S"), "None")
	cur = dt.datetime.now()
	end = estimaT.start + (cur-estimaT.start)*(1-estimaT.sadv)/(adv-estimaT.sadv)
	return (estimaT.start.strftime("%d-%m %H:%M:%S"), end.strftime("%d-%m %H:%M:%S"))
estimaT.start = None

complete2short = {
	"Izi Dream": "IZI",
	"Team MCES": "MCES",
	"Team Oplon":"OPL",
	"Mirage Elyandra":"ME",
	"GameWard":"GW",
	"GamersOrigin":"GO",
	"Team GO":"GO",
	"Team BDS Academy":"BDSA",
	"Solary":"SLY",
	"Misfits Premier":"MSFP",
	"Karmine Corp":"KC",
	"Vitality.Bee":"VITB",
	"LDLC OL":"LDLC",
	"Astralis":"AST",
	"Team BDS":"BDS",
	"SK Gaming":"SK",
	"MAD Lions":"MAD",
	"Team Vitality":"VIT",
	"G2 Esports":"G2",
	"Excel Esports":"XL",
	"KOI (Spanish Team)":"KOI",
	"Team Heretics":"TH",
	"Fnatic":"FNC",
	"BK ROG Esports": "BKR",
	"Aegis (French Team)": "AEG",
	"Rogue (European Team)": "RGE",
	"GIANTX": "GX",
	"MAD Lions KOI": "MDK",
	"Karmine Corp Blue": "KCB",
	"Gentle Mates": "M8",
	"Team Du Sud": "TDS",
	}
	
	
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-logos.out', 'r') as f:
	fulllogos = json.load(f)
	
n = 0
teams = []
results = dict()
secondhalf = dict()
logos = dict()
Rs = dict()
addedmatches=[]
#addedmatches += [newmatch("Joblife", "Atletec", "Joblife")]
#addedmatches += [newmatch("Joblife", "MS Company", "Joblife")]
#addedmatches += [newmatch("Joblife", "Team Du Sud", "Joblife")]
#addedmatches += [newmatch("Joblife", "ViV Esport", "Joblife")]
#addedmatches += [newmatch("Karmine Corp", "Vitality.Bee", "Vitality.Bee")]
#addedmatches += [newmatch("Karmine Corp", "Aegis (French Team)", "Aegis (French Team)")]
#addedmatches += [newmatch("Vitality.Bee", "Solary", "Solary")]
"""
addedmatches += [newmatch("G2 Esports", "MAD Lions", "G2 Esports")]
addedmatches += [newmatch("Team Vitality", "Team BDS", "Team Vitality")]
addedmatches += [newmatch("SK Gaming", "Fnatic", "Fnatic")]
addedmatches += [newmatch("KOI (Spanish Team)", "MAD Lions", "KOI (Spanish Team)")]
addedmatches += [newmatch("G2 Esports", "Team Heretics", "G2 Esports")]
addedmatches += [newmatch("Team Vitality", "G2 Esports", "G2 Esports")]
addedmatches += [newmatch("Team BDS", "MAD Lions", "Team BDS")]
addedmatches += [newmatch("Team Heretics", "MAD Lions", "Team Heretics")]
addedmatches += [newmatch("SK Gaming", "KOI (Spanish Team)", "SK Gaming")]
addedmatches += [newmatch("MAD Lions", "Fnatic", "MAD Lions")]
"""
#addedmatches += [newmatch("Team Vitality", "Karmine Corp", "Team Vitality")]
#addedmatches += [newmatch("Team Heretics", "Karmine Corp", "Karmine Corp")]
#addedmatches += [newmatch("Rogue (European Team)", "Karmine Corp", "Karmine Corp")]
#addedmatches += [newmatch("SK Gaming", "Karmine Corp", "Karmine Corp")]
#addedmatches += [newmatch("Team BDS", "Karmine Corp", "Karmine Corp")]
print("There are {} matches".format(len(games+addedmatches)))

for g in games+addedmatches:
	for t in [g.teams.BLUE, g.teams.RED]:
		name = complete2short[t.sources.leaguepedia.name]
		if name not in teams:
			n += 1
			for t1 in teams:
				results[t1][name] = 0
				secondhalf[t1][name] = 0
			results[name] = {t1:0 for t1 in teams}
			secondhalf[name] = {t1:0 for t1 in teams}
			teams += [name]
			logos[name] = fulllogos[t.sources.leaguepedia.name]
	blue = complete2short[g.teams.BLUE.sources.leaguepedia.name]
	red = complete2short[g.teams.RED.sources.leaguepedia.name]
	if g.winner == 'RED':
		results[red][blue] += 1
		if results[blue][red] + results[red][blue] == 2:
			secondhalf[red][blue] += 1
	elif g.winner == 'BLUE':
		results[blue][red] += 1
		if results[blue][red] + results[red][blue] == 2:
			secondhalf[blue][red] += 1
	else:
		print("unknown winner: {}".format(g.winner), file=sys.stderr)

mem = {tuple(): (0, [[]])}
def solve(teams, results):
	S = tuple(sorted(teams))
	if S not in mem:
		n = len(teams)
		teams2 = teams[:-1]
		t = teams[-1]
		inv, sol = solve(teams2, results)
		inversions = inv + sum(results[t1][t] for t1 in teams2)
		solutions = [[t] + s for s in sol]
		for i in range(n-1):
			teams2[i], t = t, teams2[i]
			inv, sol = solve(teams2, results)
			inv += sum(results[t1][t] for t1 in teams2)
			if inv < inversions:
				inversions = inv
				solutions = []
			if inv == inversions:
				solutions += [[t] + s for s in sol]
		mem[S] = (inversions, solutions)
	return mem[S]

n = len(teams)
inversions, solutions = solve(teams, results)
print(inversions, len(solutions))
comp = {t1: {t2: sum(s.index(t1) < s.index(t2) for s in solutions) for t2 in teams} for t1 in teams}
T = teams.copy()
res = []
while T:
	found = False
	l = []
	while not found:
		print(res, l, T)
		for t in T:
			if all(comp[t][t1] > comp[t1][t] for t1 in T if t1 != t):
				l += [t]
				T.remove(t)
				found = True
				break
			if all(comp[t][t1] >= comp[t1][t] for t1 in T if t1 != t):
				l += [t]
				T.remove(t)
				break
	res += [l]
print(res)
for t1 in teams:
	for t2 in teams:
		print(t1, t2, sum(s.index(t1) < s.index(t2) for s in solutions))
pprint(solutions)
