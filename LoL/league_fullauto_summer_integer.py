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
	}
	
complete2short.update({
	"Akroma": "AKR",
	"Atletec": "ATL",
	"Joblife": "JL",
	"Klanik Esport": "KE",
	"Lille Esport": "LiL",
	"MHSC Esport": "MHSC",
	"MS Company": "MS",
	"Project Conquerors": "PCS",
	"Team Du Sud": "TDS",
	"ViV Esport": "ViV"
	})

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
"""addedmatches += [newmatch("Team Heretics", "Karmine Corp", "Karmine Corp")]
addedmatches += [newmatch("Rogue (European Team)", "Karmine Corp", "Karmine Corp")]
addedmatches += [newmatch("SK Gaming", "Karmine Corp", "Karmine Corp")]
addedmatches += [newmatch("Team BDS", "Karmine Corp", "Karmine Corp")]
addedmatches += [newmatch("Rogue (European Team)", "MAD Lions KOI", "Rogue (European Team)")]
addedmatches += [newmatch("Rogue (European Team)", "Team BDS", "Rogue (European Team)")]
addedmatches += [newmatch("Rogue (European Team)", "GIANTX", "Rogue (European Team)")]
addedmatches += [newmatch("Fnatic", "GIANTX", "GIANTX")]
addedmatches += [newmatch("G2 Esports", "GIANTX", "GIANTX")]
addedmatches += [newmatch("MAD Lions KOI", "GIANTX", "MAD Lions KOI")]
addedmatches += [newmatch("MAD Lions KOI", "Fnatic", "Fnatic")]
addedmatches += [newmatch("MAD Lions KOI", "Team Vitality", "MAD Lions KOI")]
addedmatches += [newmatch("G2 Esports", "Team Vitality", "Team Vitality")]
addedmatches += [newmatch("SK Gaming", "Team Vitality", "Team Vitality")]
addedmatches += [newmatch("Team Heretics", "Team Vitality", "Team Heretics")]
"""
addedmatches += [newmatch("Team BDS", "Karmine Corp", "Team BDS")]
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
					for i in range(1-results[t1][t2] - results[t2][t1]):
						M += [(t1,t2)]
				else:
					for i in range(2-results[t1][t2] - results[t2][t1]):
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
def classements(teams, results, offset=0, R=None):
	global Rs, tie8
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
			Rs[tuple(l)] += 1/len(R)
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
					classements(T[i:j], results, offset+i, R)
					i = j
		else:
			while i<n:
				while j<n and W[T[i]] == W[T[j]]:
					j += 1
				classements(T[i:j], results, offset+i, R)
				i = j
		if terminal:
			#nb = 0
			for l in R:
			#	if W["BKR"] == W["SLY"] and l.index("BKR") < l.index("SLY"):
			#		nb += 1
				if tuple(l) not in Rs:
					Rs[tuple(l)] = 0
				Rs[tuple(l)] += 1/len(R)
			#if 2*nb > len(R) and len([t for t in teams if W[t] == W["BKR"]]) == 2:
			#	print("")
			#	pprint([t for t in teams if W[t] == W["BKR"]])
			#	pprint(secondhalf)
	#print(teams, R)

nb = 0
def trouve(Result, M, results, i, cut=1):
	global nb, teams
	if i == len(M):
		nb += 1
		if nb%10000 == 0:
			st, nd = estimaT(nb/2**len(M))
			print("scenario number {}, start {}, estimated end {}".format(nb, st, nd), end='\r')
		classements(teams, results)
		#print(Rs)
		#exit(0)
	else:
		Result[i] = 0
		results[M[i][0]][M[i][1]] += 1
		secondhalf[M[i][0]][M[i][1]] += 1
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, i+1, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][0]][M[i][1]] -= 1
		secondhalf[M[i][0]][M[i][1]] -= 1
		Result[i] = 1
		results[M[i][1]][M[i][0]] += 1
		secondhalf[M[i][1]][M[i][0]] += 1
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, i+1, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][1]][M[i][0]] -= 1
		secondhalf[M[i][1]][M[i][0]] -= 1

init(teams, results)
Ntot = 2**len(M)
print(len(M))
print("computing the {} scenarios".format(2**len(M)))

trouve(Result, M, results, 0, cut=cut)
print('')
print("tie8:", tie8)
print(tiet8)

for R in Rs:
	for i in range(len(R)):
		if (i+1, i+1) not in pos[R[i]]:
			pos[R[i]][(i+1, i+1)] = 0
		pos[R[i]][(i+1, i+1)] += Rs[R]

T = teams.copy()
T.sort(key=lambda t:[v[1] for v in sorted([(-pos[t][(i+1,i+1)], i) for i in range(10) if (i+1, i+1) in pos[t]])+[(2**len(M)-sum([pos[t][x] for x in pos[t]]), 8)]])
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-summer.out', 'w') as f:
	data = {
		"pos":{t:[p for p in pos[t]] for t in teams}, 
		"nb":{t:[pos[t][p] for p in pos[t]] for t in teams},
		"teams":T,
		"logos":logos,
		"N":Ntot
		}
	json.dump(data, f)
