from random import randint, seed
import sys

p = int(sys.argv[1])
n = int(sys.argv[2])
S = int(sys.argv[3])
seed(S)

def is_inv(M, p):
    M = [row[:] for row in M] # make a copy to keep original M unmodified
    N, sign, prev = len(M), 1, 1
    for i in range(N-1):
        if M[i][i] == 0: # swap with another row having nonzero i's elem
            swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
            if swapto is None:
                return False # all M[*][i] are zero => zero determinant
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i+1,N):
            for k in range(i+1,N):
                M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % p
    return M[-1][-1]!=0

def are_inv(mats, i, cur):
	j = len(cur)
	if j == n:
		return is_inv(cur, p)
	if i>=len(mats):
		return True
	res = True
	for k in range(n-j):
		#print("__",i,len(mats),k, len(mats[i]))
		res = res and are_inv(mats, i+1, cur)
		cur += [mats[i][k]]
	res = res and are_inv(mats, i+1, cur)
	for k in range(n-j):
		cur.pop(-1)
	return res

mats = [[[1 if i==j else 0 for i in range(n)] for j in range(n)]]

for c in mats[0]:
	print(*c)

for u in range(p):
	print(u)
	cur = []
	ctt = 0
	for i in range(n):
		print("i:", i, end="\r")
		cur += [[randint(0, p-1) for j in range(n)]]
		ct = 0
		while not(are_inv(mats, i, cur)) and ct<100:
			cur.pop(-1)
			ct += 1
			cur += [[randint(0, p-1) for j in range(n)]]
		ctt += ct
		if not(are_inv(mats, i, cur)):
			print("")
			print("no")
			exit(1)
		print(*cur[-1])
	mats += [cur]
	print("")
	print("fails:",ctt)
