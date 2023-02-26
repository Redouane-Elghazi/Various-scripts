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
	"Rogue (European Team)":"RGE",
	"Misfits Gaming":"MSF",
	"Fnatic":"FNC",
	}

n = 0
teams = []
results = dict()
logos = dict()
secondhalf = dict()
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
addedmatches += [newmatch("Rogue (European Team)", "MAD Lions", "Rogue (European Team)")]
addedmatches += [newmatch("G2 Esports", "Excel Esports", "G2 Esports")]
addedmatches += [newmatch("Team Vitality", "Astralis", "Astralis")]
addedmatches += [newmatch("Team BDS", "Excel Esports", "Team BDS")]
addedmatches += [newmatch("Misfits Gaming", "MAD Lions", "Misfits Gaming")]
addedmatches += [newmatch("SK Gaming", "Rogue (European Team)", "SK Gaming")]
addedmatches += [newmatch("G2 Esports", "Fnatic", "G2 Esports")]
"""
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
			logos[name] = leaguepedia_parser.get_team_logo(t.sources.leaguepedia.name)
	blue = complete2short[g.teams.BLUE.sources.leaguepedia.name]
	red = complete2short[g.teams.RED.sources.leaguepedia.name]
	if g.winner == 'RED':
		if results[red][blue]+results[blue][red] != 0:
			secondhalf[red][blue] += 1
		results[red][blue] += 1
	elif g.winner == 'BLUE':
		if results[red][blue]+results[blue][red] != 0:
			secondhalf[blue][red] += 1
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
				for i in range(2-results[t1][t2] - results[t2][t1]):
					M += [(t1,t2)]
	Result = [0]*len(M)


curR = dict()

def affect(t, p):
	global pos, Result, M
	if p not in pos[t]:
		pos[t][p] = 0
	pos[t][p] += 1
	curR[t] = p
	
foobar = 0
poss = False
def tiebreaker(teams, results, offset, R):
	global foobar, poss
	n = len(teams)
	"""p = (offset+1, offset+n)
	for k in range(n):
		affect(teams[k], p)
	return"""
	if n == 0:
		pass
	elif n == 1:
		t = teams[0]
		for l in R:
			l[offset] = t
	else:
		T = teams.copy()
		W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
		L = {t1:sum(results[t2][t1] for t2 in teams if t1!=t2) for t1 in teams}
		T.sort(key=lambda t:-W[t])
		i = 0
		while W[T[i]] > L[T[i]]:
			i += 1
		j = i
		while j<n and W[T[j]] == L[T[j]]:
			j += 1
		if i != 0:
			R = tiebreaker(T[:i], results, offset, R)
			R = tiebreaker(T[i:j], results, offset+i, R)
			R = tiebreaker(T[j:], results, offset+j, R)
		else:
			W = {t1:sum(secondhalf[t1][t2] for t2 in secondhalf[t1] if t1!=t2) for t1 in teams}
			T.sort(key=lambda t:-W[t])
			i = 0
			j = 0
			while i<n:
				while j<n and W[T[i]] == W[T[j]]:
					j += 1
				
				oR = R
				R = []
				if i+1 != j and offset+i+1<=6:
					if poss:
						poss = False
						foobar += 1
						print(f'Scénario {foobar} :')
					print(f'\t{" vs ".join(T[i:j])} pour les places {offset+i+1} à {offset+j}')
				for ol in oR:
					for subl in permutations(range(i, j)):
						l = ol.copy()
						for k in range(j-i):
							l[offset+i+k] = T[subl[k]]
						R += [l]
				i = j
	return R

def classements(teams, results):
	global Rs, poss
	poss = True
	n = len(teams)
	T = teams.copy()
	R = [[None for i in range(10)]]
	W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
	T.sort(key=lambda t:-W[t])
	i = 0
	j = 0
	while i<n:
		while j<n and W[T[i]] == W[T[j]]:
			j += 1
		if i+1==j:
			oR = R
			R = []
			for ol in oR:
				for subl in permutations(range(i, j)):
					l = ol.copy()
					for k in range(j-i):
						l[i+k] = T[subl[k]]
					R += [l]
		else:
			R = tiebreaker(T[i:j], results, i, R)
		i = j
	for l in R:
		if l[0] == "XL":
			for i in range(15):
				print(M[i][0], M[i][1], secondhalf[M[i][0]][M[i][1]])
		if tuple(l) not in Rs:
			Rs[tuple(l)] = 0
		Rs[tuple(l)] += 1/len(R)


nb = 0
def trouve(Result, M, results, secondhalf, i, cut=1):
	global nb, teams
	if i == len(M):
		nb += 1
		if nb%10000 == 0:
			print("scenario number {}".format(nb), end='\r')
		classements(teams, results)
	else:
		Result[i] = 0
		if results[M[i][0]][M[i][1]]+results[M[i][1]][M[i][0]] != 0:
			secondhalf[M[i][0]][M[i][1]] += 1
		results[M[i][0]][M[i][1]] += 1
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, secondhalf, i+1, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][0]][M[i][1]] -= 1
		if results[M[i][0]][M[i][1]]+results[M[i][1]][M[i][0]] != 0:
			secondhalf[M[i][0]][M[i][1]] -= 1
		Result[i] = 1
		if results[M[i][1]][M[i][0]]+results[M[i][0]][M[i][1]] != 0:
			secondhalf[M[i][1]][M[i][0]] += 1
		results[M[i][1]][M[i][0]] += 1
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, secondhalf, i+1, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][1]][M[i][0]] -= 1
		if results[M[i][1]][M[i][0]]+results[M[i][0]][M[i][1]] != 0:
			secondhalf[M[i][1]][M[i][0]] -= 1

init(teams, results)
Ntot = 2**len(M)
print("computing the {} scenarios".format(2**len(M)))

trouve(Result, M, results, secondhalf, 0, cut=cut)
print('')

for R in Rs:
	qualif = R[:6]
	totpts = [(basepts[R[i]]+sumpts[i], sumpts[i], R[i]) for i in range(6)]
	totpts.sort(reverse=True)
	if totpts[0][2] == "XL":
		print(totpts)
	for i in range(6):
		if totpts[i][0] == totpts[i-1][0] and totpts[i][1] == totpts[i-1][1]:
			print(f'oof {totpts[i][2]} {totpts[i-1][2]} {totpts[i][0]} {totpts[i][1]}')
		if (i+1, i+1) not in pos[totpts[i][2]]:
			pos[totpts[i][2]][(i+1, i+1)] = 0
		pos[totpts[i][2]][(i+1, i+1)] += Rs[R]

T = teams.copy()
T.sort(key=lambda t:[v[1] for v in sorted([(-pos[t][(i+1,i+1)], i) for i in range(6) if (i+1, i+1) in pos[t]])+[(2**len(M)-sum([pos[t][x] for x in pos[t]]), 6)]])
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-summer.out', 'w') as f:
	data = {
		"pos":{t:[p for p in pos[t]] for t in teams}, 
		"nb":{t:[pos[t][p] for p in pos[t]] for t in teams},
		"teams":T,
		"logos":logos,
		"N":Ntot
		}
	json.dump(data, f)
