import leaguepedia_parser
import sys
from pprint import pprint
import json

LEAGUE = sys.argv[1]
YEAR = sys.argv[2]
SEASON = sys.argv[3]

games = leaguepedia_parser.get_games("{}/{} Season/{} Season".format(LEAGUE, YEAR, SEASON))

complete2short = {
	"Team Oplon":"OPL",
	"Mirage Elyandra":"ME",
	"GameWard":"GW",
	"GamersOrigin":"GO",
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
	if w == t1:
		res.winner = "BLUE"
	else:
		res.winner = "RED"
	return res
addedmatches=[]
#addedmatches += [newmatch("Misfits Premier", "Vitality.Bee", "Misfits Premier")]
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
	

def affect(t, p):
	global pos, Result, match_import, M
	if p not in pos[t]:
		pos[t][p] = 0
	pos[t][p] += 1
	P = playoff(p)
	for i in range(len(M)):
		match_import[t][i][Result[i]][P] += 1
	

def tiebreaker(teams, results, offset):
	n = len(teams)
	"""p = (offset+1, offset+n)
	for k in range(n):
		affect(teams[k], p)
	return"""
	if n == 0:
		pass
	elif n == 1:
		t = teams[0]
		affect(t, (offset+1, offset+1))
	elif n == 2:
		t1, t2 = teams
		if results[t1][t2] > results[t2][t1]:
			affect(t1, (offset+1, offset+1))
			affect(t2, (offset+2, offset+2))
		elif results[t1][t2] < results[t2][t1]:
			affect(t1, (offset+2, offset+2))
			affect(t2, (offset+1, offset+1))
		else:
			affect(t1, (offset+1, offset+2))
			affect(t2, (offset+1, offset+2))
	else:
		T = teams.copy()
		W = {t1:sum(results[t1][t2] for t2 in teams if t1!=t2) for t1 in teams}
		L = {t1:sum(results[t2][t1] for t2 in teams if t1!=t2) for t1 in teams}
		T.sort(key=lambda t:-W[t])
		if LEAGUE == 'LEC' or LEAGUE == "LFL":
			i = 0
			while W[T[i]] > L[T[i]]:
				i += 1
			j = i
			while j<n and W[T[j]] == L[T[j]]:
				j += 1
			if i != 0:
				tiebreaker(T[:i], results, offset)
				tiebreaker(T[i:j], results, offset+i)
				tiebreaker(T[j:], results, offset+j)
			else:
				W = {t1:sum(secondhalf[t1][t2] for t2 in secondhalf[t1] if t1!=t2) for t1 in teams}
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

nb = 0
def trouve(Result, M, results, secondhalf, i):
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
		trouve(Result, M, results, secondhalf, i+1)
		results[M[i][0]][M[i][1]] -= 1
		if results[M[i][0]][M[i][1]]+results[M[i][1]][M[i][0]] != 0:
			secondhalf[M[i][0]][M[i][1]] -= 1
		Result[i] = 1
		if results[M[i][1]][M[i][0]]+results[M[i][0]][M[i][1]] != 0:
			secondhalf[M[i][1]][M[i][0]] += 1
		results[M[i][1]][M[i][0]] += 1
		trouve(Result, M, results, secondhalf, i+1)
		results[M[i][1]][M[i][0]] -= 1
		if results[M[i][1]][M[i][0]]+results[M[i][0]][M[i][1]] != 0:
			secondhalf[M[i][1]][M[i][0]] -= 1

init(teams, results)
trouve(Result, M, results, secondhalf, 0)
pprint(pos)
r = dict()
for t in pos:
	r[t] = [0,0,0]
	for p in pos[t]:
		r[t][playoff(p)] += pos[t][p]
T = teams.copy()
T.sort(key=lambda t:(-r[t][2], -r[t][1]))
with open("{}/{}-{}-{}-fullauto.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'w') as f:
	data = {
		"pos":{t:[p for p in pos[t]] for t in teams}, 
		"nb":{t:[pos[t][p] for p in pos[t]] for t in teams},
		"teams":T
		}
	json.dump(data, f)
with open("{}/{}-{}-{}-fullauto-playoff.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'w') as f:
	print("Team,,Percentage of scenarios in playoff,Percentage of scenarios in a tiebreak for playoff,Percentage of scenarios out of playoff", file=f)
	for t in T:
		print("{},=IMAGE(\"{}\"),{},{},{}".format(t, logos[t], r[t][2]/sum(r[t]), r[t][1]/sum(r[t]), r[t][0]/sum(r[t])), file=f)
with open("{}/{}-{}-{}-fullauto-pos.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'w') as f:
	print("Team,,Best position,Worst position", file=f)
	for t in T:
		print("{},=IMAGE(\"{}\"),{},{}".format(t, logos[t], min(p[0] for p in pos[t]), max(p[1] for p in pos[t])), file=f)
with open("{}/{}-{}-{}-fullauto-playoff-cond.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'w') as f:
	print("Team,Team1,Team2,No playoffs with team1 wins,Tiebreaker with team1 wins,Playoffs with team1 wins,No playoffs with team2 wins,Tiebreaker with team2 wins,Playoffs with team2 wins", file=f)
	for t in teams:
		for i in range(len(M)):
			t1, t2 = M[i]
			k, l = 0, 1
			if t2 == t:
				t1, t2 = t2, t1
				k, l = l, k
			print("{},{},{},{},{},{},{},{},{}".format(t, t1, t2, *match_import[t][i][k], *match_import[t][i][l]), file=f)

