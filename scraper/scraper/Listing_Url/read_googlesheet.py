import pandas as pd
import sys
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Google Sheets setup
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
JobTable = 'JobTable'

searchjobtable_file_path = 'scraper/scraper/Listing_Url/json_file/final_rental_link.json'

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=JobTable).execute()
values = result.get('values', [])

# Convert Google Sheets data to DataFrame
df = pd.DataFrame(values[1:], columns=values[0])

# Debugging: print out the column names to verify
print("Column names in DataFrame:", df.columns.tolist())

# Ensure column names are correct
expected_columns = ['JobID', 'InfoID', 'StartDate', 'EndDate', 'URL','Status']
missing_columns = [col for col in expected_columns if col not in df.columns]

if missing_columns:
    print(f"Missing columns in DataFrame: {missing_columns}")
    sys.exit(1)

# Generate JSON format
data = {}
batch_size = 6
batch_number = 1

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    batch_key = f"Batch{batch_number}"
    data[batch_key] = []
    for _, row in batch.iterrows():
        data[batch_key].append({
            "listing_link_format": row['URL'],
            "JobID": row['JobID'],
            "InfoID": row['InfoID']
        })
    batch_number += 1

# Save JSON to file
with open(searchjobtable_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON data saved to {searchjobtable_file_path}")