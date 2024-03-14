import json
import sys
from math import ceil, floor

LEAGUE = sys.argv[1].replace("_", " ").strip()
YEAR = sys.argv[2].strip()
SEASON = sys.argv[3].strip()

with open("{}/{}-{}-{}-fullauto-summer.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'r') as f:
	data = json.load(f)
pos = {t:{tuple(data["pos"][t][i]):data["nb"][t][i] for i in range(len(data["pos"][t]))} for t in data["pos"]}
teams = data["teams"]
logos = data["logos"]
poss = {t:[0]*10 for t in teams}
N = data["N"]
for t in teams:
	for p in pos[t]:
		a, b = p
		b += 1
		for k in range(a, b):
			poss[t][k-1] += pos[t][p]/(b-a)

#print(sum(poss["KC"][i]/N for i in range(8,10)))
#print(sum(poss["KC"][i]/N for i in range(8)))

with open("{}/{}-{}-{}-fullauto-allpos-summer.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'w') as f:
	print("Rank,"+','.join(teams), file=f)
	print(","+','.join(["=IMAGE(\"{}\")".format(logos[t]) for t in teams]), file=f)
	for i in range(10):
		print("{},".format(i+1) + ','.join(str(poss[t][i]/N) for t in teams), file=f)
