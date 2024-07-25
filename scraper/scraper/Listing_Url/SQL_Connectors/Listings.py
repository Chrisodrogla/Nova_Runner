import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

SHEET_ID = '18qCzoA5vi0EKlBf1s8sgC8F1NhSLxD_7L2rNAQcOkVY'
LISTINGS_TABLE = 'Listings'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=LISTINGS_TABLE).execute()
values = result.get('values', [])

# Print raw values for debugging
print("Raw values from Google Sheets:", values)

# Check if there are headers
if not values or len(values) < 2:
    raise ValueError("Data from Google Sheets is empty or missing headers")

# Create DataFrame
try:
    df = pd.DataFrame(values[1:], columns=values[0])
except ValueError as e:
    print("Error creating DataFrame:", e)
    raise

print("Column names in DataFrame:", df.columns.tolist())

# Rename columns in DataFrame
df.columns = ['ListingID', 'PropertyID', 'IsMainListing', 'DateCreated', 'DateUpdated', 'Status']

# Handle missing or blank values
df['ListingID'] = df['ListingID'].astype(str)
df['PropertyID'] = df['PropertyID'].astype(str)

# Replace blank or missing values in 'IsMainListing' with a default value (e.g., 0) or None
df['IsMainListing'] = df['IsMainListing'].replace('', None).astype(float)  # Convert to float, handle None as NULL

# Replace blank or invalid dates with None
df['DateCreated'] = pd.to_datetime(df['DateCreated'], errors='coerce')  # Coerce errors to NaT (not a time)
df['DateUpdated'] = pd.to_datetime(df['DateUpdated'], errors='coerce')  # Coerce errors to NaT (not a time)

# Replace blank values in 'Status' with None or a default value (e.g., 'Unknown')
df['Status'] = df['Status'].replace('', None).astype(str)

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
            INSERT INTO Listings (ListingID, PropertyID, IsMainListing, DateCreated, DateUpdated, Status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, row['ListingID'], row['PropertyID'], row['IsMainListing'], row['DateCreated'], row['DateUpdated'], row['Status'])
    conn.commit()

# Close connection
conn.close()
