import pandas as pd
import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pyodbc

SHEET_ID = '18qCzoA5vi0EKlBf1s8sgC8F1NhSLxD_7L2rNAQcOkVY'
PROPERTIES_TABLE = 'Properties'
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SHEET_ID, range=PROPERTIES_TABLE).execute()
values = result.get('values', [])

df = pd.DataFrame(values[1:], columns=values[0])

print("Column names in DataFrame:", df.columns.tolist())

# Adjust column names based on actual DataFrame columns
# Verify the column names that are actually in the DataFrame
actual_columns = df.columns.tolist()
print("Actual columns:", actual_columns)

# Define the correct column names based on actual columns
# Replace '...' with actual column names as per your DataFrame
column_mapping = {
    'PropertyID': 'PropertyID',
    'PropertyName': 'PropertyName',
    'InfoID': 'InfoID',  # Adjust these as needed
    'HostName': 'HostName',
    'CoHostName': 'CoHostName',
    'NumberOfBedRooms': 'NumberOfBedRooms',
    'NumberOfBathrooms': 'NumberOfBathrooms',
    'NumberOfGuests': 'NumberOfGuests',
    'ResortName': 'ResortName',
    'City': 'City',
    'State': 'State',
    'Country': 'Country',
    'SearchRange': 'SearchRange',
    'MainListingID': 'MainListingID'
}

# Apply the correct column names
df.rename(columns=column_mapping, inplace=True)

# Convert data types to match SQL table
df['PropertyID'] = df['PropertyID'].astype(str)
df['PropertyName'] = df['PropertyName'].astype(str)
df['InfoID'] = df['InfoID'].astype(str)
df['HostName'] = df['HostName'].astype(str)
df['CoHostName'] = df['CoHostName'].astype(str)
df['NumberOfBedRooms'] = df['NumberOfBedRooms'].astype(float)  # Use float in case there are decimals
df['NumberOfBathrooms'] = df['NumberOfBathrooms'].astype(float)  # Already float
df['NumberOfGuests'] = df['NumberOfGuests'].astype(float)  # Use float in case there are decimals
df['ResortName'] = df['ResortName'].astype(str)
df['City'] = df['City'].astype(str)
df['State'] = df['State'].astype(str)
df['Country'] = df['Country'].astype(str)
df['SearchRange'] = df['SearchRange'].astype(float)  # Use float in case there are decimals
df['MainListingID'] = df['MainListingID'].astype(str)

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
            INSERT INTO Properties (PropertyID, PropertyName, InfoID, HostName, CoHostName, NumberOfBedRooms, NumberOfBathrooms, NumberOfGuests, ResortName, City, State, Country, SearchRange, MainListingID)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row['PropertyID'], row['PropertyName'], row['InfoID'], row['HostName'], row['CoHostName'], row['NumberOfBedRooms'], row['NumberOfBathrooms'], row['NumberOfGuests'], row['ResortName'], row['City'], row['State'], row['Country'], row['SearchRange'], row['MainListingID'])
    conn.commit()

# Close connection
conn.close()
