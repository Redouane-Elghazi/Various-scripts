import pandas as pd
import numpy as np
import json
import sys
from math import ceil, floor

from matplotlib import animation
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
from matplotlib.animation import FuncAnimation
import seaborn as sns
import pandas as pd
import bar_chart_race as bcr

LEAGUE = sys.argv[1]
YEAR = sys.argv[2]
SEASON = sys.argv[3]
start = int(sys.argv[4])
end = int(sys.argv[5])

with open("{}/{}-{}-{}-fullauto-{}.out".format(LEAGUE, LEAGUE, SEASON, YEAR, start), 'r') as f:
	data = json.load(f)
teams = data["teams"]
if teams == ["RGE", "FNC", "MSF", "G2", "XL", "VIT", "SK", "MAD", "BDS", "AST"]:
	cmap = ["#00a7fe", "#ff2300", "#bd002d", "#636363", "#000000", "#f7f205", "#020406", "#e8d66d", "#ff0074", "#ff0011"]
elif set(teams) == {'LDLC', 'VITB', 'KC', 'BDSA', 'SLY', 'MSFP', 'GW', 'ME', 'GO', 'OPL'}:
	cmap = [{"LDLC":"#0a0c5d", "VITB":"#f9f104", "KC":"#00afeb", "BDSA":"#ff0072", "SLY":"#0083e0", "MSFP":"#b1002d", "GW":"#000000", "ME":"#00e6c3", "GO":"#c80004", "OPL":"#ff001a"}[t] for t in teams]
else:
	print("unknown set of teams")
	print(teams)
	exit(1)

plt.style.use("seaborn")

d6 = {t:dict() for t in teams}
d4 = {t:dict() for t in teams}
d2 = {t:dict() for t in teams}
d1 = {t:dict() for t in teams}
matchs = []
for cur in range(start, end):
	i = cur-start
	with open("{}/{}-{}-{}-fullauto-{}.out".format(LEAGUE, LEAGUE, SEASON, YEAR, cur), 'r') as f:
		data = json.load(f)
	pos = {t:{tuple(data["pos"][t][i]):data["nb"][t][i] for i in range(len(data["pos"][t]))} for t in data["pos"]}
	#teams = data["teams"]
	curmatch = data["curmatch"]
	matchs += ["{}-{}".format(*curmatch)]
	poss = {t:[0]*10 for t in teams}
	for t in teams:
		for p in pos[t]:
			a, b = p
			b += 1
			for k in range(a, b):
				poss[t][k-1] += pos[t][p]/(b-a)
	for t in teams:
		d6[t]["day {}: ".format(cur//5+1)+matchs[i]] = 100*sum(poss[t][:6])/sum(poss[t])
	for t in teams:
		d4[t]["day {}: ".format(cur//5+1)+matchs[i]] = 100*sum(poss[t][:4])/sum(poss[t])
	for t in teams:
		d2[t]["day {}: ".format(cur//5+1)+matchs[i]] = 100*sum(poss[t][:2])/sum(poss[t])
	for t in teams:
		d1[t]["day {}: ".format(cur//5+1)+matchs[i]] = 100*sum(poss[t][:1])/sum(poss[t])
df6 = pd.DataFrame(d6)
df4 = pd.DataFrame(d4)
df2 = pd.DataFrame(d2)
df1 = pd.DataFrame(d1)


bcr.bar_chart_race(df6, figsize=(4, 2.5), period_length=750, title='La course aux playoffs : retrospective !\n% de chances de playoffs après chaque match', cmap=cmap, fixed_max=True, filename="{}/{}-top6.gif".format(LEAGUE, LEAGUE))
bcr.bar_chart_race(df4, figsize=(4, 2.5), period_length=750, title='La course aux playoffs : retrospective !\n% de chances de top 4 après chaque match', cmap=cmap, fixed_max=True, filename="{}/{}-top4.gif".format(LEAGUE, LEAGUE))
bcr.bar_chart_race(df2, figsize=(4, 2.5), period_length=750, title='La course aux playoffs : retrospective !\n% de chances de top 2 après chaque match', cmap=cmap, fixed_max=True, filename="{}/{}-top2.gif".format(LEAGUE, LEAGUE))
bcr.bar_chart_race(df1, figsize=(4, 2.5), period_length=750, title='La course aux playoffs : retrospective !\n% de chances de top 1 après chaque match', cmap=cmap, fixed_max=True, filename="{}/{}-top1.gif".format(LEAGUE, LEAGUE))
