import json
import bisect
with open('../output/elo.json', 'r') as f:
	elo = json.load(f)
myteams = ["JD Gaming", "LNG Esports", "Bilibili Gaming", "Gen.G", "KT Rolster", "T1", "Dplus KIA", "NRG", "Cloud9",
	"Weibo Gaming", "MAD Lions", "GAM Esports", "Team BDS", "G2 Esports", "Team Liquid", "Fnatic",
	]

myteams = [
	"Gentle Mates",
	"GameWard",
	"Team GO",
	"Team BDS Academy",
	"Solary",
	"Karmine Corp Blue",
	"Vitality.Bee",
	"Team Du Sud",
	"Aegis (French Team)",
	"BK ROG Esports",
	]
mynteams = [
	"Karmine Corp",
	"Team BDS",
	"SK Gaming",
	"Team Vitality",
	"G2 Esports",
	"Team Heretics",
	"Fnatic",
	"Rogue (European Team)",
	"GIANTX",
	"MAD Lions KOI",
	]

with open("../output/team_names.json", "r") as json_file:
	team_names = json.load(json_file)
with open("../local/teams.json", "r") as json_file:
	teams = json.load(json_file)


myteams = [teams[t.lower()] if t.lower() in teams else t for t in myteams]
print(myteams)

date = "2024-01-30"
elos = [(([[0,0]]+elo[t])[bisect.bisect_right(elo[t], [date, float("inf")])][1], t) for t in elo if t in myteams]

elos.sort(reverse=True)
for i in range(len(myteams)):
	print(f'{i+1:3.0f}', f'{elos[i][0]:4.0f}', team_names[elos[i][1]])
