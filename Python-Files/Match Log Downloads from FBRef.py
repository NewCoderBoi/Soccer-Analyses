# %%
"""
# Run this block before running any of the leagues. It initializes the functions to get matches and the root file path
"""

# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

# this is the file path root, i.e. where this file is located
root = str(Path(os.getcwd()).parents[0]).replace('\\','/')+'/'

def _get_table(soup):
    return soup.find_all('table')[0]
def _parse_row(row):
    cols = None
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    return cols
def get_df(path):
    URL = path
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = _get_table(soup)
    data = []
    headings=[]
    headtext = soup.find_all("th",scope="col")
    for i in range(len(headtext)):
        heading = headtext[i].get_text()
        headings.append(heading)
    headings=headings[1:len(headings)]
    data.append(headings)
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    # Iterate
    for row_index in range(len(rows)):
        row = rows[row_index]
        cols = _parse_row(row)
        data.append(cols)
    # Convert to pandas dataframe. make first row the table's column names
    # and reindex.
    data = pd.DataFrame(data)
    data = data.rename(columns=data.iloc[0])
    data = data.reindex(data.index.drop(0))
    data = data.replace('',0)
    return data


# %%
"""
# Each league has 2 blocks of code to run and then one manual step in excel/google sheets etc.
"""

# %%
"""
# Bundesliga
"""

# %%
##################### VERY, VERY IMPORTANT!!! READ!!! ####################
# I built the program so that you can run once for all seasons.....
# However that will probaby get you blocked by FBRef for 12 hours becuase it's a lot of pages very quickly
# The way around this is to run the program for a single season, with the others commented out,
# Then after it finishes, wait like, 25+ seconds and then comment that season out and uncomment the next.
# What's good is that since the seasons are done, you just have to run each season one time, so be patient :)

seasons = [
    '17-18',
#     '18-19',
#     '19-20',
#     '20-21',
#     '21-22'
]
for j in range(len(seasons)):
    ssn = seasons[j]
    if ssn == "21-22":
        season_code = 's11193'
        season = '2021-2022'

        team_code = ['247c4b67', '0cdc4311', '054efa67', 'b42c6323', 'add600ae', 'f0ac8ee6', 'a486e511',
                    '12192a4c', '2818f8bc', '033ea6b8', 'bc357bf7', 'c7a9f859', '32f3ee20', 'a224b06a',
                    'acbb6a5b', '598bc722', '7a41008f', '4eaa11d7']
        
        team_name_code = ['Arminia', 'Augsburg', 'Bayern-Munich', 'Bochum', 'Dortmund', 'Eintracht-Frankfurt', 'Freiburg',
                    'Greuther-Furth', 'Hertha-BSC', 'Hoffenheim', 'Koln', 'Bayer-Leverkusen', 'Monchengladbach', 'Mainz-05',
                    'RB-Leipzig', 'Stuttgart', 'Union-Berlin', 'Wolfsburg']
        
        team_name = ['Arminia', 'Augsburg', 'Bayern Munich', 'Bochum', 'Dortmund', 'Eintracht Frankfurt', 'Freiburg',
                    'Greuther Fürth', 'Hertha BSC', 'Hoffenheim', 'Köln', 'Bayer Leverkusen', 'Monchengladbach', 'Mainz 05',
                    'RB Leipzig', 'Stuttgart', 'Union Berlin', 'Wolfsburg']

        
    if ssn == "20-21":
        season_code = 's10737'
        season = '2020-2021'

        team_code = ['247c4b67', '0cdc4311', '054efa67', 'add600ae', 'f0ac8ee6', 'a486e511',
                    '2818f8bc', '033ea6b8', 'bc357bf7', 'c7a9f859', '32f3ee20', 'a224b06a',
                    'acbb6a5b', 'c539e393', '598bc722', '7a41008f', '62add3bf', '4eaa11d7']
        
        team_name_code = ['Arminia', 'Augsburg', 'Bayern-Munich', 'Dortmund', 'Eintracht-Frankfurt', 'Freiburg',
                    'Hertha-BSC', 'Hoffenheim', 'Koln', 'Bayer-Leverkusen', 'Monchengladbach', 'Mainz-05',
                    'RB-Leipzig', 'Schalke-04', 'Stuttgart', 'Union-Berlin', 'Werder-Bremen', 'Wolfsburg']
        
        team_name = ['Arminia', 'Augsburg', 'Bayern Munich', 'Dortmund', 'Eintracht Frankfurt', 'Freiburg',
                    'Hertha BSC', 'Hoffenheim', 'Köln', 'Bayer Leverkusen', 'Monchengladbach', 'Mainz 05',
                    'RB Leipzig', 'Schalke 04', 'Stuttgart', 'Union Berlin', 'Werder Bremen', 'Wolfsburg']

        
    if ssn == "19-20":
        season_code = 's3248'
        season = '2019-2020'

        team_code = ['0cdc4311', '054efa67', 'b1278397', 'add600ae', 'f0ac8ee6', 'a486e511',
                    '2818f8bc', '033ea6b8', 'bc357bf7', 'c7a9f859', '32f3ee20', 'a224b06a',
                    'acbb6a5b', 'c539e393', '7a41008f', '62add3bf', '4eaa11d7', 'd9f93f02']
        
        team_name_code = ['Augsburg', 'Bayern-Munich', 'Dusseldorf', 'Dortmund', 'Eintracht-Frankfurt', 'Freiburg',
                    'Hertha-BSC', 'Hoffenheim', 'Koln', 'Bayer-Leverkusen', 'Monchengladbach', 'Mainz-05',
                    'RB-Leipzig', 'Schalke-04', 'Union-Berlin', 'Werder-Bremen', 'Wolfsburg', 'Paderborn-07']
        
        team_name = ['Augsburg', 'Bayern Munich', 'Dusseldorf', 'Dortmund', 'Eintracht Frankfurt', 'Freiburg',
                    'Hertha BSC', 'Hoffenheim', 'Köln', 'Bayer Leverkusen', 'Monchengladbach', 'Mainz 05',
                    'RB Leipzig', 'Schalke 04', 'Union Berlin', 'Werder Bremen', 'Wolfsburg', 'Paderborn 07']
        
        
    if ssn == "18-19":
        season_code = 's2109'
        season = '2018-2019'

        team_code = ['0cdc4311', '054efa67', 'b1278397', 'add600ae', 'f0ac8ee6', 'a486e511',
                    '2818f8bc', '033ea6b8', 'c7a9f859', '32f3ee20', 'a224b06a', '6f2c108c',
                    'acbb6a5b', 'c539e393', '598bc722', '62add3bf', '4eaa11d7', '60b5e41f']
        
        team_name_code = ['Augsburg', 'Bayern-Munich', 'Dusseldorf', 'Dortmund', 'Eintracht-Frankfurt', 'Freiburg',
                    'Hertha-BSC', 'Hoffenheim', 'Bayer-Leverkusen', 'Monchengladbach', 'Mainz-05', 'Nurnberg',
                    'RB-Leipzig', 'Schalke-04', 'Stuttgart', 'Werder-Bremen', 'Wolfsburg', 'Hannover-96']
        
        team_name = ['Augsburg', 'Bayern Munich', 'Dusseldorf', 'Dortmund', 'Eintracht Frankfurt', 'Freiburg',
                    'Hertha BSC', 'Hoffenheim', 'Bayer Leverkusen', 'Monchengladbach', 'Mainz 05', 'Nurnberg',
                    'RB Leipzig', 'Schalke 04', 'Stuttgart', 'Werder Bremen', 'Wolfsburg', 'Hannover 96']
        
        
    if ssn == "17-18":
        season_code = 's1634'
        season = '2017-2018'

        team_code = ['0cdc4311', '054efa67', 'add600ae', 'f0ac8ee6', 'a486e511', '26790c6a',
                    '2818f8bc', '033ea6b8', 'c7a9f859', '32f3ee20', 'a224b06a',
                    'acbb6a5b', 'c539e393', '62add3bf', '4eaa11d7', '60b5e41f', 'bc357bf7', '598bc722']
        
        team_name_code = ['Augsburg', 'Bayern-Munich', 'Dortmund', 'Eintracht-Frankfurt', 'Freiburg', 'Hamburger-SV',
                    'Hertha-BSC', 'Hoffenheim', 'Bayer-Leverkusen', 'Monchengladbach', 'Mainz-05',
                    'RB-Leipzig', 'Schalke-04', 'Werder-Bremen', 'Wolfsburg', 'Hannover-96', 'Koln', 'Stuttgart']
        
        team_name = ['Augsburg', 'Bayern Munich', 'Dortmund', 'Eintracht Frankfurt', 'Freiburg', 'Hamburger SV',
                    'Hertha BSC', 'Hoffenheim', 'Bayer Leverkusen', 'Monchengladbach', 'Mainz 05',
                    'RB Leipzig', 'Schalke 04', 'Werder Bremen', 'Wolfsburg', 'Hannover 96', 'Köln', 'Stuttgart']



    df = pd.DataFrame(['Time', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG',
                       'xGA', 'Poss', 'Attendance', 'Captain', 'Formation', 'Referee', 'Match Report',
                       'Notes', 'Team', 'Season', 'xGD', 'GD', 'GD-xGD', 'Season-Matchday',
                      ]).T
    df = df.rename(columns=df.iloc[0])
    df = df.reindex(df.index.drop(0))

    for i in range(0, len(team_code)):
        path = "https://fbref.com/en/squads/%s/%s/matchlogs/%s/schedule/%s-Scores-and-Fixtures-Bundesliga" %(
            team_code[i],
            season,
            season_code,
            team_name_code[i],
        )

        team = team_name[i]

        df_matches = get_df(path)

        df_matches = df_matches[df_matches['Result']!=0] # This removes any matches that haven't happened yet. For after a season, there will be none
        df_matches['xG'] = df_matches['xG'].astype('float')
        df_matches['xGA'] = df_matches['xGA'].astype('float')
        df_matches['Poss'] = df_matches['Poss'].astype('int')
        df_matches['GF'] = df_matches['GF'].astype('int')
        df_matches['GA'] = df_matches['GA'].astype('int')

        df_matches['Team'] = team
        df_matches['Season'] = season
        df_matches['xGD'] = df_matches['xG'] - df_matches['xGA']
        df_matches['GD'] = df_matches['GF'] - df_matches['GA']
        df_matches['GD-xGD'] = df_matches['GD'] - df_matches['xGD']
        df_matches['Season-Matchday'] = df_matches['Season'] + df_matches['Round']
        df_matches['Comp'] = "Bundesliga"
        list(df_matches.columns)
        df = df.append(df_matches)
    # This program creates a separate file for each season. After the program finishes feel free to delete each season, or keep them to use individually
    df.to_csv("%sBundesliga Match Log %s.csv" %(root, ssn), index=False)
    print('Done')

# %%
"""
### Run this block after running the Bundesliga code for all 5 seasons
"""

# %%
df_17_18 = pd.read_csv("%sBundesliga Match Log 17-18.csv" %root)
df_18_19 = pd.read_csv("%sBundesliga Match Log 18-19.csv" %root)
df_19_20 = pd.read_csv("%sBundesliga Match Log 19-20.csv" %root)
df_20_21 = pd.read_csv("%sBundesliga Match Log 20-21.csv" %root)
df_21_22 = pd.read_csv("%sBundesliga Match Log 21-22.csv" %root)

df = df_17_18.append(df_18_19)
df = df.append(df_19_20)
df = df.append(df_20_21)
df = df.append(df_21_22)
df = df[df['Round']!='German 1/2 Relegation/Promotion Playoffs']  # Take out the relegation playoffs
df = df[df['Round']!='German 1/2 Relegation/Promotion Play-offs'] # Take out the relegation playoffs
df = df.reset_index(drop=True)
df['Match Number'] = ''
df['G-xG'] = df['GF'] - df['xG']
df['xGA-GA'] = df['xGA'] - df['GA']
df['GA-xGA'] = df['GA'] - df['xGA']

df.to_csv("%sBundesliga Match Log.csv" %root, index=False)
print('Done')

# %%
"""
# THE ONE MANUAL STEP (sadly):

## IN THE 'MATCH NUMBER' COLUMN in the csv:
### Enter 1 for the first cell
### Then enter this formula in the next cell and drag it down:
### 
#### =IF(R2=R3,IF(S3>S2,1,Y2+1),1)
### 
### This will create the x-axis we'll use to plot the moving-averages on. With COVID moving some matches, we can't rely on the matchday to be perfectly sequential
"""

# %%


# %%
"""
# La Liga
"""

# %%
##################### VERY, VERY IMPORTANT!!! READ!!! ####################
# I built the program so that you can run once for all seasons.....
# However that will probaby get you blocked by FBRef for 12 hours becuase it's a lot of pages very quickly
# The way around this is to run the program for a single season, with the others commented out,
# Then after it finishes, wait like, 25+ seconds and then comment that season out and uncomment the next.
# What's good is that since the seasons are done, you just have to run each season one time, so be patient :)

seasons = [
    '17-18',
#     '18-19',
#     '19-20',
#     '20-21',
#     '21-22'
]
for j in range(len(seasons)):
    ssn = seasons[j]
    if ssn == "21-22":
        season_code = 's11174'
        season = '2021-2022'

        team_code = ['8d6fd021', '2b390eca', 'db3b9613', '206d90db', 'fc536746',
                     'f25da7fb', '7848bd64', '6c8b07df', '98e8af82', '2aa12281',
                     '9800b6a1', '03c57e2b', 'a0435291', 'ee7c297c', 'a8661628',
                     '53a2f082', 'e31d1cd9', 'ad2be733', 'dcc91a7b', '2a8183b3']
        
        team_name_code = ['Alaves', 'Athletic-Club', 'Atletico-Madrid', 'Barcelona', 'Real-Betis',
                         'Celta-Vigo', 'Getafe', 'Elche', 'Rayo-Vallecano', 'Mallorca',
                          'Levante', 'Osasuna', 'Granada', 'Cadiz', 'Espanyol',
                         'Real-Madrid', 'Real-Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        team_name = ['Alavés', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Real Betis',
                    'Celta Vigo', 'Getafe', 'Elche', 'Rayo Vallecano', 'Mallorca',
                     'Levante', 'Osasuna', 'Granada', 'Cádiz', 'Espanyol',
                    'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Villarreal']

        
    if ssn == "20-21":
        season_code = 's10731'
        season = '2020-2021'

        team_code = ['8d6fd021', '2b390eca', 'db3b9613', '206d90db', 'fc536746',
                     'f25da7fb', 'bea5c710', '7848bd64', '6c8b07df', 'c6c493e6',
                     '9800b6a1', '17859612', '03c57e2b', 'a0435291', 'ee7c297c',
                     '53a2f082', 'e31d1cd9', 'ad2be733', 'dcc91a7b', '2a8183b3']
        
        team_name_code = ['Alaves', 'Athletic-Club', 'Atletico-Madrid', 'Barcelona', 'Real-Betis',
                         'Celta-Vigo', 'Eibar', 'Getafe', 'Elche', 'Huesca',
                          'Levante', 'Valladolid', 'Osasuna', 'Granada', 'Cadiz',
                         'Real-Madrid', 'Real-Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        team_name = ['Alavés', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Real Betis',
                    'Celta Vigo', 'Eibar', 'Getafe', 'Elche', 'Huesca',
                     'Levante', 'Valladolid', 'Osasuna', 'Granada', 'Cádiz',
                    'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Villarreal']

        
    if ssn == "19-20":
        season_code = 's3239'
        season = '2019-2020'

        team_code = ['8d6fd021', '2b390eca', 'db3b9613', '206d90db', 'fc536746',
                     'f25da7fb', 'bea5c710', 'a8661628', '7848bd64', '2aa12281',
                     '7c6f2c78', '9800b6a1', '17859612', '03c57e2b', 'a0435291',
                     '53a2f082', 'e31d1cd9', 'ad2be733', 'dcc91a7b', '2a8183b3']
        
        team_name_code = ['Alaves', 'Athletic-Club', 'Atletico-Madrid', 'Barcelona', 'Real-Betis',
                         'Celta-Vigo', 'Eibar', 'Espanyol', 'Getafe', 'Mallorca',
                          'Leganes', 'Levante', 'Valladolid', 'Osasuna', 'Granada',
                         'Real-Madrid', 'Real-Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        team_name = ['Alavés', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Real Betis',
                    'Celta Vigo', 'Eibar', 'Espanyol', 'Getafe', 'Mallorca',
                     'Leganés', 'Levante', 'Valladolid', 'Osasuna', 'Granada',
                    'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        
    if ssn == "18-19":
        season_code = 's1886'
        season = '2018-2019'

        team_code = ['8d6fd021', '2b390eca', 'db3b9613', '206d90db', 'fc536746',
                     'f25da7fb', 'bea5c710', 'a8661628', '7848bd64', '9024a00a',
                     '7c6f2c78', '9800b6a1', 'c6c493e6', '17859612', '98e8af82',
                     '53a2f082', 'e31d1cd9', 'ad2be733', 'dcc91a7b', '2a8183b3']
        
        team_name_code = ['Alaves', 'Athletic-Club', 'Atletico-Madrid', 'Barcelona', 'Real-Betis',
                         'Celta-Vigo', 'Eibar', 'Espanyol', 'Getafe', 'Girona',
                          'Leganes', 'Levante', 'Huesca', 'Valladolid', 'Rayo-Vallecano',
                         'Real-Madrid', 'Real-Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        team_name = ['Alavés', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Real Betis',
                    'Celta Vigo', 'Eibar', 'Espanyol', 'Getafe', 'Girona',
                     'Leganés', 'Levante', 'Huesca', 'Valladolid', 'Rayo-Vallecano',
                    'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        
    if ssn == "17-18":
        season_code = 's1652'
        season = '2017-2018'

        team_code = ['8d6fd021', '2b390eca', 'db3b9613', '206d90db', 'fc536746',
                     'f25da7fb', 'bea5c710', 'a8661628', '7848bd64', '9024a00a',
                     '2a60ed82', '0049d422', '7c6f2c78', '9800b6a1', '1c896955',
                     '53a2f082', 'e31d1cd9', 'ad2be733', 'dcc91a7b', '2a8183b3']
        
        team_name_code = ['Alaves', 'Athletic-Club', 'Atletico-Madrid', 'Barcelona', 'Real-Betis',
                         'Celta-Vigo', 'Eibar', 'Espanyol', 'Getafe', 'Girona',
                          'Deportivo-La-Coruna', 'Las-Palmas', 'Leganes', 'Levante', 'Malaga',
                         'Real-Madrid', 'Real-Sociedad', 'Sevilla', 'Valencia', 'Villarreal']
        
        team_name = ['Alavés', 'Athletic Club', 'Atlético Madrid', 'Barcelona', 'Real Betis',
                    'Celta Vigo', 'Eibar', 'Espanyol', 'Getafe', 'Girona',
                     'Deportivo', 'Las Palmas', 'Leganés', 'Levante', 'Málaga',
                    'Real Madrid', 'Real Sociedad', 'Sevilla', 'Valencia', 'Villarreal']



    df = pd.DataFrame(['Time', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG',
                       'xGA', 'Poss', 'Attendance', 'Captain', 'Formation', 'Referee', 'Match Report',
                       'Notes', 'Team', 'Season', 'xGD', 'GD', 'GD-xGD', 'Season-Matchday',
                      ]).T
    df = df.rename(columns=df.iloc[0])
    df = df.reindex(df.index.drop(0))

    for i in range(0, len(team_code)):
        path = "https://fbref.com/en/squads/%s/%s/matchlogs/%s/schedule/%s-Scores-and-Fixtures-La-Liga" %(
            team_code[i],
            season,
            season_code,
            team_name_code[i],
        )

        team = team_name[i]

        df_matches = get_df(path)

        df_matches = df_matches[df_matches['Result']!=0] # This removes any matches that haven't happened yet. For after a season, there will be none
        df_matches['xG'] = df_matches['xG'].astype('float')
        df_matches['xGA'] = df_matches['xGA'].astype('float')
        df_matches['Poss'] = df_matches['Poss'].astype('int')
        df_matches['GF'] = df_matches['GF'].astype('int')
        df_matches['GA'] = df_matches['GA'].astype('int')

        df_matches['Team'] = team
        df_matches['Season'] = season
        df_matches['xGD'] = df_matches['xG'] - df_matches['xGA']
        df_matches['GD'] = df_matches['GF'] - df_matches['GA']
        df_matches['GD-xGD'] = df_matches['GD'] - df_matches['xGD']
        df_matches['Season-Matchday'] = df_matches['Season'] + df_matches['Round']
        df_matches['Comp'] = "La Liga"
        list(df_matches.columns)
        df = df.append(df_matches)
    # This program creates a separate file for each season. After the program finishes feel free to delete each season, or keep them to use individually
    df.to_csv("%sLa Liga Match Log %s.csv" %(root, ssn), index=False)
    print('Done')

# %%
"""
### Run this block after running the La Liga code for all 5 seasons
"""

# %%
df_17_18 = pd.read_csv("%sLa Liga Match Log 17-18.csv" %root)
df_18_19 = pd.read_csv("%sLa Liga Match Log 18-19.csv" %root)
df_19_20 = pd.read_csv("%sLa Liga Match Log 19-20.csv" %root)
df_20_21 = pd.read_csv("%sLa Liga Match Log 20-21.csv" %root)
df_21_22 = pd.read_csv("%sLa Liga Match Log 21-22.csv" %root)

df = df_17_18.append(df_18_19)
df = df.append(df_19_20)
df = df.append(df_20_21)
df = df.append(df_21_22)
df = df.reset_index(drop=True)
df['Match Number'] = ''
df['G-xG'] = df['GF'] - df['xG']
df['xGA-GA'] = df['xGA'] - df['GA']
df['GA-xGA'] = df['GA'] - df['xGA']

df.to_csv("%sLa Liga Match Log.csv" %root, index=False)
print('Done')

# %%
"""
# THE ONE MANUAL STEP (sadly):

## IN THE 'MATCH NUMBER' COLUMN in the csv:
### Enter 1 for the first cell
### Then enter this formula in the next cell and drag it down:
### 
#### =IF(R2=R3,IF(S3>S2,1,Y2+1),1)
### 
### This will create the x-axis we'll use to plot the moving-averages on. With COVID moving some matches, we can't rely on the matchday to be perfectly sequential
"""

# %%


# %%
"""
# Premier League
"""

# %%
##################### VERY, VERY IMPORTANT!!! READ!!! ####################
# I built the program so that you can run once for all seasons.....
# However that will probaby get you blocked by FBRef for 12 hours becuase it's a lot of pages very quickly
# The way around this is to run the program for a single season, with the others commented out,
# Then after it finishes, wait like, 25+ seconds and then comment that season out and uncomment the next.
# What's good is that since the seasons are done, you just have to run each season one time, so be patient :)

seasons = [
    '17-18',
#     '18-19',
#     '19-20',
#     '20-21',
#     '21-22'
]
for j in range(len(seasons)):
    ssn = seasons[j]
    if ssn == "21-22":
        season_code = 's11160'
        season = '2021-2022'

        team_code = ['18bb7c10', 'd07537b9', '943e8050', 'cff3d9bb',
                     '47c64c55', 'd3fd31cc', 'a2d435b3', '822bd0ba',
                     'b8fd03ef', '19538871', 'b2b47a98', '33c895d4',
                     '361ca564', '7c21e445',
                     '8cec06e1', '8602292d', '5bfb9659', '1c781004', '2abfe087', 'cd051869']
        
        team_name_code = ['Arsenal', 'Brighton-and-Hove-Albion', 'Burnley', 'Chelsea',
                          'Crystal-Palace', 'Everton', 'Leicester-City', 'Liverpool',
                          'Manchester-City', 'Manchester-United', 'Newcastle-United', 'Southampton',
                          'Tottenham-Hotspur', 'West-Ham-United',
                          'Wolverhampton-Wanderers', 'Aston-Villa', 'Leeds-United', 'Norwich-City', 'Watford', 'Brentford']
        
        team_name = ['Arsenal', 'Brighton', 'Burnley', 'Chelsea',
                     'Crystal Palace', 'Everton', 'Leicester City', 'Liverpool',
                     'Manchester City', 'Manchester United', 'Newcastle', 'Southampton',
                     'Tottenham', 'West Ham',
                     'Wolves', 'Aston Villa', 'Leeds United', 'Norwich', 'Watford', 'Brentford']

        
    if ssn == "20-21":
        season_code = 's10728'
        season = '2020-2021'

        team_code = ['18bb7c10', 'd07537b9', '943e8050', 'cff3d9bb',
                     '47c64c55', 'd3fd31cc', 'a2d435b3', '822bd0ba',
                     'b8fd03ef', '19538871', 'b2b47a98', '33c895d4',
                     '361ca564', '7c21e445',
                     '8cec06e1', '8602292d', '1df6b87e', '5bfb9659', '60c6b05f', 'fd962109']
        
        team_name_code = ['Arsenal', 'Brighton-and-Hove-Albion', 'Burnley', 'Chelsea',
                          'Crystal-Palace', 'Everton', 'Leicester-City', 'Liverpool',
                          'Manchester-City', 'Manchester-United', 'Newcastle-United', 'Southampton',
                          'Tottenham-Hotspur', 'West-Ham-United',
                          'Wolverhampton-Wanderers', 'Aston-Villa', 'Sheffield-United', 'Leeds-United', 'West-Bromwich-Albion', 'Fulham']
        
        team_name = ['Arsenal', 'Brighton', 'Burnley', 'Chelsea',
                     'Crystal Palace', 'Everton', 'Leicester City', 'Liverpool',
                     'Manchester City', 'Manchester United', 'Newcastle', 'Southampton',
                     'Tottenham', 'West Ham',
                     'Wolves', 'Aston Villa', 'Sheffield United', 'Leeds United', 'West Brom', 'Fulham']

        
    if ssn == "19-20":
        season_code = 's3232'
        season = '2019-2020'

        team_code = ['18bb7c10', '4ba7cbea', 'd07537b9', '943e8050', 'cff3d9bb',
                     '47c64c55', 'd3fd31cc', 'a2d435b3', '822bd0ba',
                     'b8fd03ef', '19538871', 'b2b47a98', '33c895d4',
                     '361ca564', '2abfe087', '7c21e445',
                     '8cec06e1', '8602292d', '1c781004', '1df6b87e']
        
        team_name_code = ['Arsenal', 'Bournemouth', 'Brighton-and-Hove-Albion', 'Burnley', 'Chelsea',
                          'Crystal-Palace', 'Everton', 'Leicester-City', 'Liverpool',
                          'Manchester-City', 'Manchester-United', 'Newcastle-United', 'Southampton',
                          'Tottenham-Hotspur', 'Watford', 'West-Ham-United',
                          'Wolverhampton-Wanderers', 'Aston-Villa', 'Norwich-City', 'Sheffield-United']
        
        team_name = ['Arsenal', 'Bournemouth', 'Brighton', 'Burnley', 'Chelsea',
                     'Crystal Palace', 'Everton', 'Leicester City', 'Liverpool',
                     'Manchester City', 'Manchester United', 'Newcastle', 'Southampton',
                     'Tottenham', 'Watford', 'West Ham',
                     'Wolves', 'Aston Villa', 'Norwich', 'Sheffield United']
        
        
    if ssn == "18-19":
        season_code = 's1889'
        season = '2018-2019'

        team_code = ['18bb7c10', '4ba7cbea', 'd07537b9', '943e8050', 'cff3d9bb',
                     '47c64c55', 'd3fd31cc', 'f5922ca5', 'a2d435b3', '822bd0ba',
                     'b8fd03ef', '19538871', 'b2b47a98', '33c895d4',
                     '361ca564', '2abfe087', '7c21e445',
                     '8cec06e1', '75fae011', 'fd962109']
        
        team_name_code = ['Arsenal', 'Bournemouth', 'Brighton-and-Hove-Albion', 'Burnley', 'Chelsea',
                          'Crystal-Palace', 'Everton', 'Huddersfield-Town', 'Leicester-City', 'Liverpool',
                          'Manchester-City', 'Manchester-United', 'Newcastle-United', 'Southampton',
                          'Tottenham-Hotspur', 'Watford', 'West-Ham-United',
                          'Wolverhampton-Wanderers', 'Cardiff-City', 'Fulham']
        
        team_name = ['Arsenal', 'Bournemouth', 'Brighton', 'Burnley', 'Chelsea',
                     'Crystal Palace', 'Everton', 'Huddersfield Town', 'Leicester City', 'Liverpool',
                     'Manchester City', 'Manchester United', 'Newcastle', 'Southampton',
                     'Tottenham', 'Watford', 'West Ham',
                     'Wolves', 'Cardiff City', 'Fulham']
        
        
    if ssn == "17-18":
        season_code = 's1631'
        season = '2017-2018'

        team_code = ['18bb7c10', '4ba7cbea', 'd07537b9', '943e8050', 'cff3d9bb',
                     '47c64c55', 'd3fd31cc', 'f5922ca5', 'a2d435b3', '822bd0ba',
                     'b8fd03ef', '19538871', 'b2b47a98', '33c895d4', '17892952',
                     'fb10988f', '361ca564', '2abfe087', '60c6b05f', '7c21e445']
        
        team_name_code = ['Arsenal', 'Bournemouth', 'Brighton-and-Hove-Albion', 'Burnley', 'Chelsea',
                          'Crystal-Palace', 'Everton', 'Huddersfield-Town', 'Leicester-City', 'Liverpool',
                          'Manchester-City', 'Manchester-United', 'Newcastle-United', 'Southampton', 'Stoke-City',
                          'Swansea-City', 'Tottenham-Hotspur', 'Watford', 'West-Bromwich-Albion', 'West-Ham-United']
        
        team_name = ['Arsenal', 'Bournemouth', 'Brighton', 'Burnley', 'Chelsea',
                     'Crystal Palace', 'Everton', 'Huddersfield Town', 'Leicester City', 'Liverpool',
                     'Manchester City', 'Manchester United', 'Newcastle', 'Southampton', 'Stoke City',
                     'Swansea', 'Tottenham', 'Watford', 'West Brom', 'West Ham']



    df = pd.DataFrame(['Time', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG',
                       'xGA', 'Poss', 'Attendance', 'Captain', 'Formation', 'Referee', 'Match Report',
                       'Notes', 'Team', 'Season', 'xGD', 'GD', 'GD-xGD', 'Season-Matchday',
                      ]).T
    df = df.rename(columns=df.iloc[0])
    df = df.reindex(df.index.drop(0))

    for i in range(0, len(team_code)):
        path = "https://fbref.com/en/squads/%s/%s/matchlogs/%s/schedule/%s-Scores-and-Fixtures-Premier-League" %(
            team_code[i],
            season,
            season_code,
            team_name_code[i],
        )

        team = team_name[i]

        df_matches = get_df(path)

        df_matches = df_matches[df_matches['Result']!=0] # This removes any matches that haven't happened yet. For after a season, there will be none
        df_matches['xG'] = df_matches['xG'].astype('float')
        df_matches['xGA'] = df_matches['xGA'].astype('float')
        df_matches['Poss'] = df_matches['Poss'].astype('int')
        df_matches['GF'] = df_matches['GF'].astype('int')
        df_matches['GA'] = df_matches['GA'].astype('int')

        df_matches['Team'] = team
        df_matches['Season'] = season
        df_matches['xGD'] = df_matches['xG'] - df_matches['xGA']
        df_matches['GD'] = df_matches['GF'] - df_matches['GA']
        df_matches['GD-xGD'] = df_matches['GD'] - df_matches['xGD']
        df_matches['Season-Matchday'] = df_matches['Season'] + df_matches['Round']
        df_matches['Comp'] = "Premier League"
        list(df_matches.columns)
        df = df.append(df_matches)
    # This program creates a separate file for each season. After the program finishes feel free to delete each season, or keep them to use individually
    df.to_csv("%sPremier League Match Log %s.csv" %(root, ssn), index=False)
    print('Done')

# %%
"""
### Run this block after running the Premier League code for all 5 seasons
"""

# %%
df_17_18 = pd.read_csv("%sPremier League Match Log 17-18.csv" %root)
df_18_19 = pd.read_csv("%sPremier League Match Log 18-19.csv" %root)
df_19_20 = pd.read_csv("%sPremier League Match Log 19-20.csv" %root)
df_20_21 = pd.read_csv("%sPremier League Match Log 20-21.csv" %root)
df_21_22 = pd.read_csv("%sPremier League Match Log 21-22.csv" %root)

df = df_17_18.append(df_18_19)
df = df.append(df_19_20)
df = df.append(df_20_21)
df = df.append(df_21_22)
df = df.reset_index(drop=True)
df['Match Number'] = ''
df['G-xG'] = df['GF'] - df['xG']
df['xGA-GA'] = df['xGA'] - df['GA']
df['GA-xGA'] = df['GA'] - df['xGA']

df.to_csv("%sPremier League Match Log.csv" %root, index=False)
print('Done')

# %%
"""
# THE ONE MANUAL STEP (sadly):

## IN THE 'MATCH NUMBER' COLUMN in the csv:
### Enter 1 for the first cell
### Then enter this formula in the next cell and drag it down:
### 
#### =IF(R2=R3,IF(S3>S2,1,Y2+1),1)
### 
### This will create the x-axis we'll use to plot the moving-averages on. With COVID moving some matches, we can't rely on the matchday to be perfectly sequential
"""

# %%


# %%
"""
# Serie A
"""

# %%
##################### VERY, VERY IMPORTANT!!! READ!!! ####################
# I built the program so that you can run once for all seasons.....
# However that will probaby get you blocked by FBRef for 12 hours becuase it's a lot of pages very quickly
# The way around this is to run the program for a single season, with the others commented out,
# Then after it finishes, wait like, 25+ seconds and then comment that season out and uncomment the next.
# What's good is that since the seasons are done, you just have to run each season one time, so be patient :)

seasons = [
    '17-18',
#     '18-19',
#     '19-20',
#     '20-21',
#     '21-22'
]
for j in range(len(seasons)):
    ssn = seasons[j]
    if ssn == "21-22":
        season_code = 's11222'
        season = '2021-2022'

        team_code = ['922493f3', '1d8099f8', 'c4260e09', '421387cf', 'a3d88bd8',
                    '658bf2de', '0e72edf2', 'd609edc0', 'e0652b02', '7213da33',
                     'dc56fe14', 'd48ad4ff', 'cf74a709', 'c5577084', '8ff9e3b3',
                    'e2befd26', '68449f6d', '105360fe', '04eea015', 'af5d5982']
        
        team_name_code = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina', 'Empoli',
                         'Genoa', 'Hellas-Verona', 'Inter', 'Juventus', 'Lazio',
                          'Milan','Napoli', 'Roma', 'Salernitana', 'Sampdoria',
                          'Sassuolo', 'Spezia', 'Torino', 'Udinese', 'Venezia']
        
        team_name = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina', 'Empoli',
                    'Genoa', 'Hellas Verona', 'Inter', 'Juventus', 'Lazio',
                     'Milan', 'Napoli', 'Roma', 'Salernitana', 'Sampdoria',
                     'Sassuolo', 'Spezia', 'Torino', 'Udinese', 'Venezia']

        
    if ssn == "20-21":
        season_code = 's10730'
        season = '2020-2021'

        team_code = ['922493f3', '1d8099f8', 'c4260e09', '421387cf',
                    '658bf2de', '0e72edf2', 'd609edc0', 'e0652b02', '7213da33',
                     'dc56fe14', 'd48ad4ff', 'cf74a709', '8ff9e3b3',
                    'e2befd26', '68449f6d', '105360fe', '04eea015', '4fcb34fd', '3074d7b1', 'eab4234c']
        
        team_name_code = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                         'Genoa', 'Hellas-Verona', 'Inter', 'Juventus', 'Lazio',
                          'Milan','Napoli', 'Roma', 'Sampdoria',
                          'Sassuolo', 'Spezia', 'Torino', 'Udinese', 'Benevento', 'Crotone', 'Parma']
        
        team_name = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                    'Genoa', 'Hellas Verona', 'Inter', 'Juventus', 'Lazio',
                     'Milan', 'Napoli', 'Roma', 'Sampdoria',
                     'Sassuolo', 'Spezia', 'Torino', 'Udinese', 'Benevento', 'Crotone', 'Parma']

        
    if ssn == "19-20":
        season_code = 's3260'
        season = '2019-2020'

        team_code = ['922493f3', '1d8099f8', 'c4260e09', '421387cf',
                    '658bf2de', '0e72edf2', 'd609edc0', 'e0652b02', '7213da33',
                     'dc56fe14', 'd48ad4ff', 'cf74a709', '8ff9e3b3',
                    'e2befd26', '105360fe', '04eea015', 'eab4234c', 'ffcbe334', '4ef57aeb', '1d2fe027']
        
        team_name_code = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                         'Genoa', 'Hellas-Verona', 'Inter', 'Juventus', 'Lazio',
                          'Milan','Napoli', 'Roma', 'Sampdoria',
                          'Sassuolo', 'Torino', 'Udinese', 'Parma', 'Lecce', 'Brescia', 'SPAL']
        
        team_name = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                    'Genoa', 'Hellas Verona', 'Inter', 'Juventus', 'Lazio',
                     'Milan', 'Napoli', 'Roma', 'Sampdoria',
                     'Sassuolo', 'Torino', 'Udinese', 'Parma', 'Lecce', 'Brescia', 'SPAL']
        
        
    if ssn == "18-19":
        season_code = 's1896'
        season = '2018-2019'

        team_code = ['922493f3', '1d8099f8', 'c4260e09', '421387cf',
                    '658bf2de', 'd609edc0', 'e0652b02', '7213da33',
                     'dc56fe14', 'd48ad4ff', 'cf74a709', '8ff9e3b3',
                    'e2befd26', '105360fe', '04eea015', 'eab4234c', '1d2fe027', 'cc919b35', 'a3d88bd8', '6a7ad59d']
        
        team_name_code = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                         'Genoa', 'Inter', 'Juventus', 'Lazio',
                          'Milan','Napoli', 'Roma', 'Sampdoria',
                          'Sassuolo', 'Torino', 'Udinese', 'Parma', 'SPAL', 'Chievo', 'Empoli', 'Frosinone']
        
        team_name = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                    'Genoa', 'Inter', 'Juventus', 'Lazio',
                     'Milan', 'Napoli', 'Roma', 'Sampdoria',
                     'Sassuolo', 'Torino', 'Udinese', 'Parma', 'SPAL', 'Chievo', 'Empoli', 'Frosinone']
        
        
    if ssn == "17-18":
        season_code = 's1640'
        season = '2017-2018'

        team_code = ['922493f3', '1d8099f8', 'c4260e09', '421387cf',
                    '658bf2de', 'd609edc0', 'e0652b02', '7213da33',
                     'dc56fe14', 'd48ad4ff', 'cf74a709', '8ff9e3b3',
                    'e2befd26', '105360fe', '04eea015', '1d2fe027', 'cc919b35', '3074d7b1', '0e72edf2', '4fcb34fd']
        
        team_name_code = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                         'Genoa', 'Inter', 'Juventus', 'Lazio',
                          'Milan','Napoli', 'Roma', 'Sampdoria',
                          'Sassuolo', 'Torino', 'Udinese', 'SPAL', 'Chievo', 'Crotone', 'Hellas-Verona', 'Benevento']
        
        team_name = ['Atalanta', 'Bologna', 'Cagliari', 'Fiorentina',
                    'Genoa', 'Inter', 'Juventus', 'Lazio',
                     'Milan', 'Napoli', 'Roma', 'Sampdoria',
                     'Sassuolo', 'Torino', 'Udinese', 'SPAL', 'Chievo', 'Crotone', 'Hellas Verona', 'Benevento']



    df = pd.DataFrame(['Time', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG',
                       'xGA', 'Poss', 'Attendance', 'Captain', 'Formation', 'Referee', 'Match Report',
                       'Notes', 'Team', 'Season', 'xGD', 'GD', 'GD-xGD', 'Season-Matchday',
                      ]).T
    df = df.rename(columns=df.iloc[0])
    df = df.reindex(df.index.drop(0))

    for i in range(0, len(team_code)):
        path = "https://fbref.com/en/squads/%s/%s/matchlogs/%s/schedule/%s-Scores-and-Fixtures-Serie-A" %(
            team_code[i],
            season,
            season_code,
            team_name_code[i],
        )

        team = team_name[i]

        df_matches = get_df(path)

        df_matches = df_matches[df_matches['Result']!=0] # This removes any matches that haven't happened yet. For after a season, there will be none
        df_matches['xG'] = df_matches['xG'].astype('float')
        df_matches['xGA'] = df_matches['xGA'].astype('float')
        df_matches['Poss'] = df_matches['Poss'].astype('int')
        df_matches['GF'] = df_matches['GF'].astype('int')
        df_matches['GA'] = df_matches['GA'].astype('int')

        df_matches['Team'] = team
        df_matches['Season'] = season
        df_matches['xGD'] = df_matches['xG'] - df_matches['xGA']
        df_matches['GD'] = df_matches['GF'] - df_matches['GA']
        df_matches['GD-xGD'] = df_matches['GD'] - df_matches['xGD']
        df_matches['Season-Matchday'] = df_matches['Season'] + df_matches['Round']
        df_matches['Comp'] = "Serie A"
        list(df_matches.columns)
        df = df.append(df_matches)
    # This program creates a separate file for each season. After the program finishes feel free to delete each season, or keep them to use individually
    df.to_csv("%sSerie A Match Log %s.csv" %(root, ssn), index=False)
    print('Done')

# %%
"""
### Run this block after running the Serie A code for all 5 seasons
"""

# %%
df_17_18 = pd.read_csv("%sSerie A Match Log 17-18.csv" %root)
df_18_19 = pd.read_csv("%sSerie A Match Log 18-19.csv" %root)
df_19_20 = pd.read_csv("%sSerie A Match Log 19-20.csv" %root)
df_20_21 = pd.read_csv("%sSerie A Match Log 20-21.csv" %root)
df_21_22 = pd.read_csv("%sSerie A Match Log 21-22.csv" %root)

df = df_17_18.append(df_18_19)
df = df.append(df_19_20)
df = df.append(df_20_21)
df = df.append(df_21_22)
df = df.reset_index(drop=True)
df['Match Number'] = ''
df['G-xG'] = df['GF'] - df['xG']
df['xGA-GA'] = df['xGA'] - df['GA']
df['GA-xGA'] = df['GA'] - df['xGA']

df.to_csv("%sSerie A Match Log.csv" %root, index=False)
print('Done')

# %%
"""
# THE ONE MANUAL STEP (sadly):

## IN THE 'MATCH NUMBER' COLUMN in the csv:
### Enter 1 for the first cell
### Then enter this formula in the next cell and drag it down:
### 
#### =IF(R2=R3,IF(S3>S2,1,Y2+1),1)
### 
### This will create the x-axis we'll use to plot the moving-averages on. With COVID moving some matches, we can't rely on the matchday to be perfectly sequential
"""