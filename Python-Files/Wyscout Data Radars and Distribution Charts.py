# %%
"""
# This program will create a radar and distribution chart for Wyscout datasets

### This is structured to work on CSVs exported from Wyscout's 'Advanced Search' feature, with every single metric included.
### If you haven't already, I recommend making a custom DISPLAY that has all variables. You can make (and save) this display by clicking the 'choose columns to display' button on the top right of the advanced search view.
### Before making your first radar, please read the commented notes next to each variable in this first block.

## TO RUN THE PROGRAM:
#### To run the radar program, first run the second block of code. There are two total blocks: the first one is where you enter the info, the second is the program itself. You must run the second block (the program code) one time when you first boot this notebook up before running the first block (with the variables) or else it won't work. If you forget to run the second one first, no worries. Just run it and then run the first block again and you're set!
#### The first block of code is the only place you really need to change anything unless you modify the progam's code itself. Enter all the required info (i.e. all but the savepath & imgpath variables) and then, after you've run the second block, you can run the first block. The radars & distribution chart will generate.
##### (note that to save the distribution chart, you will need to right-click and save it. To get the text all correctly placed, I had to go "outside" the borders of the image that auto-saves. So, sorry but there's one manual step to saving that ;)

### Feel free to DM me (@BeGriffis) if you've got any issues, questions, comments, etc
"""

# %%
scout_report(ws_datapath = 'FULL path/to your wyscout/data/filename.csv',  # Make sure your csv is UTF-8 Encoded
             savepath = 'path/to where you want/your radar image to save to',  # OPTIONAL: This will be the location the radar saves to (if you have the save_img variable as y below)
             imgpath = 'FULL path/to your image of the club/logo.png',  # OPTIONAL: if you don't add an image, comment this line out
             league = 'J3',  # name of your league (make sure your dataset league name and image folder league name match)
             season = '2022',  # for example: 2022 for summer leagues' seasons, 21-22 for winter leagues
             xtra = ' current',  # this is for the ws_datapath. I have '' for finished seasons, and ' current' for in-progress ones.
             template = 'defensive',  #  OPTIONS: attacking, defensive, gk   # This determines which radar template you want. I only have 3 right now, am looking into making more position-specific ones
             pos_buckets = 'single',   # OPTIONS: single, mult (if you want a sinlg wyscout position like CF/LCB/LAMF or if the position contains something like CB/AMF/etc, then choose single)
             pos = 'CB',  # See the 'mult position options' description below for the options (after the ###)
             player_pos = 'RCB',  # this will be included in the title, showing the player's name, age, and position you put here
             compares = 'Center Backs',   # this adds the comparison group in the notes at the bottom. essentially, "compared to League [compares]..."
             mins = 900,  # minimum minutes played filter
             name = 'Rei Ieizumi',  # Actual player name (because Wyscout doesn't use full names, but we should)
             ws_name = 'R. Ieizumi',  # Wyscout's name they use for the player
             team = 'Iwaki',  # The player's club. Variable in Wyscout I use is 'Club within selected timeframe'
             age = 22,  # Player age
             sig = 'Twitter: @BeGriffis',  # Signature you want to add to the notes at the bottom
             club_image = 'y',  # if you want a club & league logo on the radar, make sure you have the imgpath variable filled out
             save_img = 'y',  # this will save the radar automatically, not the distribution chart. That will need to be saved by right-clicking it
             extra_text = ' | Data as of 9/5/22',  # Any extra text you want to add to the notes at the bottom. I usually put ' | Data final for 21-22' or ' | Data as of 9/2/22' for example. Make sure people finding this chart in the future know if it's got an expiration date, essentially.
            )

##### mult position inculsions:

#(Since Wyscout codes very secific positions, like LWF or RWF instead of just WF, the code searches for positions that *contain* these positions below)
#(of course you can go into the code (starting line 45) and modify/add/delete any of these you want to)


### Forward
# CF, RW, LW, AMF

### CF and W
# CF, RW, LW

### Forward no ST
# AMF, LW, RW

### Winger
# WF, LAMF, RAMF, LW, RW, (excludes WBs)

### Midfielder
# CMF, DMF, AMF

### Midfielder no CAM
# CMF, DMF

### Fullback
# LB, RB, WB

### Defenders
#LB, RB, WB, CB, DMF



# %%
# import pkg_resources
# pkg_resources.require("seaborn==0.11.1")
%matplotlib inline
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean
from math import pi
sns.set_style("white")
import warnings
warnings.filterwarnings('ignore')
import matplotlib
matplotlib.rcParams.update(matplotlib.rcParamsDefault)



def scout_report(ws_datapath, league, season, xtra, template, pos_buckets, pos, player_pos, mins, compares, name, ws_name, team, age, sig, club_image, save_img, extra_text, savepath=None, imgpath=None):
    import matplotlib
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    df = pd.read_csv(ws_datapath)
    
    df['pAdj Tkl+Int per 90'] = df['PAdj Sliding tackles'] + df['PAdj Interceptions']
    df['1st, 2nd, 3rd assists'] = df['Assists per 90'] + df['Second assists per 90'] + df['Third assists per 90']
    df['xA per Shot Assist'] = df['xA per 90'] / df['Shot assists per 90']
    df['Aerial duels won per 90'] = df['Aerial duels per 90'] * (df['Aerial duels won, %']/100)
    df['Cards per 90'] = df['Yellow cards per 90'] + df['Red cards per 90']
    df['Clean sheets, %'] = df['Clean sheets'] / df['Matches played']
    df['npxG'] = df['xG'] - (.76 * df['Penalties taken'])
    df['npxG per 90'] = df['npxG'] / (df['Minutes played'] / 90)
    df['npxG per shot'] = df['npxG'] / (df['Shots'] - df['Penalties taken'])

    df['Main Position'] = ''
    for i in range(len(df)):
        df['Main Position'][i] = df['Position'][i].split()[0]
    
    #####################################################################################
    # Filter data
    dfProspect = df[df['Minutes played']>=mins]

    if pos_buckets == 'single':
        dfProspect = dfProspect[dfProspect['Main Position'].str.contains(pos)]

    if pos_buckets == 'mult':
        if pos == 'Forward':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('CF')) |
                                   (dfProspect['Main Position'].str.contains('RW')) |
                                   (dfProspect['Main Position'].str.contains('LW')) |
                                   (dfProspect['Main Position'].str.contains('AMF'))]
        if pos == 'CF and W':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('CF')) |
                                   (dfProspect['Main Position'].str.contains('RW')) |
                                   (dfProspect['Main Position'].str.contains('LW'))]
        if pos == 'Forward no ST':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('AMF')) |
                                   (dfProspect['Main Position'].str.contains('RW')) |
                                   (dfProspect['Main Position'].str.contains('LW'))]
        if pos == 'Winger':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('WF')) |
                                   (dfProspect['Main Position'].str.contains('LAMF')) |
                                   (dfProspect['Main Position'].str.contains('RAMF')) |
                                   (dfProspect['Main Position'].str.contains('LW')) |
                                   (dfProspect['Main Position'].str.contains('RW'))]
            dfProspect = dfProspect[~dfProspect['Main Position'].str.contains('WB')]
        if pos == 'Midfielder':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('CMF')) |
                                   (dfProspect['Main Position'].str.contains('DMF')) |
                                   (dfProspect['Main Position'].str.contains('AMF'))]
        if pos == 'Midfielder no CAM':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('CMF')) |
                                   (dfProspect['Main Position'].str.contains('DMF'))]
        if pos == 'Fullback':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('LB')) |
                                   (dfProspect['Main Position'].str.contains('RB')) |
                                   (dfProspect['Main Position'].str.contains('WB'))]
        if pos == 'Defenders':
            dfProspect = dfProspect[(dfProspect['Main Position'].str.contains('LB')) |
                                   (dfProspect['Main Position'].str.contains('RB')) |
                                   (dfProspect['Main Position'].str.contains('WB')) |
                                   (dfProspect['Main Position'].str.contains('CB')) |
                                   (dfProspect['Main Position'].str.contains('DMF'))]

    # FORWARD
    fwd1 = "Non-penalty goals per 90"
    fwd2 = "npxG per 90"
    fwd3 = "Assists per 90"
    fwd4 = "xA per 90"
    fwd5 = "Successful dribbles, %"
    fwd6 = "Goal conversion, %"
    fwd7 = "Shot assists per 90"
    fwd8 = "Second assists per 90"
    fwd9 = "Progressive runs per 90"
    fwd10 = "Progressive passes per 90"
    fwd11 = "Touches in box per 90"
    fwd12 = "Aerial duels won, %"
    # MIDFIELD
    mid1 = "Accurate short / medium passes, %"
    mid2 = "Accurate long passes, %"
    mid3 = "Accurate smart passes, %"
    mid4 = "Shot assists per 90"
    mid5 = "xA per 90"
    mid6 = "Assists per 90"
    mid7 = "Second assists per 90"
    mid8 = "Third assists per 90"
    mid9 = "Progressive passes per 90"
    mid10 = "Progressive runs per 90"
    mid11 = "Duels won, %"
    mid12 = "pAdj Tkl+Int per 90"
    # DEFENDER
    def1 = "Successful defensive actions per 90"
    def2 = "PAdj Sliding tackles"
    def3 = "Defensive duels won, %"
    def4 = "Fouls per 90" 
    def5 = "Cards per 90"
    def6 = "Shots blocked per 90"
    def7 = "PAdj Interceptions"
    def8 = "Aerial duels won, %"
    def9 = "Accurate long passes, %"
    def10 = "1st, 2nd, 3rd assists"
    def11 = "Progressive passes per 90"
    def12 = "Progressive runs per 90"
    # GOALKEEPER
    gk1 = "Conceded goals per 90"
    gk2 = "Prevented goals per 90"
    gk3 = "Shots against per 90"
    gk4 = "Save rate, %"
    gk5 = "Clean sheets, %"
    gk6 = "Exits per 90"
    gk7 = "Aerial duels per 90"
    gk8 = "Passes per 90"
    gk9 = "Accurate long passes, %"
    gk10 = "Average long pass length, m"
    # OTHERS
    extra = "Accurate passes, %"
    extra2 = 'Shots per 90'
    extra3 = 'Accurate crosses, %'
    extra4 = 'Smart passes per 90'
    extra5 = 'xA per Shot Assist'
    extra6 = 'Accelerations per 90'
    extra7 = 'Aerial duels won per 90'
    extra8 = 'Fouls suffered per 90'
    extra9 = 'npxG per shot'
    extra10 = 'Crosses per 90'

    df_pros = dfProspect

    dfProspect["midpct1"] = stats.rankdata(dfProspect[mid1], "average")/len(dfProspect[mid1])
    dfProspect["midpct2"] = stats.rankdata(dfProspect[mid2], "average")/len(dfProspect[mid2])
    dfProspect["midpct3"] = stats.rankdata(dfProspect[mid3], "average")/len(dfProspect[mid3])
    dfProspect["midpct4"] = stats.rankdata(dfProspect[mid4], "average")/len(dfProspect[mid4])
    dfProspect["midpct5"] = stats.rankdata(dfProspect[mid5], "average")/len(dfProspect[mid5])
    dfProspect["midpct6"] = stats.rankdata(dfProspect[mid6], "average")/len(dfProspect[mid6])
    dfProspect["midpct7"] = stats.rankdata(dfProspect[mid7], "average")/len(dfProspect[mid7])
    dfProspect["midpct8"] = stats.rankdata(dfProspect[mid8], "average")/len(dfProspect[mid8])
    dfProspect["midpct9"] = stats.rankdata(dfProspect[mid9], "average")/len(dfProspect[mid9])
    dfProspect["midpct10"] = stats.rankdata(dfProspect[mid10], "average")/len(dfProspect[mid10])
    dfProspect["midpct11"] = stats.rankdata(dfProspect[mid11], "average")/len(dfProspect[mid11])
    dfProspect["midpct12"] = stats.rankdata(dfProspect[mid12], "average")/len(dfProspect[mid12])
    dfProspect["fwdpct1"] = stats.rankdata(dfProspect[fwd1], "average")/len(dfProspect[fwd1])
    dfProspect["fwdpct2"] = stats.rankdata(dfProspect[fwd2], "average")/len(dfProspect[fwd2])
    dfProspect["fwdpct3"] = stats.rankdata(dfProspect[fwd3], "average")/len(dfProspect[fwd3])
    dfProspect["fwdpct4"] = stats.rankdata(dfProspect[fwd4], "average")/len(dfProspect[fwd4])
    dfProspect["fwdpct5"] = stats.rankdata(dfProspect[fwd5], "average")/len(dfProspect[fwd5])
    dfProspect["fwdpct6"] = stats.rankdata(dfProspect[fwd6], "average")/len(dfProspect[fwd6])
    dfProspect["fwdpct7"] = stats.rankdata(dfProspect[fwd7], "average")/len(dfProspect[fwd7])
    dfProspect["fwdpct8"] = stats.rankdata(dfProspect[fwd8], "average")/len(dfProspect[fwd8])
    dfProspect["fwdpct9"] = stats.rankdata(dfProspect[fwd9], "average")/len(dfProspect[fwd9])
    dfProspect["fwdpct10"] = stats.rankdata(dfProspect[fwd10], "average")/len(dfProspect[fwd10])
    dfProspect["fwdpct11"] = stats.rankdata(dfProspect[fwd11], "average")/len(dfProspect[fwd11])
    dfProspect["fwdpct12"] = stats.rankdata(dfProspect[fwd12], "average")/len(dfProspect[fwd12])
    dfProspect["defpct1"] = stats.rankdata(dfProspect[def1], "average")/len(dfProspect[def1])
    dfProspect["defpct2"] = stats.rankdata(dfProspect[def2], "average")/len(dfProspect[def2])
    dfProspect["defpct3"] = stats.rankdata(dfProspect[def3], "average")/len(dfProspect[def3])
    dfProspect["defpct4"] = 1-stats.rankdata(dfProspect[def4], "average")/len(dfProspect[def4])
    dfProspect["defpct5"] = 1-stats.rankdata(dfProspect[def5], "average")/len(dfProspect[def5])
    dfProspect["defpct6"] = stats.rankdata(dfProspect[def6], "average")/len(dfProspect[def6])
    dfProspect["defpct7"] = stats.rankdata(dfProspect[def7], "average")/len(dfProspect[def7])
    dfProspect["defpct8"] = stats.rankdata(dfProspect[def8], "average")/len(dfProspect[def8])
    dfProspect["defpct9"] = stats.rankdata(dfProspect[def9], "average")/len(dfProspect[def9])
    dfProspect["defpct10"] = stats.rankdata(dfProspect[def10], "average")/len(dfProspect[def10])
    dfProspect["defpct11"] = stats.rankdata(dfProspect[def11], "average")/len(dfProspect[def11])
    dfProspect["defpct12"] = stats.rankdata(dfProspect[def12], "average")/len(dfProspect[def12])
    dfProspect["gkpct1"] = 1-stats.rankdata(dfProspect[gk1], "average")/len(dfProspect[gk1])
    dfProspect["gkpct2"] = stats.rankdata(dfProspect[gk2], "average")/len(dfProspect[gk2])
    dfProspect["gkpct3"] = stats.rankdata(dfProspect[gk3], "average")/len(dfProspect[gk3])
    dfProspect["gkpct4"] = stats.rankdata(dfProspect[gk4], "average")/len(dfProspect[gk4])
    dfProspect["gkpct5"] = stats.rankdata(dfProspect[gk5], "average")/len(dfProspect[gk5])
    dfProspect["gkpct6"] = stats.rankdata(dfProspect[gk6], "average")/len(dfProspect[gk6])
    dfProspect["gkpct7"] = stats.rankdata(dfProspect[gk7], "average")/len(dfProspect[gk7])
    dfProspect["gkpct8"] = stats.rankdata(dfProspect[gk8], "average")/len(dfProspect[gk8])
    dfProspect["gkpct9"] = stats.rankdata(dfProspect[gk9], "average")/len(dfProspect[gk9])
    dfProspect["gkpct10"] = stats.rankdata(dfProspect[gk10], "average")/len(dfProspect[gk10])
    dfProspect["extrapct"] = stats.rankdata(dfProspect[extra], "average")/len(dfProspect[extra])
    dfProspect["extrapct2"] = stats.rankdata(dfProspect[extra2], "average")/len(dfProspect[extra2])
    dfProspect["extrapct3"] = stats.rankdata(dfProspect[extra3], "average")/len(dfProspect[extra3])
    dfProspect["extrapct4"] = stats.rankdata(dfProspect[extra4], "average")/len(dfProspect[extra4])
    dfProspect["extrapct5"] = stats.rankdata(dfProspect[extra5], "average")/len(dfProspect[extra5])
    dfProspect["extrapct6"] = stats.rankdata(dfProspect[extra6], "average")/len(dfProspect[extra6])
    dfProspect["extrapct7"] = stats.rankdata(dfProspect[extra7], "average")/len(dfProspect[extra7])
    dfProspect["extrapct8"] = stats.rankdata(dfProspect[extra8], "average")/len(dfProspect[extra8])
    dfProspect["extrapct9"] = stats.rankdata(dfProspect[extra9], "average")/len(dfProspect[extra9])
    dfProspect["extrapct10"] = stats.rankdata(dfProspect[extra10], "average")/len(dfProspect[extra10])
    
    ######################################################################
    
    dfRadarMF = dfProspect[(dfProspect['Player']==ws_name)].reset_index(drop=True)

    if template == 'attacking':
        dfRadarMF = dfRadarMF[["Player",
                               "midpct1","midpct2","midpct3",'extrapct3',
                               "midpct4","midpct5", 'extrapct5', "midpct6","midpct7",'extrapct4',
                               "fwdpct2","fwdpct1","fwdpct6", "extrapct9", "extrapct2", 'fwdpct11',
                               "fwdpct5", 'extrapct6', "midpct10", "midpct9",
                               "defpct1", "midpct12",'defpct8',]]
        dfRadarMF.rename(columns={'midpct1': "Short & Med\nPass %",
                                'midpct2': "Long\nPass %",
                                'midpct3': "Smart\nPass %",
                                'extrapct3': 'Cross\nCompletion %',
                                'midpct4': "Shot Assists",
                                'midpct5': "Expected\nAssists (xA)",
                                'extrapct5': 'xA per\nShot Assist',
                                'midpct6': "Assists",
                                'midpct7': "Second\nAssists",
                                'extrapct4': 'Smart Passes',
                              "fwdpct2": "npxG",
                               "fwdpct1": "Non-Pen\nGoals",
                                "fwdpct6": "Goals/Shot\non Target %",
                                  "extrapct9": 'npxG\nper shot',
                                'extrapct2': "Shots",
                                  'fwdpct11': 'Touches in\nPen Box',
                                 "fwdpct5": "Dribble\nSuccess %",
                                  'extrapct6': 'Acceleration\nwith Ball',
                                'midpct10': "Prog.\nCarries",
                                'midpct9': "Prog.\nPasses",
                                'defpct1': "Defensive\nActions",
                                'midpct12': "Tackles & Int\n(pAdj)",
                                  'defpct8': 'Aerial\nWin %'
                                 }, inplace=True)
        print('Number of players comparing to:',len(dfProspect))

    if template == 'defensive':
        dfRadarMF = dfRadarMF[["Player",
                               'defpct1', "defpct2","defpct3","defpct6", "defpct7", 'extrapct7',"defpct8",
                               "defpct9", "extrapct10", 'extrapct3',"defpct10", "defpct11", "defpct12","fwdpct5",'extrapct6',"midpct5",
                               "defpct4","defpct5",'extrapct8'
                              ]]
        dfRadarMF.rename(columns={'defpct1': 'Defensive\nActions',
                                  'defpct2': "Tackles\n(pAdj)",
                                  'defpct3': "Defensive\nDuels Won %",
                                  'defpct6': "Shot Blocks",
                                  'defpct7': "Interceptions\n(pAdj)",
                                  'extrapct7': 'Aerial Duels\nWon',
                                  'defpct8': "Aerial\nWin %",
                                  'defpct9': "Long\nPass %",
                                  'extrapct10': 'Crosses',
                                  'extrapct3': 'Cross\nCompletion %',
                                  'defpct10': "Assists &\n2nd/3rd Assists",
                                  'defpct11': "Prog.\nPasses",
                                  'defpct12': "Prog.\nCarries",
                                  "fwdpct5": "Dribble\nSucces %",
                                  'extrapct6': 'Acceleration\nwith Ball',
                                  'midpct5': "Expected\nAssists",
                                  'defpct4': "Fouls",
                                  'defpct5': "Cards",
                                  'extrapct8': 'Fouls Drawn'
                                 }, inplace=True)
        print('Number of players comparing to:',len(dfProspect))

    if template == 'gk':
        dfRadarMF = dfRadarMF[["Player",
                               'gkpct1','gkpct2','gkpct3','gkpct4','gkpct5',
                               'gkpct6','gkpct7','gkpct8','gkpct9','gkpct10'
                              ]]
        dfRadarMF.rename(columns={'gkpct1': 'Goals\nConceded',
                                  'gkpct2': "Goals Prevented\nvs Expected",
                                  'gkpct3': "Shots Against",
                                  'gkpct4': "Save %",
                                  'gkpct5': "Clean Sheet %",
                                  'gkpct6': 'Att. Cross Claims\nor Punches',
                                  'gkpct7': "Aerial Wins",
                                  'gkpct8': "Passes",
                                  'gkpct9': 'Long Passes',
                                  'gkpct10': "Long\nPass %",
                                 }, inplace=True)
        print('Number of players comparing to:',len(dfProspect))

    ###########################################################################
    
    df1 = dfRadarMF.T.reset_index()

    df1.columns = df1.iloc[0] 

    df1 = df1[1:]
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'Player': 'Metric',
                        ws_name: 'Value',
                             'index': 'Group'})
    if template == 'attacking':
        for i in range(len(df1)):
            if df1['Group'][i] <= 4:
                df1['Group'][i] = 'Passing'
            elif df1['Group'][i] <= 10:
                df1['Group'][i] = 'Creativity'
            elif df1['Group'][i] <= 16:
                df1['Group'][i] = 'Shooting'
            elif df1['Group'][i] <= 20:
                df1['Group'][i] = 'Ball Movement'
            elif df1['Group'][i] <= 23:
                df1['Group'][i] = 'Defense'

    if template == 'defensive':
        for i in range(len(df1)):
            if df1['Group'][i] <= 7:
                df1['Group'][i] = 'Defending'
            elif df1['Group'][i] <= 16:
                df1['Group'][i] = 'Attacking'
            elif df1['Group'][i] <= 19:
                df1['Group'][i] = 'Fouling'

    if template == 'gk':
        for i in range(len(df1)):
            if df1['Group'][i] <= 5:
                df1['Group'][i] = 'Traditional'
            elif df1['Group'][i] <= 10:
                df1['Group'][i] = 'Modern'

    #####################################################################
    
    ### This link below is where I base a lot of my radar code off of
    ### https://www.python-graph-gallery.com/circular-barplot-with-groups

    def get_label_rotation(angle, offset):
        # Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle + offset)+90
        if angle <= np.pi/2:
            alignment = "center"
            rotation = rotation + 180
        elif 4.3 < angle < np.pi*2:  # 4.71239 is 270 degrees
            alignment = "center"
            rotation = rotation - 180
        else: 
            alignment = "center"
        return rotation, alignment


    def add_labels(angles, values, labels, offset, ax):

        # This is the space between the end of the bar and the label
        padding = .05

        # Iterate over angles, values, and labels, to add all of them.
        for angle, value, label, in zip(angles, values, labels):
            angle = angle

            # Obtain text rotation and alignment
            rotation, alignment = get_label_rotation(angle, offset)

            # And finally add the text
            ax.text(
                x=angle, 
                y=1.05,
                s=label, 
                ha=alignment, 
                va="center", 
                rotation=rotation,
            )



    # Grab the group values
    GROUP = df1["Group"].values
    VALUES = df1["Value"].values
    LABELS = df1["Metric"].values
    OFFSET = np.pi / 2

    PAD = 2
    ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
    ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
    WIDTH = (2 * np.pi) / len(ANGLES)

    offset = 0
    IDXS = []

    if template == 'attacking':
        GROUPS_SIZE = [4,6,6,4,3]  # Attacker template
    if template == 'defensive':
        GROUPS_SIZE = [7,9,3]  # Defender template
    if template == 'gk':
        GROUPS_SIZE = [5,5]  # GK template



    for size in GROUPS_SIZE:
        IDXS += list(range(offset + PAD, offset + size + PAD))
        offset += size + PAD

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    ax.set_theta_offset(OFFSET)
    ax.set_ylim(-.5, 1)
    ax.set_frame_on(False)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])


    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

    ax.bar(
        ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS,
        edgecolor="#4A2E19", linewidth=1
    )

    add_labels(ANGLES[IDXS], VALUES, LABELS, OFFSET, ax)

    offset = 0 
    for group, size in zip(GROUPS_SIZE, GROUPS_SIZE): #replace first GROUPS SIZE with ['Passing', 'Creativity'] etc if needed
        # Add line below bars
        x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
        ax.plot(x1, [-.02] * 50, color="#4A2E19")


        # Add reference lines at 20, 40, 60, and 80
        x2 = np.linspace(ANGLES[offset], ANGLES[offset + PAD - 1], num=50)
        ax.plot(x2, [.2] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.4] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.60] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.80] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [1] * 50, color="#bebebe", lw=0.8)

        offset += size + PAD

    for bar in ax.patches:
        ax.annotate(format(bar.get_height()*100, '.0f'),
                       (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()-.1), ha='center', va='center',
                       size=12, xytext=(0, 8),
                       textcoords='offset points',
                   bbox=dict(boxstyle="round", fc='white', ec="black", lw=1))


    PAD = 0.02
    ax.text(0.15, 0 + PAD, "0", size=10, color='#4A2E19')
    ax.text(0.15, 0.2 + PAD, "20", size=10, color='#4A2E19')
    ax.text(0.15, 0.4 + PAD, "40", size=10, color='#4A2E19')
    ax.text(0.15, 0.6 + PAD, "60", size=10, color='#4A2E19')
    ax.text(0.15, 0.8 + PAD, "80", size=10, color='#4A2E19')
    ax.text(0.15, 1 + PAD, "100", size=10, color='#4A2E19')

    plt.suptitle('%s (%i, %s), %s, %s %s\nPercentile Rankings'
                 %(name, age, player_pos, team, season, league),
                 fontsize=17,
                 fontfamily="DejaVu Sans",
                color="#4A2E19", #4A2E19
                 fontweight="bold", fontname="DejaVu Sans",
                x=0.5,
                y=.97)

    plt.annotate('All values are per 90 minutes%s\nCompared to %s %s, %i+ mins\nData: Wyscout | %s\nCode by @BeGriffis' %(extra_text, league, compares, mins, sig),
                 xy = (0, -.05), xycoords='axes fraction',
                ha='left', va='center',
                fontsize=9, fontfamily="DejaVu Sans",
                color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                ) 

    if club_image == 'y':
        ######## Club Image ########
        from PIL import Image
        image = Image.open(imgpath)
        newax = fig.add_axes([.44,.43,0.15,0.15], anchor='C', zorder=1)
        newax.imshow(image)
        newax.axis('off')
        
#         ######## League Logo Image ########
#         l_image = Image.open('%s/%s/%s Logo.png' %(imgpath, league,league))
#         newax = fig.add_axes([.76,.845,0.1,0.1], anchor='C', zorder=1)
#         newax.imshow(l_image)
#         newax.axis('off')

    ax.set_facecolor('#fbf9f4')
    fig = plt.gcf()
    fig.patch.set_facecolor('#fbf9f4')
#     ax.set_facecolor('#fbf9f4')
    fig.set_size_inches(12, (12*.9)) #length, height

    if save_img == 'y':
        fig.savefig("%s/%s Radar %s %s.png" %(savepath,name,season,pos), dpi=250)
    fig.show()
    ####################################################################
    
#     if analysis == 'distribution':
    import matplotlib
    matplotlib.rcParams['figure.dpi'] = 250


    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    c = {'Metric': [], 'Value': [], 'Player': [], 'TrueVal': [], 'Group': []}
    distdf = pd.DataFrame(c)

    if template == 'attacking':
        var_list = [mid1,mid2,mid3,extra3,
                   mid4,mid5, extra5, mid6,mid7,extra4,
                   fwd2,fwd1,fwd6, extra9, extra2, fwd11,
                   fwd5, extra6, mid10, mid9,
                   def1, mid12,def8,]
    if template == 'defensive':
        var_list = [def1, def2,def3,def6, def7, extra7,def8,
                    def9, extra3,def10, def11, def12,fwd5,extra6,mid5,
                    def4,def5,extra8]
    if template == 'gk':
        var_list = [gk1, gk2,gk3,gk4, gk5, gk6,gk7,
                    gk8, gk9,gk10]


    for i in range(len(var_list)):
        n1 = var_list[i]
        n2 = df_pros[var_list[i]].values
        n2 = ((n2-min(n2))/(max(n2)-min(n2)))*len(n2)
        n3 = df_pros['Player'].values
        n4 = df_pros[var_list[i]].values
        n5 = GROUP[i]
        new = {'Metric': n1, 'Value': n2, 'Player': n3, 'TrueVal': n4, 'Group': n5}
        new_row = pd.DataFrame(new)
        distdf = distdf.append(new_row)

    distdf = distdf.reset_index(drop=True)

    if template == 'attacking':
        distdf['Metric'] = distdf['Metric'].replace({mid1: "Short & Med\nPass %",
                                    mid2: "Long\nPass %",
                                    mid3: "Smart\nPass %",
                                    extra3: 'Cross\nCompletion %',
                                    mid4: "Shot Assists",
                                    mid5: "Expected\nAssists (xA)",
                                    extra5: 'xA per\nShot Assist',
                                    mid6: "Assists",
                                    mid7: "Second\nAssists",
                                    extra4: 'Smart Passes',
                                  fwd2: "npxG",
                                   fwd1: "Non-Pen\nGoals",
                                    fwd6: "Goals/Shot\non Target %",
                                      extra9: 'npxG\nper shot',
                                    extra2: "Shots",
                                      fwd11: 'Touches in\nPen Box',
                                     fwd5: "Dribble\nSuccess %",
                                      extra6: 'Accelerations\nwith Ball',
                                    mid10: "Progressive\nCarries",
                                    mid9: "Progressive\nPasses",
                                    def1: "Defensive\nActions",
                                    mid12: "Tackles & Int\n(pAdj)",
                                      def8: 'Aerial\nWin %'
                                     })
    if template == 'defensive':
        distdf['Metric'] = distdf['Metric'].replace({def1: 'Defensive\nActions',
                                  def2: "Tackles\n(pAdj)",
                                  def3: "Defensive\nDuels Won %",
                                  def6: "Shot Blocks",
                                  def7: "Interceptions\n(pAdj)",
                                  extra7: 'Aerial Duels\nWon',
                                  def8: "Aerial\nWin %",
                                  def9: "Long\nPass %",
                                extra10: "Crosses",
                                  extra3: 'Cross\nCompletion %',
                                  def10: "Assists &\n2nd/3rd Assists",
                                  def11: "Progressive\nPasses",
                                  def12: "Progressive\nCarries",
                                  fwd5: "Dribble\nSucces %",
                                  extra6: 'Accelerations\nwith Ball',
                                  mid5: "Expected\nAssists",
                                  def4: "Fouls",
                                  def5: "Cards",
                                  extra8: 'Fouls Drawn'
                                 })
    if template == 'gk':
        distdf['Metric'] = distdf['Metric'].replace({gk1: "Goals\nConceded",
                                  gk2: "Goals Prevented\nvs Expected",
                                  gk3: "Shots Against",
                                  gk4: "Save %",
                                  gk5: "Clean Sheet %",
                                  gk6: "Att. Cross Claims\nor Punches",
                                  gk7: "Aerial Wins",
                                  gk8: "Passes",
                                  gk9: "Long Passes",
                                  gk10: "Long\nPass %",
                                 })


    x = distdf['Value']
    g = list(distdf.Metric)
    df_1 = pd.DataFrame(dict(x=x, g=g))


    team_unique = list(df_1.g.unique())
    num_teams = len(team_unique)
    means_ = range(0,num_teams)
    meds_ = range(0,num_teams)
    d = {'g': team_unique, 'Mean': means_, 'Median': meds_}
    df_means = pd.DataFrame(data=d)

    for i in range(len(team_unique)):
        a = df_1[df_1['g']==team_unique[i]]
        mu = float(a.mean())
        med = float(a.median())
        df_means['g'].iloc[i] = team_unique[i]
        df_means['Mean'].iloc[i] = mu
        df_means['Median'].iloc[i] = med
    y_order = list(df_means['g'])

    df_1 = df_1.merge(df_means, on='g', how='left')

    # add in extra columns
    df_1['Player'] = distdf['Player']
    df_1['Value'] = distdf['Value']
    df_1['TrueVal'] = distdf['TrueVal']
    df_1['Group'] = distdf['Group']
    player_df = df_1[df_1['Player']==ws_name].reset_index(drop=True)
    line_val = player_df['Value']
    true_val = round(player_df['TrueVal'], 2)
    labels = df_1['g'].unique()

    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]
    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(num_teams, rot=2.5, light=.5)
    g = sns.FacetGrid(df_1, hue='Group', row="g", aspect=15, height=.5, row_order=y_order,
    #                   palette=pal,
                     )

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "x",
          bw_adjust=.5, clip_on=False,
          fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5,)


    # draw each distribution's line
    for ax, val, COLORS, tval in zip(g.axes.flat, line_val, COLORS, true_val):
        ax.axvline(x=val, color='white', linestyle='solid', ymin=0, ymax=.7, lw=4)
        ax.axvline(x=val, color=COLORS, linestyle='solid', ymin=0, ymax=.7, lw=2)
        ax.text(max(df_1['Value'])+((max(df_1['Value'])-min(df_1['Value']))/6), 0.01, tval, color=COLORS, fontweight='bold')


    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]
#     path_eff = [path_effects.Stroke(linewidth=.5, foreground='white'), path_effects.Normal()]
    for ax, val, COLORS, lab in zip(g.axes.flat, line_val, COLORS, labels):
        ax.text(min(df_1['Value'])-((max(df_1['Value'])-min(df_1['Value']))/3), 0.01, lab, color='w', fontweight='bold', fontsize=12.1)
        ax.text(min(df_1['Value'])-((max(df_1['Value'])-min(df_1['Value']))/3), 0.01, lab, color=COLORS, fontweight='bold')

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.1)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], xticks=[], ylabel='', xlabel='')
    g.despine(bottom=True, left=True)

    fig = plt.gcf()
    fig.patch.set_facecolor('#fbf9f4')
    fig.set_size_inches(7, 15)

    plt.suptitle('%s (%i, %s), %s, %s %s'
                 %(name, age, player_pos, team, season, league),
                 fontsize=15,
                 fontfamily="DejaVu Sans",
                color="#4A2E19", #4A2E19
                 fontweight="bold", fontname="DejaVu Sans",
                x=0.5,
                y=1.01)

    plt.annotate('All values are per 90 minutes%s\nCompared to %s %s, %i+ mins\nData: Wyscout | %s\nCode by @BeGriffis' %(extra_text, league, compares, mins, sig),
                 xy = (0, -.6), xycoords='axes fraction',
                ha='left', va='center',
                fontsize=9, fontfamily="DejaVu Sans",
                color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                )   

    if template == 'attacking':
        plt.annotate("Per 90' Number",
                     xy = (.85, 20.6), xycoords='axes fraction',
                    ha='left', va='center',
                    fontsize=9, fontfamily="DejaVu Sans",
                    color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                    )  
        plt.annotate("Metric",
                     xy = (0, 20.6), xycoords='axes fraction',
                    ha='left', va='center',
                    fontsize=9, fontfamily="DejaVu Sans",
                    color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                    )
    if template == 'defensive':
        plt.annotate("Per 90' Number",
                     xy = (.85, 16), xycoords='axes fraction',
                    ha='left', va='center',
                    fontsize=9, fontfamily="DejaVu Sans",
                    color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                    )  
        plt.annotate("Metric",
                     xy = (0, 16), xycoords='axes fraction',
                    ha='left', va='center',
                    fontsize=9, fontfamily="DejaVu Sans",
                    color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                    )  
    if template == 'gk':
        plt.annotate("Per 90' Number",
                     xy = (.85, 9), xycoords='axes fraction',
                    ha='left', va='center',
                    fontsize=9, fontfamily="DejaVu Sans",
                    color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                    )  
        plt.annotate("Metric",
                     xy = (0, 9), xycoords='axes fraction',
                    ha='left', va='center',
                    fontsize=9, fontfamily="DejaVu Sans",
                    color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                    )  


    if club_image == 'y':
        from PIL import Image
        image = Image.open(imgpath)
        newax = fig.add_axes([.8,-.03,0.08,0.08], anchor='C', zorder=1)
        newax.imshow(image)
        newax.axis('off')
    plt.show()


# %%
