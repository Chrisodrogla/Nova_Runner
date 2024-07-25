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


service = build("sheets", "v4", credentials=credentials)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=LISTINGS_TABLE).execute()
values = result.get('values', [])

df = pd.DataFrame(values[1:], columns=values[0])

print("Column names in DataFrame:", df.columns.tolist())

df.columns = ['ListingID', 'PropertyID', 'IsMainListing', 'DateCreated', 'DateUpdated', 'Status']

df['ListingID'] = df['ListingID'].astype(str)
df['PropertyID'] = df['PropertyID'].astype(str)
df['IsMainListing'] = df['IsMainListing'].astype(float)  # Convert to float to handle potential decimal values (0 or 1)
df['DateCreated'] = pd.to_datetime(df['DateCreated'], errors='coerce')  # Handle possible invalid dates
df['DateUpdated'] = pd.to_datetime(df['DateUpdated'], errors='coerce')  # Handle possible invalid dates
df['Status'] = df['Status'].astype(str)


connection_string = os.environ.get('SECRET_CHRISTIANSQL_STRING')


conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

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
