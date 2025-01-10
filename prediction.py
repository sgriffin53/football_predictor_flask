import csv
import numpy as np
from scipy.stats import poisson
class DataStruct:
    def __init__(self):
        self.totHomeGoals = 0
        self.totAwayGoals = 0
        self.avgHomeGoalsPerMatch = 0
        self.avgAwayGoalsPerMatch = 0
        self.totMatches = 0

class TeamStruct:
    def __init__(self):
        self.avgHomeGoalsScored = 0
        self.avgHomeGoalsAllowed = 0
        self.totHomeGoalsScored = 0
        self.totHomeGoalsAllowed = 0
        self.avgAwayGoalsScored = 0
        self.avgAwayGoalsAllowed = 0
        self.totAwayGoalsScored = 0
        self.totAwayGoalsAllowed = 0
        self.matches = 0
        self.homeMatches = 0
        self.awayMatches = 0


def get_data(dataStruct, teamDict):

    myfile = open('alt_team_names.txt','r')
    lines = myfile.readlines()
    myfile.close()
    altNames = {}
    for line in lines:
        line = line.replace("\n","")
        name = line.split(":")[0]
        alt_name = line.split(":")[1]
        altNames[name] = alt_name
    totLeagueHomeGoals = 0
    totLeagueAwayGoals = 0
    totMatches = 0
    i = 0
    with open('data/final_dataset.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
     #       print(row[2])
            if row[5] == 'FTHG' or row[5] == '': continue
            totHomeGoals = int(row[5])
            totAwayGoals = int(row[6])
            totLeagueHomeGoals += totHomeGoals
            totLeagueAwayGoals += totAwayGoals
            homeTeam = row[3]
            awayTeam = row[4]
            if homeTeam not in teamDict and homeTeam in altNames:
                homeTeam = altNames[homeTeam]
            if awayTeam not in teamDict and awayTeam in altNames:
                awayTeam = altNames[awayTeam]
            if homeTeam not in teamDict:
                teamDict[homeTeam] = TeamStruct()
            if awayTeam not in teamDict:
                teamDict[awayTeam] = TeamStruct()
            teamDict[homeTeam].totHomeGoalsScored += totHomeGoals
            teamDict[homeTeam].totHomeGoalsAllowed += totAwayGoals
            teamDict[awayTeam].totAwayGoalsScored += totAwayGoals
            teamDict[awayTeam].totAwayGoalsAllowed += totHomeGoals
            teamDict[homeTeam].matches += 1
            teamDict[awayTeam].matches += 1
            teamDict[homeTeam].homeMatches += 1
            teamDict[awayTeam].awayMatches += 1
            totMatches += 1
            i += 1
    dataStruct.totHomeGoals = totLeagueHomeGoals
    dataStruct.totAwayGoals = totLeagueAwayGoals
    dataStruct.avgHomeGoalsPerMatch = totLeagueHomeGoals / totMatches
    dataStruct.avgAwayGoalsPerMatch = totLeagueAwayGoals / totMatches
    dataStruct.totMatches = totMatches
    for team in teamDict.keys():
        teamDict[team].avgHomeGoalsScored = teamDict[team].totHomeGoalsScored / teamDict[team].matches
        teamDict[team].avgHomeGoalsAllowed = teamDict[team].totHomeGoalsAllowed / teamDict[team].matches
        teamDict[team].avgAwayGoalsScored = teamDict[team].totAwayGoalsScored / teamDict[team].matches
        teamDict[team].avgHomeGoalsAllowed = teamDict[team].totAwayGoalsAllowed / teamDict[team].matches
    #print(dataStruct, teamDict)
    return dataStruct, teamDict
    pass

def predict_result(home_team, away_team, dataStruct, teamDict):
    homeGoalAvg = (teamDict[home_team].totHomeGoalsScored) / teamDict[home_team].homeMatches
    awayGoalAvg = (teamDict[away_team].totAwayGoalsScored) / teamDict[away_team].awayMatches
    homeAllowedAvg = (teamDict[home_team].totHomeGoalsAllowed) / teamDict[home_team].homeMatches
    awayAllowedAvg = (teamDict[away_team].totAwayGoalsAllowed) / teamDict[away_team].awayMatches
    homeAllowedAvg = teamDict[home_team].totHomeGoalsAllowed / teamDict[home_team].homeMatches
    awayAllowedAvg = teamDict[away_team].totHomeGoalsAllowed / teamDict[away_team].awayMatches
    leagueGoalAvg = (dataStruct.totHomeGoals + dataStruct.totAwayGoals) / dataStruct.totMatches
    leagueGoalAvgHome = dataStruct.totHomeGoals / dataStruct.totMatches
    leagueGoalAvgAway = dataStruct.totAwayGoals / dataStruct.totMatches
    homeAttack = homeGoalAvg / leagueGoalAvgHome
    awayAttack = awayGoalAvg / leagueGoalAvgAway
    homeDefence = homeAllowedAvg / leagueGoalAvgHome
    awayDefence = awayAllowedAvg / leagueGoalAvgAway
    mostLikelyScore = "-1"
    mostLikelyValue = -9999
    homeGoalExpectency = homeAttack * awayDefence
    awayGoalExpectency = awayAttack * homeDefence
    for i in range(0, 6):
        for j in range(0,6):
            prob = poisson.pmf(i, homeGoalExpectency) * poisson.pmf(j, awayGoalExpectency) * 100
            if prob > mostLikelyValue:
                mostLikelyScore = str(i) + " - " + str(j)
                mostLikelyValue = prob
    return mostLikelyScore, mostLikelyValue

if __name__ == '__main__':
    teamDict = {} # map team names to structs
    dataStruct = DataStruct()
    dataStruct, teamDict = get_data(dataStruct, teamDict)
    teams = ["Newcastle vs Tottenham",
             "Burnley vs Brighton",
             "Man City vs Luton",
             "Nottingham Forest vs Wolves",
             "Bournemouth vs Man United"]
    teams = ["Sheffield United vs Burnley",
             "Wolves vs Arsenal"]
    teams = ["Coventry vs Man United",
             "Everton vs Nottingham Forest",
             "Aston Villa vs Bournemouth",
             "Crystal Palace vs West Ham",
             "Fulham vs Liverpool"]
    teams = ["West Ham vs Liverpool",
             "Fulham vs Crystal Palace",
             "Man United vs Burnley",
             "Newcastle vs Sheffield United",
             "Wolves vs Luton",
             "Everton vs Brentford",
             "Aston Villa vs Chelsea"]
    teams = ["Arsenal vs Bournemouth",
             "Burnley vs Newcastle",
             "Sheffield United vs Nottingham Forest",
             "Man City vs Wolves"]
    teams = ["Fulham vs Man City",
             "Everton vs Sheffield United",
             "Newcastle vs Brighton",
             "Tottenham vs Burnley",
             "West Ham vs Luton",
             "Wolves vs Crystal Palace",
             "Nottingham Forest vs Chelsea"]
    teams = ["Arsenal vs Everton",
             "Brentford vs Newcastle",
             "Brighton vs Man United",
             "Burnley vs Nottingham Forest",
             "Chelsea vs Bournemouth",
             "Crystal Palace vs Aston Villa",
             "Liverpool vs Wolves",
             "Luton vs Fulham",
             "Man City vs West Ham",
             "Sheffield United vs Tottenham"]
    tot_prob = 1
    for team in teams:
        home_team = team.split(" vs ")[0]
        away_team = team.split(" vs ")[1]
        if home_team not in teamDict or away_team not in teamDict: continue
        pred_score, pred_prob = predict_result(home_team, away_team, dataStruct, teamDict)
        tot_prob *= (pred_prob / 100)
        print(home_team + " vs " + away_team + ": " + pred_score + " (" + str(round(pred_prob,2)) + "%)")
    print("Probability: 1/" + str(int(1 / tot_prob)))