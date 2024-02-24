import json
import sys
from math import ceil, floor

LEAGUE = sys.argv[1].replace("_", " ")
YEAR = sys.argv[2]
SEASON = sys.argv[3]

with open("{}/{}-{}-{}-fullauto.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'r') as f:
	data = json.load(f)
pos = {t:{tuple(data["pos"][t][i]):data["nb"][t][i] for i in range(len(data["pos"][t]))} for t in data["pos"]}
teams = data["teams"]
logos = data["logos"]
poss = {t:[0]*10 for t in teams}
for t in teams:
	for p in pos[t]:
		a, b = p
		b += 1
		for k in range(a, b):
			poss[t][k-1] += pos[t][p]/(b-a)


with open("{}/{}-{}-{}-fullauto-allpos.out".format(LEAGUE, LEAGUE, SEASON, YEAR), 'w') as f:
	print("Rank,"+','.join(teams), file=f)
	print(","+','.join(["=IMAGE(\"{}\")".format(logos[t]) for t in teams]), file=f)
	for i in range(len(teams)):
		print("{},".format(i+1) + ','.join(str(poss[t][i]/sum(poss[t])) for t in teams), file=f)
