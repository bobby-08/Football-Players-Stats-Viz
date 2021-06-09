#Importing the packages
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import time

class League_Player_Scraper:

    def url_gen():
        url_main = 'https://understat.com/league/'
        url_league = str(input('Please Enter the League ')).upper()
        url_year = str(input('Please Enter the Season '))
        url = url_main + url_league +'/' + url_year
        return url
    url = url_gen()

    def parsing_req(url):
        time.sleep(10)
        #Using requests to get the url
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        scripts = soup.find_all('script')
        return scripts
    scripts = parsing_req(url)

    def parse_cleaner(scripts):
        strings = scripts[3].string #.string converts it into a string

        index_start = strings.index("('")+2
        index_end = strings.index("')")
        json_data = strings[index_start:index_end]
        return json_data
    json_data = parse_cleaner(scripts)

    def get_json_data(json_data):
        json_data = json_data.encode('utf8').decode('unicode-escape')
        data = json.loads(json_data)
        return data
    data = get_json_data(json_data)

    def data_extractor(data):
        player_name, position, team_title, games, time = [], [], [], [], []
        goals,assists, xG, xA = [], [], [], []
        shots, key_passes,npg  = [], [], []
        xGChain, xGBuildup = [], []

        for index in range(len(data)):
            for key in data[index]:

                if key == 'player_name':
                    player_name.append(data[index][key])

                if key == 'position':
                    position.append(data[index][key])

                if key == 'team_title':
                    team_title.append(data[index][key])

                if key == 'games':
                    games.append(data[index][key])

                if key == 'time':
                    time.append(data[index][key])

                if key == 'goals':
                    goals.append((data[index][key]))

                if key == 'assists':
                    assists.append(data[index][key])

                if key == 'xG':
                    xG.append(data[index][key])

                if key == 'xA':
                    xA.append(data[index][key])

                if key == 'shots':
                    shots.append(data[index][key])

                if key == 'key_passes':
                    key_passes.append(data[index][key])

                if key == 'npg':
                    npg.append(data[index][key])

                if key == 'xGChain':
                    xGChain.append(data[index][key])

                if key == 'xGBuildup':
                    xGBuildup.append(data[index][key])


        col_names = ['Player', 'Position', 'Team', 'Games', 'Minutes', 'Goals','Assists', 'Exp Goals', 'Exp Assists','Shots', 'Key Passes','Non Pen Goals', 'Exp Goals Chain', 'Exp Goals BuildUp']

        football_df = pd.DataFrame([player_name,position,team_title, games, time, goals, assists, xG, xA, shots, key_passes, npg, xGChain, xGBuildup], index=col_names)
        football_df = football_df.T  
          
        num_cols = ['Games', 'Minutes', 'Goals','Assists', 'Exp Goals', 'Exp Assists','Shots',
                    'Key Passes','Non Pen Goals', 'Exp Goals Chain', 'Exp Goals BuildUp']

        football_df[num_cols] = football_df[num_cols].apply(pd.to_numeric)        
        for i in num_cols:
            football_df = football_df.round({i:3})

        football_df['Player'] = football_df['Player'].str.upper()
        return football_df
    football_df = data_extractor(data)
    
p1 = League_Player_Scraper()
football_df = p1.football_df
