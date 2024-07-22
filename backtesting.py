import csv
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


def get_data(dataStruct, teamDict):
    totLeagueHomeGoals = 0
    totLeagueAwayGoals = 0
    totMatches = 0
    i = 0
    with open('data/final_dataset.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
     #       print(row[2])
            if row[5] == 'FTHG' or row[5] == '': continue
            if '/2024' in row[1]: continue
            print(row[1])
            totHomeGoals = int(row[5])
            totAwayGoals = int(row[6])
            totLeagueHomeGoals += totHomeGoals
            totLeagueAwayGoals += totAwayGoals
            homeTeam = row[3]
            awayTeam = row[4]
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

def get_fixtures():
    fixtures = []
    with open('data/final_dataset.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if '/2024' not in row[1]: continue
            if row[5] == 'FTHG' or row[5] == '': continue
            homeTeam = row[3]
            awayTeam = row[4]
            totHomeGoals = int(row[5])
            totAwayGoals = int(row[6])
            fixtures.append((homeTeam, awayTeam, totHomeGoals, totAwayGoals))
    return fixtures

teamDict = {}  # map team names to structs
dataStruct = DataStruct()
dataStruct, teamDict = get_data(dataStruct, teamDict)
fixtures = get_fixtures() # 2021 - 2023
num_scores_correct = 0
num_scores_tried = 0
num_wdl_correct = 0
num_wdl_tried = 0
correct_scores = []
for fixture in fixtures:
    homeTeam = fixture[0]
    awayTeam = fixture[1]
    if homeTeam not in teamDict or awayTeam not in teamDict: continue
    print(homeTeam, awayTeam)
    result = predict_result(homeTeam, awayTeam, dataStruct, teamDict)
    score = result[0]
    homeGoals = int(score.split(" - ")[0])
    awayGoals = int(score.split(" - ")[1])
    resultHomeGoals = int(fixture[2])
    resultAwayGoals = int(fixture[3])
    num_wdl_tried += 1
    num_scores_tried += 1
    wdl_prediction = 'draw'
    if homeGoals > awayGoals:
        wdl_prediction = 'home_win'
    if awayGoals > homeGoals:
        wdl_prediction = 'away_win'
    wdl_result = 'draw'
    if resultHomeGoals > resultAwayGoals:
        wdl_result = 'home_win'
    if resultAwayGoals > resultHomeGoals:
        wdl_result = 'away_win'
    if wdl_prediction == wdl_result:
        num_wdl_correct += 1
    print(homeGoals, resultHomeGoals, ":", awayGoals, resultAwayGoals)
    if homeGoals == resultHomeGoals and awayGoals == resultAwayGoals:
        num_scores_correct += 1
        correct_scores.append(homeTeam + " " + score + " " + awayTeam)
    wdl_percent = num_wdl_correct * (100 / num_wdl_tried)
    wdl_percent = round(wdl_percent,1)
    scores_percent = num_scores_correct * (100 / num_scores_tried)
    scores_percent = round(scores_percent,1)
print("WDL: ", num_wdl_correct, "/", num_wdl_tried, "(" + str(wdl_percent) + "%)")
print("Scores: ", num_scores_correct, "/", num_scores_tried, "(" + str(scores_percent) + "%)")
print("Correct predictions:")
for score in correct_scores:
    print(score)