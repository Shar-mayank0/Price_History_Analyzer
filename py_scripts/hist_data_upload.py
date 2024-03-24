from web_page_info_collect_Parser import server_price_history as server 
import json
import os

directory = f"public\\temp\\price_hist_data"

# Get all files in the directory
files_in_directory = os.listdir(directory)

# Filter out files that are not json
json_files = [file for file in files_in_directory if file.endswith(".json")]

print(json_files)

for i in json_files:
    server().post_data(jsonfile=i)
