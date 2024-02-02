
class Team:
    def __init__(self, name :str):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self) -> int:
        return self.name.__hash__()
    


class Score:
    def __init__(self, localSet :int, guestSet: int):
        if (not self.__is_valid_set(localSet)):
             raise ValueError(f"invalid input localSet- {localSet}")
        if (not self.__is_valid_set(guestSet)):
            raise ValueError(f"invalid input guestSet- {guestSet}")

        self.localSet = localSet
        self.guestSet = guestSet
    
    def __is_valid_set(self, set):
        return set <=3 and set>=0

class Match:
    def __init__(self, local :Team, guest :Team, score :Score, match_num :str ="", day :str="",):
        self.local=local
        self.guest=guest
        self.score=score
        self.match_num=match_num
        self.day=day

    def winner(self):
        if (self.score.localSet == 3):
            return self.local
        else:
            return self.guest

    def points_for(self, team :Team):
        if (team != self.local and team != self.guest):
            raise ValueError(f"The team {team} didn't play the game")
        
        localPoints = 0

        if (team == self.local):
            return self.__calculate_points(self.score.localSet, self.score.guestSet)
        else:
            return self.__calculate_points(self.score.guestSet, self.score.localSet)

    def __calculate_points(self, team_score, other_score):
        if (team_score == 3):
            if (other_score == 2):
                return 2
            else:
                return 3
        if (team_score == 2):
            return 1
        else:
            return 0

    def to_json(self):
        return {
            "match":self.match_num,
            "day":self.day,
            "local":self.local.name,
            "guest":self.guest.name,
            "local-score":self.score.localSet,
            "guest-score":self.score.guestSet
        }
    


class Championship:
   
    @staticmethod
    def from_json(dic):
        c = Championship(dic["last_update"])
        for m in dic["matches"]:
            l = Team(m["local"])
            o = Team(m["guest"])
            s = Score(m["local-score"],m["guest-score"])
            m = Match(l,o,s,m["match"],m["day"])
            c.matches.append(m)
        return c
    
    def __init__(self, last_update):
        self.matches=[]
        self.last_update=last_update
        
    def add_match(self, match :Match):
        self.matches.append(match)
        return self
    
    def to_json(self):
        j = {
            "last_update":self.last_update,
            "matches":[]
        }
        for m in self.matches:
            j["matches"].append(m.to_json())
        return j

    def team_list(self):
        teams = []
        for m in self.matches:
            teams.append(m.local)
            teams.append(m.guest)
        return list(set(teams))
    
    def stats(self):
        overall = {
            "lastUpdate":self.last_update,
            "stats":[]
        }

        teams = self.team_list()

        for t in teams:
            stats_per_team = {
                "name":t.name,
                "playedMatches":0,
                "homeMatches":0,
                "guestMatches":0,
                "matchesWon":0,
                "matchesWon3_2":0,
                "matchesLost":0,
                "matchesLost2_3":0,
                "totalPoints":0
            }
            for m in self.matches:
                played = False
                local = False;
                if (m.local == t):
                    stats_per_team["playedMatches"] = stats_per_team["playedMatches"]+1
                    stats_per_team["homeMatches"] = stats_per_team["homeMatches"]+1
                    played = True
                    local = True
                elif (m.guest == t):
                    stats_per_team["playedMatches"] = stats_per_team["playedMatches"]+1
                    stats_per_team["guestMatches"] = stats_per_team["guestMatches"]+1
                    played = True

                if played:
                    winner=m.winner()
                    if (t == winner):
                        stats_per_team["matchesWon"] = stats_per_team["matchesWon"]+1
                        if local:
                            if (m.score.guestSet == 2):
                                stats_per_team["matchesWon3_2"] = stats_per_team["matchesWon3_2"]+1
                                stats_per_team["totalPoints"] = stats_per_team["totalPoints"]+2
                            else:
                                stats_per_team["totalPoints"] = stats_per_team["totalPoints"]+3
                        else:
                            if (m.score.localSet == 2):
                                stats_per_team["matchesWon3_2"] = stats_per_team["matchesWon3_2"]+1
                                stats_per_team["totalPoints"] = stats_per_team["totalPoints"]+2
                            else:
                                stats_per_team["totalPoints"] = stats_per_team["totalPoints"]+3
                    else:
                        stats_per_team["matchesLost"] = stats_per_team["matchesLost"]+1
                        if local:
                            if (m.score.localSet == 2):
                                stats_per_team["matchesLost2_3"] = stats_per_team["matchesLost2_3"]+1
                                stats_per_team["totalPoints"] = stats_per_team["totalPoints"]+1
                        else:
                            if (m.score.guestSet == 2):
                                stats_per_team["matchesLost2_3"] = stats_per_team["matchesLost2_3"]+1
                                stats_per_team["totalPoints"] = stats_per_team["totalPoints"]+1
            
            overall["stats"].append(stats_per_team)
        
        def get_total(stat):
            return stat["totalPoints"]
        
        overall["stats"].sort(key=get_total, reverse=True)

        return overall