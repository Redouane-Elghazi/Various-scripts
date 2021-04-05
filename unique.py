import matplotlib.pyplot as plt
from time import time
from random import randint

def check_set(l):
	return (len(l) != len(set(l)))

def check_sort(l):
	l.sort()
	for i in range(len(l)-1):
		if l[i] == l[i+1]:
			return True
	return False

def check_brute(l):
	for i in range(len(l)):
		for j in range(i):
			if l[i] == l[j]:
				return True
	return False

def generate(n):
	return [randint(1,n) for i in range(n)]

def benchmark(algos, n, sample=300):
	res = {algo:[0]*(n+1) for algo in algos}
	for i in range(n+1):
		print("n =", i, end="\r")
		for _ in range(sample):
			l = generate(i)
			for algo in algos:
				l_copy = l.copy()
				t = time()
				algo(l_copy)
				t = time()-t
				res[algo][i] += t
		for algo in algos:
			res[algo][i]/=sample
	return res

if __name__ == '__main__':
	algos = [check_set, check_sort, check_brute]
	n = 1000
	data = benchmark(algos, n)
	for algo in algos:
		plt.plot(list(range(n+1)), data[algo], label=algo.__name__)
	plt.legend()
	plt.show()