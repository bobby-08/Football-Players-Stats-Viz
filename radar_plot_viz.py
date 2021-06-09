import pandas as pd
#%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar
from data_preprocessor import football_df


def player_input(football_df):
    player1 = str(input('Please Enter the Player 1: ')).upper()
    player2 = str(input('Please Enter the Player 2: ')).upper()

    print('Analyzing player: ',player1)
    print('xxxxxxxxxxx')
    print('Analyzing player: ',player2)
    return player1, player2
player1, player2 = player_input(football_df)

def player_dataframe(player1, player2):
    player_df = football_df[(football_df['Player'] == player1) | (football_df['Player'] == player2)].reset_index()
    player_df = player_df.drop(['index'], axis=1)
    #Getting the columns
    cols = list(player_df.columns)
    cols = cols[4:]
    for col in cols:
        player_df[col] = pd.to_numeric(player_df[col])
    return player_df
player_df = player_dataframe(player1, player2)

#Getting the columns
cols = list(player_df.columns)
cols = cols[4:]
for col in cols:
    player_df[col] = pd.to_numeric(player_df[col])

def range_creator(player_df):
    #Creating Empty lists
    ranges = []
    a_range = []
    b_range = []

    # Adding Ranges
    for x in cols:
        a = min(player_df[cols][x])
        a = a - (a*.25)

        b = max(player_df[cols][x])
        b = b + (b*.25)

        ranges.append((a,b))

    for x in range(len(player_df['Player'])):
        if player_df['Player'][x] ==  player1:
            a_range = player_df.iloc[x].values.tolist()
        if player_df['Player'][x] == player2:
            b_range = player_df.iloc[x].values.tolist()

    a_range = a_range[4:]
    b_range = b_range[4:]

    values = [a_range,b_range]
    return ranges, values
ranges, values = range_creator(player_df)

def player_viz(ranges, values, player_df):
    #Titles
    title = dict(
        title_name=player1,
        title_color='Black',
        #subtitle_name=player_df['Team'][0],
        subtitle_color='Black',
        title_name_2=player2,
        title_color_2='Red',
        #subtitle_name_2=player_df['Team'][1],
        subtitle_color_2='Red',
        title_fontsize=18,
        subtitle_fontsize=15,
    )
    #Plotting
    radar = Radar()

    fig,ax = radar.plot_radar(ranges=ranges,params=cols,values=values,
                             radar_color=['Black','Red'],
                             alphas=[.75,.6],title=title,
                             compare=True)
    return fig,ax
fig,ax = player_viz(ranges, values, player_df)
plt.show()