from footer import get_footer

def football_results_page(request):
    outtext = '<center><h1>Jimmy\'s Football Predictor</h1>'
    outtext += '<h2>Season Prediction Results</h2>'
    outtext += 'This page shows the season\'s results compared to the predictor\'s predictions. Correct predictions are highlighted in green.<br>'
    myfile = open('/home/jimmyrustles/mysite/football_predictor/season_results.txt')
    lines = myfile.readlines()
    myfile.close()
    #outtext += str(lines)
    table_text = ''
  #  table_text = '<table border="1" style="width:900px"><tr>'
  #  table_text += '<td>Date</td><td>Teams</td><td>Score</td><td>Predicted Score</td><td>WDL result</td><td>WDL prediction</td></tr>'
    last_date = ''
    date = ''
    total_games = len(lines)
    correct_scores = 0
    correct_wdl = 0
    month = ''
    last_month = ''
    for line in lines:
        data = eval(line)
        #outtext += str(line) + '<br>'
        #outtext += data[0] + '<br>'
        last_date = date
        date = data[0]
        month = date.split(" ")[2] + " " + date.split(" ")[3]
        #if last_date == '':
         #   last_date = date
        #if last_month == '':
         #   last_month = month
        if last_date != date:
            if table_text != '': table_text += '</table><br>'
            if last_month != month:
                last_month = month
                table_text += f'<h2>{month}</h2><br>'
            table_text += '<table border="1" style="width:900px"><tr>'
            table_text += '<td>Date</td><td>Teams</td><td>Score</td><td>Predicted Score</td><td>WDL result</td><td>WDL prediction</td></tr>'
        home_team = data[1]
        away_team = data[2]
        home_score = data[3]
        away_score = data[4]
        home_pred = data[5]
        away_pred = data[6]
        outcome = data[7]
        outcome_pred = data[8]
        score_style = "background-color: red;"
        outcome_style = "background-color: red;"
        if int(home_pred) == int(home_score) and int(away_pred) == int(away_score):
            score_style = "background-color: green;"
            correct_scores += 1
        if outcome == outcome_pred:
            outcome_style = "background-color: green;"
            correct_wdl += 1
        table_text += f'<td>{date}</td><td>{home_team} {home_score} - {away_score} {away_team}</td><td>{home_score} - {away_score}</td><td style="{score_style}">{home_pred} - {away_pred}</td><td>{outcome}</td><td style="{outcome_style}">{outcome_pred}</td></tr>'
    table_text += '</table>'
    wdl_rate = correct_wdl * (100 / total_games)
    scores_rate = correct_scores * (100 / total_games)
    outtext += '<br>Stats:'
    outtext += f'<br><br>Correct scores: {correct_scores} / {total_games} ({round(scores_rate,2)}%)'
    outtext += f'<br>Correct WDL: {correct_wdl} / {total_games} ({round(wdl_rate,2)}%)<br><br>'

    outtext += table_text

    outtext += get_footer()
    return outtext