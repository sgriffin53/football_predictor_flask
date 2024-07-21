import urllib.request
import datetime

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

def get_fixtures(date):
    month = date.split("-")[0]
    year = date.split("-")[1]
    if '0' not in month and len(month) == 1: month = '0' + month
    url = 'https://www.bbc.co.uk/sport/football/premier-league/scores-fixtures/20' + year + "-" + month
    print(url)
    uf = urllib.request.urlopen(url)
    html = str(uf.read())
    lines = html.split('\n')
    fixtures = []
    year = "20" + date.split("-")[1]
    for line in lines:
        #print(line)
        month_groups = line.split("<h2 class=")
        for group in month_groups:
            if ">" not in group or "<" not in group: continue
            #print(group)
            title = group.split("<")[0].split(">")
            if len(title) < 2: continue
            title = title[1]
            title = title.replace("st "," ").replace("th ", " ").replace("rd ", " ").replace("nd "," ")
            date = title + " " + year
            tokens = group.split('<span class="visually-hidden ssrcss-1f39n02-VisuallyHidden e16en2lz0">')
            #print(date)
            for i, token in enumerate(tokens):
                if "versus" in token:
                    string = token.split("<")[0]
                    if "versus" not in string:
                        continue
                    #print(string)
                    home_team = string.split(" versus ")[0].strip().replace("&amp;","&")
                    away_team = string.split(" versus ")[1].split(" kick off ")[0].strip().replace("&amp;","&")
                    kick_off = string.split(" kick off ")[1]
                    fixtures.append((date, home_team, away_team, kick_off))
                   # print(fixtures[-1])
    return fixtures

def get_all_fixtures():
    now = datetime.datetime.now()

    # Format the date to MM-YY
    month = now.strftime("%m")
    year = now.strftime("%y")
    cur_date = month + "-" + year
    fixtures = get_fixtures(cur_date)
    while cur_date != "7-25":
        month = int(cur_date.split("-")[0])
        year = int(cur_date.split("-")[1])
        month += 1
        if month > 12:
            month = 1
            year += 1
        cur_date = str(month) + "-" + str(year)
        fixtures += get_fixtures(cur_date)
        print(cur_date)
    return_fixtures = []
    print(fixtures)
    for fixture in fixtures:
        date = fixture[0]
        parsed_date = parse_date(date)
        current_date = datetime.datetime.now()
        if parsed_date < current_date:
            # game already played
            continue
        max_limit = 60 * 60 * 24 * 90
        time_until_game = (parsed_date - current_date).total_seconds()
        #if time_until_game > max_limit:
        #    continue
        return_fixtures.append(fixture)
    myfile = open('season_fixtures.txt','a')
    for fixture in return_fixtures:
        print(fixture)
        myfile.write(str(fixture) + "\n")
    myfile.close()
