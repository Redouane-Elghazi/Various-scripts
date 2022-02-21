import sys
from pprint import pprint
import json

LEAGUE = 'LEC'
n = int(input().strip())
teams = input().strip().split()
results = {t:dict() for t in teams}
for i in range(n):
	t1 = input().strip()
	for j in range(n):
		t2 = teams[j]
		if t1 != t2:
			w, _, l = input().strip().split()
			w, l = int(w), int(l)
			results[t1][t2] = w
	TOT = input().strip()
	PER = input().strip()


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

def affect(t, p):
	global pos
	if p not in pos[t]:
		pos[t][p] = 0
	pos[t][p] += 1
	

def tiebreaker(teams, results, offset):
	n = len(teams)
	"""p = (offset+1, offset+n)
	for k in range(n):
		affect(teams[k], p)
	return"""
	if n == 1:
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
		T.sort(key=lambda t:-W[t])
		if LEAGUE == 'LEC':
			i = 0
			while W[T[i]] > n-1:
				i += 1
			if i != 0:
				tiebreaker(T[:i], results, offset)
				tiebreaker(T[i:], results, offset+i)
			else:
				p = (offset+1, offset+n)
				for k in range(n):
					affect(T[k], p)
		elif LEAGUE == 'LFL':
			for i in range(n):
				if W[T[i]] == 2*(n-i-1):
					affect(T[i], (offset+i+1, offset+i+1))
					i+=1
				else:
					break
			if i == n:
				return
			elif i == 0:
				p = (offset+1, offset+n)
				for k in range(n):
					affect(T[k], p)
			else:
				tiebreaker(T[i:n], results, offset+i)
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
def trouve(Result, M, results, i):
	global nb, teams
	if i == len(M):
		nb += 1
		print(nb, end='\r')
		classements(teams, results)
	else:
		Result[i] = 0
		results[M[i][0]][M[i][1]] += 1
		trouve(Result, M, results, i+1)
		results[M[i][0]][M[i][1]] -= 1
		Result[i] = 1
		results[M[i][1]][M[i][0]] += 1
		trouve(Result, M, results, i+1)
		results[M[i][1]][M[i][0]] -= 1

init(teams, results)
trouve(Result, M, results, 0)
pprint(pos)
with open("LEC-tot.out", 'w') as f:
	print(pos, file=f)
r = dict()
for t in pos:
	r[t] = [0,0,0]
	for a,b in pos[t]:
		if b<=6:
			r[t][0] += pos[t][(a,b)]
		if a<=6<b:
			r[t][1] += pos[t][(a,b)]
		if 6<a:
			r[t][2] += pos[t][(a,b)]
T = teams.copy()
T.sort(key=lambda t:-r[t][0])
with open("LEC-tot-playoff.out", 'w') as f:
	print("Team,Percentage of scenarios in playoff,Percentage of scenarios in a tiebreak for playoff,Percentage of scenarios out of playoff", file=f)
	for t in T:
		print("{},{},{},{}".format(t, 100*r[t][0]/sum(r[t]), 100*r[t][1]/sum(r[t]), 100*r[t][2]/sum(r[t])), file=f)
exit(0)

def nb_matches(t1, t2, results):
	return results[t1][t2]+results[t2][t1]

def with_one_loose(t, results):
	global teams
	for t2 in teams:
		if t2 != t and nb_matches(t, t2, results)<2:
			results[t2][t] += 1
			init(teams, results)
			trouve(Result, M, results, 0)
			best = 10
			for p in pos[t]:
				best = min(best, p[0])
			print(
				"""if {} loses against {}, """
				"""then they can do at best {}""".format(t, t2, best))
			results[t2][t] -= 1

for t in teams:
	with_one_loose(t, results)
