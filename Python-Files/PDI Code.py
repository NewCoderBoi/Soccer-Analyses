# %%
"""
### This code will work for any Wyscout file from the "advanced search" section. Create a view that has, literally, every single variable. Export that league and the resave as a csv, utf-8. It should automatically be a comma-delimited file, don't change to a semi-color delimiter or else the code will not work.

### Enter the basic information below, after the packages, including the full file path ('C:/Users/YourName/.../File.csv', etc) and also if you want club logos to appear in the table. If you want logos, ensure you have a folder that has the logos named the exact same as the club name in Wyscout. The logos should be .png files.

### Also make sure to enter the save path for the image. The table image will save in that location as a .png file.
"""

# %%
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings('ignore')
from statistics import mean, harmonic_mean
import seaborn as sns
from math import exp
import matplotlib.pyplot as plt
from PIL import Image
############################################################################

# enter some basic information. mins is the minimum minutes threshold
lg = 'Latvian Virsliga'
season = '2022'
mins = 900
data_time = 'Data final for 2022'
path = "ENTER THE FILEPATH FOR A CSV UTF-8 ENCODED COMMA-SEPARATED FILE HERE"
table_save_path = 'ENTER YOUR DESIRED LOCATION TO SAVE THE TABLE IMAGE'

# write 'y' for club_img and enter the folder path for club images below, if you want images on the table
club_img = ''
logos_file_path = 'C:/Users/Ben/From Mac/Python/FBRef/FBRef Files/Images'

# if you want to export this league's PDI ranking (including their 4 input metrics) as a csv file,
# write 'y' here. It will save to the table_save_path location
pdi_data_table_export = 'y'

############################################################################

df = pd.read_csv(path)
df = df.dropna(subset=['Age', 'Position']).reset_index(drop=True)
df['Main Position'] = ''
for i in range(len(df)):
    df['Main Position'][i] = df['Position'][i].split()[0]
df = df[df['Minutes played']>=mins].reset_index(drop=True)
df['All deep completions per 90'] = df['Deep completed crosses per 90'] + df['Deep completions per 90']
df['Smart passes completed per 90'] = df['Smart passes per 90'] * (df['Accurate smart passes, %']/100)

for i in range(len(df)):
    lastchar = df[['Main Position']].iloc[i].values[0][-1]
    if lastchar == ',':
        df['Main Position'].iloc[i] = df[['Main Position']].iloc[i].values[0][:-1]

############################################################################

## This section is the  PDI code, the harmonic mean calculation
varlist = ['Smart passes completed per 90', 'All deep completions per 90', 'Shot assists per 90', 'Key passes per 90']

df['Passing Danger Index'] = 0.0
for i in range(len(df)):
    df['Passing Danger Index'].iloc[i] = harmonic_mean(df[varlist].iloc[i])
allvars = ['Player', 'Age', 'Main Position', 'Team within selected timeframe', 'Passing Danger Index',]+varlist
indexdf = df[allvars].sort_values(by=['Passing Danger Index'], ascending=False).reset_index(drop=True)
indexdf.rename(columns={'Team within selected timeframe':'Team'}, inplace=True)
if pdi_data_table_export == 'y':
    indexdf.to_csv('%s/%s PDI Table %s.csv' %(table_save_path,lg,season))
##

############################################################################
def ax_logo(team, ax, lg):
    league = lg
    path = imagefilepath
    club_icon = Image.open('%s/%s.png' %(logos_file_path,team))
    ax.imshow(club_icon)
    ax.axis('off')
    return ax
############################################################################

sns.set(rc={'axes.facecolor':'#fbf9f4', 'figure.facecolor':'#fbf9f4',
           'ytick.labelcolor':'#4A2E19', 'xtick.labelcolor':'#4A2E19'})


indexdf_short = indexdf[['Player', 'Team', 'Age', 'Main Position', 'Passing Danger Index']].head(20).sort_values(by=['Passing Danger Index'], ascending=True).reset_index(drop=True)
indexdf_short.Age = indexdf_short.Age.astype(int)
indexdf_short.rename(columns={'Passing Danger Index':'PDI', 'Main Position':'Pos.'}, inplace=True)

fig = plt.figure(figsize=(7,8), dpi=200)
ax = plt.subplot()

ncols = len(indexdf_short.columns.tolist())+1
nrows = indexdf_short.shape[0]

ax.set_xlim(0, ncols + .5)
ax.set_ylim(0, nrows + 1.5)

positions = [0.25, 2.5, 4.5, 5.25, 6]
columns = indexdf_short.columns.tolist()

# Add table's main text
for i in range(nrows):
    for j, column in enumerate(columns):
        if 'PDI' in column:
            text_label = f'{indexdf_short[column].iloc[i]:,.2f}'
            weight = 'bold'
        else:
            text_label = f'{indexdf_short[column].iloc[i]}'
            weight = 'regular'
        ax.annotate(
            xy=(positions[j], i + .5),
            text = text_label,
            ha='left',
            va='center', color='#4A2E19',
            weight=weight
        )

# Add column names
column_names = columns
for index, c in enumerate(column_names):
        ax.annotate(
            xy=(positions[index], nrows + .25),
            text=column_names[index],
            ha='left',
            va='bottom',
            weight='bold', color='#4A2E19'
        )

# Add dividing lines
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=1.5, color='black', marker='', zorder=4)
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color='black', marker='', zorder=4)
for x in range(1, nrows):
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color='gray', ls=':', zorder=3 , marker='')

ax.set_axis_off()

DC_to_FC = ax.transData.transform
FC_to_NFC = fig.transFigure.inverted().transform
# -- Take data coordinates and transform them to normalized figure coordinates
DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))
# -- Add nation axes
ax_point_1 = DC_to_NFC([2.25, 0.25])
ax_point_2 = DC_to_NFC([2.75, 0.75])
ax_width = abs(ax_point_1[0] - ax_point_2[0])
ax_height = abs(ax_point_1[1] - ax_point_2[1])
if club_img == 'y':
    for x in range(0, nrows):
        ax_coords = DC_to_NFC([2.0, x + .25])
        flag_ax = fig.add_axes(
            [ax_coords[0], ax_coords[1], ax_width, ax_height]
        )
        ax_logo(indexdf_short['Team'].iloc[x], flag_ax, lg)

fig.text(
    x=0.15, y=.9,
    s='%s %s Passing Danger Index Top 20' %(season,lg),
    ha='left',
    va='bottom',
    weight='bold',
    size=13, color='#4A2E19'
)
fig.text(
    x=0.15, y=.895,
    s='Includes players with at least %i minutes played | %s\nData via Wyscout | Table code by @sonofacorner | PDI code by Ben Griffis' %(mins, data_time),
    ha='left',
    va='top',
    weight='bold',
    size=7, color='#4A2E19'
)

xtranote = 'all adjusted per 90 minutes'
fig.text(
    x=0.15, y=.11,
    s="PDI is the harmonic mean of Smart Passes, Deep Completions, Shot Assists, & Key Passes (%s)" %(xtranote),
    ha='left',
    va='top',
    weight='regular',
    size=6, color='#4A2E19'
)


plt.savefig(
    '%s/%s PDI Table %s.png' %(table_save_path,lg,season),
    dpi=300,
    transparent=False,
    bbox_inches='tight'
)


# %%
