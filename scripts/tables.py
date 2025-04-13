# Tables
import pandas as pd

def process_date_range(dataframes, labels, start_date, end_date):
    min_results = []  # Store minimum value DataFrames
    max_results = []  # Store maximum value DataFrames
    mean_results = []  # Store mean value DataFrames

    for i, df in enumerate(dataframes):
        # Calculate min, max, and mean values for each row in the input DataFrame
        hourly_min = df.min(axis=1)
        hourly_max = df.max(axis=1)
        hourly_mean = df.mean(axis=1)

        # Filter data by the specified date range for all dataframes
        filtered_min = hourly_min[(hourly_min.index >= start_date) & (hourly_min.index <= end_date)]
        filtered_max = hourly_max[(hourly_max.index >= start_date) & (hourly_max.index <= end_date)]
        filtered_mean = hourly_mean[(hourly_mean.index >= start_date) & (hourly_mean.index <= end_date)]

        # Create DataFrames for the indicator
        min_df = pd.DataFrame({f'{labels[i]}': filtered_min})
        max_df = pd.DataFrame({f'{labels[i]}': filtered_max})
        mean_df = pd.DataFrame({f'{labels[i]}': filtered_mean})

        # Append DataFrames to respective result lists
        min_results.append(min_df)
        max_results.append(max_df)
        mean_results.append(mean_df)

    # Concatenate the results into separate DataFrames
    min_hourly_indicators = pd.concat(min_results, axis=1)
    max_hourly_indicators = pd.concat(max_results, axis=1)
    mean_hourly_indicators = pd.concat(mean_results, axis=1)

    return min_hourly_indicators, max_hourly_indicators, mean_hourly_indicators

def daily_indicators(df, df_name, date_ranges):
    
    df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
    df = df.loc[:, (df != 0).any(axis=0)]  # Drop columns with all zeros
    
        # Calculate min, max, and mean values for each row in the input DataFrame
    daily_min = df.min(axis=1)
    daily_max = df.max(axis=1)
    daily_mean = df.mean(axis=1)

    # Create empty DataFrames to store the results for each date range
    min_results = []
    max_results = []
    mean_results = []

    for start_date, end_date in date_ranges:
        # Filter data by the current date range
        filtered_min = daily_min[(daily_min.index >= start_date) & (daily_min.index <= end_date)]
        filtered_max = daily_max[(daily_max.index >= start_date) & (daily_max.index <= end_date)]
        filtered_mean = daily_mean[(daily_mean.index >= start_date) & (daily_mean.index <= end_date)]

        # Create DataFrames for the current date range and indicator
        min_df = pd.DataFrame({'Min': filtered_min})
        max_df = pd.DataFrame({'Max': filtered_max})
        mean_df = pd.DataFrame({'Mean': filtered_mean})

        # Append DataFrames to respective result lists
        min_results.append(min_df)
        max_results.append(max_df)
        mean_results.append(mean_df)

    # Concatenate the results into separate DataFrames
    min_daily_indicators = pd.concat(min_results, axis=0)
    max_daily_indicators = pd.concat(max_results, axis=0)
    mean_daily_indicators = pd.concat(mean_results, axis=0)

    # Rename the columns with df_name prefix
    min_daily_indicators.columns = [f'{df_name}']
    max_daily_indicators.columns = [f'{df_name}']
    mean_daily_indicators.columns = [f'{df_name}']

    return min_daily_indicators, max_daily_indicators, mean_daily_indicators



