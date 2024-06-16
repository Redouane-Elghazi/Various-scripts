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
if len(sys.argv)>4:
	cut = int(sys.argv[4])
else:
	cut = 1

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
#addedmatches += [newmatch("Joblife", "MS Company", "Joblife")]
#addedmatches += [newmatch("Joblife", "Team Du Sud", "Joblife")]
#addedmatches += [newmatch("Joblife", "ViV Esport", "Joblife")]
#addedmatches += [newmatch("Karmine Corp", "Vitality.Bee", "Vitality.Bee")]
#addedmatches += [newmatch("Karmine Corp", "Aegis (French Team)", "Aegis (French Team)")]
#addedmatches += [newmatch("Vitality.Bee", "Solary", "Solary")]
"""
addedmatches += [newmatch("MAD Lions KOI", "GIANTX", "MAD Lions KOI")]
addedmatches += [newmatch("MAD Lions KOI", "Fnatic", "Fnatic")]
addedmatches += [newmatch("MAD Lions KOI", "Team Vitality", "MAD Lions KOI")]
addedmatches += [newmatch("G2 Esports", "Team Vitality", "Team Vitality")]
addedmatches += [newmatch("SK Gaming", "Team Vitality", "Team Vitality")]
addedmatches += [newmatch("Team Heretics", "Team Vitality", "Team Heretics")]


addedmatches += [newmatch("Team BDS", "Karmine Corp", "Karmine Corp")]
addedmatches += [newmatch("Rogue (European Team)", "Karmine Corp", "Karmine Corp")]
addedmatches += [newmatch("SK Gaming", "Karmine Corp", "SK Gaming")]
"""



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
			results[name] = {t1:0 for t1 in teams}
			secondhalf[name] = {t1:0 for t1 in teams}
			teams += [name]
			logos[name] = fulllogos[t.sources.leaguepedia.name]
	blue = complete2short[g.teams.BLUE.sources.leaguepedia.name]
	red = complete2short[g.teams.RED.sources.leaguepedia.name]
	if red == curt1 and blue == curt2:
		curt1, curt2, curscore1, curscore2 = curt2, curt1, curscore2, curscore1
	if blue != curt1 or red != curt2 or g.gameInSeries != gis+1:
		if curt1 is not None:
			if curscore1>curscore2:
				results[curt1][curt2] += 1
				if results[curt1][curt2] + results[curt2][curt1] == 2:
					secondhalf[curt1][curt2] += 1
			elif curscore2>curscore1:
				results[curt2][curt1] += 1
				if results[curt1][curt2] + results[curt2][curt1] == 2:
					secondhalf[curt2][curt1] += 1
			else:
				print("unknown winner: {} vs {}".format(curt1, curt2), file=sys.stderr)
		curt1, curt2, curscore1, curscore2, gis = (blue, red, 0, 0, 0)
	gis = g.gameInSeries
	if g.winner == 'RED':
		curscore2 += 1
	elif g.winner == 'BLUE':
		curscore1 += 1
	else:
		print("unknown winner: {}".format(g.winner), file=sys.stderr)
if curt1 is not None:
	if curscore1>curscore2:
		results[curt1][curt2] += 1
		if results[curt1][curt2] + results[curt2][curt1] == 2:
			secondhalf[curt1][curt2] += 1
	elif curscore2>curscore1:
		results[curt2][curt1] += 1
		if results[curt1][curt2] + results[curt2][curt1] == 2:
			secondhalf[curt2][curt1] += 1
	else:
		print("unknown winner: {} vs {}".format(curt1, curt2), file=sys.stderr)

if LEAGUE.lower() == "lec" and SEASON.lower() == "summer":
	basepts = {
		"G2":90,
		"RGE":70,
		"FNC":50,
		"MSF":30,
		"MAD":20,
		"VIT":20,
		"XL":10,
		"SK":0,
		"AST":0,
		"BDS":0
		}
	sumpts = [120,90,70,50,30,20,0,0,0]
else:
	basepts = {t:0 for t in teams}
	sumpts = [120,90,70,50,30,20,0,0,0]

"""with open("{}-tot.in".format(LEAGUE), "r") as f:
	n = int(f.readline().strip())
	teams = f.readline().strip().split()
	results = {t:dict() for t in teams}
	for i in range(n):
		t1 = f.readline().strip()
		for j in range(n):
			t2 = teams[j]
			if t1 != t2:
				w, _, l = f.readline().strip().split()
				w, l = int(w), int(l)
				results[t1][t2] = w
		TOT = f.readline().strip()
		PER = f.readline().strip()
"""

def init(teams, results):
	global pos, M, Result
	pos = {t:dict() for t in teams}
	M = []
	for t1 in teams:
		for t2 in teams:
			if t1 < t2:
				if LEAGUE.lower() == "lec":
					for i in range(1-round(results[t1][t2] + results[t2][t1])):
						M += [(t1,t2)]
				else:
					for i in range(2-round(results[t1][t2] + results[t2][t1])):
						M += [(t1,t2)]
	Result = [0]*len(M)
	print(M)


curR = dict()

def affect(t, p):
	global pos, Result, M
	if p not in pos[t]:
		pos[t][p] = 0
	pos[t][p] += 1
	curR[t] = p

def get_SoV(teams, results):
	n = len(teams)
	T = teams.copy()
	R = [[None for i in range(10)]]
	W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
	T.sort(key=lambda t:-W[t])
	nb = dict()
	prev = None
	SoV = {t: 0 for t in teams}
	cnt = 0
	for i in range(n):
		if W[T[i]] == prev:
			nb[T[i]] = nb[T[i-1]]
			cnt += 1
		else:
			nb[T[i]] = 10-i
			prev = W[T[i]]
			if cnt == 2:
				t1, t2 = T[i-2], T[i-1]
				if results[t1][t2] < results[t2][t1]:
					nb[t1] -= 1
				if results[t1][t2] > results[t2][t1]:
					nb[t2] -= 1
			cnt = 1
	if cnt == 2:
		t1, t2 = T[-2], T[-1]
		if results[t1][t2] < results[t2][t1]:
			nb[t1] -= 1
		if results[t1][t2] > results[t2][t1]:
			nb[t2] -= 1
	for t1 in teams:
		for t2 in teams:
			if t1!=t2:
				SoV[t1] += results[t1][t2]*nb[t2]
	return SoV
	
tie8 = 0
tiet8 = dict()
qualif = 0
tie = 0
out = 0
def classements(teams, results, p, offset=0, R=None):
	global Rs, tie8, qualif, tie, out
	terminal = R is None
	#print(teams, R)
	if LEAGUE.lower() == "lec":
		n = len(teams)
		T = teams.copy()
		if R is None:
			R = [[None for i in range(10)]]
		W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
		SoV = get_SoV(teams, results)
		T.sort(key=lambda t:(-W[t], -SoV[t]))
		i = 0
		j = 0
		while i<n:
			while j<n and ((W[T[i]], SoV[T[i]]) == (W[T[j]], SoV[T[j]]) or (7==i and W[T[7]] == W[T[8]] == W[T[j]]) or (6==i and W[T[6]] == W[T[7]] == W[T[8]] == W[T[j]] and W[T[6]] != W[T[9]])):
				j += 1
			if 'KC' in T[i:j]:
				if j < 8:
					qualif += p
				elif i < 8 <= j:
					tie += p
				elif 8 <= i:
					out += p
				else:
					print("b2oba")
			if i <= 7 and 9 <= j:
				for t in T[i:8]:
					if t not in tiet8:
						tiet8[t] = 0
					tiet8[t] += 1
				#print(tiet8)
				tie8+=1
				#print("tie8:", tie8)
			if i+2==j:
				t1, t2 = T[i], T[i+1]
				if results[t1][t2] < results[t2][t1]:
					perms = [[t2, t1]]
				elif results[t1][t2] > results[t2][t1]:
					perms = [[t1, t2]]
				else:
					perms = [[t1, t2], [t2, t1]]
				oR = R
				R = []
				for ol in oR:
					for subl in perms:
						l = ol.copy()
						for k in range(j-i):
							l[i+k] = subl[k]
						R += [l]
			else:
				oR = R
				R = []
				for ol in oR:
					for subl in permutations(range(i, j)):
						l = ol.copy()
						for k in range(j-i):
							l[i+k] = T[subl[k]]
						R += [l]
					
			i = j
		for l in R:
			if tuple(l) not in Rs:
				Rs[tuple(l)] = 0
			Rs[tuple(l)] += p/len(R)
	else:
		n = len(teams)
		T = teams.copy()
		if R is None:
			R = [[None for i in range(10)]]
		W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
		T.sort(key=lambda t:-W[t])
		i = 0
		j = 0
		alleq = True
		t0 = None
		for t in teams:
			if t0 is None:
				t0 = t
			else:
				if W[t0] != W[t]:
					alleq = False
		if alleq:
			W = {t1:sum(secondhalf[t1][t2] for t2 in results[t1] if t1!=t2) for t1 in teams}
			T.sort(key=lambda t:-W[t])
			alleq = True
			t0 = None
			for t in teams:
				if t0 is None:
					t0 = t
				else:
					if W[t0] != W[t]:
						alleq = False
			if alleq:
				oR = R.copy()
				R.clear()
				for ol in oR:
					for subl in permutations(range(0, n)):
						l = ol.copy()
						for k in range(n):
							l[offset+i+k] = T[subl[k]]
						R += [l]
			else:
				while i<n:
					while j<n and W[T[i]] == W[T[j]]:
						j += 1
					classements(T[i:j], results, p, offset+i, R)
					i = j
		else:
			while i<n:
				while j<n and W[T[i]] == W[T[j]]:
					j += 1
				classements(T[i:j], results, p, offset+i, R)
				i = j
		if terminal:
			#nb = 0
			for l in R:
			#	if W["BKR"] == W["SLY"] and l.index("BKR") < l.index("SLY"):
			#		nb += 1
				if tuple(l) not in Rs:
					Rs[tuple(l)] = 0
				Rs[tuple(l)] += p/len(R)
			#if 2*nb > len(R) and len([t for t in teams if W[t] == W["BKR"]]) == 2:
			#	print("")
			#	pprint([t for t in teams if W[t] == W["BKR"]])
			#	pprint(secondhalf)
	#print(teams, R)

nb = 0
aaa = 0
def trouve(Result, M, results, i, p, probawin, cut=1):
	global nb, teams, aaa
	if i == len(M):
		nb += 1
		aaa += p
		#print(nb, aaa)
		if nb%10000 == 0:
			st, nd = estimaT(nb/2**len(M))
			print("scenario number {}, start {}, estimated end {}".format(nb, st, nd), end='\r')
		classements(teams, results, p)
		#print(Rs)
		#exit(0)
	else:
		Result[i] = 0
		results[M[i][0]][M[i][1]] += 1
		secondhalf[M[i][0]][M[i][1]] += 1
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, i+1, p*probawin[M[i][0]][M[i][1]], probawin, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][0]][M[i][1]] -= 1
		secondhalf[M[i][0]][M[i][1]] -= 1
		Result[i] = 1
		results[M[i][1]][M[i][0]] += 1
		secondhalf[M[i][1]][M[i][0]] += 1
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, i+1, p*probawin[M[i][1]][M[i][0]], probawin, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][1]][M[i][0]] -= 1
		secondhalf[M[i][1]][M[i][0]] -= 1

init(teams, results)
Ntot = 2**len(M)
print(len(M))
print("computing the {} scenarios".format(2**len(M)))

try:
	with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-probawin.out', 'r') as f:
		probawin = json.load(f)
	for t1, t2 in M:
		probawin[t1][t2] *= 2
		probawin[t2][t1] *= 2
except Exception as e:
	print(e)
	print("failed to load probabilities")
	probawin = {t:dict() for t in teams}
	for t1, t2 in M:
		probawin[t1][t2] = 1
		probawin[t2][t1] = 1

trouve(Result, M, results, 0, 1, probawin, cut=cut)
print(f'{qualif/nb},{tie/nb},{out/nb}')
print('')
print("tie8:", tie8)
print(tiet8)

for R in Rs:
	for i in range(len(R)):
		if (i+1, i+1) not in pos[R[i]]:
			pos[R[i]][(i+1, i+1)] = 0
		pos[R[i]][(i+1, i+1)] += Rs[R]

T = teams.copy()
if LEAGUE.lower() == "lec":
	T.sort(key=lambda t:[v[1] for v in sorted([(-pos[t][(i+1,i+1)], i) for i in range(10) if (i+1, i+1) in pos[t]])+[(2**len(M)-sum([pos[t][x] for x in pos[t]]), 8)]])
else:
	T.sort(key=lambda t:[v[1] for v in sorted([(-pos[t][(i+1,i+1)], i) for i in range(10) if (i+1, i+1) in pos[t]])+[(2**len(M)-sum([pos[t][x] for x in pos[t]]), 6)]])
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-summer.out', 'w') as f:
	data = {
		"pos":{t:[p for p in pos[t]] for t in teams}, 
		"nb":{t:[pos[t][p] for p in pos[t]] for t in teams},
		"teams":T,
		"logos":logos,
		"N":Ntot
		}
	json.dump(data, f)
