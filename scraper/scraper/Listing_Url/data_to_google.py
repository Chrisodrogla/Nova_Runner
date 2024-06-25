import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import json

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
SHEET_NAME1 = 'Properties'  # Sheet to clear data below header and write new data

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# File path
json_file_path = 'scraper/scraper/Listing_Url/json_file/listing_attribute.json'

# Read JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Create DataFrame from JSON data
df = pd.DataFrame(data)

# Reorganize DataFrame columns
columns = [
    'property_id', 'description', 'host_name', 'bedrooms',
    'baths', 'guest', 'City', 'State', 'Country',
    'listing_id', 'airbnb_link'
]
df = df[columns]

# Write new data to the "Properties" sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()

print("Data has been successfully written to the Google Sheet")
