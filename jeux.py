from random import randint
def ess():
	l = [0]*4
	while True:
		l[0] += randint(1,3)
		if l[0] >= 15:
			return 1
		for i in range(1,4):
			l[i] += randint(1,3)
			if l[i] >= 15:
				return 0

N = 100000
nb = 0
for i in range(N):
	nb += ess()
print(nb/N)