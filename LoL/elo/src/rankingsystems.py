from math import exp, log
from datetime import datetime
from collections import defaultdict
import json
#LEVIATAN bought a slot in an other league (moving from division 1 to 
#division 3) making it inconsistent (the same id represents 2 different teams)
#so we ignore LEVIATAN temporarily for the union find used to create team clusters
LEVIATAN = '107598699275015260'

def uffind(uf, u):
	if u not in uf:
		uf[u] = u
	if uf[u] != u:
		uf[u] = uffind(uf, uf[u])
	return uf[u]
def ufunion(uf, u, v):
	if LEVIATAN in [u, v]:
		return
	u = uffind(uf, u)
	v = uffind(uf, v)
	u, v = min(u,v), max(u,v)
	uf[v] = u

class RankingSystem:
	def __init__(self):
		self.elo = dict()
		self.uf = dict()
		self.starting_elo = 2000
		self.current_starting_elo = 2000
		self.games = dict()
		self.tournaments = dict()
		
	def get_ranking(self):
		res = [(self.elo[t], t) for t in self.elo]
		res.sort(reverse=True)
		if self.uf != dict():
			dres = dict()
			for e, t in res:
				r = uffind(self.uf, t)
				if r not in dres:
					dres[r] = []
				dres[r] += [(t,e)]
			res = [dres[r] for r in dres]
		else:
			res = [[(t,e) for e,t in res]]
		return res
		

#TODO: update to get lists of history
class DummyEloSystem(RankingSystem):
	def __init__(self):
		super().__init__()
		self.variance = dict()
		self.s = 400
		self.eta = 100
		self.K = 60
		self.uf = dict()
		self.lastknownteam = dict()
		self.tournaments = dict()
		self.leagues = dict()
		self.league2teams = defaultdict(dict)

	def update(self, team1, team2, perf1, perf2=None, date=None):#cf wikipedia https://en.wikipedia.org/wiki/Elo_rating_system#Formal_derivation_for_win/loss_games
		if perf2 is None:
			perf2 = 1-perf1
		perf = perf1 / (perf1 + perf2)
		team1 = team1[0]
		team2 = team2[0]
		if team1 not in self.elo:
			self.elo[team1] = self.current_starting_elo
		if team2 not in self.elo:
			self.elo[team2] = self.current_starting_elo
		def sigma(r):
			#print(-r/self.s)
			return 1/(1+10**(-r/self.s))
		Ew = sigma(self.elo[team1] - self.elo[team2])
		El = sigma(self.elo[team2] - self.elo[team1])
		#K = self.eta*log(10)/self.s
		self.elo[team1] += self.K*(perf-Ew)
		self.elo[team2] += self.K*((1-perf)-El)
		ufunion(self.uf, team1, team2)
		
	def soft_reset(self, teams=None):
		if teams is None:
			teams = list(self.elo)
		if len(teams) == 0:
			return
		rankedteams = [team for team in teams if team in self.elo]
		if len(rankedteams) == 0:
			avgelo = self.starting_elo
		else:
			avgelo = sum([self.elo[team] for team in rankedteams])/len(rankedteams)
		for team in teams:
			if team not in self.elo:
				self.elo[team] = avgelo
		for team in teams:
			self.elo[team] = (self.elo[team] + avgelo)/2
	def hard_reset(self, teams=None):
		if teams is None:
			teams = list(self.elo)
		if len(teams) == 0:
			return
		rankedteams = [team for team in teams if team in self.elo]
		if len(rankedteams) == 0:
			avgelo = self.starting_elo
		else:
			avgelo = sum([self.elo[team] for team in rankedteams])/len(rankedteams)
		for team in teams:
			if team not in self.elo:
				self.elo[team] = avgelo
		for team in teams:
			self.elo[team] = avgelo
	def start_league(self, teams=None):
		if teams is None:
			teams = list(self.elo)
		if len(teams) == 0:
			return
		rankedteams = [team for team in teams if team in self.elo]
		if len(rankedteams) == 0:
			avgelo = self.starting_elo
		else:
			avgelo = sum([self.elo[team] for team in rankedteams])/len(rankedteams)
		self.current_starting_elo = avgelo
	def process(self, match):
		date, K, args, m, league, starting_elo = match
		self.K = K
		self.update(*args, date, league, starting_elo)

	def restart_clusters(self):
		self.uf = dict()
		self.leagues = dict()

	def write_clusters(self, json_file):
		clusters = dict()
		l = list(self.uf)
		for x in l:
			r = uffind(self.uf, x)
			if r not in clusters:
				clusters[r] = {'leagues':set(), 'teams':[]}
			clusters[r]['teams'] += [x]
			clusters[r]['leagues'] |= self.leagues[x]
		clusters = [{'leagues':list(clusters[x]['leagues']), 'teams':clusters[x]['teams']} for x in clusters]
		json.dump(clusters, json_file)

	def change_month(self):
		pass
		
	def save(self, json_file):
		res = self.elo
		json.dump(res, json_file)
	
	def clear_elo(self):
		self.league2teams = defaultdict(dict)
		self.elo = dict()
		

class PlayerEloSystem(DummyEloSystem):
	def __init__(self):
		super().__init__()
		self.individual = dict()
		self.win = defaultdict(int)
		self.loss = defaultdict(int)
		
	def teamelo(self, team):
		return exp(sum(log(self.individual[p]) for p in team)/len(team))
		#return sum(self.individual[p] for p in team)/len(team)
		
	def update(self, team1, team2, perf1, perf2, date, league, starting_elo):#cf wikipedia https://en.wikipedia.org/wiki/Elo_rating_system#Formal_derivation_for_win/loss_games
		todelete = []
		for team in self.league2teams[league]:
			if (datetime.strptime(date[:10], "%Y-%m-%d") - datetime.strptime(self.league2teams[league][team][:10], "%Y-%m-%d")).days > 365:
				todelete += [team]
		for team in todelete:
			del self.league2teams[league][team]
		#starting_elo = sum(self.elo[team][-1][1] for team in self.league2teams[league])/len(self.league2teams[league]) if self.league2teams[league] else self.current_starting_elo
		self.league2teams[league][team1[0]] = date
		self.league2teams[league][team2[0]] = date
		
		for p in team1+team2:
			if p not in self.individual:
				self.individual[p] = starting_elo
				
		if team1[1:] or team1[0] not in self.lastknownteam:
			self.lastknownteam[team1[0]] = team1[1:]
		if team2[1:] or team2[0] not in self.lastknownteam:
			self.lastknownteam[team2[0]] = team2[1:]
			
		perf = perf1 / (perf1 + perf2)
		if perf < 0.5:
			perf = 1-perf
			team1, team2 = team2, team1
			
		for p in team1:
			self.win[p] += 1
		for p in team2:
			self.loss[p] += 1
		elo1 = exp(sum(log(self.individual[p]) for p in team1)/len(team1))
		elo2 = exp(sum(log(self.individual[p]) for p in team2)/len(team2))
		#elo1 = (self.individual[team1[0]]*len(team1)+sum(self.individual[p] for p in team1[1:]))/(2*len(team1)+1)
		#elo2 = (self.individual[team2[0]]*len(team2)+sum(self.individual[p] for p in team2[1:]))/(2*len(team2)+1)
		def sigma(r):
			return 1/(1+10**(-r/self.s))
		Ew = sigma(elo1 - elo2)
		El = sigma(elo2 - elo1)
		for dperf, team in [(perf-Ew, team1), ((1-perf)-El, team2)]:
			elos = [self.individual[p] for p in team]
			delta = self.K*dperf*len(elos)
			if dperf > 0:
				m = min(elos)
			else:
				m = max(elos)
			coeffs = {p:exp((m-self.individual[p])/delta) for p in team}
			S = sum(coeffs[p] for p in coeffs)
			for p in team:
				self.individual[p] += delta*coeffs[p]/S
		ufunion(self.uf, team1[0], team2[0])
		for t in [team1[0], team2[0]]:
			if t not in self.leagues:
				self.leagues[t] = set()
			self.leagues[t] |= {league}
			if t not in self.elo:
				self.elo[t] = []
		self.elo[team1[0]] += [(date, self.teamelo(team1))]
		self.elo[team2[0]] += [(date, self.teamelo(team2))]

	def get_ranking(self):
		res = [((self.elo[t]+sum(self.elo[p] for p in self.lastknownteam[t]))/(len(self.lastknownteam[t])+1), t) for t in self.lastknownteam]
		res.sort(reverse=True)
		if self.uf != dict():
			dres = dict()
			for e, t in res:
				r = uffind(self.uf, t)
				if r not in dres:
					dres[r] = []
				dres[r] += [(t,e)]
			res = [dres[r] for r in dres]
		else:
			res = [[(t,e) for e,t in res]]
		return res

