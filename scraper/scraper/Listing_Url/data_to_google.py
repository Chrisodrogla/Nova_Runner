import pandas as pd
import sys
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
PROPERTIES_SHEET_NAME = 'Properties'
LISTINGS_SHEET_NAME = 'Listings'
MARKETDATA_SHEET_NAME = 'MarketData'
SEARCHJOBTABLE_SHEET_NAME = 'SearchJobTable'

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# File paths
json_file_path = 'scraper/scraper/Listing_Url/json_file/listing_attribute.json'
json_market_file_path = 'scraper/scraper/Listing_Url/output/final_results.json'
searchjobtable_file_path = 'scraper/scraper/Listing_Url/json_file/final_rental_link.json'

# Read JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Read Market JSON data
with open(json_market_file_path, 'r') as file:
    market_data = json.load(file)

# Read SearchJobTable JSON data
with open(searchjobtable_file_path, 'r') as file:
    searchjobtable_data = json.load(file)

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

def update_marketdata_sheet(market_data):
    # Create DataFrame from Market JSON data
    df = pd.DataFrame(market_data)

    # Add 'Updatedat' column with the current date
    df['Updatedat'] = datetime.today().strftime('%Y-%m-%d')

    # Write new data to the "MarketData" sheet starting from row 2
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"{MARKETDATA_SHEET_NAME}!A2",
        valueInputOption="RAW",
        body={"values": df.values.tolist()}
    ).execute()

# def update_marketdata_sheet(market_data):
#     # Create DataFrame from Market JSON data
#     df = pd.DataFrame(market_data)
#
#     # Write new data to the "MarketData" sheet starting from row 2
#     service.spreadsheets().values().update(
#         spreadsheetId=SHEET_ID,
#         range=f"{MARKETDATA_SHEET_NAME}!A2",
#         valueInputOption="RAW",
#         body={"values": df.values.tolist()}
#     ).execute()


def update_searchjobtable_sheet(searchjobtable_data):
    rows = []
    for batch, entries in searchjobtable_data.items():
        for entry in entries:
            row = {
                'SearchJobID': '',
                'start_date': entry['start_date'],
                'end_date': entry['end_date'],
                'airbnb_link': entry['airbnb_link'],
                'bedrooms': entry['bedrooms'],
                'baths': entry['baths'],
                'guest': entry['guest'],
                'beds': entry['beds'],
                'RunStatus': '',
                'SearchDateTime': ''
            }
            rows.append(row)

    # Create DataFrame from the rows list
    df = pd.DataFrame(rows)

    # Write new data to the "SearchJobTable" sheet starting from row 2
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=f"{SEARCHJOBTABLE_SHEET_NAME}!A2",
        valueInputOption="RAW",
        body={"values": df.values.tolist()}
    ).execute()


if sheet_to_update.lower() == "properties":
    update_properties_sheet(data)
elif sheet_to_update.lower() == "listings":
    update_listings_sheet(data)
elif sheet_to_update.lower() == "market":
    update_marketdata_sheet(market_data)
elif sheet_to_update.lower() == "searchjobtable":
    update_searchjobtable_sheet(searchjobtable_data)
else:
    print("Invalid argument. Use 'properties', 'listings', 'market', or 'searchjobtable'.")

print(f"Data has been successfully written to the {sheet_to_update.capitalize()} sheet")
