# %%
"""
# Change the file names, the first 4 lines of code, if you want  each file to be named differently
### The 'raw' files are intermediate steps
### You will only end up using the 'final' files
"""

# %%
# File names to change if needed
raw_nongk = 'Raw FBRef 2022-2023'
raw_gk = 'Raw FBRef GK 2022-2023'
final_nongk = 'Final FBRef 2022-2023'
final_gk = 'Final FBRef GK 2022-2023'

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import time
import warnings
warnings.filterwarnings("ignore")

# this is the file path root, i.e. where this file is located
root = str(Path(os.getcwd()).parents[0]).replace('\\','/')+'/'

# This section creates the programs that gather data from FBRef.com... Data is from FBRef and Opta
def _get_table(soup):
    return soup.find_all('table')[0]

def _get_opp_table(soup):
    return soup.find_all('table')[1]

def _parse_row(row):
    cols = None
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    return cols

def get_df(path):
    URL = path
    time.sleep(4)
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

    for row_index in range(len(rows)):
        row = rows[row_index]
        cols = _parse_row(row)
        data.append(cols)
    
    data = pd.DataFrame(data)
    data = data.rename(columns=data.iloc[0])
    data = data.reindex(data.index.drop(0))
    data = data.replace('',0)
    return data

def get_opp_df(path):
    URL = path
    time.sleep(4)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = _get_opp_table(soup)
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

    for row_index in range(len(rows)):
        row = rows[row_index]
        cols = _parse_row(row)
        data.append(cols)
    
    data = pd.DataFrame(data)
    data = data.rename(columns=data.iloc[0])
    data = data.reindex(data.index.drop(0))
    data = data.replace('',0)
    return data


# this section gets the raw tables from FBRef.com

standard = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
shooting = "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats"
passing = "https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats"
pass_types = "https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats"
gsca = "https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats"
defense = "https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats"
poss = "https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats"
misc = "https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats"

df_standard = get_df(standard)
df_shooting = get_df(shooting)
df_passing = get_df(passing)
df_pass_types = get_df(pass_types)
df_gsca = get_df(gsca)
df_defense = get_df(defense)
df_poss = get_df(poss)
df_misc = get_df(misc)

# this section sorts the raw tables then resets their indexes. Without this step, you will
# run into issues with players who play minutes for 2 clubs in a season.

df_standard.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_shooting.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_passing.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_pass_types.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_gsca.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_defense.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_poss.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_misc.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)

df_standard = df_standard.reset_index(drop=True)
df_shooting = df_shooting.reset_index(drop=True)
df_passing = df_passing.reset_index(drop=True)
df_pass_types = df_pass_types.reset_index(drop=True)
df_gsca = df_gsca.reset_index(drop=True)
df_defense = df_defense.reset_index(drop=True)
df_poss = df_poss.reset_index(drop=True)
df_misc = df_misc.reset_index(drop=True)

# Now the fun part... merging all raw tables into one.
# Change any column name you want to change:
# Example --   'Gls': 'Goals'  changes column "Gls" to be named "Goals", etc.
## Note that I inclide all columns but don't always change the names... this is useful to me when I need to update the columns, like when FBRef witched to Opta data haha. I got lucky as this made it easier on me!

df = df_standard.iloc[:, 0:10]
df = df.join(df_standard.iloc[:, 13])
df = df.join(df_standard.iloc[:, 26])
df = df.rename(columns={'G-PK': 'npGoals', 'Gls':'Glsxx'})
df = df.join(df_shooting.iloc[:,8:25])
df = df.rename(columns={'Gls': 'Goals', 'Sh': 'Shots', 'SoT': 'SoT', 'SoT%': 'SoT%', 'Sh/90': 'Sh/90', 'SoT/90': 'SoT/90', 'G/Sh': 'G/Sh', 'G/SoT': 'G/SoT', 'Dist': 'AvgShotDistance', 'FK': 'FKShots', 'PK': 'PK', 'PKatt': 'PKsAtt', 'xG': 'xG', 'npxG': 'npxG', 'npxG/Sh': 'npxG/Sh', 'G-xG': 'G-xG', 'np:G-xG': 'npG-xG'})

df = df.join(df_passing.iloc[:,8:13])
df = df.rename(columns={'Cmp': 'PassesCompleted', 'Att': 'PassesAttempted', 'Cmp%': 'TotCmp%', 'TotDist': 'TotalPassDist', 'PrgDist': 'ProgPassDist', })
df = df.join(df_passing.iloc[:,13:16])
df = df.rename(columns={'Cmp': 'ShortPassCmp', 'Att': 'ShortPassAtt', 'Cmp%': 'ShortPassCmp%', })
df = df.join(df_passing.iloc[:,16:19])
df = df.rename(columns={'Cmp': 'MedPassCmp', 'Att': 'MedPassAtt', 'Cmp%': 'MedPassCmp%', })
df = df.join(df_passing.iloc[:,19:22])
df = df.rename(columns={'Cmp': 'LongPassCmp', 'Att': 'LongPassAtt', 'Cmp%': 'LongPassCmp%', })
df = df.join(df_passing.iloc[:,22:31])
df = df.rename(columns={'Ast': 'Assists', 'xAG':'xAG', 'xA': 'xA', 'A-xAG': 'A-xAG', 'KP': 'KeyPasses', '1/3': 'Final1/3Cmp', 'PPA': 'PenAreaCmp', 'CrsPA': 'CrsPenAreaCmp', 'PrgP': 'ProgPasses', })

df = df.join(df_pass_types.iloc[:, 9:23])
df = df.rename(columns={'Live': 'LivePass', 'Dead': 'DeadPass', 'FK': 'FKPasses', 'TB': 'ThruBalls', 'Sw': 'Switches', 'Crs': 'Crs', 'CK': 'CK', 'In': 'InSwingCK', 'Out': 'OutSwingCK', 'Str': 'StrCK', 'TI': 'ThrowIn', 'Off': 'PassesToOff', 'Blocks':'PassesBlocked', 'Cmp':'Cmpxxx'})

df = df.join(df_gsca.iloc[:, 8:16].rename(columns={'SCA': 'SCA', 'SCA90': 'SCA90', 'PassLive': 'SCAPassLive', 'PassDead': 'SCAPassDead', 'TO': 'SCADrib', 'Sh': 'SCASh', 'Fld': 'SCAFld', 'Def': 'SCADef'}))
df = df.join(df_gsca.iloc[:, 16:24].rename(columns={'GCA': 'GCA', 'GCA90': 'GCA90', 'PassLive': 'GCAPassLive', 'PassDead': 'GCAPassDead', 'TO': 'GCADrib', 'Sh': 'GCASh', 'Fld': 'GCAFld', 'Def': 'GCADef'}))

df = df.join(df_defense.iloc[:,8:13].rename(columns={'Tkl': 'Tkl', 'TklW': 'TklWinPoss', 'Def 3rd': 'Def3rdTkl', 'Mid 3rd': 'Mid3rdTkl', 'Att 3rd': 'Att3rdTkl'}))
df = df.join(df_defense.iloc[:,13:24].rename(columns={'Tkl': 'DrbTkl', 'Att': 'DrbPastAtt', 'Tkl%': 'DrbTkl%', 'Lost': 'DrbPast', 'Blocks': 'Blocks', 'Sh': 'ShBlocks', 'Pass': 'PassBlocks', 'Int': 'Int', 'Tkl+Int': 'Tkl+Int', 'Clr': 'Clr', 'Err': 'Err'}))

df = df.join(df_poss.iloc[:,8:30])
df = df.rename(columns={'Touches': 'Touches', 'Def Pen': 'DefPenTouch', 'Def 3rd': 'Def3rdTouch', 'Mid 3rd': 'Mid3rdTouch', 'Att 3rd': 'Att3rdTouch', 'Att Pen': 'AttPenTouch', 'Live': 'LiveTouch', 'Succ': 'SuccDrb', 'Att': 'AttDrb', 'Succ%': 'DrbSucc%', 'Tkld':'TimesTackled', 'Tkld%':'TimesTackled%', 'Carries':'Carries', 'TotDist':'TotalCarryDistance', 'PrgDist':'ProgCarryDistance', 'PrgC':'ProgCarries', '1/3':'CarriesToFinalThird', 'CPA':'CarriesToPenArea', 'Mis': 'CarryMistakes', 'Dis': 'Disposesed', 'Rec': 'ReceivedPass', 'PrgR':'ProgPassesRec'})

df = df.join(df_misc.iloc[:, 8:14])
df = df.rename(columns={'CrdY': 'Yellows', 'CrdR': 'Reds', '2CrdY': 'Yellow2', 'Fls': 'Fls', 'Fld': 'Fld', 'Off': 'Off', })
df = df.join(df_misc.iloc[:,17:24])
df = df.rename(columns={'PKwon': 'PKwon', 'PKcon': 'PKcon', 'OG': 'OG', 'Recov': 'Recov', 'Won': 'AerialWins', 'Lost': 'AerialLoss', 'Won%': 'AerialWin%', })

# Make sure to drop all blank rows (FBRef's tables have several)
df.dropna(subset = ["Player"], inplace=True)

# Turn the minutes columns to integers. So from '1,500' to '1500'. Otherwise it can't do calculations with minutes
for i in range(0,len(df)):
    df.iloc[i][9] = df.iloc[i][9].replace(',','')
df.iloc[:,9:] = df.iloc[:,9:].apply(pd.to_numeric)

# Save the file to the root location
df.to_csv("%s%s.csv" %(root, raw_nongk), index=False)


##################################################################################
############################## GK SECTION ########################################
##################################################################################

gk = "https://fbref.com/en/comps/Big5/keepers/players/Big-5-European-Leagues-Stats"
advgk = "https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats"

df_gk = get_df(gk)
df_advgk = get_df(advgk)

df_gk.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)
df_advgk.sort_values(['Player', 'Squad'], ascending=[True, True], inplace=True)

df_gk = df_gk.reset_index(drop=True)
df_advgk = df_advgk.reset_index(drop=True)

###############################################################################

df = pd.read_csv("%s%s.csv" %(root, raw_nongk))
df = df[df['Pos'].str.contains("GK")].reset_index().iloc[:,1:]
df_gk['Pos'] = df_gk['Pos'].astype(str)
df_gk = df_gk[df_gk['Pos'].str.contains('GK')]
df_gk = df_gk.reset_index().iloc[:,1:]
df_gk = df_gk.rename(columns={'PKatt':'PKsFaced'})

df = df.join(df_gk.iloc[:, 11:26].astype(float), lsuffix='.1', rsuffix='.2')
df = df.rename(columns={'GA': 'GA', 'GA90': 'GA90', 'SoTA': 'SoTA', 'Saves': 'Saves', 'Save%.1': 'Save%', 'W': 'W', 'D': 'D', 'L': 'L', 'CS': 'CS', 'CS%': 'CS%', 'PKsFaced': 'PKsFaced', 'PKA': 'PKA', 'PKsv': 'PKsv', 'PKm': 'PKm', 'Save%.2': 'PKSave%', })

df_advgk['Pos'] = df_advgk['Pos'].astype(str)
df_advgk = df_advgk[df_advgk['Pos'].str.contains('GK')]
df_advgk = df_advgk.reset_index().iloc[:,1:]
df = df.join(df_advgk.iloc[:,9:20].astype(float).rename(columns={'PKA': 'PKGA', 'FK': 'FKGA', 'CK': 'CKGA', 'OG': 'OGA', 'PSxG': 'PSxG', 'PSxG/SoT': 'PSxG/SoT', 'PSxG+/-': 'PSxG+/-', '/90': 'PSxG+/- /90', 'Cmp': 'LaunchCmp', 'Att': 'LaunchAtt', 'Cmp%': 'LaunchPassCmp%'}))
df = df.join(df_advgk.iloc[:,20:24].astype(float).rename(columns={'Att': 'PassAtt', 'Thr': 'PassThr', 'Launch%': 'PassesLaunch%', 'AvgLen': 'AvgLenLaunch'}))
df = df.join(df_advgk.iloc[:,24:33].astype(float).rename(columns={'Att': 'GoalKicksAtt', 'Launch%': 'GoalKicksLaunch%', 'AvgLen': 'AvgLen', 'Opp': 'OppCrs', 'Stp': 'StpCrs', 'Stp%': 'CrsStp%', '#OPA': '#OPA', '#OPA/90': '#OPA/90', 'AvgDist': 'AvgDistOPA'}))

df.to_csv("%s%s.csv" %(root,raw_gk), index=False)

##################################################################################
##################### Final file for outfield data ###############################
##################################################################################

df = pd.read_csv("%s%s.csv" %(root, raw_nongk))
df_90s = pd.read_csv("%s%s.csv" %(root, raw_nongk))
df_90s['90s'] = df_90s['Min']/90
for i in range(10,125):
    df_90s.iloc[:,i] = df_90s.iloc[:,i]/df_90s['90s']
df_90s = df_90s.iloc[:,10:].add_suffix('Per90')
df_new = df.join(df_90s)

for i in range(len(df_new)):
    df_new['Age'][i] = int(df_new['Age'][i][:2])

df_new.to_csv("%s%s.csv" %(root, final_nongk), index=False)


##################################################################################
##################### Final file for keeper data #################################
##################################################################################

df = pd.read_csv("%s%s.csv" %(root, raw_gk))
df_90s = pd.read_csv("%s%s.csv" %(root, raw_gk))
df_90s['90s'] = df_90s['Min']/90
for i in range(10,164):
    df_90s.iloc[:,i] = df_90s.iloc[:,i]/df_90s['90s']
df_90s = df_90s.iloc[:,10:].add_suffix('Per90')
df_new = df.join(df_90s)

for i in range(len(df_new)):
    df_new['Age'][i] = int(df_new['Age'][i][:2])

df_new.to_csv("%s%s.csv" %(root, final_gk), index=False)


##################################################################################
################ Download team data, for possession-adjusting ####################
##################################################################################

standard = "https://fbref.com/en/comps/Big5/stats/squads/Big-5-European-Leagues-Stats"
poss = "https://fbref.com/en/comps/Big5/possession/squads/Big-5-European-Leagues-Stats"

df_standard = get_df(standard)
df_poss = get_df(poss)

df_standard = df_standard.reset_index(drop=True)
df_poss = df_poss.reset_index(drop=True)

############################################

df = df_standard.iloc[:, 0:30]

# Gets the number of touches a team has per 90
df['TeamTouches90'] = float(0.0)
for i in range(len(df)):
    df.iloc[i,30] = float(df_poss.iloc[i,5]) / float(df_poss.iloc[i,4])

# Take out the comma in minutes like above
for j in range(0,len(df)):
    df.at[j,'Min'] = df.at[j,'Min'].replace(',','')
df.iloc[:,7:] = df.iloc[:,7:].apply(pd.to_numeric)
df.to_csv("%s%s TEAMS.csv" %(root, final_nongk), index=False)


##################################################################################
################ Download opposition data, for possession-adjusting ##############
##################################################################################

opp_poss = "https://fbref.com/en/comps/Big5/possession/squads/Big-5-European-Leagues-Stats"

df_opp_poss = get_opp_df(opp_poss)
df_opp_poss = df_opp_poss.reset_index(drop=True)

############################################

df = df_opp_poss.iloc[:, 0:15]
df = df.rename(columns={'Touches':'Opp Touches'})
df = df.reset_index()

#############################################

df1 = pd.read_csv("%s%s TEAMS.csv"%(root, final_nongk))

df1['Opp Touches'] = 1
for i in range(len(df1)):
    df1['Opp Touches'][i] = df['Opp Touches'][i]
df1 = df1.rename(columns={'Min':'Team Min'})
df1.to_csv("%s%s TEAMS.csv" %(root, final_nongk), index=False)


##################################################################################
################ Make the final, complete, outfield data file ####################
##################################################################################

df = pd.read_csv("%s%s.csv" %(root, final_nongk))
teams = pd.read_csv("%s%s TEAMS.csv" %(root, final_nongk))

df['AvgTeamPoss'] = float(0.0)
df['OppTouches'] = int(1)
df['TeamMins'] = int(1)
df['TeamTouches90'] = float(0.0)

player_list = list(df['Player'])

for i in range(len(player_list)):
    team_name = df[df['Player']==player_list[i]]['Squad'].values[0]
    team_poss = teams[teams['Squad']==team_name]['Poss'].values[0]
    opp_touch = teams[teams['Squad']==team_name]['Opp Touches'].values[0]
    team_mins = teams[teams['Squad']==team_name]['Team Min'].values[0]
    team_touches = teams[teams['Squad']==team_name]['TeamTouches90'].values[0]
    df.at[i, 'AvgTeamPoss'] = team_poss
    df.at[i, 'OppTouches'] = opp_touch
    df.at[i, 'TeamMins'] = team_mins
    df.at[i, 'TeamTouches90'] = team_touches

# All of these are the possession-adjusted columns. A couple touch-adjusted ones at the bottom
df['pAdjTkl+IntPer90'] = (df['Tkl+IntPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjClrPer90'] = (df['ClrPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjShBlocksPer90'] = (df['ShBlocksPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjPassBlocksPer90'] = (df['PassBlocksPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjIntPer90'] = (df['IntPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjDrbTklPer90'] = (df['DrbTklPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjTklWinPossPer90'] = (df['DrbTklPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjDrbPastPer90'] = (df['DrbPastPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjAerialWinsPer90'] = (df['AerialWinsPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjAerialLossPer90'] = (df['AerialLossPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjDrbPastAttPer90'] = (df['DrbPastAttPer90']/(100-df['AvgTeamPoss']))*50
df['TouchCentrality'] = (df['TouchesPer90']/df['TeamTouches90'])*100
# df['pAdj#OPAPer90'] =(df['#OPAPer90']/(100-df['AvgTeamPoss']))*50
df['Tkl+IntPer600OppTouch'] = df['Tkl+Int'] /(df['OppTouches']*(df['Min']/df['TeamMins']))*600
df['pAdjTouchesPer90'] = (df['TouchesPer90']/(df['AvgTeamPoss']))*50
df['CarriesPer50Touches'] = df['Carries'] / df['Touches'] * 50
df['ProgCarriesPer50Touches'] = df['ProgCarries'] / df['Touches'] * 50
df['ProgPassesPer50CmpPasses'] = df['ProgPasses'] / df['PassesCompleted'] * 50


# Now we'll add the players' actual positions, from @jaseziv, into the file
tm_pos = pd.read_csv('https://github.com/griffisben/Soccer-Analyses/blob/main/TransfermarktPositions-Jase_Ziv83.csv?raw=true')
df = pd.merge(df, tm_pos, on ='Player', how ='left')

for i in range(len(df)):
    if df.Pos[i] == 'GK':
        df['Main Position'][i] = 'Goalkeeper'
df.to_csv("%s%s.csv" %(root, final_nongk), index=False, encoding='utf-8-sig')


##################################################################################
################ Make the final, complete, keepers data file #####################
##################################################################################

df = pd.read_csv("%s%s.csv" %(root, final_gk))
teams = pd.read_csv("%s%s TEAMS.csv" %(root, final_nongk))

df['AvgTeamPoss'] = float(0.0)
df['OppTouches'] = int(1)
df['TeamMins'] = int(1)
df['TeamTouches90'] = float(0.0)

player_list = list(df['Player'])

for i in range(len(player_list)):
    team_name = df[df['Player']==player_list[i]]['Squad'].values[0]
    team_poss = teams[teams['Squad']==team_name]['Poss'].values[0]
    opp_touch = teams[teams['Squad']==team_name]['Opp Touches'].values[0]
    team_mins = teams[teams['Squad']==team_name]['Team Min'].values[0]
    team_touches = teams[teams['Squad']==team_name]['TeamTouches90'].values[0]
    df.at[i, 'AvgTeamPoss'] = team_poss
    df.at[i, 'OppTouches'] = opp_touch
    df.at[i, 'TeamMins'] = team_mins
    df.at[i, 'TeamTouches90'] = team_touches

# Same thing, makes pAdj stats for the GK file
df['pAdjTkl+IntPer90'] = (df['Tkl+IntPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjClrPer90'] = (df['ClrPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjShBlocksPer90'] = (df['ShBlocksPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjPassBlocksPer90'] = (df['PassBlocksPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjIntPer90'] = (df['IntPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjDrbTklPer90'] = (df['DrbTklPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjTklWinPossPer90'] = (df['DrbTklPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjDrbPastPer90'] = (df['DrbPastPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjAerialWinsPer90'] = (df['AerialWinsPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjAerialLossPer90'] = (df['AerialLossPer90']/(100-df['AvgTeamPoss']))*50
df['pAdjDrbPastAttPer90'] = (df['DrbPastAttPer90']/(100-df['AvgTeamPoss']))*50
df['TouchCentrality'] = (df['TouchesPer90']/df['TeamTouches90'])*100
df['pAdj#OPAPer90'] =(df['#OPAPer90']/(100-df['AvgTeamPoss']))*50
df['Tkl+IntPer600OppTouch'] = df['Tkl+Int'] /(df['OppTouches']*(df['Min']/df['TeamMins']))*600
df['pAdjTouchesPer90'] = (df['TouchesPer90']/(df['AvgTeamPoss']))*50
df['CarriesPer50Touches'] = df['Carries'] / df['Touches'] * 50
df['ProgCarriesPer50Touches'] = df['ProgCarries'] / df['Touches'] * 50
df['ProgPassesPer50CmpPasses'] = df['ProgPasses'] / df['PassesCompleted'] * 50


# Just adding the main positions to the GK too, but of course, they will all be GK lol. Keeps other program variables clean
tm_pos = pd.read_csv('https://github.com/griffisben/Soccer-Analyses/blob/main/TransfermarktPositions-Jase_Ziv83.csv?raw=true')
df = pd.merge(df, tm_pos, on ='Player', how ='left')

for i in range(len(df)):
    if df.Pos[i] == 'GK':
        df['Main Position'][i] = 'Goalkeeper'
df.to_csv("%s%s.csv" %(root, final_gk), index=False, encoding='utf-8-sig')
print('Done :) Files are located at  %s' %root)



# %%
"""
## Run this code below to see where to place the 2 files if necessary
"""

# %%
root