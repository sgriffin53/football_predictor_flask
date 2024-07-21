import csv
import numpy as np
from scipy.stats import poisson
import datetime
import get_fixtures
from footer import get_footer

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
    totLeagueHomeGoals = 0
    totLeagueAwayGoals = 0
    totMatches = 0
    i = 0
    with open('/home/jimmyrustles/mysite/data/final_dataset.csv', newline='') as csvfile:
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

def get_predictions():
    myfile = open('/home/jimmyrustles/mysite/alt_team_names.txt','r')
    lines = myfile.readlines()
    myfile.close()
    altNames = {}
    for line in lines:
        line = line.replace("\n","")
        name = line.split(":")[0]
        alt_name = line.split(":")[1]
        altNames[name] = alt_name
    myfile = open('/home/jimmyrustles/mysite/season_fixtures.txt','r')
    lines = myfile.readlines()
    myfile.close()
    fixtures = []
    for line in lines:
        line = line.replace(", ",",")
        line = line.replace("\n","").replace("(","").replace(")","").replace("' ","").replace("'","").strip()
        tokens = line.split(",")
        fixtures.append((tokens[0], tokens[1], tokens[2], tokens[3]))
        #fixtures.append(line.replace("\n",""))
    teamDict = {}  # map team names to structs
    dataStruct = DataStruct()
    dataStruct, teamDict = get_data(dataStruct, teamDict)
    teams = []
    tot_prob = 1
    predictions = []
    used_dates = []
    for fixture in fixtures:
        date = fixture[0]
        if date not in used_dates:
            used_dates.append(date)
            print("--- " + date + " ---")
        home_team = fixture[1]
        away_team = fixture[2]
        if home_team not in teamDict:
            home_team = altNames[home_team]
        if away_team not in teamDict:
            away_team = altNames[away_team]
        if home_team not in teamDict:
            pass
            #print("not found:", home_team)
        if away_team not in teamDict:
            pass
           # print("not_found:", away_team)
        if home_team not in teamDict or away_team not in teamDict: continue
        result = predict_result(home_team, away_team, dataStruct, teamDict)
        predictions.append((date, home_team, away_team, result[0], result[1], fixture[3]))
    return predictions

def get_single_prediction(home_team, away_team):
    myfile = open('/home/jimmyrustles/mysite/alt_team_names.txt','r')
    lines = myfile.readlines()
    myfile.close()
    altNames = {}
    for line in lines:
        line = line.replace("\n","")
        name = line.split(":")[0]
        alt_name = line.split(":")[1]
        altNames[name] = alt_name
    teamDict = {}  # map team names to structs
    dataStruct = DataStruct()
    dataStruct, teamDict = get_data(dataStruct, teamDict)
    home_team = home_team.title()
    away_team = away_team.title()
    if home_team not in teamDict:
        if home_team in altNames.keys(): home_team = altNames[home_team]
    if away_team not in teamDict:
        if away_team in altNames.keys(): away_team = altNames[away_team]
    if home_team not in teamDict:
        return "Home team (" + home_team + ") not found."
    if away_team not in teamDict:
        return "Away team (" + away_team + ") not found."
    result = predict_result(home_team, away_team, dataStruct, teamDict)
    return home_team + " " + result[0] + " " + away_team + " (" + str(round(float(result[1]),2)) + "%)"

def football_page(request):
    outtext = '<center><h1>Jimmy\'s Football Predictor</h1>'
    outtext += 'Predicts results of upcoming Premier League games. It shows each game\'s result prediction with a probability of how likely the model thinks it is to occur.<br>'
    outtext += 'The model uses the Gaussian Naive Bayes model to predict results based on past performance.<br>'
    outtext += 'The model is based on data from the 2021 to 2024 seasons.<br>'
    outtext += 'It shows the predictions for the next 30 days of games, and will update throughout the season.<br>'
    outtext += '<h2>Predictions</h2>'
    outtext += '<span style="font-family: Arial; font-size: 16px;">'
    predictions = get_predictions()
    used_dates = []
    for prediction in predictions:
        date = prediction[0]
        home_team = prediction[1]
        away_team = prediction[2]
        result = prediction[3]
        probability = round(float(prediction[4]), 2)
        kick_off = prediction[5]
        parsed_date = get_fixtures.parse_date(date)
        current_date = datetime.datetime.now()
        if parsed_date < current_date:
            # game already played
            continue
        max_limit = 60 * 60 * 24 * 30
        time_until_game = (parsed_date - current_date).total_seconds()
        if time_until_game > max_limit:
            continue
        if date not in used_dates:
            used_dates.append(date)
            outtext += '<h2>' + date + '</h2>'
        outtext += kick_off + ': ' + home_team + ' <b>' + result + '</b> ' + away_team + ' (' + str(probability) + '%) <br>'
    get_home_team = request.args.get("home_team")
    if get_home_team == None: get_home_team = ""
    get_away_team = request.args.get("away_team")
    if get_away_team == None: get_away_team = ""
    outtext += '''<br>
    View prediction for custom teams:<br>
    <form action="/football" method="GET">
    Home team: <input type="text" name="home_team" value="''' + get_home_team.title() + '''"><br>
    Away team: <input type="text" name="away_team" value="''' + get_away_team.title() + '''"><br>
    <input type="submit" value="Get Prediction">
    </form>
    '''
    if request.method == "GET":
        home_team = request.args.get("home_team")
        away_team = request.args.get("away_team")
        if home_team != None and away_team != None:
            result = get_single_prediction(home_team, away_team)
            outtext += "<b>Custom prediction:<br><br>"
            outtext += result + "</b><br>"
    outtext += '</span>'
    outtext += get_footer()
    return outtext