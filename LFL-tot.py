import sys
from pprint import pprint

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

M = []
for t1 in teams:
	for t2 in teams:
		if t1 < t2:
			for i in range(2-results[t1][t2] - results[t2][t1]):
				M += [(t1,t2)]

Result = [0]*len(M)

pos = {t:dict() for t in teams}

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

	if n == 2:
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
		for i in range(n):
			if W[T[i]] == 2*(n-i-1):
				affect(T[i], (offset+i+1, offset+i+1))
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

trouve(Result, M, results, 0)
pprint(pos)
