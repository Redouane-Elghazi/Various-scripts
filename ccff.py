from math import comb, factorial
from random import randrange, random

n = 35

def proba(F, C, n=None):
	if n is None:n=F+C
	p_brut = (comb(C, 4)*comb(F, 5) + comb(C, 5)*comb(F, 4) + comb(C, 6)*comb(F, 3) + comb(C, 7)*comb(F, 2) + comb(C, 8)*comb(F, 1))/comb(n, 9)
	p_fail = comb(C, 5)*comb(F, 4)/comb(n,9)*comb(5, 2)/comb(9,2) + comb(C, 4)*comb(F, 5)/comb(n,9)*(comb(4, 2)+comb(4, 1)*comb(5, 1))/comb(9,2)
	return p_brut - p_fail

for F in range(n+1):
	C = n-F
	p = proba(F=F, C=C, n=n)
	print(F, C, p)
	
	
def sample(F, C, p, n=None):
	if n is None:n=F+C
	l = ['F']*F+['C']*C
	H = []
	for t in range(5):
		H += [l.pop(randrange(0, len(l)))]
	if H.count('F') == 0 or H.count('F') >=3:
		l = ['F']*F+['C']*C
		H = []
		for t in range(5):
			H += [l.pop(randrange(0, len(l)))]
	for i in range(2):
		aa, bb = None, None
		for a in range(5):
			for b in range(a):
				if H[a] == 'C' and H[b] == 'C' and random() <= p:
					aa = a
					bb = b
		if aa is None:
			return False
		H.pop(aa)
		H.pop(bb)
		for t in range(2):
			H += [l.pop(randrange(0, len(l)))]
	if 'F' not in H:
		return False
	return True

N = 100000
for F in range(36):
	nb = 0
	for i in range(N):
		if sample(F=F, C=n-F, p=0.95):
			nb += 1
	print(F, nb/N)
