import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

# Constants
SHEET_ID = '10OgYeu7oj5Lwtr4gGy14zXuZlAk0gibSbgq_AmUtf7Q'
PROPERTIES_TABLE = 'Listing_Reservation'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=PROPERTIES_TABLE).execute()
values = result.get('values', [])

# Create a DataFrame from the Google Sheets data
df = pd.DataFrame(values[1:], columns=values[0])

# Ensure correct data types to match SQL table
df['CheckIn'] = pd.to_datetime(df['CheckIn'], errors='coerce').dt.date
df['CheckOut'] = pd.to_datetime(df['CheckOut'], errors='coerce').dt.date
df['Earnings'] = pd.to_numeric(df['Earnings'], errors='coerce')
df['NumberOfAdults'] = pd.to_numeric(df['# of adults'], errors='coerce')
df['NumberOfChildren'] = pd.to_numeric(df['# of children'], errors='coerce')
df['NumberOfInfants'] = pd.to_numeric(df['# of infants'], errors='coerce')
df['BookedDate'] = pd.to_datetime(df['Booked'], errors='coerce').dt.date

# Rename columns to match SQL table structure
df.rename(columns={
    'Status': 'Status',
    'GuestName': 'GuestName',
    'Listing': 'Listing',
    'ConfirmationCode': 'ConfirmationCode',
    'Contact': 'Contact',
    'GuestLink': 'GuestLink',
    'BookedTime': 'BookedTime',
    'Review': 'Review'
}, inplace=True)

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
            INSERT INTO ListingReservation (Status, GuestName, CheckIn, CheckOut, Listing, ConfirmationCode, Earnings, Contact, GuestLink, NumberOfAdults, NumberOfChildren, NumberOfInfants, BookedDate, BookedTime, Review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['Status'], row['GuestName'], row['CheckIn'], row['CheckOut'], row['Listing'], row['ConfirmationCode'], row['Earnings'], row['Contact'], row['GuestLink'], row['NumberOfAdults'], row['NumberOfChildren'], row['NumberOfInfants'], row['BookedDate'], row['BookedTime'], row['Review'])
    conn.commit()

# Close connection
conn.close()
