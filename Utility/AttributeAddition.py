class AttributeAddition:
    def add_attribute_to_df(self, df_league_data):

        # 1. Expected assists per Key Pass
        xA_per_KP = []
        for itr in range(len(df_league_data['xA'])):
            if df_league_data['KeyPasses'][itr] == 0:
                xA_per_KP.append(0)
            else:
                xA_per_KP.append(df_league_data['xAPer90'][itr] / df_league_data['KeyPassesPer90'][itr])

        df_league_data['xA per Key Pass'] = xA_per_KP

        # 2. Touches in Def 3rd per touch
        def3rdtouch_per_touch = df_league_data['Def3rdTouchPer90']/df_league_data['TouchesPer90']
        df_league_data['Def 3rd Touches Per Touch'] = def3rdtouch_per_touch

        return df_league_data
