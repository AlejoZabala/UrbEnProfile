import datetime as dt
import pandas as pd
import os
from scripts.global_variables import * # database_path, root_path, input_path, output_path

def typical_meteorological_year(filepath: str, datetime_index) -> pd.DataFrame:

    # Load data from Excel file
    tmy_data = pd.read_excel(filepath)
    
    # Remove metadata and header rows, and reset the index
    tmy_data = tmy_data.iloc[12:].reset_index(drop=True)
    tmy_data.columns = tmy_data.iloc[0]
    tmy_data.drop([0, 1], inplace=True)

    # Convert data types and return DataFrame
    data_dict = {'temp_amb':tmy_data['Tamb'].astype(float).values + 273.15, 'wind_speed': tmy_data['WindVel'].astype(float).values}
    df = pd.DataFrame(data = data_dict, index=datetime_index)
    return df
