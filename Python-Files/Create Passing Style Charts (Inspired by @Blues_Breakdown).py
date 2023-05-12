# %%
"""
# Input the final names into the second block of code (if you changed the names from the FBRef data download file). Then run that block, then input the required info into the first block.
### No need to rerun the 2nd block. Just change the info in the first block and run!
"""

# %%
ScoutReport(season = "22-23",               # Season (In the future I'll upload code on my GitHub that will download prior years' data)
            player_pos = "Right Winger",          # Position of player & comparisons
            playerPrompt = "Lionel Messi",  # Player name
            SquadPrompt = "",               # Optional. But Required for players who played for more than one team
            minutesPlayed = 450,            # The number of minutes to filter by (I recommend minimum of 450, as I've ensured all player positions are right for at least 450 minutes)
            compP = "ligue 1",              # OPTIONS: epl, la liga, bundesliga, serie a, ligue 1 ('n' will be all 5 leagues)
            saveinput = "n",                # 'y' if you want to save figure, 'n' if not
            signature = "@BeGriffis",     # Your handle
            data_date = 'Data as of 12/19/22'    # The date you downloaded the FBRef data. IMPORTANT TO NOTE THE DATE
           )

##### Single-Position Options #####
# Goalkeeper
# Centre-Back
# Left-Back
# Right-Back
# Defensive Midfield
# Central Midfield
# Left Midfield
# Right Midfield
# Attacking Midfield
# Left Winger
# Right Winger
# Second Striker
# Centre-Forward

##### Multiple Position Options #####
# Fullback (RB + LB)
# Midfielder (DM + CM + CAM)
# Winger (RM + LM + RW + RM))
# Forward (RW + LW + SS + ST)
# Striker (CF + SS)

# %%
# Packages
%matplotlib inline
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean
from math import pi
from PIL import Image
import os
from pathlib import Path

# this is the file path root, i.e. where this file is located
root = str(Path(os.getcwd()).parents[0]).replace('\\','/')+'/'

# Set the default style to white
sns.set_style("white")

pct = '%'
def ScoutReport(season, player_pos, playerPrompt, SquadPrompt, minutesPlayed, compP, saveinput, signature, data_date):
    # # Ask what file to use
    ssn = season
    if player_pos == "Goalkeeper":
        root = str(Path(os.getcwd()).parents[0]).replace('\\','/')+'/'
        final_gk = 'Final FBRef GK 2022-2023' ####################################### INPUT FILE NAME HERE
        path = "%s%s.csv" %(root, final_gk)
    else:
        root = str(Path(os.getcwd()).parents[0]).replace('\\','/')+'/'
        final_nongk = 'Final FBRef 2022-2023' ####################################### INPUT FILE NAME HERE
        path = "%s%s.csv" %(root, final_nongk)
            
########### I WILL UPDATE GITHUB IN THE FUTURE WITH CODE FOR PRIOR SEASONS ###########

    # Data
    df = pd.read_csv(path)
    df["AerialWin%"] = (df["AerialWins"]/(df["AerialWins"]+df["AerialLoss"]))*100
    df["Dispossessed"] = df["Disposesed"]
    df["DispossessedPer90"] = df["DisposesedPer90"]
    df["PctCmpFinal1/3"] = (df["Final1/3Cmp"]/df["PassesCompleted"])*100
    df["Comp"] = df["Comp"].replace("eng Premier League","Premier League")
    df["Comp"] = df["Comp"].replace("fr Ligue 1","Ligue 1")
    df["Comp"] = df["Comp"].replace("de Bundesliga","Bundesliga")
    df["Comp"] = df["Comp"].replace("it Serie A","Serie A")
    df["Comp"] = df["Comp"].replace("es La Liga","La Liga")
    df = df.fillna(0)
    df['AvgPassLen'] = df['TotalPassDist']/df['PassesCompleted']
#     df['GroundPer90Pct'] = df['GroundPer90']/(df['GroundPer90']+df['LowPer90']+df['HighPer90'])*100
#     df['LowPer90Pct'] = df['LowPer90']/(df['GroundPer90']+df['LowPer90']+df['HighPer90'])*100
#     df['HighPer90Pct'] = df['HighPer90']/(df['GroundPer90']+df['LowPer90']+df['HighPer90'])*100


    def passing():
        f, axes = plt.subplots(3, 3, figsize=(20,10))

        # Filter data
        player = df[df['Player']==playerPrompt]
        dfFilt = df[df['Min']>=minutesPlayed]
        if ((player_pos == 'Goalkeeper') or
            (player_pos == 'Centre-Back') or
            (player_pos == 'Left-Back') or
            (player_pos == 'Right-Back') or
            (player_pos == 'Defensive Midfield') or
            (player_pos == 'Central Midfield') or
            (player_pos == 'Left Midfield') or
            (player_pos == 'Right Midfield') or
            (player_pos == 'Attacking Midfield') or
            (player_pos == 'Left Winger') or
            (player_pos == 'Right Winger') or
            (player_pos == 'Second Striker') or
            (player_pos == 'Centre-Forward')
           ):
            dfFilt = dfFilt[dfFilt['Main Position'].str.contains(player_pos)]
        if player_pos == 'Fullback':
            dfFilt = dfFilt[(dfFilt['Main Position'].str.contains('Left-Back')) |
                            (dfFilt['Main Position'].str.contains('Right-Back'))]
        if player_pos == 'Midfielder':
            dfFilt = dfFilt[(dfFilt['Main Position'].str.contains('Defensive Midfield')) |
                            (dfFilt['Main Position'].str.contains('Central Midfield')) |
                            (dfFilt['Main Position'].str.contains('Attacking Midfield'))]
        if player_pos == 'Winger':
            dfFilt = dfFilt[(dfFilt['Main Position'].str.contains('Right Midfield')) |
                            (dfFilt['Main Position'].str.contains('Left Midfield')) |
                            (dfFilt['Main Position'].str.contains('Left Winger')) |
                            (dfFilt['Main Position'].str.contains('Right Winger'))]
        if player_pos == 'Forward':
            dfFilt = dfFilt[(dfFilt['Main Position'].str.contains('Centre-Forward')) |
                            (dfFilt['Main Position'].str.contains('Second Striker')) |
                            (dfFilt['Main Position'].str.contains('Left Winger')) |
                            (dfFilt['Main Position'].str.contains('Right Winger'))]

        if SquadPrompt != "":
            player = player[player['Squad']==SquadPrompt]
        if compP == "n":
            dfFilt = dfFilt
        if compP == "epl":
            dfFilt = dfFilt[dfFilt['Comp']=="Premier League"]
        if compP == "bundesliga":
            dfFilt = dfFilt[dfFilt['Comp']=="Bundesliga"]
        if compP == "la liga":
            dfFilt = dfFilt[dfFilt['Comp']=="La Liga"]
        if compP == "ligue 1":
            dfFilt = dfFilt[dfFilt['Comp']=="Ligue 1"]
        if compP == "serie a":
            dfFilt = dfFilt[dfFilt['Comp']=="Serie A"]
        Comp = player['Comp'].values[0]

        # Variables to be plotted        
        stat1 = "PassesAttemptedPer90"
        stat2 = "ReceivedPassPer90"
        stat3 = "TouchCentrality"
        
        stat4 = "ShortPassCmp%"
        stat5 = "MedPassCmp%"
        stat6 = "LongPassCmp%"
        
        stat7 = "AvgPassLen"
        stat8 = "SwitchesPer90"
        stat9 = "ProgPassesPer90"
        
        #Get the specific player's value (and name)
        x1 = player[stat1].values[0]
        x2 = player[stat2].values[0]
        x3 = player[stat3].values[0]
        x4 = player[stat4].values[0]
        x5 = player[stat5].values[0]
        x6 = player[stat6].values[0]
        x7 = player[stat7].values[0]
        x8 = player[stat8].values[0]
        x9 = player[stat9].values[0]
        playerName = player["Player"].values[0]
        teamName = player["Squad"].values[0]
        str_age = player["Age"][:2]
        age = str_age.values[0]
        minutes = player['Min'].values[0]

        # Calculate their percentile
        pct1 = stats.percentileofscore(dfFilt[stat1],x1)
        pct2 = stats.percentileofscore(dfFilt[stat2],x2)
        pct3 = stats.percentileofscore(dfFilt[stat3],x3)
        pct4 = stats.percentileofscore(dfFilt[stat4],x4)
        pct5 = stats.percentileofscore(dfFilt[stat5],x5)
        pct6 = stats.percentileofscore(dfFilt[stat6],x6)
        pct7 = stats.percentileofscore(dfFilt[stat7],x7)
        pct8 = stats.percentileofscore(dfFilt[stat8],x8)
        pct9 = stats.percentileofscore(dfFilt[stat9],x9)
        pctMins = stats.percentileofscore(dfFilt['Min'],minutes)

        if pct1 >= 95:
            col = "darkgreen"
        if 84 <= pct1 < 95:
            col = "yellowgreen"
        if 16 <= pct1 < 84:
            col = "darkgrey"
        if 5 <= pct1 < 16:
            col = "orange"
        if 0 <= pct1 < 5:
            col = "red"
        # The plot & player line
        ax1 = sns.kdeplot(dfFilt[stat1], color=col, fill=col, ax=axes[0,0])
        ax1.axvline(x1, 0, .95, lw=2.5, color=col)
        ## Percentile lines
        #x1_50 = np.percentile(dfFilt[stat1], 50)
        #x1_90 = np.percentile(dfFilt[stat1], 90)
        #ax1.axvline(x1_50, 0, .9, color="black", linestyle="--", label="95th Percentile")
        #ax1.axvline(x1_90, 0, .9, color="Black", linestyle=":", label="80th Percentile")
        ax1.set_title("Passess Attempted: %.1f\n%i percentile" % (x1, pct1))
        # Clean graph
        ax1.set(xlabel=None)
        ax1.set(ylabel=None)
        ax1.set(yticks=[])

        if pct2 >= 95:
            col = "darkgreen"
        if 84 <= pct2 < 95:
            col = "yellowgreen"
        if 16 <= pct2 < 84:
            col = "darkgrey"
        if 5 <= pct2 < 16:
            col = "orange"
        if 0 <= pct2 < 5:
            col = "red"
        # The plot & player line
        ax2 = sns.kdeplot(dfFilt[stat2], color=col, fill=col, ax=axes[0,1])
        ax2.axvline(x2, 0, .95, lw=2.5, color=col)
        ax2.set_title("Received Passes: %.1f\n%i percentile" % (x2, pct2))
        # Clean graph
        ax2.set(xlabel=None)
        ax2.set(ylabel=None)
        ax2.set(yticks=[])

        if pct3 >= 95:
            col = "darkgreen"
        if 84 <= pct3 < 95:
            col = "yellowgreen"
        if 16 <= pct3 < 84:
            col = "darkgrey"
        if 5 <= pct3 < 16:
            col = "orange"
        if 0 <= pct3 < 5:
            col = "red"
        # The plot & player line
        ax3 = sns.kdeplot(dfFilt[stat3], color=col, fill=col, ax=axes[0,2])
        ax3.axvline(x3, 0, .95, lw=2.5, color=col)
        ax3.set_title("Centrality (%s of Squad's touches/90): %.2f\n%i percentile" % (pct, x3, pct3))
        # Clean graph
        ax3.set(xlabel=None)
        ax3.set(ylabel=None)
        ax3.set(yticks=[])

        if pct4 >= 95:
            col = "darkgreen"
        if 84 <= pct4 < 95:
            col = "yellowgreen"
        if 16 <= pct4 < 84:
            col = "darkgrey"
        if 5 <= pct4 < 16:
            col = "orange"
        if 0 <= pct4 < 5:
            col = "red"
        # The plot & player line
        ax4 = sns.kdeplot(dfFilt[stat4], color=col, fill=col, ax=axes[1,0])
        ax4.axvline(x4, 0, .95, lw=2.5, color=col)
        ax4.set_title("Short Completion %s: %.1f\n%i percentile" % (pct, x4, pct4))
        # Clean graph
        ax4.set(xlabel=None)
        ax4.set(ylabel=None)
        ax4.set(yticks=[])

        if pct5 >= 95:
            col = "darkgreen"
        if 84 <= pct5 < 95:
            col = "yellowgreen"
        if 16 <= pct5 < 84:
            col = "darkgrey"
        if 5 <= pct5 < 16:
            col = "orange"
        if 0 <= pct5 < 5:
            col = "red"
        # The plot & player line
        ax5 = sns.kdeplot(dfFilt[stat5], color=col, fill=col, ax=axes[1,1])
        ax5.axvline(x5, 0, .95, lw=2.5, color=col)
        ax5.set_title("Medium Completion %s: %.1f\n%i percentile" % (pct, x5, pct5))
        # Clean graph
        ax5.set(xlabel=None)
        ax5.set(ylabel=None)
        ax5.set(yticks=[])

        if pct6 >= 95:
            col = "darkgreen"
        if 84 <= pct6 < 95:
            col = "yellowgreen"
        if 16 <= pct6 < 84:
            col = "darkgrey"
        if 5 <= pct6 < 16:
            col = "orange"
        if 0 <= pct6 < 5:
            col = "red"
        # The plot & player line
        ax6 = sns.kdeplot(dfFilt[stat6], color=col, fill=col, ax=axes[1,2])
        ax6.axvline(x6, 0, .95, lw=2.5, color=col)
        ax6.set_title("Long Completion %s: %.1f\n%i percentile" % (pct, x6, pct6))
        # Clean graph
        ax6.set(xlabel=None)
        ax6.set(ylabel=None)
        ax6.set(yticks=[])

        if pct7 >= 95:
            col = "darkgreen"
        if 84 <= pct7 < 95:
            col = "yellowgreen"
        if 16 <= pct7 < 84:
            col = "darkgrey"
        if 5 <= pct7 < 16:
            col = "orange"
        if 0 <= pct7 < 5:
            col = "red"
        # The plot & player line
        ax7 = sns.kdeplot(dfFilt[stat7], color=col, fill=col, ax=axes[2,0])
        ax7.axvline(x7, 0, .95, lw=2.5, color=col)
        ax7.set_title("Avg Pass Len (yds): %.1f\n%i percentile" % (x7, pct7))
        # Clean graph
        ax7.set(xlabel=None)
        ax7.set(ylabel=None)
        ax7.set(yticks=[])

        if pct8 >= 95:
            col = "darkgreen"
        if 84 <= pct8 < 95:
            col = "yellowgreen"
        if 16 <= pct8 < 84:
            col = "darkgrey"
        if 5 <= pct8 < 16:
            col = "orange"
        if 0 <= pct8 < 5:
            col = "red"
        # The plot & player line
        ax8 = sns.kdeplot(dfFilt[stat8], color=col, fill=col, ax=axes[2,1])
        ax8.axvline(x8, 0, .95, lw=2.5, color=col)
        ax8.set_title("Switches: %.1f\n%i percentile" % (x8, pct8))
        # Clean graph
        ax8.set(xlabel=None)
        ax8.set(ylabel=None)
        ax8.set(yticks=[])

        if pct9 >= 95:
            col = "darkgreen"
        if 84 <= pct9 < 95:
            col = "yellowgreen"
        if 16 <= pct9 < 84:
            col = "darkgrey"
        if 5 <= pct9 < 16:
            col = "orange"
        if 0 <= pct9 < 5:
            col = "red"
        # The plot & player line
        ax9 = sns.kdeplot(dfFilt[stat9], color=col, fill=col, ax=axes[2,2])
        ax9.axvline(x9, 0, .95, lw=2.5, color=col)
        ax9.set_title("Progressive Passes %.1f\n%i percentile" % (x9, pct9))
        # Clean graph
        ax9.set(xlabel=None)
        ax9.set(ylabel=None)
        ax9.set(yticks=[])

        # Finish the graphs
        sns.despine(left=True)
        plt.subplots_adjust(hspace = 1)
        plt.style.use("default")
        
        fig = plt.gcf()
        
        fig.text(0.11, .05,
                   'Red: -2 Standard Deviations (bottom 5%)',
                   fontsize=10, color='red')
        fig.text(0.26, .05,
                   'Orange: -1 Standard Deviation (bottom 16%)',
                   fontsize=10, color='orange')
        fig.text(0.4225, .05,
                   'Grey: Within 1 Standard Deviation (middle 68%)',
                   fontsize=10, color='darkgrey')
        fig.text(0.5975, .05,
                   'Light Green: +1 Standard Deviation (top 16%)',
                   fontsize=10, color='yellowgreen')
        fig.text(0.765, .05,
                   'Dark Green: +2 Standard Deviations (top 5%)',
                   fontsize=10, color='darkgreen')
        
        fig.text(0.11,-.01,
                'All values per 90 minutes | Inspired by @blues_breakdown\nCompared to %s %ss, %i+ minutes\nData from Opta via FBRef)' %(Comp, player_pos, minutesPlayed),
                fontsize=14, color='#4A2E19', va='top', ha='left')
        fig.text(0.92,-.01,
                '%s\n\nCreated: %s | Code by @BeGriffis' %(data_date, signature),
                fontsize=14, color='#4A2E19', va='top', ha='right')
        
        fig.text(.5,1.0,
                '%s (%i, %s, %s) Passing Style' %(playerName, age, teamName, ssn),
                fontsize=25, color="#4A2E19", fontweight="bold", va='center', ha='center')
        
        fig.patch.set_facecolor('#fbf9f4')
        ax1.set_facecolor('#fbf9f4')
        ax2.set_facecolor('#fbf9f4')
        ax3.set_facecolor('#fbf9f4')
        ax4.set_facecolor('#fbf9f4')
        ax5.set_facecolor('#fbf9f4')
        ax6.set_facecolor('#fbf9f4')
        ax7.set_facecolor('#fbf9f4')
        ax8.set_facecolor('#fbf9f4')
        ax9.set_facecolor('#fbf9f4')
        
        fig.set_size_inches(20, 10) #length, height
        
        # IF YOU WANT IMAGES, IT'S PRE-BUILT FOR TEAM/LEAGUE IMAGES
        # Just create a folder with images of the teams & their leagues, name them exactly what
        # they are named in the dataset. Then uncomment these lines below & enter your
        # image folder pathway
        
#         image_folder = '/IMAGE FOLDER FILE PATH HERE/'
#         image = Image.open('%s%s.png' %(image_folder, teamName))
#         newax = fig.add_axes([0.05,.875,0.1,0.1], anchor='C', zorder=1)
#         newax.imshow(image)
#         newax.axis('off')
#         image2 = Image.open('%s%s.png' %(image_folder, Comp))
#         newax = fig.add_axes([0.875,.875,0.1,0.1], anchor='C', zorder=1)
#         newax.imshow(image2)
#         newax.axis('off')
        
        if saveinput == "y":
            fig.savefig("%s%s %s passing profile.png" %(root, playerName, ssn), dpi=220, bbox_inches='tight')
        print("Minutes: %i — %i percentile" %(minutes,pctMins))
        fig = plt.gcf()
        fig.set_size_inches(20, 10) #length, height
        fig


    def main():
        if player_pos != "":
            passing()
    main()

# %%
