import sys
from pprint import pprint

n = int(input())
teams = dict()
W = []
for i in range(n):
	t, w, l = input().split()
	w, l = int(w), int(l)
	teams[t] = len(teams)
	W += [w]
T = list(teams.keys())

m = int(input())
M = []
for j in range(m):
	s = input().split()
	for i in range(n//2):
		M += [(teams[s[2*i]], teams[s[2*i+1]])]

Result = [0]*len(M)

T.sort(key=lambda t:-W[teams[t]])
print(T)

pos = {t:dict() for t in T}

nb = 0
def trouve(Result, M, W, i):
	global nb, T
	if i == len(M):
		nb += 1
		print(nb, end='\r')
		T.sort(key=lambda t:-W[teams[t]])
		i = 0
		j = 0
		while i<n:
			while j<n and W[teams[T[i]]] == W[teams[T[j]]]:
				j += 1
			p = (i+1, j)
			for k in range(i,j):
				if p not in pos[T[k]]:
					pos[T[k]][p] = 0
				pos[T[k]][p] += 1
			i = j
	else:
		Result[i] = 0
		W[M[i][0]] += 1
		trouve(Result, M, W, i+1)
		W[M[i][0]] -= 1
		Result[i] = 1
		W[M[i][1]] += 1
		trouve(Result, M, W, i+1)
		W[M[i][1]] -= 1

trouve(Result, M, W, 0)
pprint(pos)
