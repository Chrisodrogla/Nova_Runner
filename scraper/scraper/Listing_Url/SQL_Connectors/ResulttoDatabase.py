import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc


SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
JobTable = 'JobTable_Results'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

#Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

#Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=JobTable).execute()
values = result.get('values', [])

df = pd.DataFrame(values[1:], columns=values[0])

print("Column names in DataFrame:", df.columns.tolist())

columns = ['JobID', 'InfoID', 'host_name', 'listingId', 'Url', 'orig_price_per_night', 'cleaning_fee', 'service_fee', 'total_price', 'price_per_night', 'StartDate', 'EndDate', 'Run_Date']

df.columns = ['JobID', 'InfoID', 'HostName', 'ListingID', 'URL', 'OrigPricePerNight', 'CleaningFee', 'ServiceFee', 'TotalPrice', 'PricePerNight', 'StartDate', 'EndDate', 'RunDate']

# Convert data types to match SQL table
df['JobID'] = df['JobID'].astype(int)
df['InfoID'] = df['InfoID'].astype(int)
df['OrigPricePerNight'] = df['OrigPricePerNight'].astype(float)
df['CleaningFee'] = df['CleaningFee'].astype(float)
df['ServiceFee'] = df['ServiceFee'].astype(float)
df['TotalPrice'] = df['TotalPrice'].astype(float)
df['PricePerNight'] = df['PricePerNight'].astype(float)
df['StartDate'] = pd.to_datetime(df['StartDate'])
df['EndDate'] = pd.to_datetime(df['EndDate'])
df['RunDate'] = pd.to_datetime(df['RunDate'])

# Connection string from environment variable using secrets on github
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
            INSERT INTO JobDataResults (JobID, InfoID, HostName, ListingID, URL, OrigPricePerNight, CleaningFee, ServiceFee, TotalPrice, PricePerNight, StartDate, EndDate, RunDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['JobID'], row['InfoID'], row['HostName'], row['ListingID'], row['URL'], row['OrigPricePerNight'], row['CleaningFee'], row['ServiceFee'], row['TotalPrice'], row['PricePerNight'], row['StartDate'], row['EndDate'], row['RunDate'])
    conn.commit()

# Close connection
conn.close()