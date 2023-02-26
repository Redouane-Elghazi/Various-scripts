def separations(l):
	lbase = l
	if l == []:
		yield [], []
		return
#		return [([], [])]
	l = l.copy()
	a = l[-1]
	l.pop(-1)
	b = l[-1]
	l.pop(-1)
	for cur in range(len(l)+1):
		for l1, l2 in separations(l):
			yield [min(a, b)]+l1, [max(a, b)]+l2 
		if cur != len(l):
			l[cur], b = b, l[cur]

def gsl(teams):
	res = {t:0 for t in teams}
	N = 0
	for l11, l12 in separations(teams):
		for l21, l22 in separations(l11):
			for l23, l24 in separations(l12):
				for l31, l32 in separations(l22+l23):
					for t in l21+l31:
						res[t] += 1
					N += 1
	return res, N

def gsl_per(teams):
	scenar, N = gsl(teams)
	res = {t:scenar[t]/N for t in teams}
	return res

def suffix(i):
	if i == 1:
		return 'st'
	if i == 2:
		return 'nd'
	if i == 3:
		return 'rd'
	if i <= 10:
		return 'th'
	return '(w)th'

per = gsl_per(list(range(8)))

for i in range(8):
	print(f'{i+1}{suffix(i+1)} team\t{round(100*per[i])}%')
