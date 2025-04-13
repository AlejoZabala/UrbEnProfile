import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec

def plot_heat_demand_hour(data_frames, labels, target_dates, line_colors, face_colors):
    # Convert target dates to datetime objects (remove this line to use the provided target_dates)
    target_dates = pd.to_datetime(target_dates)

    # Create a figure with 4 subplots for each DataFrame
    num_data_frames = len(data_frames)
    num_target_dates = len(target_dates)
    fig, axs = plt.subplots(num_data_frames, num_target_dates, figsize=(25, 4*num_data_frames), sharey=True)

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

            # Customize subplot titles and legends using labels parameter
            ax.set_title(f'{labels[i]} on {target_date.date()}')

            # Add grid lines to the current subplot
            ax.grid(color='k', linestyle='dotted', linewidth=1)

            # Set y-axis major locator and format
            ax.yaxis.set_major_locator(plt.FixedLocator(np.arange(0, 0.0004, 0.00005)))

            # Check if we are in the last set of 4 plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                ax.tick_params(axis='x')  # Show x-axis labels for the last set
                ax.set_xlabel(f'Time (h)')

            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

        # Display the legend for the first subplot in the set of four
        axs[i, 0].legend()
        axs[i, 0].set_ylabel(f'Normalized heat demand')

        
    # Display the subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()

def plot_heat_demand_month(data_frames, labels, line_colors, face_colors, date_ranges):
    # Check if the number of DataFrames, labels, line_colors, and face_colors match
    if len(data_frames) != len(labels) != len(line_colors) != len(face_colors):
        raise ValueError("The number of DataFrames, labels, line_colors, and face_colors must match.")

    # Create subplots grid
    num_data_frames = len(data_frames)
    num_date_ranges = len(date_ranges)
    fig, axs = plt.subplots(num_data_frames, num_date_ranges, figsize=(30, 4*num_data_frames), sharey=True)
    
    # Labels for the y-axes (one for each subplot)
    y_labels = ['Min', 'Mean', 'Max']  # Adjust the labels as needed
    
    # Loop through DataFrames, labels, line_colors, and face_colors
    for i, (df, label) in enumerate(zip(data_frames, labels)):
        for j, (start_date, end_date) in enumerate(date_ranges):
            start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
            end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

            # Filter the DataFrame based on the date range
            df_filtered = df[(df.index >= start_date) & (df.index <= end_date)]

            # Calculate min, max, and mean values for each row in the processed DataFrame
            daily_min = df_filtered.min(axis=1)
            daily_max = df_filtered.max(axis=1)
            daily_mean = df_filtered.mean(axis=1)

            ax = axs[i, j]  # Get the current subplot

            # Plot min, mean, and max values on the current subplot
            ax.plot(daily_min.index, daily_min, label='Min', linewidth=0.5, color=line_colors[i])
            ax.plot(daily_mean.index, daily_mean, label='Mean', linewidth=2, color=line_colors[i])
            ax.plot(daily_max.index, daily_max, label='Max', linewidth=0.5, color=line_colors[i])
            
            ax.fill_between(daily_mean.index, daily_min, daily_mean, facecolor=face_colors[i], alpha=0.2)
            ax.fill_between(daily_mean.index, daily_mean, daily_max, facecolor=face_colors[i], alpha=0.2)

            # Set x-axis limits
            ax.set_xlim(start_date, end_date)
            ax.yaxis.tick_left()

            # Set subplot title and labels
            ax.set_title(f'{label}')
          
            # Add grid lines to the current subplot
            ax.grid(color='k', linestyle='dotted', linewidth=1)

            # Set y-axis major locator and format
            ax.yaxis.set_major_locator(plt.FixedLocator(np.arange(0, 0.01, 0.002)))

            # Check if we are in the last set of 4 plots (corresponding to the last dataframe)
            if i == len(data_frames) - 1:
                ax.tick_params(axis='x')  # Show x-axis labels for the last set
                ax.set_xlabel(f'Time (h)')
            else:
                ax.set_xticklabels([])  # Hide x-axis labels for other sets

        # Display the legend for the first subplot in the set of four
        axs[i, 0].legend()
        axs[i, 0].set_ylabel(f'Normalized heat demand')
        
    # Set the super title
    # plt.suptitle(f'Normalized data for modelled heat demand in Neighborhood during a month in January, April, July, and October')

    # Adjust layout and display subplots
    # Display the subplots
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    plt.show()

def plot_heat_demand_year(data_frames, labels, start_date, end_date, line_colors, face_colors):
    
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

    # Check if the number of DataFrames, labels, line_colors, and face_colors match

    if len(data_frames) != len(labels) != len(line_colors) != len(face_colors):
        
        raise ValueError("The number of DataFrames, labels, line_colors, and face_colors must match.")

    # Create 8 separate subplots
    fig, axs = plt.subplots(8, 1, figsize=(15, 25), sharex=True)
    plt.subplots_adjust(hspace=0)  # Adjust the 'hspace' parameter to reduce vertical spacing

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
            axs[i].plot(filtered_df.index, min_values, label='Min', linewidth=0.5, color=line_color)
            axs[i].plot(filtered_df.index, mean_values, label='Mean', linewidth=2, color=line_color)
            axs[i].plot(filtered_df.index, max_values, label='Max', linewidth=0.5, color=line_color)

            # Add shadows between min and mean, and between mean and max with specified facecolor
            axs[i].fill_between(filtered_df.index, min_values, mean_values, facecolor=face_color, alpha=0.2)
            axs[i].fill_between(filtered_df.index, mean_values, max_values, facecolor=face_color, alpha=0.2)

            # Set subplot title and labels
            axs[i].set_title(label, loc='right')
            axs[i].set_ylabel('Normalize heat demand')
            axs[i].legend(loc='lower right')
          
            # Add grid lines to the current subplot
            axs[i].grid(color='k', linestyle='dotted', linewidth=1)

            # Set y-axis major locator and format
            axs[i].yaxis.set_major_locator(plt.FixedLocator(np.arange(0, 0.01, 0.002)))

    # Set the common x-axis label
    axs[-1].set_xlabel('Date')

    # Adjust spacing for suptitle
    #plt.subplots_adjust(top=0.3)  # Adjust the 'top' parameter as needed to create space

    # Set the super title
    plt.suptitle(f'Normalized data for modelled heat demand in Neighborhood during a year')

    # Adjust layout and display subplots
    plt.tight_layout()
    plt.show()

def create_plots_month(dataframes, start_date, end_date, labels):
    # Create empty lists to store minimum, mean, and maximum values for each DataFrame
    min_values = []
    mean_values = []
    max_values = []

    # Loop through each DataFrame and calculate the statistics
    for df in dataframes:
        # Process the DataFrame and drop columns containing only zeros
        df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
        df = df.loc[:, (df != 0).any(axis=0)]  # Drop columns with all zeros

        # Calculate min, max, and mean values for each row in the processed DataFrame
        monthly_min = df.min(axis=1)
        monthly_max = df.max(axis=1)
        monthly_mean = df.mean(axis=1)

        # Filter the DataFrames based on the date range
        filtered_min = monthly_min[start_date:end_date]
        filtered_max = monthly_max[start_date:end_date]
        filtered_mean = monthly_mean[start_date:end_date]

        # Append the statistics to the respective lists
        min_values.append(filtered_min)
        mean_values.append(filtered_mean)
        max_values.append(filtered_max)

    # Create subplots with 3 rows and 1 column
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Define titles
    titles = ['Minimum Values', 'Mean Values', 'Maximum Values']

    # Plot minimum values with labels
    for min_data, label in zip(min_values, labels):
        axes[0].plot(min_data.index, min_data, label=f'{label} Monthly Min')

    # Plot mean values with labels
    for mean_data, label in zip(mean_values, labels):
        axes[1].plot(mean_data.index, mean_data, label=f'{label} Monthly Mean')

    # Plot maximum values with labels
    for max_data, label in zip(max_values, labels):
        axes[2].plot(max_data.index, max_data, label=f'{label} Monthly Max')

    # Customize the plots and set titles with date range
    for ax, title in zip(axes, titles):
        ax.set_title(f'{title} normalized data for modelled heat demand per type of UEU in ({start_date} to {end_date})')
        ax.set_xlabel('Time (month)')
        ax.set_ylabel('Normalized data for modelled heat demand')
        ax.legend()
        ax.grid(True)

    # Set the date format for the x-axis
    date_format = mdates.DateFormatter('%Y-%m-%d')
    axes[-1].xaxis.set_major_formatter(date_format)

    # Adjust subplot spacing
    plt.tight_layout()

    # Display the plots
    plt.show()

def plot_elect_demand_hour(df, labels, target_dates):
    # Convert target dates to datetime objects (remove this line to use the provided target_dates)
    target_dates = pd.to_datetime(target_dates)

    # Process the DataFrame
    df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

    # Calculate min, max, and mean values for each row in the processed DataFrame
    hourly_min = df.min(axis=1)
    hourly_max = df.max(axis=1)
    hourly_mean = df.mean(axis=1)

    # Set the figure size here
    fig, axs = plt.subplots(1, 4, figsize=(25, 5), sharey=True)

    # Labels for the y-axes (one for each subplot)
    y_labels = ['Min', 'Mean', 'Max', 'Custom Label']  # Adjust the labels as needed

    # Loop through target dates and plot on subplots
    for i, target_date in enumerate(target_dates):
        start_time = target_date
        end_time = target_date + pd.DateOffset(hours=23)

        filtered_min = hourly_min[start_time:end_time]
        filtered_max = hourly_max[start_time:end_time]
        filtered_mean = hourly_mean[start_time:end_time]

        ax = axs[i]  # Get the current subplot

        # Plot min, mean, and max values on the current subplot
        ax.plot(filtered_min.index, filtered_min, label='Min', linewidth=0.5, color='red')
        ax.plot(filtered_mean.index, filtered_mean, label='Mean', linewidth=2, color='red')
        ax.plot(filtered_max.index, filtered_max, label='Max', linewidth=1, color='red')
        ax.fill_between(filtered_mean.index, filtered_min, filtered_mean, facecolor='C1', alpha=0.2)
        ax.fill_between(filtered_mean.index, filtered_mean, filtered_max, facecolor='C1', alpha=0.2)

        # Set x-axis limits
        ax.set_xlim(start_time, end_time)
        ax.yaxis.tick_left()

        # Customize subplot titles and legends using labels parameter
        ax.set_title(f'{labels} on {target_date.date()}')  # Use labels[i] for customization
        ax.set_xlabel(f'Time (h)')
        ax.set_ylabel(f'Normalized electricity energy demand')
 
    # Display the legend outside the loop
    axs[0].legend()

    # Display the subplots
    plt.suptitle(f'Normalized data for modelled electricity demand in Neighborhood {labels} during a day in Winter, Spring, Summer and Autumn')
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1)
    plt.show()

def plot_elect_demand_day(dataframes, start_date, end_date, labels):
    # Convert target dates to datetime objects (remove this line to use the provided target_dates)
    target_dates = pd.to_datetime(target_dates)

    # Process the DataFrame
    df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

    # Calculate min, max, and mean values for each row in the processed DataFrame
    hourly_min = df.min(axis=1)
    hourly_max = df.max(axis=1)
    hourly_mean = df.mean(axis=1)

    # Set the figure size here
    fig, axs = plt.subplots(1, 4, figsize=(25, 4), sharey=True)

    # Labels for the y-axes (one for each subplot)
    y_labels = ['Min', 'Mean', 'Max', 'Custom Label']  # Adjust the labels as needed

    # Loop through target dates and plot on subplots
    for i, target_date in enumerate(target_dates):
        start_time = target_date
        end_time = target_date + pd.DateOffset(hours=23)

        filtered_min = hourly_min[start_time:end_time]
        filtered_max = hourly_max[start_time:end_time]
        filtered_mean = hourly_mean[start_time:end_time]

        ax = axs[i]  # Get the current subplot

        # Plot min, mean, and max values on the current subplot
        ax.plot(filtered_min.index, filtered_min, label='Min', linewidth=0.5, color='red')
        ax.plot(filtered_mean.index, filtered_mean, label='Mean', linewidth=2, color='red')
        ax.plot(filtered_max.index, filtered_max, label='Max', linewidth=1, color='red')
        ax.fill_between(filtered_mean.index, filtered_min, filtered_mean, facecolor='C1', alpha=0.2)
        ax.fill_between(filtered_mean.index, filtered_mean, filtered_max, facecolor='C1', alpha=0.2)

        # Set x-axis limits
        ax.set_xlim(start_time, end_time)
        ax.yaxis.tick_left()

        # Customize subplot titles and legends using labels parameter
        ax.set_title(f'{labels} on {target_date.date()}')  # Use labels[i] for customization
        ax.set_xlabel(f'Time (h)')
        ax.set_ylabel(f'Normalized electricity energy demand')
 
    # Display the legend outside the loop
    axs[0].legend()

    # Display the subplots
    plt.suptitle(f'Normalized data for modelled electricity demand in Neighborhood {labels} during a Month in Winter, Spring, Summer and Autumn')
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1)
    plt.show()

# Define a function to create the plots for a DataFrame
def create_plots_day(df, df_name):
    # Process the DataFrame
    df_f = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')

    # Calculate min, max, and mean values for each row in the processed DataFrame
    hourly_min = df_f.min(axis=1)
    hourly_max = df_f.max(axis=1)
    hourly_mean = df_f.mean(axis=1)

    # List of target dates
    target_dates = ['2100-01-15', '2100-04-15', '2100-07-15', '2100-10-15']

    # Create subplots with 2 rows and 2 columns
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))

    # Flatten the 2x2 axes array to make it easier to work with
    axes = axes.flatten()

    # Loop through target dates and plot on subplots
    for i, target_date in enumerate(target_dates):
        start_time = target_date + ' 00:00:00'
        end_time = target_date + ' 23:00:00'

        filtered_min = hourly_min[start_time:end_time]
        filtered_max = hourly_max[start_time:end_time]
        filtered_mean = hourly_mean[start_time:end_time]
      
        # Plot on the current subplot
        ax = axes[i]
        ax.plot(filtered_min.index, filtered_min, label='Min', linewidth=2, color='blue')
        ax.plot(filtered_max.index, filtered_max, label='Max', linewidth=2, color='red')
        ax.plot(filtered_mean.index, filtered_mean, label='Mean', linewidth=2, color='green')
        ax.fill_between(filtered_mean.index, filtered_min, filtered_mean, facecolor='C0', alpha=0.4)
        ax.fill_between(filtered_mean.index, filtered_mean, filtered_max, facecolor='C1', alpha=0.4)

        # Customize subplot titles, labels, and legends
        ax.set_title(f'Normalized data for modelled heat demand in Neighborhoud {df_name} on {target_date}')
        ax.set_xlabel('Time (h)')
        ax.set_ylabel('Normalized data for modelled heat demand')
        ax.legend()
        ax.grid()

    # Adjust layout and display the subplots
    plt.tight_layout()
    plt.show()

def create_plots_h(dataframes, start_date, end_date, labels):
    # Create empty lists to store minimum, mean, and maximum values for each DataFrame
    min_values = []
    mean_values = []
    max_values = []

    # Loop through each DataFrame and calculate the statistics
    for df in dataframes:
        # Process the DataFrame and drop columns containing only zeros
        df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
        df = df.loc[:, (df != 0).any(axis=0)]  # Drop columns with all zeros

        # Calculate min, max, and mean values for each row in the processed DataFrame
        daily_min = df.min(axis=1)
        daily_max = df.max(axis=1)
        daily_mean = df.mean(axis=1)

        # Filter the DataFrames based on the date range
        filtered_min = daily_min[start_date:end_date]
        filtered_max = daily_max[start_date:end_date]
        filtered_mean = daily_mean[start_date:end_date]

        # Append the statistics to the respective lists
        min_values.append(filtered_min)
        mean_values.append(filtered_mean)
        max_values.append(filtered_max)

    # Create subplots with 3 rows and 1 column
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Define titles
    titles = ['Minimum Values', 'Mean Values', 'Maximum Values']

    # Plot minimum values with labels
    for min_data, label in zip(min_values, labels):
        axes[0].plot(min_data.index, min_data, label=f'{label} Daily Min')

    # Plot mean values with labels
    for mean_data, label in zip(mean_values, labels):
        axes[1].plot(mean_data.index, mean_data, label=f'{label} Daily Mean')

    # Plot maximum values with labels
    for max_data, label in zip(max_values, labels):
        axes[2].plot(max_data.index, max_data, label=f'{label} Daily Max')

    # Customize the plots and set titles with date range
    for ax, title in zip(axes, titles):
        ax.set_title(f'{title} normalized data for modelled heat demand per type of UEU in ({start_date} to {end_date})')
        ax.set_xlabel('Time(h)')
        ax.set_ylabel('Normalized data for modelled heat demand')
        ax.legend()
        ax.grid(True)

    # Set the date format for the x-axis
    date_format = mdates.DateFormatter('%Y-%m-%d')
    axes[-1].xaxis.set_major_formatter(date_format)

    # Adjust subplot spacing
    plt.tight_layout()

    # Display the plots
    plt.show()

def create_plots_week_heat(dataframes, labels, date_ranges):
    # Convert date strings to datetime objects
    date_ranges = [(pd.to_datetime(start), pd.to_datetime(end)) for start, end in date_ranges]

    # Set the figure size here
    fig, axs = plt.subplots(1, len(date_ranges), figsize=(28, 5), sharey=True)

    # Labels for the y-axes (one for each subplot)
    y_labels = ['Min', 'Mean', 'Max']  # Adjust the labels as needed

    for i, (start_date, end_date) in enumerate(date_ranges):
        # Filter the DataFrame based on the date range
        df_filtered = dataframes[start_date:end_date]

        # Calculate min, max, and mean values for each row in the processed DataFrame
        daily_min = df_filtered.min(axis=1)
        daily_max = df_filtered.max(axis=1)
        daily_mean = df_filtered.mean(axis=1)

        ax = axs[i]  # Get the current subplot

        # Plot min, mean, and max values on the current subplot
        ax.plot(daily_min.index, daily_min, label='Min', linewidth=0.5, color='red')
        ax.plot(daily_mean.index, daily_mean, label='Mean', linewidth=2, color='red')
        ax.plot(daily_max.index, daily_max, label='Max', linewidth=1, color='red')
        ax.fill_between(daily_mean.index, daily_min, daily_mean, facecolor='C1', alpha=0.2)
        ax.fill_between(daily_mean.index, daily_mean, daily_max, facecolor='C1', alpha=0.2)

        # Set x-axis limits
        ax.set_xlim(start_date, end_date)
        ax.yaxis.tick_left()

        # Customize subplot titles and legends using labels parameter
        ax.set_title(f'{labels} on {start_date.date()} to {end_date.date()}')
        ax.set_xlabel(f'Time (h)')
        ax.set_ylabel(f'Normalized heat energy demand')

        # Display the legend inside the loop for each subplot
        ax.legend()

    # Display the subplots
    plt.suptitle(f'Normalized data for modelled heat demand in Neighborhood {labels}')
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1)
    plt.show()

def create_plots_week_elect(dataframes, labels, date_ranges):
    # Convert date strings to datetime objects
    date_ranges = [(pd.to_datetime(start), pd.to_datetime(end)) for start, end in date_ranges]

    # Set the figure size here
    fig, axs = plt.subplots(1, len(date_ranges), figsize=(28, 5), sharey=True)

    # Labels for the y-axes (one for each subplot)
    y_labels = ['Min', 'Mean', 'Max']  # Adjust the labels as needed

    for i, (start_date, end_date) in enumerate(date_ranges):
        # Filter the DataFrame based on the date range
        df_filtered = dataframes[start_date:end_date]

        # Calculate min, max, and mean values for each row in the processed DataFrame
        daily_min = df_filtered.min(axis=1)
        daily_max = df_filtered.max(axis=1)
        daily_mean = df_filtered.mean(axis=1)

        ax = axs[i]  # Get the current subplot

        # Plot min, mean, and max values on the current subplot
        ax.plot(daily_min.index, daily_min, label='Min', linewidth=0.5, color='red')
        ax.plot(daily_mean.index, daily_mean, label='Mean', linewidth=2, color='red')
        ax.plot(daily_max.index, daily_max, label='Max', linewidth=1, color='red')
        ax.fill_between(daily_mean.index, daily_min, daily_mean, facecolor='C1', alpha=0.2)
        ax.fill_between(daily_mean.index, daily_mean, daily_max, facecolor='C1', alpha=0.2)

        # Set x-axis limits
        ax.set_xlim(start_date, end_date)
        ax.yaxis.tick_left()

        # Customize subplot titles and legends using labels parameter
        ax.set_title(f'{labels} on {start_date.date()} to {end_date.date()}')
        ax.set_xlabel(f'Time (h)')
        ax.set_ylabel(f'Normalized electricity energy demand')

        # Display the legend inside the loop for each subplot
        ax.legend()

    # Display the subplots
    plt.suptitle(f'Normalized data for modelled electricity demand in Neighborhood {labels}')
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.1)
    plt.show()

def plot_electricity_demand_monthly(data_frames, labels, start_date, end_date):

    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

    # Check if the number of DataFrames and labels match
    if len(data_frames) != len(labels):
        raise ValueError("The number of DataFrames and labels must match.")

    # Create 8 separate subplots
    fig, axs = plt.subplots(8, 1, figsize=(15, 25), sharex=False)

    # Loop through DataFrames and labels
    for i, (df, label) in enumerate(zip(data_frames, labels)):
        # Check if the DataFrame has a valid index
        if not df.index.empty:
            # Filter the DataFrame based on the date range
            filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]

            # Calculate min, mean, and max values
            min_values = filtered_df.min(axis=1)
            mean_values = filtered_df.mean(axis=1)
            max_values = filtered_df.max(axis=1)

            # Plot min, mean, and max values on the current subplot
            axs[i].plot(filtered_df.index, min_values, label='Min', linewidth=0.5, color='red')
            axs[i].plot(filtered_df.index, mean_values, label='Mean', linewidth=2, color='red')
            axs[i].plot(filtered_df.index, max_values, label='Max', linewidth=0.5, color='red')

            # Add shadows between min and mean, and between mean and max
            axs[i].fill_between(filtered_df.index, min_values, mean_values, facecolor='red', alpha=0.2)
            axs[i].fill_between(filtered_df.index, mean_values, max_values, facecolor='red', alpha=0.2)

            # Set subplot title and labels
            axs[i].set_title(label)
            axs[i].set_ylabel('Heat Demand')
            axs[i].legend()

            # Add x and y axis lines
            axs[i].axhline(0, color='black', linewidth=0.5)
            axs[i].axvline(start_date, color='black', linewidth=0.5)

    # Set the common x-axis label
    axs[-1].set_xlabel('Date')

    # Adjust spacing for suptitle
    plt.subplots_adjust(top=0.2)  # Adjust the 'top' parameter as needed to create space

    # Set the super title
    plt.suptitle(f'Normalized data for modelled electricity demand in Neighborhood during a year')

    # Adjust layout and display subplots
    plt.tight_layout()
    plt.show()

def create_plots_el_week(dataframes, start_date, end_date, labels):
    # Create empty lists to store minimum, mean, and maximum values for each DataFrame
    min_values = []
    mean_values = []
    max_values = []

    # Loop through each DataFrame and calculate the statistics
    for df in dataframes:
        # Process the DataFrame and drop columns containing only zeros
        df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
        df = df.loc[:, (df != 0).any(axis=0)]  # Drop columns with all zeros

        # Calculate min, max, and mean values for each row in the processed DataFrame
        daily_min = df.min(axis=1)
        daily_max = df.max(axis=1)
        daily_mean = df.mean(axis=1)

        # Filter the DataFrames based on the date range
        filtered_min = daily_min[start_date:end_date]
        filtered_max = daily_max[start_date:end_date]
        filtered_mean = daily_mean[start_date:end_date]

        # Append the statistics to the respective lists
        min_values.append(filtered_min)
        mean_values.append(filtered_mean)
        max_values.append(filtered_max)

    # Create subplots with 3 rows and 1 column
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Define titles
    titles = ['Minimum Values', 'Mean Values', 'Maximum Values']

    # Plot minimum values with labels
    for min_data, label in zip(min_values, labels):
        axes[0].plot(min_data.index, min_data, label=f'{label} Daily Min')

    # Plot mean values with labels
    for mean_data, label in zip(mean_values, labels):
        axes[1].plot(mean_data.index, mean_data, label=f'{label} Daily Mean')

    # Plot maximum values with labels
    for max_data, label in zip(max_values, labels):
        axes[2].plot(max_data.index, max_data, label=f'{label} Daily Max')

    # Customize the plots and set titles with date range
    for ax, title in zip(axes, titles):
        ax.set_title(f'{title} normalized data for modelled electricity demand per type of UEU in ({start_date} to {end_date})')
        ax.set_xlabel('Time(day)')
        ax.set_ylabel('Normalized data for modelled electricity demand')
        ax.legend()
        ax.grid(True)

    # Set the date format for the x-axis
    date_format = mdates.DateFormatter('%Y-%m-%d')
    axes[-1].xaxis.set_major_formatter(date_format)

    # Adjust subplot spacing
    plt.tight_layout()

    # Display the plots
    plt.show()

def create_plots_el_month(dataframes, start_date, end_date, labels):
    # Create empty lists to store minimum, mean, and maximum values for each DataFrame
    min_values = []
    mean_values = []
    max_values = []

    # Loop through each DataFrame and calculate the statistics
    for df in dataframes:
        # Process the DataFrame and drop columns containing only zeros
        df = df.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
        df = df.loc[:, (df != 0).any(axis=0)]  # Drop columns with all zeros

        # Calculate min, max, and mean values for each row in the processed DataFrame
        monthly_min = df.min(axis=1)
        monthly_max = df.max(axis=1)
        monthly_mean = df.mean(axis=1)

        # Filter the DataFrames based on the date range
        filtered_min = monthly_min[start_date:end_date]
        filtered_max = monthly_max[start_date:end_date]
        filtered_mean = monthly_mean[start_date:end_date]

        # Append the statistics to the respective lists
        min_values.append(filtered_min)
        mean_values.append(filtered_mean)
        max_values.append(filtered_max)

    # Create subplots with 3 rows and 1 column
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Define titles
    titles = ['Minimum Values', 'Mean Values', 'Maximum Values']

    # Plot minimum values with labels
    for min_data, label in zip(min_values, labels):
        axes[0].plot(min_data.index, min_data, label=f'{label} Monthly Min')

    # Plot mean values with labels
    for mean_data, label in zip(mean_values, labels):
        axes[1].plot(mean_data.index, mean_data, label=f'{label} Monthly Mean')

    # Plot maximum values with labels
    for max_data, label in zip(max_values, labels):
        axes[2].plot(max_data.index, max_data, label=f'{label} Monthly Max')

    # Customize the plots and set titles with date range
    for ax, title in zip(axes, titles):
        ax.set_title(f'{title} normalized data for modelled electricity demand per type of UEU in ({start_date} to {end_date})')
        ax.set_xlabel('Time (month)')
        ax.set_ylabel('Normalized data for modelled electricity demand')
        ax.legend()
        ax.grid(True)

    # Set the date format for the x-axis
    date_format = mdates.DateFormatter('%Y-%m-%d')
    axes[-1].xaxis.set_major_formatter(date_format)

    # Adjust subplot spacing
    plt.tight_layout()

    # Display the plots
    plt.show()