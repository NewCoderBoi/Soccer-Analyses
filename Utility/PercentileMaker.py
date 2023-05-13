class PercentileMaker:
    def get_percentile_of_reqd_columns(self, df, column_list):
        for column in column_list:
            percentile_column = df[column].rank(pct=True)
            df['%s-Percentile' % column] = percentile_column * 100
        return df