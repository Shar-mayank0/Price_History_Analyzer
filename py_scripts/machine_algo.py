import pandas as pd
import numpy as np
import os
import json
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score, f1_score
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import filedialog
from joblib import Parallel, delayed
# Function to setup DataFrame and engineer features
def datafrm_setup(dates, prices):
    # Create a DataFrame with the dates and prices
    df = pd.DataFrame({
        'dates': pd.to_datetime(dates),
        'prices': prices
    })

    # Set the dates as the index of the DataFrame
    df.set_index('dates', inplace=True)

    # Resample the data to 1-month, 2-month, 3-month intervals and calculate the mode for each interval
    M1modedf = df.resample('M').apply(lambda x: stats.mode(x)[0])
    M2modedf = df.resample('2M').apply(lambda x: stats.mode(x)[0])
    M3modedf = df.resample('3M').apply(lambda x: stats.mode(x)[0])

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

    # Forward fill missing values
    df['Regular'].fillna(method='ffill', inplace=True) # type: ignore
    df['Long_regular'].fillna(method='ffill', inplace=True) # type: ignore
    df['Actual_price'].fillna(method='ffill', inplace=True) # type: ignore

    # Calculate the discount from the mode value for each price
    df['actual_discount'] = (df['Actual_price'] - df['prices']) / df['Actual_price'] * 100

    # Drop rows with any remaining missing values
    df.dropna(inplace=True)

    # maximum price
    max_price_all_time = df['Actual_price'].max()

    # Calculate the discount from the maximum price for each price
    df['discount_from_max_price'] = (max_price_all_time - df['prices']) / max_price_all_time * 100

    # Feature Engineering

    # Discount Discrepancy
    df['discount_discrepancy'] = df['discount_from_max_price'] - df['actual_discount']

    # Price Volatility
    price_volatility = df['prices'].std()  # Compute standard deviation as a measure of volatility

    # Price Trends
    # Calculate a simple moving average of prices over a specific window size
    window_size = 30
    df['price_moving_average'] = df['prices'].rolling(window=window_size).mean()

    # Abnormal Price Spikes
    # Define a threshold for abnormal price spikes based on historical data
    threshold = 2 * price_volatility  # For example, two times the standard deviation
    df['abnormal_price_spike'] = (df['prices'] - df['price_moving_average']) > threshold

    df['price_change_freq'] = df['prices'].diff().ne(0).rolling(window=30).sum()
    df['price_variance'] = df['prices'].rolling(window=30).std()
    df['price_reversions'] = df['prices'].diff().abs().rolling(window=30).sum() / df['prices']


    return df

# Path to JSON files
json_files_path = 'py_scripts\\training data'

# List to store DataFrames
dataframes = []

# Read all JSON files
for file_name in os.listdir(json_files_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(json_files_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
            dates = data.get('dates')
            prices = data.get('prices')
            df = datafrm_setup(dates, prices)
            df['product_id'] = file_name.split('.')[0]  # Add product ID to the DataFrame
            dataframes.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dataframes)

# Extract relevant features for clustering
features = combined_df[['prices', 'actual_discount', 'discount_discrepancy', 'price_moving_average', 'abnormal_price_spike', 'price_change_freq', 'price_variance', 'price_reversions']].fillna(0).values

# Normalize the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
best_eps = 0.01
best_min_samples = 1
best_score = -1

# Apply DBSCAN for anomaly detection and clustering and find the best hyperparameters
# def find_best_dbscan(eps, min_samples):
#     eps = eps / 100
#     db = DBSCAN(eps=eps, min_samples=min_samples).fit(features_scaled)
#     if len(set(db.labels_)) > 1:  # Ensure there is more than one cluster
#         score = silhouette_score(features_scaled, db.labels_)
#         return eps, min_samples, score

# results = Parallel(n_jobs=6, backend='threading')(delayed(find_best_dbscan)(eps, min_samples) for eps in range(1, 100, 1) for min_samples in range(1, 10, 1))
# # Filter out None values from results
# filtered_results = [result for result in results if result is not None]

# # Ensure filtered_results is not empty to avoid ValueError from max()
# if filtered_results:
#     # Find the tuple with the maximum score
#     best_tuple = max(filtered_results, key=lambda x: x[2])

#     # Extract the best eps and min_samples values
#     best_eps = best_tuple[0] * 100  # Multiplying by 100 to revert the earlier division
#     best_min_samples = best_tuple[1]

#     print(f'Best DBSCAN eps: {best_eps}, min_samples: {best_min_samples}, Silhouette Score: {best_tuple[2]}')
# else:
#     print("No suitable parameters found for DBSCAN.")
# print(f'Best DBSCAN eps: {best_eps}, min_samples: {best_min_samples}, Silhouette Score: {best_score}')



db = DBSCAN(eps=0.25, min_samples=4).fit(features_scaled)
combined_df['cluster'] = db.labels_
combined_df['anomaly_dbscan'] = combined_df['cluster'] == -1


# dropped isolation forest algo due to high complexity n non understandable results


# best_contamination = 0.01
# best_score = -1

# for contamination in range(1, 100, 1):
#     contamination = contamination / 100
#     iso_forest = IsolationForest(contamination=contamination, random_state=42)
#     iso_forest.fit(features_scaled)
#     scores = iso_forest.decision_function(features_scaled)
#     threshold = np.percentile(scores, 100 * contamination)
#     anomalies = scores < threshold
#     score = f1_score(combined_df['anomaly_dbscan'], anomalies)
#     if score > best_score:
#         best_score = score
#         best_contamination = contamination

# iso_forest = IsolationForest(contamination=best_contamination, random_state=42)
# combined_df['anomaly_iso_forest'] = iso_forest.fit_predict(features_scaled) == -1

# print(f'Best Isolation Forest contamination: {best_contamination}, F1 Score: {best_score}')

# combined_df['anomaly'] = combined_df['anomaly_dbscan'] | combined_df['anomaly_iso_forest']

# # Visualizing Anomalies Detected by Isolation Forest
# plt.figure(figsize=(15, 8))
# for product_id, product_df in combined_df.groupby('product_id'):
#     plt.figure(figsize=(15, 8))  # Create a new figure for each product
#     plt.plot(product_df.index, product_df['prices'], label=f'Price - {product_id}')
#     plt.scatter(product_df.index[product_df['anomaly_iso_forest']], product_df['prices'][product_df['anomaly_iso_forest']], label=f'Isolation Forest Anomaly - {product_id}')
#     plt.legend()
#     plt.title(f'Price History with Isolation Forest Anomalies - {product_id}')
#     plt.show()
# plt.legend()
# plt.title('Price History with Isolation Forest Anomalies')
# plt.show()


# Visualizing Anomalies Detected by DBSCAN
plt.figure(figsize=(15, 8))
for product_id, product_df in combined_df.groupby('product_id'):

    plt.figure(figsize=(15, 8))  # Create a new figure for each product
    plt.plot(product_df.index, product_df['prices'], label=f'Price - {product_id}')
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.scatter(product_df.index[product_df['anomaly_dbscan']], product_df['prices'][product_df['anomaly_dbscan']], label=f'DBSCAN Anomaly - {product_id}')
    plt.legend()
    plt.title(f'Price History with DBSCAN Anomalies - {product_id}')
    # Save the figure as a JPEG image
    plt.savefig(f'results/res_dbscan_{product_id}.jpeg')
    plt.close()
    

