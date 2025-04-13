import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, FixedLocator


def plot_heat_demand_hour(data_frames, labels, target_dates, line_colors, face_colors):
    # Convert target dates to datetime objects (remove this line to use the provided target_dates)
    target_dates = pd.to_datetime(target_dates)

    # Create a figure with 4 subplots for each DataFrame
    num_data_frames = len(data_frames)
    num_target_dates = len(target_dates)
    fig, axs = plt.subplots(num_data_frames, num_target_dates, figsize=(25, 32), sharey=True)

    for i, df in enumerate(data_frames):
        # Process the DataFrame
        df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

        # Calculate min, max, and mean values for each row in the processed DataFrame
        hourly_min = df.min(axis=1)
        hourly_max = df.max(axis=1)
        hourly_mean = df.mean(axis=1)

        for j, target_date in enumerate(target_dates):
            start_time = target_date
            end_time = target_date + pd.DateOffset(hours=23)

            filtered_min = hourly_min[start_time:end_time]
            filtered_max = hourly_max[start_time:end_time]
            filtered_mean = hourly_mean[start_time:end_time]

            ax = axs[i, j]  # Get the current subplot

            # Plot min, mean, and max values on the current subplot with customizable colors
            line_color = line_colors[i % len(line_colors)]  # Cycle through colors
            ax.plot(filtered_min.index, filtered_min, label='Min', linewidth=0.5, color=line_color)
            ax.plot(filtered_mean.index, filtered_mean, label='Mean', linewidth=2, color=line_color)
            ax.plot(filtered_max.index, filtered_max, label='Max', linewidth=0.5, color=line_color)
            
            face_color = face_colors[i % len(face_colors)]  # Cycle through colors
            ax.fill_between(filtered_mean.index, filtered_min, filtered_mean, facecolor=face_color, alpha=0.2)
            ax.fill_between(filtered_mean.index, filtered_mean, filtered_max, facecolor=face_color, alpha=0.2)

            ax.set_xticks(filtered_mean.index)

            # Customize subplot titles and legends using labels parameter
            if i == 0:
                ax.set_title(f'{target_date.strftime("%B-%d")}')
            
            # Add grid lines to the current subplot
            ax.grid(color='#FFFFFF', linestyle='dashed', linewidth=1)
            ax.set_xlim(start_time, end_time)

            #'{:.3%}' specifies that the y-axis labels should be formatted as percentages with three decimal places. 
            # This will format values like 0.000000% as 0.000% and values like 0.004000% as 0.004%.
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.3%}'.format(y)))

            # Check if we are in the last set of 4 plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                ax.tick_params(axis='x')  # Show x-axis labels for the last set
                ax.set_xlabel(f'Time (h)')
                ax.set_xticklabels([hour.strftime("%H") for hour in filtered_mean.index])            
            
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

        # Display the legend for the first subplot in the set of four
        axs[i, 0].legend(loc = "upper left", title = labels[i])
        axs[i, 0].set_ylabel(f'Normalized heat demand')
        
    # Display the subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()


def plot_heat_demand_month(data_frames, labels, line_colors, face_colors, date_ranges):
    if len(data_frames) != len(labels) or len(data_frames) != len(line_colors) or len(data_frames) != len(face_colors):
        raise ValueError("The number of DataFrames, labels, line_colors, and face_colors must match.")

    num_data_frames = len(data_frames)
    num_date_ranges = len(date_ranges)
    fig, axs = plt.subplots(num_data_frames, num_date_ranges, figsize=(25, 32), sharey=True)
    
    y_labels = ['Min', 'Mean', 'Max']

    for i, (df, label) in enumerate(zip(data_frames, labels)):
        for j, (start_date, end_date) in enumerate(date_ranges):
            start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
            end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

            df_filtered = df[(df.index >= start_date) & (df.index <= end_date)]

            monthly_min = df_filtered.min(axis=1)
            monthly_max = df_filtered.max(axis=1)
            monthly_mean = df_filtered.mean(axis=1)

            ax = axs[i, j]

            ax.plot(df_filtered.index, monthly_min, label='Min', linewidth=0.5, color=line_colors[i])
            ax.plot(df_filtered.index, monthly_mean, label='Mean', linewidth=2, color=line_colors[i])
            ax.plot(df_filtered.index, monthly_max, label='Max', linewidth=0.5, color=line_colors[i])

            ax.fill_between(df_filtered.index, monthly_min, monthly_mean, facecolor=face_colors[i], alpha=0.2)
            ax.fill_between(df_filtered.index, monthly_mean, monthly_max, facecolor=face_colors[i], alpha=0.2)

            ax.set_xlim(start_date, end_date)
            ax.yaxis.tick_left()

            if i == 0:
                ax.set_title(f'{start_date.strftime("%B")}')

            ax.grid(color='#FFFFFF', linestyle='dashed', linewidth=1)

            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2%}'.format(y))
            )
       
            # Check if we are in the last set of plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                # Set the x-axis locator and formatter
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))  # For example, every 7 days
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

        axs[i, 0].legend(loc="upper left", title=labels[i])
        axs[i, 0].set_ylabel(f'Normalized heat demand')
        
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()
    
def plot_heat_demand_year(data_frames, labels, start_date, end_date, line_colors, face_colors):
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

    # Check if the number of DataFrames, labels, line_colors, and face_colors match
    if len(data_frames) != len(labels) or len(data_frames) != len(line_colors) or len(data_frames) != len(face_colors):
        raise ValueError("The number of DataFrames, labels, line_colors, and face_colors must match.")

    # Create a figure with rows for each DataFrame
    num_data_frames = len(data_frames)
    fig, axs = plt.subplots(num_data_frames, 1, figsize=(25, 32), sharey=True)

    # Define a monthly date locator and formatter
    months = mdates.MonthLocator()
    months_fmt = mdates.DateFormatter('%B')

    # Loop through DataFrames, labels, line_colors, and face_colors
    for i, (df, label, line_color, face_color) in enumerate(zip(data_frames, labels, line_colors, face_colors)):
        
        # Check if the DataFrame has a valid index
        if not df.index.empty:
            # Filter the DataFrame based on the date range
            filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]

            # Calculate min, mean, and max values
            min_values = filtered_df.min(axis=1)
            mean_values = filtered_df.mean(axis=1)
            max_values = filtered_df.max(axis=1)

            # Plot min, mean, and max values on the current subplot with specified colors
            ax = axs[i]  # Get the current subplot
            ax.plot(filtered_df.index, min_values, label='Min', linewidth=0.5, color=line_color)
            ax.plot(filtered_df.index, mean_values, label='Mean', linewidth=2, color=line_color)
            ax.plot(filtered_df.index, max_values, label='Max', linewidth=0.5, color=line_color)

            # Add shadows between min and mean, and between mean and max with specified facecolor
            ax.fill_between(filtered_df.index, min_values, mean_values, facecolor=face_color, alpha=0.2)
            ax.fill_between(filtered_df.index, mean_values, max_values, facecolor=face_color, alpha=0.2)

            # Set subplot title and labels
            ax.set_ylabel('Normalized heat demand')
            # Display the legend for the first subplot in the set of four
            ax.legend(loc="upper left", title=labels[i])
            
            # Add grid lines to the current subplot
            ax.grid(color='#FFFFFF', linestyle='dashed', linewidth=1)
            ax.set_xlim(start_date, end_date)

            # Set y-axis major locator and format
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))

             # Check if we are in the last set of plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                # Set the x-axis locator and formatter
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_major_formatter(months_fmt)
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

    # Adjust layout and display subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()

def plot_elec_demand_hour(data_frames, labels, target_dates, line_colors, face_colors):
# Convert target dates to datetime objects (remove this line to use the provided target_dates)
    target_dates = pd.to_datetime(target_dates)

    # Create a figure with 4 subplots for each DataFrame
    num_data_frames = len(data_frames)
    num_target_dates = len(target_dates)
    fig, axs = plt.subplots(num_data_frames, num_target_dates, figsize=(25, 32), sharey=True)

    for i, df in enumerate(data_frames):
        # Process the DataFrame
        df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

        # Calculate min, max, and mean values for each row in the processed DataFrame
        hourly_min = df.min(axis=1)
        hourly_max = df.max(axis=1)
        hourly_mean = df.mean(axis=1)

        for j, target_date in enumerate(target_dates):
            start_time = target_date
            end_time = target_date + pd.DateOffset(hours=23)

            filtered_min = hourly_min[start_time:end_time]
            filtered_max = hourly_max[start_time:end_time]
            filtered_mean = hourly_mean[start_time:end_time]

            ax = axs[i, j]  # Get the current subplot

            # Plot min, mean, and max values on the current subplot with customizable colors
            line_color = line_colors[i % len(line_colors)]  # Cycle through colors
            ax.plot(filtered_min.index, filtered_min, label='Min', linewidth=0.5, color=line_color)
            ax.plot(filtered_mean.index, filtered_mean, label='Mean', linewidth=2, color=line_color)
            ax.plot(filtered_max.index, filtered_max, label='Max', linewidth=0.5, color=line_color)
            
            face_color = face_colors[i % len(face_colors)]  # Cycle through colors
            ax.fill_between(filtered_mean.index, filtered_min, filtered_mean, facecolor=face_color, alpha=0.2)
            ax.fill_between(filtered_mean.index, filtered_mean, filtered_max, facecolor=face_color, alpha=0.2)

            ax.set_xticks(filtered_mean.index)

            # Customize subplot titles and legends using labels parameter
            if i == 0:
                ax.set_title(f'{target_date.strftime("%B-%d")}')
            
            # Add grid lines to the current subplot
            ax.grid(color='#FFFFFF', linestyle='dashed', linewidth=1)
            ax.set_xlim(start_time, end_time)

            #'{:.3%}' specifies that the y-axis labels should be formatted as percentages with three decimal places. 
            # This will format values like 0.000000% as 0.000% and values like 0.004000% as 0.004%.
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2%}'.format(y)))

            # Check if we are in the last set of 4 plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                ax.tick_params(axis='x')  # Show x-axis labels for the last set
                ax.set_xlabel(f'Time (h)')
                ax.set_xticklabels([hour.strftime("%H") for hour in filtered_mean.index])            
            
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

        # Display the legend for the first subplot in the set of four
        axs[i, 0].legend(loc = "upper left", title = labels[i])
        axs[i, 0].set_ylabel(f'Normalized electricity demand')
        
    # Display the subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()

def plot_electricity_demand_month(data_frames, labels, line_colors, face_colors, date_ranges):
    if len(data_frames) != len(labels) or len(data_frames) != len(line_colors) or len(data_frames) != len(face_colors):
        raise ValueError("The number of DataFrames, labels, line_colors, and face_colors must match.")

    num_data_frames = len(data_frames)
    num_date_ranges = len(date_ranges)
    fig, axs = plt.subplots(num_data_frames, num_date_ranges, figsize=(25, 32), sharey=True)
    
    y_labels = ['Min', 'Mean', 'Max']

    for i, (df, label) in enumerate(zip(data_frames, labels)):
        for j, (start_date, end_date) in enumerate(date_ranges):
            start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
            end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

            df_filtered = df[(df.index >= start_date) & (df.index <= end_date)]

            monthly_min = df_filtered.min(axis=1)
            monthly_max = df_filtered.max(axis=1)
            monthly_mean = df_filtered.mean(axis=1)

            ax = axs[i, j]

            ax.plot(df_filtered.index, monthly_min, label='Min', linewidth=0.5, color=line_colors[i])
            ax.plot(df_filtered.index, monthly_mean, label='Mean', linewidth=2, color=line_colors[i])
            ax.plot(df_filtered.index, monthly_max, label='Max', linewidth=0.5, color=line_colors[i])

            ax.fill_between(df_filtered.index, monthly_min, monthly_mean, facecolor=face_colors[i], alpha=0.2)
            ax.fill_between(df_filtered.index, monthly_mean, monthly_max, facecolor=face_colors[i], alpha=0.2)

            ax.set_xlim(start_date, end_date)
            ax.yaxis.tick_left()

            if i == 0:
                ax.set_title(f'{start_date.strftime("%B")}')

            ax.grid(color='#FFFFFF', linestyle='dashed', linewidth=1)

            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
       
            # Check if we are in the last set of plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                # Set the x-axis locator and formatter
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))  # For example, every 7 days
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

        axs[i, 0].legend(loc="upper left", title=labels[i])
        axs[i, 0].set_ylabel(f'Normalized electricity demand')
        
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()

def plot_electricity_demand_year(data_frames, labels, start_date, end_date, line_colors, face_colors):
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

    # Check if the number of DataFrames, labels, line_colors, and face_colors match
    if len(data_frames) != len(labels) or len(data_frames) != len(line_colors) or len(data_frames) != len(face_colors):
        raise ValueError("The number of DataFrames, labels, line_colors, and face_colors must match.")

    # Create a figure with rows for each DataFrame
    num_data_frames = len(data_frames)
    fig, axs = plt.subplots(num_data_frames, 1, figsize=(25, 32), sharey=True)

    # Define a monthly date locator and formatter
    months = mdates.MonthLocator()
    months_fmt = mdates.DateFormatter('%B')

    # Loop through DataFrames, labels, line_colors, and face_colors
    for i, (df, label, line_color, face_color) in enumerate(zip(data_frames, labels, line_colors, face_colors)):
        
        # Check if the DataFrame has a valid index
        if not df.index.empty:
            # Filter the DataFrame based on the date range
            filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]

            # Calculate min, mean, and max values
            min_values = filtered_df.min(axis=1)
            mean_values = filtered_df.mean(axis=1)
            max_values = filtered_df.max(axis=1)

            # Plot min, mean, and max values on the current subplot with specified colors
            ax = axs[i]  # Get the current subplot
            ax.plot(filtered_df.index, min_values, label='Min', linewidth=0.5, color=line_color)
            ax.plot(filtered_df.index, mean_values, label='Mean', linewidth=2, color=line_color)
            ax.plot(filtered_df.index, max_values, label='Max', linewidth=0.5, color=line_color)

            # Add shadows between min and mean, and between mean and max with specified facecolor
            ax.fill_between(filtered_df.index, min_values, mean_values, facecolor=face_color, alpha=0.2)
            ax.fill_between(filtered_df.index, mean_values, max_values, facecolor=face_color, alpha=0.2)

            # Set subplot title and labels
            ax.set_ylabel('Normalized electricity demand')
            # Display the legend for the first subplot in the set of four
            ax.legend(loc="upper left", title=labels[i])
            
            # Add grid lines to the current subplot
            ax.grid(color='#FFFFFF', linestyle='dashed', linewidth=1)
            ax.set_xlim(start_date, end_date)

            # Set y-axis major locator and format
            ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.2%}'.format(y)))

             # Check if we are in the last set of plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                # Set the x-axis locator and formatter
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_major_formatter(months_fmt)
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

    # Adjust layout and display subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()

def separate(dataframe, column_index):
    """
    Copy and convert a specific column from a DataFrame.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        column_index (int): The index of the column to copy and convert.

    Returns:
        pd.DataFrame: A new DataFrame with the copied and converted column.
    """
    copied_column = dataframe.iloc[:, column_index].copy()
    copied_column = pd.DataFrame(copied_column)
    copied_column = copied_column.astype(float)
    return copied_column

def process_data(df, label):
    for hour in range(24):
        hour_str = f'{hour:02}:00'
        df[hour_str] = 0

    # Create a new timestamp column if it doesn't exist
    if 'timestamp' not in df:
        df['timestamp'] = pd.date_range(start='2100-01-01', periods=len(df), freq='H')

    # Add day of the year information
    df['day_of_year'] = df['timestamp'].dt.dayofyear

    # Loop through hours from 00:00 to 23:00 and filter data
    for hour in range(24):
        time_str = f'{hour:02}:00:00'
        time = pd.to_datetime(time_str).time()
        filtered_rows = df[df['timestamp'].dt.time == time]
        column_name = f'{hour:02}:00'
        df[column_name] = filtered_rows[label]

    # Drop the 'UEU1_ht' and 'timestamp' columns
    df = df.drop([label, 'timestamp' , 'day_of_year'], axis=1)

    return df

def filter_dataframe(df):
    df_plot = pd.DataFrame()
    
    for col in df.columns:
        df_plot[col] = df[col].dropna().reset_index(drop=True)
    
    return df_plot

def plot_energy_demand_distribution(data_frames, labels):
    # Create a figure with rows for each DataFrame
    num_data_frames = len(data_frames)
    fig, axs = plt.subplots(num_data_frames, 1, figsize=(25, 32), sharey=True)

    # Define the common colormap
    cmap = plt.get_cmap('coolwarm')

    # Define the common value scale (min and max values)
    vmin = 0.00000
    vmax = 0.00030

    # Loop through DataFrames, labels, and subplots
    for i, (df, label) in enumerate(zip(data_frames, labels)):
        ax = axs[i]  # Get the current subplot

        # Create a pcolormesh plot with transposed data
        pcm = ax.pcolormesh(df.values.T, cmap=cmap, vmin=vmin, vmax=vmax)

        # Add a color bar on the right side of the plot
        cbar = fig.colorbar(pcm, ax=ax, label='Value Scale', orientation='vertical')

        # Set the colorbar's ticks to display as percentages
        cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.3%}'.format(y)))

        # Set the y-axis labels and title
        ax.set_ylabel('Hours')
        ax.set_title(f'{label}')

        if i == len(data_frames) - 1:
            # If this is the last plot, set the x-axis locator and formatter
            ax.set_xlabel('Days')
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Use integer hours on x-axis

        else:
            ax.set_xticklabels([])  # Hide x-axis labels for other sets

    # Adjust layout and display subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()