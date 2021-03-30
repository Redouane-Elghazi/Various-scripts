from functools import lru_cache

@lru_cache(maxsize=None)
def comb_replacements(n, k):
	if k == 0:
		return 1
	if n == 0:
		return 0
	return comb_replacements(n-1, k) + comb_replacements(n, k-1)

@lru_cache(maxsize=None)
def comb_no_replacements(n, k):
	if k == 0:
		return 1
	if n == 0:
		return 0
	return comb_no_replacements(n-1, k) + comb_no_replacements(n-1, k-1)

seconds_to_years = 365*24*60*60
approx_nb = 27000*seconds_to_years

n1 = 1
while comb_replacements(n1,5) < approx_nb:
	n1 += 1
n2 = 1
while comb_no_replacements(n2,5) < approx_nb:
	n2 += 1
print("approx number of comb", approx_nb)
print(
	"found number of comb ", comb_replacements(n1, 5),
	"with", n1, "cards and replacements, needing",
	comb_replacements(n1, 5)/seconds_to_years, "years")
print("found number of comb ", comb_no_replacements(n2, 5),
	"with", n2, "cards and no replacements, needing",
	comb_no_replacements(n2, 5)/seconds_to_years, "years")
