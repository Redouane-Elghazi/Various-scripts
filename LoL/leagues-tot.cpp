/* Copyright (C) Redouane ELGHAZI
 * TBD
 */
#pragma GCC optimize ("O3")
#ifdef ONLINE_JUDGE
#pragma GCC optimize("O3")
#pragma GCC target("avx2")
#define NDEBUG
#endif

#include <bits/stdc++.h>
using namespace std;
#define REP(i,a,b) for (int i = (a); i <= (b); ++i)
#define REPD(i,a,b) for (int i = (a); i >= (b); --i)
#define FORI(i,n) REP(i,1,n)
#define FOR(i,n) REP(i,0,(int)(n)-1)
#define mp make_pair
#define pb push_back
#define pii pair<int,int>
#define vi vector<int>
#define pll pair<ll, ll>
#define vl vector<ll>
#define ll long long
#define ld long double
#define SZ(x) (int)((x).size())
#define DBG(v) cerr << #v << " = " << (v) << endl;
#define FOREACH(i,t) for (auto i = t.begin(); i != t.end(); ++i)
#define fi first
#define se second

unordered_map<string, map<pair<ll, ll>, ll> > pos;
vector<pair<string, string> > M;
vector<ll> Result;
ll nb = 0;
void init(vector<string> &teams, unordered_map<string, unordered_map<string, ll> > &results){
    pos.clear();
    for(string s:teams){
        pos[s] = map<pair<ll, ll>, ll>();
    }
    M.clear();
    Result.clear();
    for(string t1:teams){
        for(string t2:teams){
            if(t1<t2){
				for(int i = 0; i<2-results[t1][t2]-results[t2][t1]; ++i){
                    M.emplace_back(t1, t2);
                    Result.push_back(0);
				}
            }
        }
    }
}

void affect(string t, pair<ll, ll> p){
    if(pos[t].find(p) == pos[t].end()){
        pos[t][p] = 0;
    }
    pos[t][p] += 1;
}

void tiebreaker(vector<string> &teams, ll i, ll j,
                unordered_map<string, unordered_map<string, ll> > &results){
    ll n = j-i;
    if(n==0){
    }
    else if(n == 1){
        string t = teams[i];
        affect(t, make_pair(i+1, i+1));
    }
    else if(n == 2){
        string t1 = teams[i], t2 = teams[i+1];
		if(results[t1][t2] > results[t2][t1]){
			affect(t1, make_pair(i+1, i+1));
			affect(t2, make_pair(i+2, i+2));
		}
		else if(results[t1][t2] < results[t2][t1]){
			affect(t1, make_pair(i+2, i+2));
			affect(t2, make_pair(i+1, i+1));
        }
		else{
			affect(t1, make_pair(i+1, i+2));
			affect(t2, make_pair(i+1, i+2));
		}
    }
    else{
        unordered_map<string, ll> W, L;
        for(ll k = i; k<j; ++k){
            string t1 = teams[k];
            W[t1] = 0;
            L[t1] = 0;
            for(ll l = i; l<j; ++l){
                if(k!=l){
                    string t2 = teams[l];
                    W[t1] += results[t1][t2];
                    L[t1] += results[t2][t1];
                }
            }
        }
        sort(teams.begin()+i, teams.begin()+j,
             [&W](const string &t1, const string &t2) -> bool
             {
                 return W[t1]>W[t2];
             });
        ll k = i;
        while(W[teams[k]] > L[teams[k]]){
            ++k;
        }
        ll l = k;
        while(l<j and W[teams[l]] == L[teams[l]]){
            ++l;
        }
        if(k!=i){
            tiebreaker(teams, i, k, results);
            tiebreaker(teams, k, l, results);
            tiebreaker(teams, l, j, results);
        }
        else{
            pair<ll, ll> p(i+1, j);
            for(ll k = i; k<j; ++k){
                affect(teams[k], p);
            }
        }
    }
}

void classements(vector<string> &teams,
                 unordered_map<string, unordered_map<string, ll> > &results){
    ll n = teams.size();
    unordered_map<string, ll> W, L;
    for(ll k = 0; k<n; ++k){
        string t1 = teams[k];
        W[t1] = 0;
        L[t1] = 0;
        for(ll l = 0; l<n; ++l){
            if(k!=l){
                string t2 = teams[l];
                W[t1] += results[t1][t2];
                L[t1] += results[t2][t1];
            }
        }
    }
    sort(teams.begin(), teams.end(),
         [&W](const string &t1, const string &t2) -> bool
         {
             return W[t1]>W[t2];
         });
    ll i = 0, j = 0;
    while(i<n){
        while(j<n and W[teams[i]] == W[teams[j]]){
            ++j;
        }
        if(i+1==j){
            affect(teams[i], make_pair(i+1, i+1));
        }
        else{
            tiebreaker(teams, i, j, results);
        }
        i = j;
    }
}


void trouve(vector<string> &teams,
            unordered_map<string, unordered_map<string, ll> > &results,
            ll i){
    if((unsigned)i==M.size()){
        ++nb;
        if(nb%1000000==0){
            cerr << nb << endl;
        }
        classements(teams, results);
    }
    else{
		Result[i] = 0;
		results[M[i].first][M[i].second] += 1;
		trouve(teams, results, i+1);
		results[M[i].first][M[i].second] -= 1;
		Result[i] = 1;
		results[M[i].second][M[i].first] += 1;
		trouve(teams, results, i+1);
		results[M[i].second][M[i].first] -= 1;
    }
}

int main(){
	cin.sync_with_stdio(0);
	cin.tie(0);
    ll n;
    cin >> n;
    vector<string> teams(n);
    for(string &s:teams){
        cin >> s;
    }
    ll w, l;
    string s;
    unordered_map<string, unordered_map<string, ll> > results;//TODO: make it a vector bruh
    for(ll i = 0; i<n; ++i){
        string t1;
        cin >> t1;
        for(ll j = 0; j<n; ++j){
            string t2 = teams[j];
            if(t1 != t2){
                cin >> w >> s >> l;
                results[t1][t2] = w;
            }
        }
        cin >> w >> s >> l;
        cin >> s;
    }
    init(teams, results);
    trouve(teams, results, 0);
    unordered_map<string, ll> win, tie, los;
    for(string &t:teams){
        win[t] = 0;
        tie[t] = 0;
        los[t] = 0;
        for(auto x:pos[t]){
            ll a = x.fi.fi, b = x.fi.se, n = x.se;
            if(b<=6){
                win[t] += n;
            }
            if(a<=6 and 6<b){
                tie[t] += n;
            }
            if(6<a){
                los[t] += n;
            }
        }
    }
    sort(teams.begin(), teams.begin(),
         [&win](const string &t1, const string &t2) -> bool
         {
             return win[t1]>win[t2];
         });
    cout << "Team,Percentage of scenarios in playoff,Percentage of scenarios in a tiebreak for playoff,Percentage of scenarios out of playoff" << endl;
    for(string &t:teams){
        ll tot = win[t]+tie[t]+los[t];
        cerr << t << " " << tot << endl;
        cout << t << "," <<
                100.0*win[t]/tot << "," <<
                100.0*tie[t]/tot << "," <<
                100.0*los[t]/tot << endl;
    }
	return 0;
}
