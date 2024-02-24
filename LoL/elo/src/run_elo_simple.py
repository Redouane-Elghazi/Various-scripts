import json
from datetime import datetime, timedelta
from collections import defaultdict
from rankingsystems import DummyEloSystem, PlayerEloSystem, uffind

class identitydict(dict):
    def __missing__(self, key):
        return key

def choose_K(name, tourn_importance):
	if tourn_importance[name] == 1:
		return 40
	elif tourn_importance[name] == 2:
		return 20
	elif tourn_importance[name] == 4:
		return 1
	else:
		print(name)
		exit(1)
"""
	if 'msi' in name or 'world' in name or 'emea' in name or 'eum' in name or ('eu' in name and 'masters' in name) or ('mid' in name and "season" in name and "invit" in name):
		#print('int competition', name)
		baseK = 20
	else:
		#print('reg competition', name)
		baseK = 10
	if 'playoff' in name or 'knockout' in name or 'final' in name or 'qualifier'  in name or 'promotion' in name or 'bracket' in name:# or "play in" in name or "play_in" in name or "playin" in name o "main event" in name:
		K = baseK
	else:
		K = 2*baseK
	return K
"""

def choose_starting_elo(name, tourn_importance):
	if tourn_importance[name] == 1:
		return 2200
	elif tourn_importance[name] == 2:
		return 2000
	elif tourn_importance[name] == 4:
		return 2000
	else:
		print(name)
		exit(1)
	

# date, K, [[equipe, joueurs], [equipe, joueurs], score, score], None (match), None (league)
# teams = ["JD Gaming", "LNG Esports", "Bilibili Gaming", "Gen.G", "KT Rolster", "T1", "Dplus KIA", "NRG", "Cloud9", "Weibo Gaming", "MAD Lions", "GAM Esports", "Team BDS", "G2 Esports", "Team Liquid", "Fnatic"]
if __name__ == "__main__":
	id2players = identitydict()
	
	id2teams = identitydict()
	id2code = identitydict()
	matches = []
	with open("../local/matches.json", "r") as json_file:
		matches = json.load(json_file)
	with open("../local/teams.json", "r") as json_file:
		teams = json.load(json_file)
	with open("../local/players.json", "r") as json_file:
		players = json.load(json_file)
	with open("../local/tourn_importance.json", "r") as json_file:
		tourn_importance = json.load(json_file)

	team_names = dict()
	
	cluster_date = (datetime.strptime(matches[-1]["DateTime UTC"][:10], "%Y-%m-%d") - timedelta(days=250)).strftime("%Y-%m-%d")

	ds = PlayerEloSystem()

	ds.win = defaultdict(int)
	ds.loss = defaultdict(int)
	ds.restart_clusters()
	ds.clear_elo()
	i = 0
	for match in matches:
		i += 1
		if i%100 == 0:
			print(i, len(matches), end='\r')
		for t in [match["Team1"], match["Team2"]]:
			if t.lower() not in teams:
				teams[t.lower()] = t
			team_names[teams[t.lower()]] = t
		for p in match["Team1Players"].split(',')+match["Team2Players"].split(','):
			if p.lower() not in players:
				players[p.lower()] = p
		m = (match["DateTime UTC"], choose_K(match["OverviewPage"], tourn_importance), [[teams[match["Team1"].lower()]]+[players[p.lower()] for p in match["Team1Players"].split(',')], [teams[match["Team2"].lower()]]+[players[p.lower()] for p in match["Team2Players"].split(',')], (match["Winner"] == "1"), (match["Winner"] == "2")], None, None, choose_starting_elo(match["OverviewPage"], tourn_importance))
		ds.process(m)
		if match["DateTime UTC"] < cluster_date:
			ds.restart_clusters()
	with open(f"../output/clusters.json", "w") as json_file:
		ds.write_clusters(json_file)
	with open(f'../output/elo.json', 'w') as json_file:
		ds.save(json_file)
	with open("../output/teams.json", "w") as json_file:
		json.dump({t:{"team_id": t, "team_code": id2code[t], "team_name": id2teams[t], "win": ds.win[t], "loss":ds.loss[t], "lastMatch":{"date": ds.elo[t][-1][0], "players": ds.lastknownteam[t]}} for t in ds.elo}, json_file)
	with open("../output/players.json", "w") as json_file:
		json.dump({p:{"player_id": p, "player_name": id2players[p], "elo": ds.individual[p], "win": ds.win[p], "loss":ds.loss[p]} for p in ds.individual if p not in ds.elo}, json_file)
	with open("../output/team_names.json", "w") as json_file:
		json.dump(team_names, json_file)
