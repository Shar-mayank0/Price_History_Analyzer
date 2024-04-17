import pandas as pd
import json
from scipy import stats
import numpy as np
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as plt



directory = f"py_scripts\\training data"

# Get all files in the directory
files_in_directory = os.listdir(directory)

# Filter out files that are not json
json_files = [file for file in files_in_directory if file.endswith(".json")]

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'App'
        self.left = 10
        self.top = 10
        self.width: int =  800
        self.height: int = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create a QWidget as the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a QVBoxLayout for the central widget
        self.layout = lambda: QVBoxLayout(self.central_widget)

        # Create a Figure and a FigureCanvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout().addWidget(self.canvas)

        # Create dropdown menus
        self.dropdown_files = QComboBox(self)
        self.dropdown_files.addItems(json_files)  # Assuming json_files is a list of file names
        self.layout.addWidget(self.dropdown_files)

        self.dropdown_mode_prices = QComboBox(self)
        self.dropdown_mode_prices.addItems(['1 month mode', '2 months mode', '3 months mode'])
        self.layout.addWidget(self.dropdown_mode_prices)

        self.dropdown_discounts = QComboBox(self)
        self.dropdown_discounts.addItems(['Actual discount', 'Discount from max price', 'Discount discrepancy'])
        self.layout.addWidget(self.dropdown_discounts)

        # Create buttons
        self.button_moving_average = QPushButton('Add Moving Average', self)
        self.layout.addWidget(self.button_moving_average)

        self.button_price_volatility = QPushButton('Add Price Volatility', self)
        self.layout.addWidget(self.button_price_volatility)

        self.button_abnormal_price_spikes = QPushButton('Add Abnormal Price Spikes', self)
        self.layout.addWidget(self.button_abnormal_price_spikes)

        self.button_clear_all = QPushButton('Clear All', self)
        self.layout.addWidget(self.button_clear_all)
        self.data = None

        def datafrm_setup(self, data):
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

            return df
        
        selected_file = self.dropdown_files.currentText()
        file_path = os.path.join(directory, selected_file)
        with open(file_path, 'r') as file:
            self.data = json.load(file)

        # Connect dropdown menus and buttons to functions
        self.dropdown_files.currentIndexChanged.connect(self.update_plot)
        self.dropdown_mode_prices.currentIndexChanged.connect(self.update_plot)
        self.dropdown_discounts.currentIndexChanged.connect(self.update_plot)

        self.button_moving_average.clicked.connect(self.add_moving_average)
        self.button_price_volatility.clicked.connect(self.add_price_volatility)
        self.button_abnormal_price_spikes.clicked.connect(self.add_abnormal_price_spikes)
        self.button_clear_all.clicked.connect(lambda: self.clear_all(self.datafrm_setup(self.data)))

    def update_plot(self):
        # Update the plot with the selected feature overlay
        selected_file = self.dropdown_files.currentText()
        selected_mode = self.dropdown_mode_prices.currentText()
        selected_discount = self.dropdown_discounts.currentText()

        # Get the data for the selected file
        file_path = os.path.join(directory, selected_file)
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Set up the DataFrame
        df = self.datafrm_setup(data)  # Modified line

        # Clear the plot
        self.figure.clear()

        # Plot the price history
        ax = self.figure.add_subplot(111)
        ax.plot(df.index, df['prices'], label='Price History')

        # Add the selected feature overlay
        if selected_mode == '1 month mode':
            ax.plot(df.index, df['Regular'], label='1 Month Mode')
            ax.plot(df.index, df['prices'], label='Prices')
        elif selected_mode == '2 months mode':
            ax.plot(df.index, df['Long_regular'], label='2 Months Mode')
            ax.plot(df.index, df['prices'], label='Prices')
        elif selected_mode == '3 months mode':
            ax.plot(df.index, df['Actual_price'], label='3 Months Mode')
            ax.plot(df.index, df['prices'], label='Prices')

        # Add the selected discount overlay
        if selected_discount == 'Actual discount':
            ax.plot(df.index, df['actual_discount'], label='Actual Discount')
            ax.plot(df.index, df['prices'], label='Prices')
        elif selected_discount == 'Discount from max price':
            ax.plot(df.index, df['prices'].max() - df['prices'], label='Discount from Max Price')
            ax.plot(df.index, df['prices'], label='Prices')
        elif selected_discount == 'Discount discrepancy':
            ax.plot(df.index, df['discount_discrepancy'], label='Discount Discrepancy')
            ax.plot(df.index, df['prices'], label='Prices')

        # Set the legend and show the plot
        ax.legend()
        self.canvas.draw()

    def clear_all(self, df):
        # Reset the plot to the price history graph
        ax = self.figure.gca()
        ax.clear()
        ax.plot(df.index, df['prices'], label='Price History')
        ax.legend()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())