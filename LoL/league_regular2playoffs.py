import sys
from mwrogue.esports_client import EsportsClient
from time import time
import json
from pprint import pprint

site = EsportsClient("lol")
LEAGUES = [l.replace("_", " ").strip() for l in sys.argv[1:]]
ranks = []
for l in LEAGUES:
	r = site.cargo_client.query(tables = "TournamentResults", fields="Event, Place, Team", where=f'Event LIKE "{l} 2%"')
	if r:
		ranks += r
	else:
		print(f"nothing for league {l}")

d = dict()
for r in ranks:
	if any(word in r["Event"] for word in ["Promotion", "Qualification", "Qualifier", "Relegations"]) or ('2022' not in r["Event"] and '2023' not in r["Event"] and '2024' not in r["Event"]):
		continue
	#if "NQ"==r["Place"]:
	#	print(r)
	#	continue
	if r["Event"] not in d:
		d[r["Event"]] = dict()
	if r["Team"] not in d[r["Event"]]:
		d[r["Event"]][r["Team"]] = []
	for i in r["Place"].split('-'):
		d[r["Event"]][r["Team"]] += [int(i)]

res = [[0]*10 for _ in range(10)]

for e in d:
	reg = e[:-9]
	if reg in d:
		for team in d[e]:
			if team is not None:
				if team in d[e] and team in d[reg]:
					for ind in d[e][team]:
						for indr in d[reg][team]:
							res[indr-1][ind-1] += 1/len(d[e][team])/len(d[reg][team])

#for l in res:
#	print(", ".join([str(x) for x in l]))

for l in res[:6]:
	S = sum(l)
	if S:
		print(", ".join([str(x/S) for x in l[:6]]))