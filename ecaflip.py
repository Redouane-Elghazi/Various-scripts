from random import randint

def sample(base_crit, bonus_crit, N=1000):
	cur = base_crit
	res = 0
	for i in range(N):
		coin = randint(1,100)
		if coin <= cur:
			res += 1
			cur = base_crit
		else:
			cur += bonus_crit
	return 100*res/N

print("base\tbonus\tavg\tdiff")

for bonus in [6,8]:
	for base in range(0, 101, 10):
		r = sample(base, bonus, 100000)
		print("{}\t{}\t{}\t{}".format(base, bonus, r, r-base))