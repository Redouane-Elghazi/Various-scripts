import sys
from pprint import pprint
import json
from random import random
from math import log, exp
from itertools import permutations
import datetime as dt

from teams import complete2short

#LEAGUES = LFL, LEC, LFL_Division_2
LEAGUE = sys.argv[1].replace("_", " ").strip()
YEAR = sys.argv[2].strip()
SEASON = sys.argv[3].strip()

def newmatch(t1, t2, w, gis=0):
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
	res.gameInSeries = gis
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
	
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-logos.out', 'r') as f:
	fulllogos = json.load(f)
	
n = 0
teams = []
results = dict()
secondhalf = dict()
logos = dict()
Rs = dict()
addedmatches=[]
"""
addedmatches += [newmatch("T1 Esports Academy", "Hanwha Life Esports Challengers", "T1 Esports Academy", 1)]
addedmatches += [newmatch("T1 Esports Academy", "Hanwha Life Esports Challengers", "Hanwha Life Esports Challengers", 2)]
addedmatches += [newmatch("T1 Esports Academy", "Hanwha Life Esports Challengers", "Hanwha Life Esports Challengers", 3)]

addedmatches += [newmatch("BK ROG Esports", "GameWard", "BK ROG Esports")]
addedmatches += [newmatch("Vitality.Bee", "Team GO", "Team GO")]
addedmatches += [newmatch("Team BDS Academy", "Gentle Mates", "Vitality.Bee")]
addedmatches += [newmatch("Aegis (French Team)", "Karmine Corp Blue", "Karmine Corp Blue")]
addedmatches += [newmatch("Solary", "Team Du Sud", "Team Du Sud")]
"""
#addedmatches += [newmatch("Zerance", "Akroma", "Zerance")]
#addedmatches += [newmatch("Esprit Shōnen", "Joblife", "Esprit Shōnen")]
#addedmatches += [newmatch("Joblife", "MS Company", "Joblife")]
#addedmatches += [newmatch("Joblife", "Team Du Sud", "Joblife")]
#addedmatches += [newmatch("Joblife", "ViV Esport", "Joblife")]
#addedmatches += [newmatch("Karmine Corp", "Vitality.Bee", "Vitality.Bee")]
#addedmatches += [newmatch("Karmine Corp", "Aegis (French Team)", "Aegis (French Team)")]
#addedmatches += [newmatch("Vitality.Bee", "Solary", "Solary")]

"""
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

curt1, curt2, curscore1, curscore2, gis = (None, None, None, None, None)
for g in games+addedmatches:
	for t in [g.teams.BLUE, g.teams.RED]:
		name = complete2short[t.sources.leaguepedia.name]
		if name not in teams:
			n += 1
			for t1 in teams:
				results[t1][name] = 0
				secondhalf[t1][name] = 0
			teams += [name]
			results[name] = {t1:0 for t1 in teams}
			secondhalf[name] = {t1:0 for t1 in teams}
			logos[name] = fulllogos[t.sources.leaguepedia.name]
	blue = complete2short[g.teams.BLUE.sources.leaguepedia.name]
	red = complete2short[g.teams.RED.sources.leaguepedia.name]
	if red == curt1 and blue == curt2:
		curt1, curt2, curscore1, curscore2 = curt2, curt1, curscore2, curscore1
	if blue != curt1 or red != curt2 or g.gameInSeries != gis+1:
		if curt1 is not None:
			if "KDF.C" in (curt1, curt2):
				print(curt1, curt2, curscore1, curscore2, blue, red)
			results[curt1][curt2] += curscore1/(curscore1+curscore2)
			results[curt2][curt1] += curscore2/(curscore1+curscore2)
		curt1, curt2, curscore1, curscore2, gis = (blue, red, 0, 0, 0)
	gis = g.gameInSeries
	if g.winner == 'RED':
		curscore2 += 1
	elif g.winner == 'BLUE':
		curscore1 += 1
	else:
		print("unknown winner: {}".format(g.winner), file=sys.stderr)
if curt1 is not None:
	results[curt1][curt2] += curscore1/(curscore1+curscore2)
	results[curt2][curt1] += curscore2/(curscore1+curscore2)


"""_____________________start______________________"""

def f(X, nb_matches, w):
	def g(x):
		S = sum(g.nb_matches[t] for t in g.X)
		return sum(g.nb_matches[t]/(1+10**(g.X[t]-x)) for t in g.X) - (g.w+1)/(S+2)*S
		#Base formula (doesn't handle teams with 100% or 0% winrate
		#return sum(g.nb_matches[t]/(1+10**(g.X[t]-x)) for t in g.X) - g.w
	g.nb_matches = nb_matches.copy()
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
	"""#Used to remove teams with 100% or 0% winrate
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
	"""
	nb_matches = {t1:{t2:results[t1][t2]+results[t2][t1] for t2 in teams} for t1 in teams}
	n = len(teams)
	X = {t:0 for t in teams}
	W = {t:sum([results[t][t1] for t1 in teams]) for t in teams}
	print(W)
	err = sum(abs(f({t1:X[t1] for t1 in teams if (results[t][t1]+results[t1][t] != 0)}, nb_matches[t], W[t])(X[t])) for t in teams)
	#print(f'err={err}')
	#return
	for _ in range(1000):
		for i in range(1, n):
			t = teams[i]
			X[t] = dicho_incr(f({t1:X[t1] for t1 in teams if (results[t][t1]+results[t1][t] != 0)}, nb_matches[t], W[t]))
		#print(f'iteration n°{_+1}', end=" ")
		err = sum(abs(f({t1:X[t1] for t1 in teams if (results[t][t1]+results[t1][t] != 0)}, nb_matches[t], W[t])(X[t])) for t in teams)
	print(f'err={err}')
	return X, unbounded_pos, unbounded_neg

elo, ub_pos, ub_neg = find_elo(teams, results)
average, m, M = sum(elo[t] for t in elo)/len(elo), min(elo[t] for t in elo), max(elo[t] for t in elo) #TODO: what if len(elo)==0?

if LEAGUE.lower() in ["lpl", "lck"]:
	target_average = 2600
elif LEAGUE.lower() in ["lec", "lcs"]:
	target_average = 2500
else:
	target_average = 2000
diff = 400
pelo = {t:((elo[t]-avg)*diff)+targ for t in elo}
W = {t:int(sum([results[t][t1] for t1 in teams])) for t in teams}
L = {t:int(sum([results[t1][t] for t1 in teams])) for t in teams}
currank = {t:len([t1 for t1 in teams if W[t1] > W[t]])+1 for t in teams}
estrank = {t:len([t1 for t1 in teams if pelo[t1] > pelo[t]])+1 for t in teams}
for e, t in sorted([(pelo[t],t) for t in pelo], reverse=True):
	print(f'{currank[t]},({W[t]}-{L[t]}),,{t:3},{e:7.2f},{estrank[t]}')

M = []
tt = 0
for t1 in teams:
	for t2 in teams:
		if t1 < t2:
			if LEAGUE.lower() == "lec":
				for i in range(1-round(results[t1][t2] + results[t2][t1])):
					M += [(t1,t2)]
			else:
				print(t1, t2, 2-round(results[t1][t2] + results[t2][t1]))
				tt += 2-round(results[t1][t2] + results[t2][t1])
				for i in range(2-round(results[t1][t2] + results[t2][t1])):
					M += [(t1,t2)]
print(tt, len(M))

probawin = {t:dict() for t in teams}
for t1, t2 in M:
	if t1 in ub_pos and t2 in ub_pos:
		print(f'{t1},,skipped,skipped,,{t2}')
		print(f'{t2},,skipped,skipped,,{t1}')
		pass
	elif t1 in ub_pos:
		probawin[t1][t2] = 1
		probawin[t2][t1] = 0
		print(f'{t1},,1,0,,{t2}')
		print(f'{t2},,0,1,,{t1}')
	elif t2 in ub_pos:
		probawin[t1][t2] = 0
		probawin[t2][t1] = 1
		print(f'{t1},,0,1,,{t2}')
		print(f'{t2},,1,0,,{t1}')
	elif t1 in ub_neg and t2 in ub_neg:
		print(f'{t1},,skipped,skipped,,{t2}')
		print(f'{t2},,skipped,skipped,,{t1}')
	elif t1 in ub_neg:
		probawin[t1][t2] = 0
		probawin[t2][t1] = 1
		print(f'{t1},,0,1,,{t2}')
		print(f'{t2},,1,0,,{t1}')
	elif t2 in ub_neg:
		probawin[t1][t2] = 1
		probawin[t2][t1] = 0
		print(f'{t1},,1,0,,{t2}')
		print(f'{t2},,0,1,,{t1}')
	else:
		probawin[t1][t2] = 1/(1+10**(elo[t2]-elo[t1]))
		probawin[t2][t1] = 1/(1+10**(elo[t1]-elo[t2]))
		print(f'{t1},,{1/(1+10**(elo[t2]-elo[t1]))},vs,{1/(1+10**(elo[t1]-elo[t2]))},,{t2}')
		print(f'{t2},,{1/(1+10**(elo[t1]-elo[t2]))},vs,{1/(1+10**(elo[t2]-elo[t1]))},,{t1}')

with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-probawin.out', 'w') as f:
	json.dump(probawin, f)
