
import pandas as pd

def resample_dataframes(input_dataframe):
    # Resample to daily sum
       
    df_daily = input_dataframe.resample('D').sum()
    
    # Resample to weekly sum
    df_weekly = input_dataframe.resample('W').sum()
    
    # Resample to monthly sum
    df_monthly = input_dataframe.resample('M').sum()

    # Process the DataFrames
    df_daily = df_daily.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
    df_weekly = df_weekly.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
    df_monthly = df_monthly.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
    df_daily = df_daily.loc[:, (df_daily != 0).any(axis=0)]  # Drop columns with all zeros
    df_weekly = df_weekly.loc[:, (df_weekly != 0).any(axis=0)]  # Drop columns with all zeros
    df_monthly = df_monthly.loc[:, (df_monthly != 0).any(axis=0)]  # Drop columns with all zeros

    
    return df_daily, df_weekly, df_monthly