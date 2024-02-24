import leaguepedia_parser
import sys
from pprint import pprint
import json
from random import random
from math import log, exp

LEAGUE = sys.argv[1]
YEAR = sys.argv[2]
SEASON = sys.argv[3]
if len(sys.argv)>4:
	cut = int(sys.argv[4])
else:
	cut = 1
if len(sys.argv)>5:
	suff = sys.argv[5]
else:
	suff = ""

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
	"BK ROG Esports":"BKR",
	"Aegis (French Team)":"AEG",
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
match_import = dict()
logos = dict()
secondhalf = dict()
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
	print(t1, t2)
	if w == t1:
		res.winner = "BLUE"
	else:
		res.winner = "RED"
	return res
addedmatches=[]
interrestingpairs = [("SLY", "KC")]#, ("BKR", "KC"), ("SLY", "BKR")]
#interrestingpairs += [(t1, t2) for t1 in {'XL', 'VIT', 'SK', 'MAD'} for t2 in {'XL', 'VIT', 'SK', 'MAD'} if t1<t2]
prob2 = {}
prob = {p:0 for p in interrestingpairs}
#addedmatches += [newmatch("Karmine Corp", "LDLC OL", "LDLC OL")]
#addedmatches += [newmatch("Karmine Corp", "Vitality.Bee", "Vitality.Bee")]
#addedmatches += [newmatch("Solary", "Vitality.Bee", "Vitality.Bee")]
"""
addedmatches += [newmatch("Misfits Gaming", "Astralis", "Misfits Gaming")]
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

if suff:
	if int(suff)^1:
		addedmatches += [newmatch("Misfits Gaming", "SK Gaming", "Misfits Gaming")]
	else:
		addedmatches += [newmatch("Misfits Gaming", "SK Gaming", "SK Gaming")]
	if int(suff)^2:
		addedmatches += [newmatch("Astralis", "Rogue (European Team)", "Astralis")]
	else:
		addedmatches += [newmatch("Astralis", "Rogue (European Team)", "Rogue (European Team)")]
	if int(suff)^4:
		addedmatches += [newmatch("MAD Lions", "Excel Esports", "MAD Lions")]
	else:
		addedmatches += [newmatch("MAD Lions", "Excel Esports", "Excel Esports")]
	if int(suff)^8:
		addedmatches += [newmatch("Fnatic", "Team BDS", "Fnatic")]
	else:
		addedmatches += [newmatch("Fnatic", "Team BDS", "Team BDS")]

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
	global pos, M, Result, match_import
	pos = {t:dict() for t in teams}
	M = []
	for t1 in teams:
		for t2 in teams:
			if t1 < t2:
				for i in range(2-results[t1][t2] - results[t2][t1]):
					M += [(t1,t2)]
	Result = [0]*len(M)
	match_import = {t:[[[0,0,0], [0,0,0]] for i in range(len(M))] for t in teams}

def playoff(p):
	a,b = p
	if b<=6:
		return 2
	if a<=6:
		return 1
	if 6<a:
		return 0
		
def playoff2(p1, p2):
	if p1 == p2:
		a,b = p1
		if playoff(p1):
			if b<=6:
				return 1
			else:
				return (6-a+1)*(6-a)/((b-a+1)*(b-a))
		else:
			return 0
	else:
		if playoff(p1) and playoff(p2):
			a, b = max(p1, p2)
			if b<=6:
				return 1
			else:
				return (6-a+1)/(b-a+1)
		else:
			return 0
		
def top2(p1, p2):
	if p1 == p2:
		a,b = p1
		if a==1:
			if b<=2:
				return 1
			else:
				return (2-a+1)*(2-a)/((b-a+1)*(b-a))
		else:
			return 0
	else:
		if p1[0]<=2 and p2[0]<=2:
			a, b = max(p1, p2)
			if b<=2:
				return 1
			else:
				return (2-a+1)/(b-a+1)
		else:
			return 0

curR = dict()

def affect(t, p):
	global pos, Result, match_import, M
	if p not in pos[t]:
		pos[t][p] = 0
	pos[t][p] += 1
	curR[t] = p
	P = playoff(p)
	for i in range(len(M)):
		match_import[t][i][Result[i]][P] += 1
	
acc = 0
def tiebreaker(teams, results, offset):
	global acc
	n = len(teams)
	"""p = (offset+1, offset+n)
	for k in range(n):
		affect(teams[k], p)
	return"""
	check = False
	if set(teams) == {"BDSA", "LDLC"}:
		check = False#True
		loc = acc
		acc += 1
	if n == 0:
		pass
	elif n == 1:
		t = teams[0]
		affect(t, (offset+1, offset+1))
	else:
		T = teams.copy()
		W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
		if check:
			print(acc)
			print(T)
			print(W)
		L = {t1:sum(results[t2][t1] for t2 in teams if t1!=t2) for t1 in teams}
		T.sort(key=lambda t:-W[t])
		if check:
			print(acc)
			print(T)
			print(W)
		if LEAGUE == 'LEC' or LEAGUE == "LFL":
			i = 0
			while W[T[i]] > L[T[i]]:
				i += 1
			j = i
			while j<n and W[T[j]] == L[T[j]]:
				j += 1
			if check:
				print(acc)
				print(T)
				print(W)
			if i != 0:
				tiebreaker(T[:i], results, offset)
				tiebreaker(T[i:j], results, offset+i)
				tiebreaker(T[j:], results, offset+j)
			else:
				if check:
					print(acc)
					print(T)
					print(W)
				W = {t1:sum(secondhalf[t1][t2] for t2 in secondhalf[t1] if t1!=t2) for t1 in teams}
				if check:
					print(acc)
					print(T)
					print(W)
				T.sort(key=lambda t:-W[t])
				i = 0
				j = 0
				while i<n:
					while j<n and W[T[i]] == W[T[j]]:
						j += 1
					p = (offset+i+1, offset+j)
					for k in range(i,j):
						affect(T[k], p)
					i = j
		else:
			print("tie breaker for this league not implemented", file=sys.stderr)
			exit(0)

def classements(teams, results):
	global foo, bar
	n = len(teams)
	T = teams.copy()
	W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
	T.sort(key=lambda t:-W[t])
	i = 0
	j = 0
	while i<n:
		while j<n and W[T[i]] == W[T[j]]:
			j += 1
		if i+1==j:
			p = (i+1, j)
			affect(T[i], p)
		else:
			tiebreaker(T[i:j], results, i)
		i = j
	for t1, t2 in interrestingpairs:
		prob[(t1, t2)] += playoff2(curR[t1], curR[t2])
		if playoff2(curR[t1], curR[t2]) != 0:
			print(curR)
	for t1 in teams:
		for t2 in teams:
			if t1 < t2:
				if top2(curR[t1], curR[t2]) != 0:
					if (t1, t2) not in prob2:
						prob2[(t1, t2)] = 0
					prob2[(t1, t2)] += top2(curR[t1], curR[t2])
	if curR["LDLC"][1] > 6:
		#print(curR)
		bar += [(curR["LDLC"], foo.copy())]

nb = 0
foo = dict()
bar = list()
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
		foo[M[i]] = M[i][0]
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
		foo[M[i]] = M[i][1]
		if random() < exp(log(1/cut)/len(M)):
			trouve(Result, M, results, secondhalf, i+1, cut=cut)
		else:
			nb += 2**(len(M)-i-1)
		results[M[i][1]][M[i][0]] -= 1
		if results[M[i][1]][M[i][0]]+results[M[i][0]][M[i][1]] != 0:
			secondhalf[M[i][1]][M[i][0]] -= 1

init(teams, results)
print(M)
print("computing the {} scenarios".format(2**len(M)))

trouve(Result, M, results, secondhalf, 0, cut=cut)
pprint(pos)
r = dict()
for t in pos:
	r[t] = [0,0,0]
	for p in pos[t]:
		r[t][playoff(p)] += pos[t][p]
T = teams.copy()
T.sort(key=lambda t:(-sum(results[t][t2] for t2 in results[t]), -r[t][2], -r[t][1]))
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto{suff}.out', 'w') as f:
	data = {
		"pos":{t:[p for p in pos[t]] for t in teams}, 
		"nb":{t:[pos[t][p] for p in pos[t]] for t in teams},
		"teams":T,
		"logos":logos
		}
	json.dump(data, f)
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-playoff{suff}.out', 'w') as f:
	print("Team,,Percentage of scenarios in playoff,Percentage of scenarios in a tiebreak for playoff,Percentage of scenarios out of playoff", file=f)
	for t in T:
		print("{},=IMAGE(\"{}\"),{},{},{}".format(t, logos[t], r[t][2]/sum(r[t]), r[t][1]/sum(r[t]), r[t][0]/sum(r[t])), file=f)
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-pos{suff}.out', 'w') as f:
	print("Team,,Best position,Worst position", file=f)
	for t in T:
		print("{},=IMAGE(\"{}\"),{},{}".format(t, logos[t], min(p[0] for p in pos[t]), max(p[1] for p in pos[t])), file=f)
with open(f'{LEAGUE}/{LEAGUE}-{SEASON}-{YEAR}-fullauto-playoff-cond{suff}.out', 'w') as f:
	print("Team,Team1,Team2,No playoffs with team1 wins,Tiebreaker with team1 wins,Playoffs with team1 wins,No playoffs with team2 wins,Tiebreaker with team2 wins,Playoffs with team2 wins", file=f)
	for t in teams:
		for i in range(len(M)):
			t1, t2 = M[i]
			k, l = 0, 1
			if t2 == t:
				t1, t2 = t2, t1
				k, l = l, k
			print("{},{},{},{},{},{},{},{},{}".format(t, t1, t2, *match_import[t][i][k], *match_import[t][i][l]), file=f)

for t1, t2 in interrestingpairs:
	print("{},{},{}".format(t1, t2, prob[(t1,t2)]/2**len(M)))
for t1, t2 in prob2:
	print("{},{},{}".format(t1, t2, prob2[(t1,t2)]/2**len(M)))

l = [match for match in bar[0][1]]
print(",".join(["rank"]+[m[0]+"-"+m[1] for m in l]))
for s in bar:
	print(",".join([str(s[0][0])+"-"+str(s[0][1])]+[s[1][match] for match in l]))
