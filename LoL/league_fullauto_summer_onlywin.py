import leaguepedia_parser
import sys
from pprint import pprint
import json
from random import random
from math import log, exp
from itertools import permutations

LEAGUE = sys.argv[1]
YEAR = sys.argv[2]
SEASON = sys.argv[3]
if len(sys.argv)>4:
	cut = int(sys.argv[4])
else:
	cut = 1

games = leaguepedia_parser.get_games("{}/{} Season/{} Season".format(LEAGUE, YEAR, SEASON))

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
	}

n = 0
teams = []
results = dict()
logos = dict()
Rs = dict()
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
addedmatches=[]
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
print("There are {} matches".format(len(games+addedmatches)))

for g in games+addedmatches:
	for t in [g.teams.BLUE, g.teams.RED]:
		name = complete2short[t.sources.leaguepedia.name]
		if name not in teams:
			n += 1
			for t1 in teams:
				results[t1][name] = 0
			results[name] = {t1:0 for t1 in teams}
			teams += [name]
			logos[name] = leaguepedia_parser.get_team_logo(t.sources.leaguepedia.name)
	blue = complete2short[g.teams.BLUE.sources.leaguepedia.name]
	red = complete2short[g.teams.RED.sources.leaguepedia.name]
	if g.winner == 'RED':
		results[red][blue] += 1
	elif g.winner == 'BLUE':
		results[blue][red] += 1
	else:
		print("unknown winner: {}".format(g.winner), file=sys.stderr)
	
if LEAGUE == "LEC" and SEASON == "SUMMER":
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
				for i in range(1-results[t1][t2] - results[t2][t1]):
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
	

def classements(teams, results):
	global Rs
	n = len(teams)
	T = teams.copy()
	R = [[None for i in range(10)]]
	W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
	SoV = get_SoV(teams, results)
	T.sort(key=lambda t:(-W[t], -SoV[t]))
	i = 0
	j = 0
	while i<n:
		while j<n and (W[T[i]], SoV[T[i]]) == (W[T[j]], SoV[T[j]]):
			j += 1
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


nb = 0
def trouvewins(t, Result, M, results, i, cut=1):
	global nb, teams
	if i == len(M):
		nb += 1
		if nb%100 == 0:
			print("scenario number {}".format(nb), end='\r')
		classements(teams, results)
	else:
		if M[i][0] == t:
			Result[i] = 0
			results[M[i][0]][M[i][1]] += 1
			if random() < exp(log(1/cut)/len(M)):
				trouvewins(t, Result, M, results, i+1, cut=cut)
			else:
				nb += 2**(len(M)-i-1)
			results[M[i][0]][M[i][1]] -= 1
		elif M[i][1] == t:
			Result[i] = 1
			results[M[i][1]][M[i][0]] += 1
			if random() < exp(log(1/cut)/len(M)):
				trouvewins(t, Result, M, results, i+1, cut=cut)
			else:
				nb += 2**(len(M)-i-1)
			results[M[i][1]][M[i][0]] -= 1
		else:
			Result[i] = 0
			results[M[i][0]][M[i][1]] += 1
			if random() < exp(log(1/cut)/len(M)):
				trouvewins(t, Result, M, results, i+1, cut=cut)
			else:
				nb += 2**(len(M)-i-1)
			results[M[i][0]][M[i][1]] -= 1
			Result[i] = 1
			results[M[i][1]][M[i][0]] += 1
			if random() < exp(log(1/cut)/len(M)):
				trouvewins(t, Result, M, results, i+1, cut=cut)
			else:
				nb += 2**(len(M)-i-1)
			results[M[i][1]][M[i][0]] -= 1

init(teams, results)
Ntot = 2**len([m for m in M if teams[0] not in m])
print("computing the {} scenarios for each team".format(Ntot))

for t in teams:
	if 2**len([m for m in M if t not in m]) != Ntot:
		print("iuhu")
		exit(1)
	print("team {}".format(t))
	Rs = dict()
	nb = 0
	trouvewins(t, Result, M, results, 0, cut=cut)
	print('')

	for R in Rs:
		for i in range(len(R)):
			if R[i] == t:
				if (i+1, i+1) not in pos[R[i]]:
					pos[R[i]][(i+1, i+1)] = 0
				pos[R[i]][(i+1, i+1)] += Rs[R]

T = teams.copy()
T.sort(key=lambda t:[v[1] for v in sorted([(-pos[t][(i+1,i+1)], i) for i in range(8) if (i+1, i+1) in pos[t]])+[(2**len(M)-sum([pos[t][x] for x in pos[t]]), 8)]])
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-summer-onlywin.out', 'w') as f:
	data = {
		"pos":{t:[p for p in pos[t]] for t in teams}, 
		"nb":{t:[pos[t][p] for p in pos[t]] for t in teams},
		"teams":T,
		"logos":logos,
		"N":Ntot
		}
	json.dump(data, f)
