import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

# Constants
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
PROPERTIES_TABLE = 'Listing_Metrics'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=PROPERTIES_TABLE).execute()
values = result.get('values', [])

df = pd.DataFrame(values[1:], columns=values[0])

# Check if ListingID column exists and print the first few values
if 'ListingID' in df.columns:
    print("ListingID values in DataFrame:", df['ListingID'].head())
else:
    print("ListingID column not found in the DataFrame.")

# Ensure ListingID is properly handled and converted to the correct type
df['ListingID'] = df['ListingID'].astype(str)  # Ensure ListingID is treated as a string

# Convert data types to match SQL table
df = df.apply(pd.to_numeric, errors='ignore')  # Convert numeric columns to appropriate types

# Handle missing or empty values
df = df.replace('', None)

# Connection string from environment variable
connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish SQL Server connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Insert data into SQL Server table in batches
batch_size = 100000
for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start+batch_size]
    for index, row in batch.iterrows():
        cursor.execute("""
            INSERT INTO ListingMetrics (ListingID, StartDate, EndDate, FPImpression, TotalPageView, TotalPageView_comp, FPImpressionRate, ClickThroughRate, ViewtoBookRate, OverallConversionRate, OverallConversionRate_comp, LeadingTime, LeadingTime_comp, WishlistAdditions, WishlistAdditions_comp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['ListingID'], row['StartDate'], row['EndDate'], row['FPImpression'], row['TotalPageView'], row['TotalPageView_comp'], row['FPImpressionRate'], row['ClickThroughRate'], row['ViewtoBookRate'], row['OverallConversionRate'], row['OverallConversionRate_comp'], row['LeadingTime'], row['LeadingTime_comp'], row['WishlistAdditions'], row['WishlistAdditions_comp'])
    conn.commit()

# Close connection
conn.close()
