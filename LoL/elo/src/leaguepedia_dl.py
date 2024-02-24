from mwrogue.esports_client import EsportsClient
from time import time
import json

site = EsportsClient("lol")
#matches = site.cargo_client.query(tables = "MatchScheduleGame", fields="RiotPlatformGameId")

def uffind(uf, u):
	if u not in uf:
		uf[u] = u
	if uf[u] != u:
		uf[u] = uffind(uf, uf[u])
	return uf[u]

def ufunion(uf, u, v):
	u = uffind(uf, u)
	v = uffind(uf, v)
	if u > v:
		u, v = v, u
	uf[u] = v

players_uf = dict()
players_final = set()
players_redirects = site.cargo_client.query(tables = "PlayerRedirects", fields="GROUP_CONCAT(AllName)=Names, _pageName=PageName", group_by="PageName")
for player in players_redirects:
	players_final |= {player['PageName']}
	for p in player['Names'].split(',')+[player['PageName']]:
		ufunion(players_uf, player['PageName'].lower(), p.lower())
players_renames = site.cargo_client.query(tables = "PlayerRenames", fields="OriginalName, NewName", order_by="Date")
#new = []
#for player in players_renames:
#	ufunion(players_uf, player['OriginalName'].lower(), player['NewName'].lower())
#	new += [player['NewName']]
rep = dict()
for p in players_final:
	rep[uffind(players_uf, p.lower())] = p
#for p in new:
#	rep[uffind(players_uf, p.lower())] = p

players = {p:rep[uffind(players_uf, p)] for p in players_uf}

teams_uf = dict()
teams_final = set()
teams_redirects = site.cargo_client.query(tables = "TeamRedirects", fields="GROUP_CONCAT(AllName)=Names, _pageName=PageName", group_by="PageName")
for team in teams_redirects:
	teams_final |= {team['PageName']}
	for t in team['Names'].split(',')+[team['PageName']]:
		ufunion(teams_uf, team['PageName'].lower(), t.lower())
teams_renames = site.cargo_client.query(tables = "TeamRenames", fields="OriginalName, NewName, Verb", order_by="Date")
new = []
for team in teams_renames:
	if team['Verb'].lower() in ['acquire', 'acuire']:
		ufunion(teams_uf, team['OriginalName'].lower(), team['NewName'].lower())
		new += [team['NewName']]
rep = dict()
for t in teams_final:
	rep[uffind(teams_uf, t.lower())] = t
for t in new:
	rep[uffind(teams_uf, t.lower())] = t

teams = {t:rep[uffind(teams_uf, t)] for t in teams_uf}


with open("../local/players.json", "w") as json_file:
	json.dump(players, json_file)
with open("../local/teams.json", "w") as json_file:
	json.dump(teams, json_file)
with open("../local/players_renames.json", "w") as json_file:
	json.dump(players_renames, json_file)
with open("../local/teams_renames.json", "w") as json_file:
	json.dump(teams_renames, json_file)
	
tourns = site.cargo_client.query(tables = "Tournaments", fields="TournamentLevel, OverviewPage")
importance = {'Primary': 1, 'Secondary': 2, None: 2, 'Showmatch': 4, 'Major': 2, 'Minor': 2, 'Premier': 2, 'Campionato Piazza Esport Playoffs': 2, 'Campionato Piazza Esport Qualifier': 2, 'Campionato Piazza Esport Regular Season': 2}
tourn_importance = {t["OverviewPage"]:importance[t["TournamentLevel"]] for t in tourns}
with open("../local/tourn_importance.json", "w") as json_file:
	json.dump(tourn_importance, json_file)
#exit(0)

matches = site.cargo_client.query(tables = "ScoreboardGames", fields="GameId,Gamename,OverviewPage,Tournament,Team1,Team2,DateTime_UTC,Winner,Team1Players,Team2Players", order_by="DateTime_UTC")
with open("../local/matches.json", "w") as json_file:
	json.dump(matches, json_file)


"""

# use PlayerRedirect to handle nickname changes
# PlayerRenames
#
#
players = site.cargo_client.query(tables = "PlayerRedirects", fields="GROUP_CONCAT(AllName)=Names, _pageName=PageName", group_by="PageName")
teams = site.cargo_client.query(tables = "TeamRedirects", fields="GROUP_CONCAT(AllName)=Names, _pageName=PageName", group_by="PageName")

# Commande permettant d'extraire les donnees des matchs des Worlds 2023
# Retourne l'ID du BO (type 2012 MLG Pro Circuit/Fall/Championship_Round 2_1_1), la date, les teams, le nom de la team gagnante et les golds de chacune
# Le tout trié par la date.

tournament = "2023 Season World Championship"
response = site.cargo_client.query(
    tables="ScoreboardGames=SG,MatchSchedule=MS",
	where='SG.Tournament="%s"' % tournament,
    join_on="SG.MatchId=MS.MatchId",
    fields="MS.DateTime_UTC, SG.GameId, SG.Team1, SG.Team2, SG.WinTeam, SG.Team1Gold, SG.Team2Gold",
	order_by="MS.DateTime_UTC"
)

def extract_game_lp(data, timeline):
	# data:
	## participants(each):
	### participantId
	### riotIdName ? (empty?)
	### riotIdTagline ? (empty?)
	### summonerId ?
	### summonerName
	### teamId
	## teams(each):?
	### win ?
	# timeline:
	## frames(each):
	### timestamp => gameTime
	### participantsFrames(each): => stats_update event
	#### participantId
	#### totalGold
	#### xp
	### last event of last frame:
	#### if type = 'GAME_END'
	##### realTimestamp => eventTime
	##### winningTeam
	
	#datetime.fromtimestamp(realTimestamp/1000)
	pass
	

# Given the platform_game_id of a game, we can download the json file of its timeline in a format very similar to the hackathon files
i = 0
s = time()
for d in matches:
	platform_game_id = d['RiotPlatformGameId']
	if platform_game_id is None:
		continue
	i += 1
	if i%10 == 0:
		print(f'{i} in {s-time():4.f}s', end='\r')
	try:
		data, timeline = site.get_data_and_timeline(platform_game_id, version=5) # try to get V5 data, returns two values, the data and timeline json
	except KeyError:
		data, timeline = site.get_data_and_timeline(platform_game_id, version=4) # if it fails try getting V4 data
"""
