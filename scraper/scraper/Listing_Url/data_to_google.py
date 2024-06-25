import pandas as pd
import sys
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
PROPERTIES_SHEET_NAME = 'Properties'
LISTINGS_SHEET_NAME = 'Listings'

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

# Determine which sheet to update
sheet_to_update = sys.argv[1] if len(sys.argv) > 1 else "properties"

def update_properties_sheet(data):
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
        range=f"{PROPERTIES_SHEET_NAME}!A2",
        valueInputOption="RAW",
        body={"values": df.values.tolist()}
    ).execute()

def update_listings_sheet(data):
    # Create DataFrame from JSON data
    df = pd.DataFrame(data)

    # Select only the required columns
    df = df[['host_name', 'address']]

    # Write new data to the "Listings" sheet starting from row 2
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f"{LISTINGS_SHEET_NAME}!A2",
        valueInputOption="RAW",
        body={"values": df.values.tolist()}
    ).execute()

if sheet_to_update.lower() == "properties":
    update_properties_sheet(data)
elif sheet_to_update.lower() == "listings":
    update_listings_sheet(data)
else:
    print("Invalid argument. Use 'properties' or 'listings'.")

print(f"Data has been successfully written to the {sheet_to_update.capitalize()} sheet")
