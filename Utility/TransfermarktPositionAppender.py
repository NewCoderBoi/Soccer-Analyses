import os
from pathlib import Path
import pandas as pd

class TransfermarktPositionAppender:

    def position_update(self, df_league_data):
        root = str(Path(os.getcwd()).parents[0]).replace('\\','/')+'/'
        filename = 'TransfermarktPositions-Jase_Ziv83'

        df_position_data = pd.read_csv("%s%s.csv" %(root,filename))

        for key, value in df_position_data.iterrows():
            player_name = value[0]
            player_position = value[1]

            df_league_data.loc[df_league_data.Player==player_name, 'Pos'] = player_position

        return df_league_data

# df_league_data = pd.read_csv("C:/Analytics/Soccer-Analyses/Final FBRef 2022 - Brasileirão.csv")
# df_league_data = transfermarkt_position_appender.position_update(df_league_data)
# print(df_league_data[['Player', 'Pos']].head(20))