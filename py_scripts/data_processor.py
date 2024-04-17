import json
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from web_page_info_collect_Parser import WebPageInfoCollectAndParser
from web_page_info_collect_Parser import flipkart_prod_list
from web_page_info_collect_Parser import amazon_prod_list

def prod_id(): 
    for entry in flipkart_prod_list:
        filename = entry
        yield filename
    print("filename is ")
    print(filename)

prod_id_inst = prod_id()
# Read the JSON file
data = json.load(open(f"C:\\Users\\Mayank Sharma\\Desktop\\VSlab\\dark_pattern_buster\\json\\trainer_data\\{prod_id_inst}.json", "r"))
#
# Extract the dates and prices from the JSON data
dates = data.get('dates')
prices = data.get('prices')

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
df['Regular'].fillna('ffill', inplace=True)
df['Long_regular'].fillna('ffill', inplace=True)
df['Actual_price'].fillna('ffill', inplace=True)

# Calculate the discount from the mode value for each price
df['actual_discount'] = (df['Actual_price'] - df['prices']) / df['Actual_price'] * 100

df = df.dropna()

print(df)

# Feature Engineering
# Discount Discrepancy
df['discount_discrepancy'] = (df['Actual_price'] - df['prices']) / df['Actual_price']

# Price Volatility
price_volatility = df['prices'].std()  # Compute standard deviation as a measure of volatility

# Price Trends
# For simplicity, let's calculate a simple moving average of prices over a specific window size
window_size = 30
df['price_moving_average'] = df['prices'].rolling(window=window_size).mean()

# Abnormal Price Spikes
# Define a threshold for abnormal price spikes based on historical data
threshold = 2 * price_volatility  # For example, two times the standard deviation
df['abnormal_price_spike'] = (df['prices'] - df['price_moving_average']) > threshold

# Scaling the Features (if necessary)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['discount_discrepancy', 'price_volatility']])

# Now, 'scaled_features' contains the scaled values of the selected features

# You can further proceed with model selection, training, and evaluation using the preprocessed data and engineered features.

# Create a figure and a set of subplots
fig, axs = plt.subplots(6, sharex=True, figsize=(10, 15))

# Plot the original prices and mode prices on the first y-axis
axs[0].plot(df['dates'], df['prices'], label='Price')
axs[1].plot(df['dates'], df['Actual_price'], label='Actual_price')
axs[2].plot(df['dates'], df['Long_regular'], label='Long_regula')
axs[3].plot(df['dates'], df['Regular'], label='Regular')

# Plot the discount on the second y-axis
axs[4].plot(df['dates'], df['actual_discount'], label='Discount', linestyle='--', color='red')

# Draw a horizontal line at 0% discount
axs[4].axhline(0, color='green', linestyle='--')

# Draw a horizontal line at maximum discount
max_discount = df['actual_discount'].max()
axs[5].axhline(max_discount, color='blue', linestyle='--')

# Set labels and titles
for i, label in enumerate(['Price', 'Actual_price', 'Long_regular', 'Regular', 'Discount', 'Max Discount']):
    axs[i].set_ylabel(label)
    axs[i].legend()
    axs[i].grid(True)

plt.xlabel('Date')
plt.suptitle('Price History')
plt.tight_layout()
plt.show()