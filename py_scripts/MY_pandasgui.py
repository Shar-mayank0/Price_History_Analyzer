import pandas as pd
import json
from scipy import stats
import numpy as np
import sys
import os
from pandasgui import show
import tkinter as tk
from tkinter import filedialog



def datafrm_setup(data):
            dates = data.get('dates')
            prices = data.get('prices')

            # Create a DataFrame with the dates and prices
            df = pd.DataFrame({
                'dates': pd.to_datetime(dates, format="%d %b %Y"),
                'prices': prices
            })

            # Set the dates as the index of the DataFrame
            df.set_index('dates', inplace=True)

            # Resample the data to 1-month, 2-month, 3-month intervals and calculate the mode for each interval
            M1modedf = df.resample('ME').apply(lambda x: stats.mode(x)[0])
            M2modedf = df.resample('2ME').apply(lambda x: stats.mode(x)[0])
            M3modedf = df.resample('3ME').apply(lambda x: stats.mode(x)[0])

            # Reset the index of modedf to prepare for merging
            M1modedf = M1modedf.reset_index()
            M2modedf = M2modedf.reset_index()
            M3modedf = M3modedf.reset_index()

            # Rename the columns of modedf to avoid conflicts during merge
            M1modedf.columns = ['dates', 'Regular']
            M2modedf.columns = ['dates', 'Long_regular']
            M3modedf.columns = ['dates', 'Actual_price']

            # Merge df and modedf
            df = pd.merge(df, M1modedf, on='dates', how='left')
            df = pd.merge(df, M2modedf, on='dates', how='left')
            df = pd.merge(df, M3modedf, on='dates', how='left')

            # Fill NaN values with forward fill
            df.loc[:, 'Regular'] = df['Regular'].ffill()
            df.loc[:, 'Long_regular'] = df['Long_regular'].ffill()
            df.loc[:, 'Actual_price'] = df['Actual_price'].ffill()

            # Calculate max discount%
            df['max_discount%'] = (df['prices'].max() - df['prices']) / df['prices'].max() * 100

            # Calculate actual discount%
            df['actual_discount%'] = (df['Actual_price'] - df['prices']) / df['Actual_price'] * 100

            # Calculate discount discrepancy
            df['discount_discrepancy'] = df['max_discount%'] - df['actual_discount%']

            # Calculate moving average
            window_size = 30
            df['moving_average'] = df['prices'].rolling(window=window_size).mean()

            # Calculate abnormal price spikes
            threshold = 2 * df['prices'].std()
            df['abnormal_price_spikes'] = (df['prices'] - df['moving_average']) > threshold

            # Calculate price volatility for 1M, 2M, 3M, and all time
            df['price_volatility_1M'] = df['prices'].rolling(window=30).std()
            df['price_volatility_2M'] = df['prices'].rolling(window=60).std()
            df['price_volatility_3M'] = df['prices'].rolling(window=90).std()
            df['price_volatility_all_time'] = df['prices'].std()

            # Calculate threshold for 1M, 2M, 3M
            df['threshold_1M'] = 2 * df['price_volatility_1M']
            df['threshold_2M'] = 2 * df['price_volatility_2M']
            df['threshold_3M'] = 2 * df['price_volatility_3M']

            print(df)
            return df


def file_selector():
    directory = "py_scripts\\training data"

    # Get all files in the directory
    files_in_directory = os.listdir(directory)

    # Filter out files that are not json
    json_files = [file for file in files_in_directory if file.endswith(".json")]

    # Create a Tkinter window
    root = tk.Tk()

    # Create a StringVar to store the selected file
    selected_file = tk.StringVar(root)

    # Create an OptionMenu with the json_files as options
    option_menu = tk.OptionMenu(root, selected_file, *json_files)
    option_menu.pack()

    def select_file():
        # Get the selected file
        file = selected_file.get()

        # Open the selected file
        with open(os.path.join(directory, file), 'r') as f:
            data = json.load(f)
            df = datafrm_setup(data)
            show(pd.DataFrame(df))
            

    # Create a button to select the file
    select_button = tk.Button(root, text="Select File", command=select_file)
    select_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

file_selector()