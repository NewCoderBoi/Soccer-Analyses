import os
from pathlib import Path
import pandas as pd
from Utility import AttributeAddition, TransfermarktPositionAppender, PercentileMaker

root = str(Path(os.getcwd()).parents[0]).replace('\\', '/') + '/'


class MidfielderClassifier:

    def main(self):
        transfermarktPositionAppender = TransfermarktPositionAppender.TransfermarktPositionAppender()
        attributeAddition = AttributeAddition.AttributeAddition()
        percentileMaker = PercentileMaker.PercentileMaker()

        df_league_data = pd.read_csv("%sFinal FBRef 2022 - Brasileirão.csv" % root)  # make this path name variable.

        # Inversing age.
        df_league_data['1/Age'] = 1/df_league_data['Age']

        # Calculating %ile of required columns
        df_league_data = percentileMaker.get_percentile_of_reqd_columns(df_league_data, ['Min', '1/Age', 'PassesAttemptedPer90','KeyPassesPer90'])

        # Adding transfermarkt defined positions - dataset created by Jase_Ziv83 - Having issues with player mapping
        #df_league_data = transfermarktPositionAppender.position_update(df_league_data)

        # Adding columns which are needed - more columns will be added in this utility class
        df_league_data = attributeAddition.add_attribute_to_df(df_league_data)

        # #################################### ALGORITHM ##############################################3##

        # Looking for central midfielder and attacking midfielder, > 1000 minutes, checking for >80% pass acc,
        # >= 1/6th touches in def 3rd, xA per key pass >= 0.09, sort them by greater pass value or lower age,
        # or a weighted average value of both of them, not decided yet .

        # ##################################################################################################

        df_league_data.rename(columns={'TotCmp%': 'TotCompPercent'}, inplace=True)
        df_league_data.columns = df_league_data.columns.str.replace(' ', '')

        # print(df_league_data.loc[df_league_data['Player']=='Victor Hugo'][['Player', 'Pos', 'Min','TotCompPercent']])
        #
        # for column in list(df_league_data.columns):
        #     print(column)

        #df_league_data = df_league_data[(df_league_data.Pos == "Central Midfield")
        #                                | (df_league_data.Pos == "Attacking Midfield")]

        df_league_data = df_league_data[(df_league_data.Pos == "MF")
                                        | (df_league_data.Pos == "MF,FW")]

        df_league_data = df_league_data[(df_league_data.Min >= 1000) & (df_league_data.TotCompPercent >= 80)]

        df_league_data = df_league_data[(df_league_data.xAperKeyPass >= 0.09)
                                        & (df_league_data.Def3rdTouchesPerTouch >= 0.16)]

        # GIVING THE FINAL PLAYERS SCORES

        weight=0.25
        overall_score = []

        for index in df_league_data.index:

            min_ile = df_league_data['Min-Percentile'][index]
            age_inv_ile = df_league_data['1/Age-Percentile'][index]
            pass_p90_ile = df_league_data['PassesAttemptedPer90-Percentile'][index]
            xa_p90_ile = df_league_data['KeyPassesPer90-Percentile'][index]

            score = (min_ile * weight) + (age_inv_ile * weight) + (pass_p90_ile * weight)\
                    + (xa_p90_ile * weight)

            overall_score.append(score)

        df_league_data['Overall Score'] = overall_score

        # SORT BY DECREASING ORDER OF SCORE

        # df_league_data

        print(len(df_league_data['Player']))
        print(df_league_data[['Player', 'Pos', 'Overall Score']]
              .sort_values('Overall Score', ascending=False).head(20))



if __name__ == "__main__":
    midfieldClassifier = MidfielderClassifier()
    midfieldClassifier.main()
