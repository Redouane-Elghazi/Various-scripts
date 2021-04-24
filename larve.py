import sys
from fractions import Fraction
from matplotlib import pyplot as plt

probMem = [[[[-1 for _ in range(15)] for _ in range(15)] for _ in range(15)] for _ in range(15)]

nb = 0

def prob(i, j, k, l):
	if i>=15:
		return Fraction(1)
	if max(j,k,l)>=15:
		return Fraction(0)
	if probMem[i][j][k][l] == -1:
		global nb
		nb += 1
		print(nb, 15**4, file=sys.stderr)
		res = 0
		for a in range(1,4):
			for b in range(1,4):
				for c in range(1,4):
					for d in range(1,4):
						res += (Fraction(1,3)**4)*prob(i+a, j+b, k+c, l+d)
		probMem[i][j][k][l] = res
	return probMem[i][j][k][l]

probMemT = [[[[-1 for _ in range(15)] for _ in range(15)] for _ in range(15)] for _ in range(15)]

nb = 0

def probT(i, j, k, l):
	if max(i, j, k, l) >=15:
		return [1 if t==0 else 0 for t in range(16)]
	if probMemT[i][j][k][l] == -1:
		global nb
		nb += 1
		print(nb, 15**4, file=sys.stderr)
		res = [0 for _ in range(16)]
		for a in range(1,4):
			for b in range(1,4):
				for c in range(1,4):
					for d in range(1,4):
						sv = probT(i+a, j+b, k+c, l+d)
						for t in range(15):
							res[t+1] += (Fraction(1,3)**4)*sv[t]
		probMemT[i][j][k][l] = res
	return probMemT[i][j][k][l]

r = probT(0,0,0,0)
for t in range(15):
	r[t+1] = r[t+1]+r[t]
plt.plot(range(16), r)
plt.show()