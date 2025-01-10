import urllib.request
import datetime
import re
from prediction import *

# Function to parse the date string
def parse_date(date_str):
    # Remove the day of the week from the string
    date_str = date_str.split(' ', 1)[1]
    # Define the date format
    date_format = "%d %B %Y"
    # Replace 'th', 'st', 'nd', 'rd' to standardize the format
    #date_str = date_str.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
    # Parse the date string
    return datetime.datetime.strptime(date_str, date_format)

def get_results(date, dataStruct, teamDict):
    myfile = open('alt_team_names.txt','r')
    lines = myfile.readlines()
    myfile.close()
    altNames = {}
    for line in lines:
        line = line.replace("\n","")
        name = line.split(":")[0]
        alt_name = line.split(":")[1]
        altNames[name] = alt_name
    month = date.split("-")[0]
    year = date.split("-")[1]
    if '0' not in month and len(month) == 1: month = '0' + month
    url = 'https://www.bbc.co.uk/sport/football/premier-league/scores-fixtures/20' + year + "-" + month
    print(url)
    uf = urllib.request.urlopen(url)
    html = str(uf.read())
    lines = html.split('\n')
    results = []
    for line in lines:
        year = "20" + date.split("-")[1]
        for line in lines:
            # print(line)
            month_groups = line.split("<h2 class=")
            for group in month_groups:
                if ">" not in group or "<" not in group: continue
                # print(group)
                title = group.split("<")[0].split(">")
                if len(title) < 2: continue
                title = title[1]
                title = title.replace("st ", " ").replace("th ", " ").replace("rd ", " ").replace("nd ", " ")
                date = title + " " + year
                tokens = group.split('<span class="visually-hidden ssrcss-1f39n02-VisuallyHidden e16en2lz0">')
                for token in tokens:
                    string = token.split("<")[0]
                    #print(string)
                    if "Full time" not in string: continue
                    pattern = r"([A-Za-z\s]+)\s(\d+)\s?,\s?([A-Za-z\s]+)\s(\d+)"

                    # Search for the pattern in the input string
                    match = re.search(pattern, string)

                    if match:
                        # Extract team names and scores
                        team1 = match.group(1).strip()
                        score1 = int(match.group(2))
                        team2 = match.group(3).strip()
                        score2 = int(match.group(4))
                        if team1 not in teamDict and team1 in altNames:
                            team1 = altNames[team1]
                        if team2 not in teamDict and team2 in altNames:
                            team2 = altNames[team2]
                        if team1 not in teamDict or team2 not in teamDict:
                            continue
                        prediction = predict_result(team1, team2, dataStruct, teamDict)
                        home_pred = int(prediction[0].split(" - ")[0])
                        away_pred = int(prediction[0].split(" - ")[1])
                        outcome_pred = 'Draw'
                        if home_pred > away_pred:
                            outcome_pred = 'Home Win'
                        if home_pred < away_pred:
                            outcome_pred = 'Away Win'
                        actual_outcome = 'Draw'
                        if score1 > score2:
                            actual_outcome = 'Home Win'
                        if score1 < score2:
                            actual_outcome = 'Away Win'
                        #print(prediction)
                        #print(team1, score1, team2, score2, )
                        to_add = (date, team1, team2, score1, score2, home_pred, away_pred, actual_outcome, outcome_pred)
                        #print(to_add)
                        results.append(to_add)
    results = list(reversed(results))
    for result in results:
        print(result)
    return results

def get_all_results(dataStruct, teamDict):
    now = datetime.datetime.now()

    # Format the date to MM-YY
    month = now.strftime("%m")
    year = now.strftime("%y")
    month = '08'
    year = '24'
    cur_date = month + "-" + year

    # Format the date to MM-YY
    month = now.strftime("%m")
    year = now.strftime("%y")
    cur_date = "08-24"
    now_date = month + "-" + year
    results = get_results(cur_date, dataStruct, teamDict)
    while cur_date != now_date:
        month = int(cur_date.split("-")[0])
        year = int(cur_date.split("-")[1])
        month += 1
        if month > 12:
            month = 1
            year += 1
        cur_date = str(month) + "-" + str(year)
        new_results = get_results(cur_date, dataStruct, teamDict)
        results += new_results
        if len(new_results) == 0: break
        print(cur_date)
    myfile = open('season_results.txt', 'w', encoding='utf-8')
    for result in results:
        myfile.write(str(result) + "\n")
    myfile.close()


teamDict = {} # map team names to structs
dataStruct = DataStruct()
dataStruct, teamDict = get_data(dataStruct, teamDict)
get_all_results(dataStruct, teamDict)
#get_results('08-24', dataStruct, teamDict)