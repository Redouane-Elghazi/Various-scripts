import pandas as pd
import numpy as np
import json
import sys
from math import ceil, floor
from sklearn.neighbors import KernelDensity

from scipy.interpolate import UnivariateSpline, BivariateSpline
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as grid_spec
import matplotlib.animation as animation

LEAGUE = sys.argv[1]
YEAR = sys.argv[2]
SEASON = sys.argv[3]

teams = ["RGE", "FNC", "MSF", "G2", "XL", "VIT", "SK", "MAD", "BDS", "AST"]
#teams = ["RGE"]
colors = ['#0000ff', '#3300cc', '#660099', '#990066', '#cc0033', '#ff0000', '#0000ff', '#3300cc', '#660099', '#990066']

start = 65
end = 76

fig = plt.figure(figsize=(16,9))
ims = []

for cur in [start]*3+list(range(start, end))+[end-1]*5:
	with open("{}/{}-{}-{}-fullauto-{}.out".format(LEAGUE, LEAGUE, SEASON, YEAR, cur), 'r') as f:
		data = json.load(f)
	pos = {t:{tuple(data["pos"][t][i]):data["nb"][t][i] for i in range(len(data["pos"][t]))} for t in data["pos"]}
	curmatch = data["curmatch"]
	gs = grid_spec.GridSpec(len(teams), 1)
	#fig = plt.figure(figsize=(16,9))

	i = 0

	ax_objs = []
	for i in range(len(teams)):
		t = teams[i]
		y = [0]*10
		for p in pos[t]:
			a, b = p
			b += 1
			for k in range(a, b):
				y[k-1] += pos[t][p]/(b-a)
		S = sum(y)
		y = [v/S for v in y]
		x = np.linspace(1,10, 10)
		spl = UnivariateSpline(x, y, s = 0)
		xs = np.linspace(1, 10, 1000)
		ys = spl(xs)

		

		#kde = KernelDensity(bandwidth=0.03, kernel='gaussian')
		#kde.fit(x[:, None])

		#logprob = kde.score_samples(x_d[:, None])

		# creating new axes object
		ax_objs.append(fig.add_subplot(gs[i:i+1, 0:]))

		# plotting the distribution
		R = range(len(xs))
		ax_objs[-1].plot([xs[i] for i in R if y[floor(xs[i])-1]!=0 and y[ceil(xs[i])-1]!=0], [ys[i] for i in R if y[floor(xs[i])-1]!=0 and y[ceil(xs[i])-1]!=0],color="#f0f0f0",lw=1)	
		print(t, y)
		#ax_objs[-1].fill_between(xs, [ys[i] if y[floor(xs[i])-1]!=0 or y[ceil(xs[i])-1]!=0 else 0 for i in range(len(xs))], alpha=1,color=colors[i])
		ax_objs[-1].fill_between([xs[i] for i in R if y[floor(xs[i])-1]!=0 and y[ceil(xs[i])-1]!=0], [ys[i] for i in R if y[floor(xs[i])-1]!=0 and y[ceil(xs[i])-1]!=0], alpha=1,color=colors[i])


		# setting uniform x and y lims
		ax_objs[-1].set_xlim(1,10)
		ax_objs[-1].set_ylim(0,1.5)

		# make background transparent
		rect = ax_objs[-1].patch
		rect.set_alpha(0)

		# remove borders, axis ticks, and labels
		ax_objs[-1].set_yticklabels([])

		if i == len(teams)-1:
			ax_objs[-1].set_xlabel("Position à la fin du split", fontsize=16,fontweight="bold")
		else:
			ax_objs[-1].set_xticklabels([])
		if i == 0:
			ax_objs[-1].annotate(
				"""Projection des équipes {} à la fin du split de {} {}""".format(LEAGUE, SEASON, YEAR), 
				(6,1), fontsize=20,fontweight="bold", ha="center")
			ax_objs[-1].annotate(
				"""(match {} - {})""".format(cur//5, curmatch[0]+(3-len(curmatch[0]))*" ", (3-len(curmatch[1]))*" "+curmatch[1]), 
				(6,0.75), fontsize=20,fontweight="bold", ha="center")

		spines = ["top","right","left","bottom"]
		for s in spines:
			ax_objs[-1].spines[s].set_visible(False)

		adj_country = t.replace(" ","\n")
		ax_objs[-1].text(-0.02,0,adj_country,fontweight="bold",fontsize=18,ha="right", color="green" if sum(y[6:]) == 0 else "red" if sum(y[:6]) == 0 else "black")
		ax_objs[-1].axes.get_yaxis().set_visible(False)
		#ax_objs[-1].grid(axis="x")

		#plt.yaxis('off')


		i += 1

	gs.update(hspace=-0.7)

	#fig.text(0.07,0.85,"Projection des équipes {} à la fin du split de {} {}, \nau day {} (match {} - {})".format(LEAGUE, SEASON, YEAR, cur//5, *curmatch),fontsize=20)

	plt.tight_layout()
	ims.append(ax_objs)

	#plt.savefig("{}/{}-{}-{}-pos-{}.png".format(LEAGUE, LEAGUE, SEASON, YEAR, cur))
ani = animation.ArtistAnimation(fig, ims)
ani.save('anim.gif', writer="imagemagick")
ani.save('anim.mp4', writer="ffmpeg")
plt.show()
