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
	"Karmine Corp Blue":"KCB",
	"Gentle Mates":"M8",
	"Team Du Sud":"TDS",
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

for t1 in teams:
	for t2 in teams:
		if t2 not in results[t1]:
			results[t1][t2] = 0

"""_____________________start______________________"""

def f(X, w):
	def g(x):
		return sum(1/(1+10**(g.X[t]-x)) for t in g.X) - g.w
	g.X = X.copy()
	g.w = w
	return g

def dicho_incr(f, val=0, a=None, b=None, eps=1e-10):
	if a is None:
		a = -1
		while f(a) > val:
			a*=2
	if b is None:
		b = 1
		while f(b) < val:
			b*=2
	while b-a > eps:
		m = (a+b)/2
		if f(m) < val:
			a = m
		else:
			b = m
	return a

def find_elo(teams, results): ### ajouter le nombre de matchs (pour la LFL)
	teams = teams.copy()
	found = True
	unbounded_pos, unbounded_neg = [], []
	while found and len(teams)>0:
		found = False
		for t in teams:
			if all(results[t][t1] == 0 for t1 in teams if t1 != t):
				found = True
				unbounded_neg += [t]
				teams.remove(t)
				break
			if all(results[t1][t] == 0 for t1 in teams if t1 != t):
				found = True
				unbounded_pos += [t]
				teams.remove(t)
				break
	
	n = len(teams)
	X = {t:0 for t in teams}
	W = {t:sum([results[t][t1] for t1 in teams]) for t in teams}
	print(W)
	err = sum(abs(f({t1:X[t1] for t1 in teams if (results[t][t1]+results[t1][t] != 0)}, W[t])(X[t])) for t in teams)
	print(f'err={err}')
	#return
	for _ in range(1000):
		for i in range(1, n):
			t = teams[i]
			X[t] = dicho_incr(f({t1:X[t1] for t1 in teams if (results[t][t1]+results[t1][t] != 0)}, W[t]))
		print(f'iteration n°{_+1}', end=" ")
		err = sum(abs(f({t1:X[t1] for t1 in teams if (results[t][t1]+results[t1][t] != 0)}, W[t])(X[t])) for t in teams)
		print(f'err={err}')
	return X, unbounded_pos, unbounded_neg

elo, ub_pos, ub_neg = find_elo(teams, results)
avg, m, M = sum(elo[t] for t in elo)/len(elo), min(elo[t] for t in elo), max(elo[t] for t in elo) #TODO: what if len(elo)==0?
if LEAGUE.lower() in ["lpl", "lck"]:
	targ = 2600
elif LEAGUE.lower() in ["lec", "lcs"]:
	targ = 2500
else:
	targ = 2000
diff = 400
pelo = {t:((elo[t]-avg)*diff)+targ for t in elo}
pprint(pelo)

M = []
for t1 in teams:
	for t2 in teams:
		if t1 < t2:
			if LEAGUE.lower() == "lec":
				for i in range(1-results[t1][t2] - results[t2][t1]):
					M += [(t1,t2)]
			else:
				for i in range(2-results[t1][t2] - results[t2][t1]):
					M += [(t1,t2)]

probawin = {t:dict() for t in teams}
for t1, t2 in M:
	if t1 in ub_pos and t2 in ub_pos:
		print(f'passed {t1}-{t2}')
		pass
	elif t1 in ub_pos:
		probawin[t1][t2] = 1
		probawin[t2][t1] = 0
		print(f'{t1},,1,0,,{t2}')
	elif t2 in ub_pos:
		probawin[t1][t2] = 0
		probawin[t2][t1] = 1
		print(f'{t1},,0,1,,{t2}')
	elif t1 in ub_neg and t2 in ub_neg:
		print(f'passed {t1}-{t2}')
	elif t1 in ub_neg:
		probawin[t1][t2] = 0
		probawin[t2][t1] = 1
		print(f'{t1},,0,1,,{t2}')
	elif t2 in ub_neg:
		probawin[t1][t2] = 1
		probawin[t2][t1] = 0
		print(f'{t1},,1,0,,{t2}')
	else:
		probawin[t1][t2] = 1/(1+10**(elo[t2]-elo[t1]))
		probawin[t2][t1] = 1/(1+10**(elo[t1]-elo[t2]))
		print(f'{t1},,{1/(1+10**(elo[t2]-elo[t1]))},{1/(1+10**(elo[t1]-elo[t2]))},,{t2}')
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-probawin.out', 'w') as f:
	json.dump(probawin, f)
