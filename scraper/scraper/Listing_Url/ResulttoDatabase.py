import pandas as pd
import sys
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc
import datetime

# Google Sheets setup
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
JobTable = 'JobTable_Results'

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
columns = ['JobID', 'InfoID', 'host_name', 'listingId', 'Url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'StartDate', 'EndDate', 'Run_Date']

# Ensure that columns match the expected order and names
df = df[columns]

# Convert data types to match SQL table
df['JobID'] = df['JobID'].astype(int)
df['InfoID'] = df['InfoID'].astype(int)
df['orig_price_per_night'] = df['orig_price_per_night'].astype(float)
df['cleaning_fee'] = df['cleaning_fee'].astype(float)
df['service_fee'] = df['service_fee'].astype(float)
df['total_price'] = df['total_price'].astype(float)
df['price_per_night'] = df['price_per_night'].astype(float)
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])
df['Run_Date'] = pd.to_datetime(df['Run_Date'])

# Connection string from environment variable
connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')

# Establish SQL Server connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Insert data into SQL Server table
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO JobDataResults (JobID, InfoID, host_name, listingId, Url, orig_price_per_night, cleaning_fee, service_fee, total_price, price_per_night, StartDate, EndDate, Run_Date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row['JobID'], row['InfoID'], row['host_name'], row['listingId'], row['Url'], row['orig_price_per_night'], row['cleaning_fee'], row['service_fee'], row['total_price'], row['price_per_night'], row['StartDate'], row['EndDate'], row['Run_Date'])

# Commit changes
conn.commit()

# Close connection
conn.close()
